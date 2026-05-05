frappe.provide("vetcare");

vetcare = {
    fetch_pet_details(frm, patient_field) {
        const patient = frm.doc[patient_field || "patient"];
        if (!patient) return;
        frappe.db.get_doc("Patient Pet", patient).then((pet) => {
            if (frm.fields_dict["owner"]) frm.set_value("owner", pet.owner);
            if (frm.fields_dict["patient_name"]) frm.set_value("patient_name", pet.pet_name);
            if (frm.fields_dict["weight_kg"]) frm.set_value("weight_kg", pet.weight_kg);
        });
    },

    quick_appointment(patient, owner) {
        const d = new frappe.ui.Dialog({
            title: __("Quick Appointment"),
            fields: [
                { fieldname: "patient", label: __("Pet"), fieldtype: "Link", options: "Patient Pet", default: patient, reqd: 1 },
                { fieldname: "veterinarian", label: __("Veterinarian"), fieldtype: "Link", options: "Veterinarian", reqd: 1 },
                { fieldname: "appointment_date", label: __("Date"), fieldtype: "Date", default: frappe.datetime.get_today(), reqd: 1 },
                { fieldname: "appointment_time", label: __("Time"), fieldtype: "Time", reqd: 1 },
                { fieldname: "appointment_type", label: __("Type"), fieldtype: "Select", options: "Consultation\nVaccination\nGrooming\nFollow-up\nEmergency", reqd: 1 },
                { fieldname: "chief_complaint", label: __("Chief Complaint"), fieldtype: "Text", reqd: 1 },
            ],
            primary_action_label: __("Book Appointment"),
            primary_action(values) {
                values.owner = owner;
                frappe.new_doc("Vet Appointment", values);
                d.hide();
            },
        });
        d.show();
    },

    format_urgency(urgency) {
        const map = {
            Normal: '<span style="color:green">● Normal</span>',
            Urgent: '<span style="color:orange">● Urgent</span>',
            Emergency: '<span style="color:red;font-weight:bold">⚠ Emergency</span>',
        };
        return map[urgency] || urgency;
    },
};

$(document).on("app_ready", function () {
    console.log("🐾 Vetcare Management loaded successfully.");
});
