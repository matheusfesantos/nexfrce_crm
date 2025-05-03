import frappe 
from frappe.model.document import Document

class Appoiment(Document):
    def validate(self):
        overlapping_appointments = frappe.get_all("Appointment", filters={
            "seller": self.seller,
            "status": "Scheduled",
            "start_date": ("<=", self.end_date),
            "end_date": (">=", self.start_date)
        })
        if overlapping_appointments:
            frappe.throw("O vendedor não possui disponibilidade nesse dia")

fields = [
    {"fieldname": "client_name", "fieldtype": "Data", "label": "Client Name"},
    {"fieldname": "start_date", "fieldtype": "Datetime", "label": "Start Date"},
    {"fieldname": "end_date", "fieldtype": "Datetime", "label": "End Date"},
    {"fieldname": "duration", "fieldtype": "Time", "label": "Duration"},
    {"fieldname": "description", "fieldtype": "Small Text", "label": "Description"},
    {"fieldname": "seller", "fieldtype": "Link", "label": "Seller", "options": "User"},
    {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Scheduled\nFinished\nCanceled"}
]           