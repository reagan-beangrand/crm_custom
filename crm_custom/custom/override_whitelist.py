
import frappe
import json
from frappe import _
from frappe.utils import get_url_to_list
from crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings import  get_contact,get_contacts,get_erpnext_site_client
#from crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings import get_erpnext_site_client
from crm.fcrm.doctype.crm_deal.crm_deal import  create_contact

@frappe.whitelist()
def get_quotation_url(crm_deal: str, organization: str | None = None):
	erpnext_crm_settings = frappe.get_single("ERPNext CRM Settings")
	if not erpnext_crm_settings.enabled:
		frappe.throw(_("ERPNext is not integrated with the CRM"))

	contact = get_contact(crm_deal)
	address = get_contact_address(contact)
	address = address.get("name") if address else None

	if not erpnext_crm_settings.is_erpnext_in_different_site:
		base_url = f"{get_url_to_list('Quotation')}/new"
		params = {
			"quotation_to": "CRM Deal",
			"crm_deal": crm_deal,
			"party_name": crm_deal,
			"company": erpnext_crm_settings.erpnext_company,
			"contact_person": contact,
			"customer_address": address,
		}
	else:
		site_url = erpnext_crm_settings.get("erpnext_site_url")
		base_url = f"{site_url}/app/quotation/new"
		prospect = create_prospect_in_remote_site(crm_deal, erpnext_crm_settings)
		params = {
			"quotation_to": "Prospect",
			"crm_deal": crm_deal,
			"party_name": prospect,
			"company": erpnext_crm_settings.erpnext_company,
			"contact_person": contact,
			"customer_address": address,
		}

	# Filter out None values and build query string
	query_string = "&".join(f"{key}={value}" for key, value in params.items() if value is not None)

	return f"{base_url}?{query_string}"

def get_contact_address(contact_name):	
	address = frappe.db.get_value("Contact", contact_name, "address")
	address = frappe.get_cached_doc("Address", address) if address else None
	if not address:
		return None
	return {
		"name": address.name,
		"address_title": address.address_title,
		"address_type": address.address_type,
		"address_line1": address.address_line1,
		"address_line2": address.address_line2,
		"city": address.city,
		"county": address.county,
		"state": address.state,
		"country": address.country,
		"pincode": address.pincode,
	}

def create_prospect_in_remote_site(crm_deal, erpnext_crm_settings):
	try:
		client = get_erpnext_site_client(erpnext_crm_settings)
		doc = frappe.get_cached_doc("CRM Deal", crm_deal)
		contacts = get_contacts(doc)
		contact_name = contacts[0]['contact']		
		address = get_contact_address(contact_name) or None

		if address and not isinstance(address, dict):
			address = address.as_dict()

		return client.post_api(
			"erpnext.crm.frappe_crm_api.create_prospect_against_crm_deal",
			{				
				"lead_name": doc.lead_name,
				"deal_owner": doc.deal_owner,
				"crm_deal": doc.name,				
				"contacts": json.dumps(contacts) if contacts else None,
				"erpnext_company": erpnext_crm_settings.erpnext_company,
				"address": json.dumps(address) if address else None,
			},
		)		
		
	except Exception:
		frappe.log_error(
			frappe.get_traceback(),
			f"Error while creating prospect in remote site: {erpnext_crm_settings.erpnext_site_url}",
		)
		frappe.throw(_("Error while creating prospect in ERPNext, check error log for more details"))

@frappe.whitelist()
def create_deal(doc: dict):
	deal = frappe.new_doc("CRM Deal")

	contact = doc.get("contact")
	if not contact and (
		doc.get("first_name") or doc.get("last_name") or doc.get("email") or doc.get("mobile_no")
	):
		contact = create_contact(doc)

	lead = doc.get("lead") or create_lead(doc)
	lead_name = lead.lead_name #if hasattr(lead, 'lead_name') else set_lead_name(doc)
	deal.update(
		{
			"lead": lead.name,
			"lead_name": lead_name,
			"contacts": [{"contact": contact, "is_primary": 1}] if contact else [],
		}
	)

	#doc.pop("organization", None)

	deal.update(doc)

	deal.insert(ignore_permissions=True)
	return deal.name

def create_lead(doc):
	#existing_contact = contact_exists(doc)
	#if existing_contact:
	#	return existing_contact

	lead = frappe.new_doc("CRM Lead")
	lead.update(
		{
			"first_name": doc.get("first_name"),
			"last_name": doc.get("last_name"),
			"salutation": doc.get("salutation"),
			"email": doc.get("email"),
			"mobile_no": doc.get("mobile_no"),
			"gender": doc.get("gender"),
			#"lead_name": set_lead_name(doc),
			"status": "Qualified",
			"converted": "1",
			"communication_status":"Replied"
		}
	)
	
	lead.insert(ignore_permissions=True)
	lead.reload()  # load changes by hooks on lead

	return lead

def set_lead_name(doc):
		if doc.get("first_name"):
			return " ".join(
				name
				for name in [
					doc.get("salutation"),
					doc.get("first_name"),
					doc.get("middle_name"),
					doc.get("last_name"),
				]
				if name
			)