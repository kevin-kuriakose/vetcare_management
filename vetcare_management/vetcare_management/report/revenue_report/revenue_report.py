import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart

def get_columns():
    return [
        {"label": _("Month"), "fieldname": "month", "fieldtype": "Data", "width": 120},
        {"label": _("Appointments"), "fieldname": "appointment_revenue", "fieldtype": "Currency", "width": 140},
        {"label": _("Lab Tests"), "fieldname": "lab_revenue", "fieldtype": "Currency", "width": 120},
        {"label": _("Total"), "fieldname": "total", "fieldtype": "Currency", "width": 130},
    ]

def get_data(filters):
    filters = filters or {}
    year = filters.get("year", frappe.utils.getdate().year)
    appts = frappe.db.sql("""
        SELECT DATE_FORMAT(appointment_date, '%%Y-%%m') as month, SUM(consultation_fee) as revenue
        FROM `tabVet Appointment`
        WHERE YEAR(appointment_date) = %s AND docstatus = 1
        GROUP BY month ORDER BY month
    """, (year,), as_dict=True)
    labs = frappe.db.sql("""
        SELECT DATE_FORMAT(test_date, '%%Y-%%m') as month, SUM(test_amount) as revenue
        FROM `tabLab Test`
        WHERE YEAR(test_date) = %s AND docstatus = 1
        GROUP BY month ORDER BY month
    """, (year,), as_dict=True)
    months = set()
    appt_map = {r.month: r.revenue for r in appts}
    lab_map = {r.month: r.revenue for r in labs}
    for r in appts + labs:
        months.add(r.month)
    data = []
    for month in sorted(months):
        a = appt_map.get(month, 0) or 0
        l = lab_map.get(month, 0) or 0
        data.append({"month": month, "appointment_revenue": a, "lab_revenue": l, "total": a + l})
    return data

def get_chart(data):
    return {
        "data": {
            "labels": [r["month"] for r in data],
            "datasets": [
                {"name": "Appointments", "values": [r["appointment_revenue"] for r in data]},
                {"name": "Lab Tests", "values": [r["lab_revenue"] for r in data]},
            ]
        },
        "type": "bar", "title": "Monthly Revenue"
    }
