import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today, add_days
from frappe import _

class VetAppointment(Document):
    def validate(self):
        self.fetch_owner_from_pet()
        if getdate(self.appointment_date) < getdate(today()):
            frappe.throw(_("Appointment date cannot be in the past."))

    def fetch_owner_from_pet(self):
        if self.patient and not self.owner:
            self.owner = frappe.db.get_value("Patient Pet", self.patient, "owner")

    def on_submit(self):
        self.db_set("status", "Confirmed")
        self.send_confirmation_notification()

    def on_cancel(self):
        self.db_set("status", "Cancelled")

    def send_confirmation_notification(self):
        owner = frappe.get_doc("Pet Owner", self.owner)
        if owner.email_id:
            frappe.sendmail(
                recipients=[owner.email_id],
                subject=f"Appointment Confirmed - {self.patient_name}",
                message=f"""<p>Dear {owner.full_name},</p>
                <p>Appointment for <strong>{self.patient_name}</strong> confirmed.</p>
                <p><strong>Date:</strong> {self.appointment_date} | <strong>Time:</strong> {self.appointment_time}<br>
                <strong>Vet:</strong> {self.veterinarian_name} | <strong>Type:</strong> {self.appointment_type}</p>""",
                now=True
            )

def send_appointment_reminders():
    tomorrow = add_days(today(), 1)
    appointments = frappe.get_all("Vet Appointment",
        filters={"appointment_date": tomorrow, "status": "Confirmed", "docstatus": 1},
        fields=["name", "patient_name", "owner", "appointment_time", "veterinarian_name"])
    for apt in appointments:
        owner = frappe.get_doc("Pet Owner", apt.owner)
        if owner.email_id:
            frappe.sendmail(
                recipients=[owner.email_id],
                subject=f"Appointment Reminder - {apt.patient_name}",
                message=f"<p>Dear {owner.full_name},</p><p>Reminder: {apt.patient_name} has appointment tomorrow at {apt.appointment_time} with {apt.veterinarian_name}.</p>",
                now=True)

def get_permission_query_conditions(user):
    if "Vet Admin" in frappe.get_roles(user) or "System Manager" in frappe.get_roles(user):
        return ""
    vet = frappe.db.get_value("Veterinarian", {"user": user}, "name")
    if vet:
        return f"`tabVet Appointment`.`veterinarian` = '{vet}'"
    return "1=0"
