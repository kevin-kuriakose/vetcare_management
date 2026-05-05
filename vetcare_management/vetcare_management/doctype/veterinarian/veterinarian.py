from frappe.model.document import Document
import frappe

class Veterinarian(Document):
    def validate(self):
        if self.user:
            user_roles = frappe.get_roles(self.user)
            if "Veterinarian" not in user_roles:
                user_doc = frappe.get_doc("User", self.user)
                user_doc.append("roles", {"role": "Veterinarian"})
                user_doc.save(ignore_permissions=True)
