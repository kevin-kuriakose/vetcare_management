frappe.ui.form.on("Lab Test", {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Print Report"), () => {
                frappe.utils.print(frm.doctype, frm.doc.name, "Lab Test Report");
            });
        }
    }
});
