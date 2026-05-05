import frappe
from frappe import _

def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        {"label": _("Lab Test ID"), "fieldname": "name", "fieldtype": "Link", "options": "Lab Test", "width": 130},
        {"label": _("Date"), "fieldname": "test_date", "fieldtype": "Date", "width": 100},
        {"label": _("Pet Name"), "fieldname": "patient_name", "fieldtype": "Data", "width": 120},
        {"label": _("Owner"), "fieldname": "owner", "fieldtype": "Link", "options": "Pet Owner", "width": 120},
        {"label": _("Test Type"), "fieldname": "lab_test_type", "fieldtype": "Data", "width": 140},
        {"label": _("Sample Type"), "fieldname": "sample_type", "fieldtype": "Data", "width": 100},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Interpretation"), "fieldname": "interpretation", "fieldtype": "Data", "width": 120},
        {"label": _("Technician"), "fieldname": "lab_technician", "fieldtype": "Data", "width": 120},
        {"label": _("Amount"), "fieldname": "test_amount", "fieldtype": "Currency", "width": 100},
    ]

def get_data(filters):
    filters = filters or {}
    conditions = "WHERE docstatus != 2"
    values = {}
    if filters.get("from_date"):
        conditions += " AND test_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND test_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]
    if filters.get("status"):
        conditions += " AND status = %(status)s"
        values["status"] = filters["status"]
    if filters.get("lab_test_type"):
        conditions += " AND lab_test_type = %(lab_test_type)s"
        values["lab_test_type"] = filters["lab_test_type"]
    return frappe.db.sql(f"""
        SELECT name, test_date, patient_name, owner, lab_test_type,
               sample_type, status, interpretation, lab_technician, test_amount
        FROM `tabLab Test` {conditions}
        ORDER BY test_date DESC
    """, values, as_dict=True)
