import frappe
from frappe.model.document import Document

class Prescription(Document):
    def validate(self):
        if not self.medications:
            frappe.throw("At least one medication is required.")
