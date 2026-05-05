from frappe.model.document import Document

class AnimalBreed(Document):
    def validate(self):
        self.breed_name = self.breed_name.strip().title()
