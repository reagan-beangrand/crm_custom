#import frappe
#from frappe import _
from crm.fcrm.doctype.crm_deal.crm_deal import CRMDeal

class ExtendedCRMDeal(CRMDeal):

	@staticmethod
	def default_kanban_settings():
		return {
			"column_field": "status",
			"title_field": "name",
			"kanban_fields": '["lead_name","email", "mobile_no", "_assign", "modified"]',
		}
	@staticmethod
	def default_list_data():
		columns = [
			{
				"label": "Lead Name",
				"type": "Data",
				"key": "lead_name",
				"width": "11rem",
			},		
			{
				"label": "Status",
				"type": "Link",
				"options": "CRM Deal Status",
				"key": "status",
				"width": "10rem",
			},
			{
				"label": "Email",
				"type": "Data",
				"key": "email",
				"width": "12rem",
			},
			{
				"label": "Mobile No.",
				"type": "Data",
				"key": "mobile_no",
				"width": "11rem",
			},
			{
				"label": "Assigned To",
				"type": "Text",
				"key": "_assign",
				"width": "10rem",
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
			"lead_name",
			"status",
			"email",
			"currency",
			"mobile_no",
			"deal_owner",
			"sla_status",
			"response_by",
			"first_response_time",
			"first_responded_on",
			"modified",
			"_assign",
		]
		return {"columns": columns, "rows": rows}    