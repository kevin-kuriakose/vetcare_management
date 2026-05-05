frappe.ui.form.on("Vet Consultation", {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__("Create Prescription"), () => {
                frappe.new_doc("Prescription", { consultation: frm.doc.name, patient: frm.doc.patient, owner: frm.doc.owner, veterinarian: frm.doc.veterinarian });
            }, __("Actions"));
            frm.add_custom_button(__("Request Lab Test"), () => {
                frappe.new_doc("Lab Test", { patient: frm.doc.patient, owner: frm.doc.owner, veterinarian: frm.doc.veterinarian });
            }, __("Actions"));
            frm.add_custom_button(__("Imaging Request"), () => {
                frappe.new_doc("Imaging Request", { patient: frm.doc.patient, owner: frm.doc.owner });
            }, __("Actions"));
        }
    }
});
