import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, getdate

class BoardingRecord(Document):
    def before_save(self):
        if self.check_in_date and self.expected_check_out:
            self.total_days = date_diff(self.expected_check_out, getdate(self.check_in_date)) or 1
            if self.daily_rate:
                self.total_amount = self.total_days * self.daily_rate
