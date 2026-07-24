import frappe
from frappe import _
from crm.fcrm.doctype.crm_lead.crm_lead import CRMLead

class ExtendedCRMLead(CRMLead):

	def validate(self):		
		self.validate_mobileNumber()
		super().validate()

	
	def validate_mobileNumber(self):
		if self.is_new():
			if self.mobile_no and not self.flags.get("skip_duplicate_validation"):
				self.person_exists(throw=True)
				# existing_person = self.person_exists(throw=True)
				# if existing_person:
				# 	frappe.throw(_("Person already exists with Mobile No: {0}").format(self.mobile_no), title=_("Person Already Exists"))

	def set_lead_name(self):
		if not self.lead_name:
			# Check for leads being created through data import
			if not self.organization and not self.mobile_no and not self.email and not self.flags.ignore_mandatory:
				frappe.throw(_("Requires a person's mobile number"))
			elif self.organization:
				self.lead_name = self.organization
			elif self.email:
				self.lead_name = self.email.split("@")[0]
			else:
				self.lead_name = "Unnamed Lead"

	def person_exists(self, throw=True):				
		mobile_exist = frappe.db.exists("CRM Lead", {"mobile_no": self.mobile_no})

		doctype = "CRM Lead"
		name = mobile_exist

		if name:
			value = "{0}: {1}".format("Mobile No", self.mobile_no)
			person = frappe.db.get_value(doctype, name,)

			if throw:
				frappe.throw(
					_("Person already exists with {0}").format(value),
					title=_("Person Already Exists"),
				)
			return person

		return False

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