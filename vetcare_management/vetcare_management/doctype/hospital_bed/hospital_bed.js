frappe.ui.form.on("Hospital Bed", {
    refresh(frm) {
        const color = { "Available": "green", "Occupied": "red", "Under Maintenance": "orange", "Reserved": "blue" };
        if (frm.doc.status) frm.set_intro(`Status: <strong>${frm.doc.status}</strong>`, color[frm.doc.status]);
    }
});
