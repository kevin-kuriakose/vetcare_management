frappe.ui.form.on("Pet Hospitalization", {
    refresh(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.status === "Admitted") {
            frm.add_custom_button(__("Discharge Patient"), function () {
                let d = new frappe.ui.Dialog({
                    title: __("Discharge Patient"),
                    fields: [
                        { label: __("Discharge Condition"), fieldname: "discharge_condition", fieldtype: "Select",
                          options: "Recovered\nImproved\nUnchanged\nDeteriorated\nDeceased\nDischarged Against Advice", reqd: 1 },
                        { label: __("Discharge Notes"), fieldname: "discharge_notes", fieldtype: "Text Editor" }
                    ],
                    primary_action_label: __("Discharge"),
                    primary_action(values) {
                        frappe.call({ method: "discharge_patient", doc: frm.doc, args: values,
                            callback() { frm.reload_doc(); d.hide(); } });
                    }
                });
                d.show();
            }, __("Actions"));
        }
    }
});
