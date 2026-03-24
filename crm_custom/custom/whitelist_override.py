import frappe
#import json
from frappe import _
from frappe.utils import get_url_to_list
from crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings import  get_contact, get_erpnext_site_client, create_prospect_in_remote_site

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