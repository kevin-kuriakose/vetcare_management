import frappe
from frappe.model.document import Document

class AnimalSpecies(Document):
    def validate(self):
        self.species_name = self.species_name.strip().title()
