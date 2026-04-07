import frappe
from frappe import _
from frappe.model.naming import make_autoname
from crm.fcrm.doctype.crm_deal.crm_deal import CRMDeal

class ExtendedCRMDeal(CRMDeal):	

	def validate(self):
		super().validate()
		self.custom_validate()		      

	def before_insert(self):
		self.set_admission_batch_number()

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

	def custom_validate(self):
		self.validate_service_type_field()
		self.validate_event_tab_fields()		

	def validate_service_type_field(self):
		if not self.custom_service_type:
			frappe.throw(_("Service Type is required."), frappe.MandatoryError)
		
	def validate_event_tab_date(self,datetimeValue,fieldname):
		if datetimeValue is not None and datetimeValue < frappe.utils.nowdate():
			frappe.throw(_("{0} should not be a past date").format(fieldname))
	
	def validate_mua_poc(self):
		if self.custom_primary_mua is not None and self.custom_secondary_mua is not None:
			if self.custom_primary_mua.lower() == self.custom_secondary_mua.lower():
				frappe.throw(_("Primary MUA and Secondary MUA should not be the same"), frappe.ValidationError)

	def validate_event_tab_fields(self):
		if self.custom_service_type and self.custom_service_type.strip().lower() == "bridal makeup":
			self.validate_event_tab_date(self.custom_datetime,"DateTime")			
			self.validate_mua_poc()
		else:
			self.validate_event_tab_date(self.custom_date_of_joining,"Date of Joining")			          
    	
	def validate_class_fields(self):
		if not self.custom_admission_number:
			frappe.throw(_("Admission Number is required."), frappe.MandatoryError)
		if not self.custom_batch:
			frappe.throw(_("Batch is required."), frappe.MandatoryError)
		if not self.custom_date_of_joining:
			frappe.throw(_("Date of Joining is required."), frappe.MandatoryError)
	
	def validate_event_fields(self):
		if not self.custom_event:
			frappe.throw(_("Event is required."), frappe.MandatoryError)
		if not self.custom_datetime:
			frappe.throw(_("Date and Time is required."), frappe.MandatoryError)
		if not self.custom_primary_mua:
			frappe.throw(_("Primary MUA/POC is required."), frappe.MandatoryError)
		if not self.custom_secondary_mua:
			frappe.throw(_("Secondary MUA is required."), frappe.MandatoryError)

	def set_admission_batch_number(self):
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