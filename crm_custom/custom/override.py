import frappe
import json
from crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings import get_contacts,create_customer_in_remote_site
from erpnext.crm.frappe_crm_api import create_customer

def create_customer_in_erpnext(doc, method):
	erpnext_crm_settings = frappe.get_single("ERPNext CRM Settings")
	if (
		not erpnext_crm_settings.enabled
		or not erpnext_crm_settings.create_customer_on_status_change
		or doc.status != erpnext_crm_settings.deal_status
	):
		return

	contacts = get_contacts(doc)
	contact_name = contacts[0]['contact']	
	address = get_contact_address(contact_name)	

	customer = {
		"customer_name": contact_name,
		"customer_group": "Individual",
		"customer_type": "Individual",
		"default_currency": doc.currency,
		"crm_deal": doc.name,
		"contacts": json.dumps(contacts),
		"address": json.dumps(address) if address else None,
	}
	


	if not erpnext_crm_settings.is_erpnext_in_different_site:
		create_customer(customer)
	else:
		create_customer_in_remote_site(customer, erpnext_crm_settings)

	frappe.publish_realtime("crm_customer_created")
	
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

