from frappe.model.naming import make_autoname
from crm.fcrm.doctype.crm_deal.crm_deal import CRMDeal

class ExtendedCRMDeal(CRMDeal):
	def validate(self):pass      

	def before_insert(self):
		self.set_admission__batch_number(self)

	def autoname(self):
		self.set_admission__batch_number(self)
    
	def before_naming(self):
		self.set_admission__batch_number(self)

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

def set_admission__batch_number(self):
     if self.custom_service_type == "Saree Drape Class (SD)":
      if not self.custom_admission_number:
       self.custom_admission_number=make_autoname("ADM-SD-.MM.-.YYYY.-.#####")
      if not self.custom_batch:
       self.custom_batch=make_autoname("BAT-SD-.MM.-.YYYY.-.#####")
     elif self.custom_service_type == "Master Class (MC)":
      if not self.custom_admission_number:
       self.custom_admission_number=make_autoname("ADM-MC-.MM.-.YYYY.-.#####")
      if not self.custom_batch:
       self.custom_batch=make_autoname("BAT-MC-.MM.-.YYYY.-.#####") 