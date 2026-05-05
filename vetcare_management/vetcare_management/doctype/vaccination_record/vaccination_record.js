frappe.ui.form.on("Vaccination Record", {
    refresh(frm) {
        if (frm.doc.next_due_date && frm.doc.next_due_date < frappe.datetime.get_today()) {
            frm.set_intro(__("⚠ Vaccination overdue!"), "red");
        }
    },
    vaccine(frm) {
        if (frm.doc.vaccine) {
            frappe.db.get_value("Vaccine", frm.doc.vaccine, "manufacturer", (r) => {
                if (r) frm.set_value("manufacturer", r.manufacturer);
            });
        }
    }
});
