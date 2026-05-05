import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, today
from frappe import _

class PatientPet(Document):
    def validate(self):
        self.calculate_age()
        if self.is_deceased and not self.date_of_death:
            self.date_of_death = today()

    def calculate_age(self):
        if self.date_of_birth:
            days = date_diff(today(), self.date_of_birth)
            years = days // 365
            months = (days % 365) // 30
            self.age = f"{years}y {months}m" if years > 0 else f"{months} month(s)"
        else:
            self.age = "Unknown"
