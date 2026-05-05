from . import __version__ as app_version

app_name = "vetcare_management"
app_title = "Vetcare Management"
app_publisher = "Your Company"
app_description = "Complete Veterinary Hospital Management System for ERPNext v15+"
app_email = "info@yourcompany.com"
app_license = "MIT"

required_apps = ["frappe", "erpnext"]

app_include_css = "/assets/vetcare_management/css/vetcare.css"
app_include_js = "/assets/vetcare_management/js/vetcare.js"

doc_events = {
    "Vet Appointment": {
        "on_submit": "vetcare_management.vetcare_management.doctype.vet_appointment.vet_appointment.on_submit",
        "on_cancel": "vetcare_management.vetcare_management.doctype.vet_appointment.vet_appointment.on_cancel",
    },
    "Lab Test": {
        "on_submit": "vetcare_management.vetcare_management.doctype.lab_test.lab_test.on_submit",
    },
    "Pet Hospitalization": {
        "on_submit": "vetcare_management.vetcare_management.doctype.pet_hospitalization.pet_hospitalization.on_submit",
        "on_cancel": "vetcare_management.vetcare_management.doctype.pet_hospitalization.pet_hospitalization.on_cancel",
    },
    "Vaccination Record": {
        "on_submit": "vetcare_management.vetcare_management.doctype.vaccination_record.vaccination_record.on_submit",
    },
}

scheduler_events = {
    "daily": [
        "vetcare_management.vetcare_management.doctype.vaccination_record.vaccination_record.send_vaccination_reminders",
        "vetcare_management.vetcare_management.doctype.pet_hospitalization.pet_hospitalization.check_discharge_alerts",
    ],
    "hourly": [
        "vetcare_management.vetcare_management.doctype.vet_appointment.vet_appointment.send_appointment_reminders",
    ],
}

fixtures = [
    {"dt": "Custom Field"},
    {
        "dt": "Role",
        "filters": [
            ["name", "in", ["Veterinarian", "Vet Receptionist", "Vet Lab Technician", "Vet Admin", "Vet Groomer"]]
        ],
    },
    {"dt": "Workspace", "filters": [["name", "=", "Vetcare Management"]]},
]

permission_query_conditions = {
    "Vet Appointment": "vetcare_management.vetcare_management.doctype.vet_appointment.vet_appointment.get_permission_query_conditions",
}
