import frappe
from frappe.model.document import Document

class VetConsultation(Document):
    def validate(self):
        if self.patient and self.weight_kg:
            frappe.db.set_value("Patient Pet", self.patient, "weight_kg", self.weight_kg)

    def on_submit(self):
        if self.appointment:
            frappe.db.set_value("Vet Appointment", self.appointment, "status", "Completed")
