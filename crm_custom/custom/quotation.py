import frappe
from erpnext.selling.doctype.quotation.quotation import Quotation

class ExtendedQuotation(Quotation):

    def validate(self):
        super().validate()
        if self.quotation_to == "CRM Deal" and self.party_name:            
            self.customer_name = frappe.db.get_value("CRM Deal", self.party_name, "lead_name")