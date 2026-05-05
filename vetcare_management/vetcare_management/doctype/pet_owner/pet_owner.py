import frappe
from frappe.model.document import Document
from frappe import _

class PetOwner(Document):
    def after_insert(self):
        self.create_customer()

    def create_customer(self):
        if not self.customer:
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": self.full_name,
                "customer_type": "Individual",
                "customer_group": frappe.db.get_single_value("Selling Settings", "customer_group") or "All Customer Groups",
                "territory": frappe.db.get_single_value("Selling Settings", "territory") or "All Territories",
                "mobile_no": self.mobile_no,
                "email_id": self.email_id,
            })
            customer.insert(ignore_permissions=True)
            self.db_set("customer", customer.name)
            frappe.msgprint(_("Customer {0} created.").format(customer.name))
