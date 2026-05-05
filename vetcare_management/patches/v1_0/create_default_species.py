import frappe

def execute():
    """Create default animal species on first install."""
    default_species = [
        "Dog", "Cat", "Rabbit", "Bird", "Turtle",
        "Guinea Pig", "Hamster", "Fish", "Reptile", "Horse"
    ]
    for species in default_species:
        if not frappe.db.exists("Animal Species", species):
            frappe.get_doc({
                "doctype": "Animal Species",
                "species_name": species,
            }).insert(ignore_permissions=True)
    frappe.db.commit()
    print("✅ Default animal species created.")
