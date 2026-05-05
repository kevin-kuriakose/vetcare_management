import frappe
from frappe.model.document import Document
from frappe import _

class SurgeryRecord(Document):
    def validate(self):
        if not self.consent_obtained:
            frappe.msgprint(_("Warning: Consent not yet obtained for surgery."), alert=True)
