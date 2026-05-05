import frappe
from frappe import _
from frappe.utils import add_days, today

def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        {"label": _("Pet Name"), "fieldname": "patient_name", "fieldtype": "Data", "width": 130},
        {"label": _("Owner"), "fieldname": "owner", "fieldtype": "Link", "options": "Pet Owner", "width": 130},
        {"label": _("Owner Mobile"), "fieldname": "owner_mobile", "fieldtype": "Data", "width": 120},
        {"label": _("Vaccine"), "fieldname": "vaccine", "fieldtype": "Data", "width": 140},
        {"label": _("Last Vaccinated"), "fieldname": "vaccination_date", "fieldtype": "Date", "width": 120},
        {"label": _("Due Date"), "fieldname": "next_due_date", "fieldtype": "Date", "width": 100},
        {"label": _("Days Overdue"), "fieldname": "days_overdue", "fieldtype": "Int", "width": 100},
        {"label": _("Status"), "fieldname": "due_status", "fieldtype": "Data", "width": 100},
    ]

def get_data(filters):
    filters = filters or {}
    days_ahead = filters.get("days_ahead", 30)
    cutoff_date = add_days(today(), int(days_ahead))
    records = frappe.db.sql("""
        SELECT v.patient_name, v.owner, po.mobile_no as owner_mobile,
               v.vaccine, v.vaccination_date, v.next_due_date,
               DATEDIFF(NOW(), v.next_due_date) as days_overdue
        FROM `tabVaccination Record` v
        LEFT JOIN `tabPet Owner` po ON po.name = v.owner
        WHERE v.docstatus = 1 AND v.next_due_date <= %s
        ORDER BY v.next_due_date ASC
    """, (cutoff_date,), as_dict=True)
    for rec in records:
        rec.due_status = "⚠ Overdue" if (rec.days_overdue and rec.days_overdue > 0) else "🔔 Due Soon"
    return records
