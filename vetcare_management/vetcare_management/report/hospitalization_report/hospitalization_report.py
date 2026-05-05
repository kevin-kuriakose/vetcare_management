import frappe
from frappe import _

def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        {"label": _("ID"), "fieldname": "name", "fieldtype": "Link", "options": "Pet Hospitalization", "width": 130},
        {"label": _("Pet Name"), "fieldname": "patient_name", "fieldtype": "Data", "width": 120},
        {"label": _("Owner"), "fieldname": "owner", "fieldtype": "Link", "options": "Pet Owner", "width": 120},
        {"label": _("Bed"), "fieldname": "bed", "fieldtype": "Data", "width": 80},
        {"label": _("Ward"), "fieldname": "ward", "fieldtype": "Data", "width": 100},
        {"label": _("Admitted By"), "fieldname": "admitted_by", "fieldtype": "Data", "width": 130},
        {"label": _("Admission Date"), "fieldname": "admission_date", "fieldtype": "Datetime", "width": 140},
        {"label": _("Expected Discharge"), "fieldname": "expected_discharge_date", "fieldtype": "Date", "width": 130},
        {"label": _("Actual Discharge"), "fieldname": "discharge_date", "fieldtype": "Datetime", "width": 130},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 90},
        {"label": _("Discharge Condition"), "fieldname": "discharge_condition", "fieldtype": "Data", "width": 130},
    ]

def get_data(filters):
    filters = filters or {}
    conditions = "WHERE docstatus != 2"
    values = {}
    if filters.get("status"):
        conditions += " AND status = %(status)s"
        values["status"] = filters["status"]
    if filters.get("from_date"):
        conditions += " AND DATE(admission_date) >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND DATE(admission_date) <= %(to_date)s"
        values["to_date"] = filters["to_date"]
    return frappe.db.sql(f"""
        SELECT name, patient_name, owner, bed, ward, admitted_by,
               admission_date, expected_discharge_date, discharge_date,
               status, discharge_condition
        FROM `tabPet Hospitalization` {conditions}
        ORDER BY admission_date DESC
    """, values, as_dict=True)
