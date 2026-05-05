import frappe
from frappe.model.document import Document

class LabTest(Document):
    def on_submit(self):
        self.db_set("status", "Completed")
        if self.owner:
            owner = frappe.get_doc("Pet Owner", self.owner)
            if owner.email_id:
                frappe.sendmail(recipients=[owner.email_id],
                    subject=f"Lab Results Ready - {self.patient_name}",
                    message=f"<p>Dear {owner.full_name},</p><p>Lab results for {self.patient_name} ({self.lab_test_type}) are ready. Interpretation: {self.interpretation or 'Pending review'}.</p>",
                    now=True)
