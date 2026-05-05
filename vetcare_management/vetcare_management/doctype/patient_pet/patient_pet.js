frappe.ui.form.on("Patient Pet", {
    refresh(frm) {
        if (frm.doc.is_deceased) {
            frm.disable_save();
            frm.set_intro(__("This pet is marked as deceased."), "red");
        }
        if (!frm.is_new()) {
            frm.add_custom_button(__("New Appointment"), () => {
                frappe.new_doc("Vet Appointment", { patient: frm.doc.name, owner: frm.doc.owner });
            }, __("Actions"));
            frm.add_custom_button(__("Medical History"), () => {
                frappe.route_options = { patient: frm.doc.name };
                frappe.set_route("query-report", "Patient History Report");
            }, __("Reports"));
            frm.add_custom_button(__("Vaccination Records"), () => {
                frappe.set_route("List", "Vaccination Record", { patient: frm.doc.name });
            }, __("Reports"));
        }
    },
    breed(frm) {
        if (frm.doc.breed) {
            frappe.db.get_value("Animal Breed", frm.doc.breed, "species", (r) => {
                if (r && r.species) frm.set_value("species", r.species);
            });
        }
    }
});
