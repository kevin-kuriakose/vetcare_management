import frappe
from frappe import _

def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        {"label": _("Appointment ID"), "fieldname": "name", "fieldtype": "Link", "options": "Vet Appointment", "width": 140},
        {"label": _("Date"), "fieldname": "appointment_date", "fieldtype": "Date", "width": 100},
        {"label": _("Time"), "fieldname": "appointment_time", "fieldtype": "Time", "width": 80},
        {"label": _("Pet Name"), "fieldname": "patient_name", "fieldtype": "Data", "width": 120},
        {"label": _("Owner"), "fieldname": "owner_name", "fieldtype": "Data", "width": 130},
        {"label": _("Veterinarian"), "fieldname": "veterinarian_name", "fieldtype": "Data", "width": 130},
        {"label": _("Type"), "fieldname": "appointment_type", "fieldtype": "Data", "width": 120},
        {"label": _("Urgency"), "fieldname": "urgency_level", "fieldtype": "Data", "width": 80},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "options": "Branch Clinic", "width": 120},
        {"label": _("Fee"), "fieldname": "consultation_fee", "fieldtype": "Currency", "width": 100},
    ]

def get_data(filters):
    filters = filters or {}
    conditions = "WHERE docstatus != 2"
    values = {}
    if filters.get("from_date"):
        conditions += " AND appointment_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND appointment_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]
    if filters.get("veterinarian"):
        conditions += " AND veterinarian = %(veterinarian)s"
        values["veterinarian"] = filters["veterinarian"]
    if filters.get("status"):
        conditions += " AND status = %(status)s"
        values["status"] = filters["status"]
    if filters.get("branch"):
        conditions += " AND branch = %(branch)s"
        values["branch"] = filters["branch"]
    return frappe.db.sql(f"""
        SELECT name, appointment_date, appointment_time, patient_name, owner_name,
               veterinarian_name, appointment_type, urgency_level, status, branch, consultation_fee
        FROM `tabVet Appointment` {conditions}
        ORDER BY appointment_date DESC, appointment_time DESC
    """, values, as_dict=True)
