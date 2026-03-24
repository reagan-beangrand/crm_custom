#import frappe
#from frappe import _
from crm.fcrm.doctype.crm_lead.crm_lead import CRMLead

class ExtendedCRMLead(CRMLead):   

	@staticmethod
	def default_kanban_settings():
		return {
			"column_field": "status",
			"title_field": "lead_name",
			"kanban_fields": '["email", "mobile_no", "_assign", "modified"]',
		}
	
	@staticmethod
	def default_list_data():
		columns = [
			{
				"label": "Name",
				"type": "Data",
				"key": "lead_name",
				"width": "12rem",
			},			
			{
				"label": "Status",
				"type": "Link",
				"options": "CRM Lead Status",
				"key": "status",
				"width": "8rem",
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
			"mobile_no",
			"lead_owner",
			"first_name",
			"sla_status",
			"response_by",
			"first_response_time",
			"first_responded_on",
			"modified",
			"_assign",
			"image",
		]
		return {"columns": columns, "rows": rows}

	def create_organization(self, existing_organization=None):
		if not self.organization and not existing_organization:
			return

		existing_organization = existing_organization or frappe.db.exists(
			"CRM Organization", {"organization_name": self.organization}
		)
		if existing_organization:
			self.db_set("organization", existing_organization)
			return existing_organization

		organization = frappe.new_doc("CRM Organization")
		organization.update(
			{
				"organization_name": "MTBS",#self.organization,
				"website": "https://makeuptrendselite.com/",#self.website,
				#"territory": self.territory,
				"industry": "Service",#self.industry,
				"annual_revenue": 0,#self.annual_revenue,
			}
		)
		organization.insert(ignore_permissions=True)
		return organization.name