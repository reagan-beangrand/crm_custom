import frappe
from frappe import _
import json
from crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings import get_contacts as _get_contacts
from crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings import create_customer_in_remote_site #as _create_customer_in_remote_site
from erpnext.crm.frappe_crm_api import create_customer
from frappe.frappeclient import FrappeClient

def create_customer_in_erpnext(doc, method):
	erpnext_crm_settings = frappe.get_single("ERPNext CRM Settings")
	if (
		not erpnext_crm_settings.enabled
		or not erpnext_crm_settings.create_customer_on_status_change
		or doc.status != erpnext_crm_settings.deal_status
	):
		return

	contacts = _get_contacts(doc)
	contact_name = contacts[0]['contact']	
	address = get_contact_address(contact_name)	

	customer = {
		"customer_name": contact_name,
		"customer_group": "Individual",
		"customer_type": "Individual",
		"default_currency": doc.currency,
		"crm_deal": doc.name,
		"gender": contacts[0]['gender'],
		"contacts": json.dumps(contacts),
		"address": json.dumps(address) if address else None,
	}
	


	""" if not erpnext_crm_settings.is_erpnext_in_different_site:
		create_customer(customer)
	else:
		create_customer_in_remote_site(customer, erpnext_crm_settings) """

	try:
		if not erpnext_crm_settings.is_erpnext_in_different_site:
			customer_name = create_customer(customer)
		else:
			customer_name = create_customer_in_remote_site(customer, erpnext_crm_settings)

		if not customer_name:
			frappe.log_error(
				"Customer name not returned from ERPNext after creation",
				f"Error while creating customer in ERPNext for CRM Deal: {doc.name}",
			)
			frappe.throw(_("Error while creating customer in ERPNext, check error log for more details"))
	except Exception:
		frappe.log_error(frappe.get_traceback(), "Error while creating customer in ERPNext")
		frappe.throw(_("Error while creating customer in ERPNext, check error log for more details"))

	if customer_name:
		frappe.db.set_value("CRM Deal", doc.name, "erpnext_customer", customer_name)
		frappe.publish_realtime("crm_customer_created")

	frappe.publish_realtime("crm_customer_created")

def create_customer_in_remote_site(customer, erpnext_crm_settings):
	client = get_erpnext_site_client(erpnext_crm_settings)
	try:
		return client.post_api("erpnext.crm.frappe_crm_api.create_customer", customer)
	except Exception:
		frappe.log_error(frappe.get_traceback(), "Error while creating customer in remote site")
		frappe.throw(_("Error while creating customer in ERPNext, check error log for more details"))

def get_erpnext_site_client(erpnext_crm_settings):
	site_url = erpnext_crm_settings.erpnext_site_url
	api_key = erpnext_crm_settings.api_key
	api_secret = erpnext_crm_settings.get_password("api_secret", raise_exception=False)

	return FrappeClient(site_url, api_key=api_key, api_secret=api_secret)

	
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

