import frappe
from frappe.model.document import Document
from frappe.utils import add_days
from frappe import _

class VaccinationRecord(Document):
    def before_save(self):
        if self.vaccine and self.vaccination_date:
            interval = frappe.db.get_value("Vaccine", self.vaccine, "booster_interval_days") or 365
            self.next_due_date = add_days(self.vaccination_date, int(interval))

    def on_submit(self):
        frappe.msgprint(_("Next vaccination due: {0}").format(self.next_due_date))

def send_vaccination_reminders():
    from frappe.utils import today
    reminder_date = add_days(today(), 7)
    records = frappe.get_all("Vaccination Record",
        filters={"next_due_date": reminder_date, "docstatus": 1},
        fields=["name", "patient_name", "owner", "vaccine", "next_due_date"])
    for rec in records:
        owner = frappe.get_doc("Pet Owner", rec.owner)
        if owner.email_id:
            frappe.sendmail(recipients=[owner.email_id],
                subject=f"Vaccination Due Reminder - {rec.patient_name}",
                message=f"<p>Dear {owner.full_name},</p><p>{rec.patient_name} is due for {rec.vaccine} on {rec.next_due_date}.</p>",
                now=True)
