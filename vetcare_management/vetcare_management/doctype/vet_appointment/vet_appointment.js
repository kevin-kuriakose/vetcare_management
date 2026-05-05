frappe.ui.form.on("Vet Appointment", {
    refresh(frm) {
        if (frm.doc.urgency_level === "Emergency") {
            frm.dashboard.set_headline_alert(`<div class="alert alert-danger">${__("⚠ EMERGENCY CASE")}</div>`);
        }
        if (!frm.is_new() && frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Create Consultation"), () => {
                frappe.new_doc("Vet Consultation", { appointment: frm.doc.name, patient: frm.doc.patient, owner: frm.doc.owner, veterinarian: frm.doc.veterinarian });
            }, __("Actions"));
            frm.add_custom_button(__("Create Invoice"), () => {
                frappe.new_doc("Vet Invoice", { patient: frm.doc.patient, owner: frm.doc.owner, appointment: frm.doc.name });
            }, __("Actions"));
        }
    },
    patient(frm) {
        if (frm.doc.patient) {
            frappe.db.get_value("Patient Pet", frm.doc.patient, "owner", (r) => {
                if (r) frm.set_value("owner", r.owner);
            });
        }
    }
});
