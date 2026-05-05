frappe.ui.form.on("Prescription", {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Print Prescription"), () => {
                frappe.utils.print(frm.doctype, frm.doc.name, "Veterinary Prescription");
            });
        }
    }
});
