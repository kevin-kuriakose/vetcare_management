import frappe
from frappe.model.document import Document
from frappe.utils import today
from frappe import _

class PetHospitalization(Document):
    def validate(self):
        if self.bed:
            existing = frappe.db.get_value(
                "Pet Hospitalization",
                {"bed": self.bed, "status": "Admitted", "name": ["!=", self.name or ""]},
                "name"
            )
            if existing:
                frappe.throw(_("Bed {0} is already occupied by {1}").format(self.bed, existing))

    def on_submit(self):
        self.db_set("status", "Admitted")
        frappe.db.set_value("Hospital Bed", self.bed, {"status": "Occupied", "current_patient": self.patient})

    def on_cancel(self):
        self.db_set("status", "Discharged")
        frappe.db.set_value("Hospital Bed", self.bed, {"status": "Available", "current_patient": None})

    @frappe.whitelist()
    def discharge_patient(self, discharge_condition, discharge_notes=""):
        self.discharge_date = frappe.utils.now_datetime()
        self.discharge_condition = discharge_condition
        self.discharge_notes = discharge_notes
        self.status = "Discharged"
        self.save()
        frappe.db.set_value("Hospital Bed", self.bed, {"status": "Available", "current_patient": None})
        frappe.msgprint(_("Patient discharged successfully."))

def check_discharge_alerts():
    records = frappe.get_all("Pet Hospitalization",
        filters={"expected_discharge_date": today(), "status": "Admitted", "docstatus": 1},
        fields=["name", "patient_name", "owner", "bed"])
    for rec in records:
        owner = frappe.get_doc("Pet Owner", rec.owner)
        if owner.email_id:
            frappe.sendmail(recipients=[owner.email_id],
                subject=f"Discharge Reminder - {rec.patient_name}",
                message=f"<p>Dear {owner.full_name},</p><p>{rec.patient_name} is scheduled for discharge today.</p>",
                now=True)
