
import frappe
from frappe.contacts.doctype.contact.contact import Contact
#from crm.overrides.contact.customcontact import CustomContact
#crm/crm/overrides/contact.py
class ExtendedContact(Contact):
	@staticmethod
	def default_list_data():
		#frappe.log("ExtendedContact default_list_data called")
		columns = [
			{
				"label": "First Name",
				"type": "Data",
				"key": "first_name",
				"width": "12rem",
			}, 
			{
				"label": "Full Name",
				"type": "Data",
				"key": "full_name",
				"width": "17rem",
			},
			{
				"label": "Email",
				"type": "Data",
				"key": "email_id",
				"width": "12rem",
			},
			{
				"label": "Phone",
				"type": "Data",
				"key": "mobile_no",
				"width": "12rem",
			},			
			{
				"label": "Last Modified",
				"type": "Datetime",
				"key": "modified",
				"width": "8rem",
			},
		]
		rows = [
			"name",
			"first_name",
			"full_name",			
			"email_id",
			"mobile_no",
			"modified",
			"image",
		]
		return {"columns": columns, "rows": rows}