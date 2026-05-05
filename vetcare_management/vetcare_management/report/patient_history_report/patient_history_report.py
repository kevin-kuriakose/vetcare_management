import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart

def get_columns():
    return [
        {"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 100},
        {"label": _("Event Type"), "fieldname": "event_type", "fieldtype": "Data", "width": 130},
        {"label": _("Reference"), "fieldname": "reference", "fieldtype": "Data", "width": 150},
        {"label": _("Veterinarian"), "fieldname": "veterinarian", "fieldtype": "Data", "width": 130},
        {"label": _("Details"), "fieldname": "details", "fieldtype": "Data", "width": 250},
        {"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 100},
    ]

def get_data(filters):
    filters = filters or {}
    data = []
    patient = filters.get("patient")
    if not patient:
        return []
    from_date = filters.get("from_date", "2000-01-01")
    to_date = filters.get("to_date", frappe.utils.today())

    appts = frappe.db.sql("""
        SELECT appointment_date as date, 'Appointment' as event_type, name as reference,
               veterinarian_name as veterinarian, appointment_type as details, consultation_fee as amount
        FROM `tabVet Appointment`
        WHERE patient = %s AND appointment_date BETWEEN %s AND %s AND docstatus != 2
    """, (patient, from_date, to_date), as_dict=True)
    data.extend(appts)

    cons = frappe.db.sql("""
        SELECT consultation_date as date, 'Consultation' as event_type, name as reference,
               veterinarian as veterinarian, diagnosis as details, 0 as amount
        FROM `tabVet Consultation`
        WHERE patient = %s AND consultation_date BETWEEN %s AND %s AND docstatus != 2
    """, (patient, from_date, to_date), as_dict=True)
    data.extend(cons)

    vacs = frappe.db.sql("""
        SELECT vaccination_date as date, 'Vaccination' as event_type, name as reference,
               administered_by as veterinarian, vaccine as details, 0 as amount
        FROM `tabVaccination Record`
        WHERE patient = %s AND vaccination_date BETWEEN %s AND %s AND docstatus != 2
    """, (patient, from_date, to_date), as_dict=True)
    data.extend(vacs)

    labs = frappe.db.sql("""
        SELECT test_date as date, 'Lab Test' as event_type, name as reference,
               veterinarian as veterinarian, lab_test_type as details, test_amount as amount
        FROM `tabLab Test`
        WHERE patient = %s AND test_date BETWEEN %s AND %s AND docstatus != 2
    """, (patient, from_date, to_date), as_dict=True)
    data.extend(labs)

    data.sort(key=lambda x: str(x.get("date", "")), reverse=True)
    return data

def get_chart(data):
    event_counts = {}
    for row in data:
        t = row.get("event_type", "Other")
        event_counts[t] = event_counts.get(t, 0) + 1
    return {
        "data": {"labels": list(event_counts.keys()), "datasets": [{"values": list(event_counts.values())}]},
        "type": "donut", "title": "Medical Events Distribution"
    }
