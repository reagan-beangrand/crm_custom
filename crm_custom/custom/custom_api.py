import frappe

@frappe.whitelist(allow_guest=True)
def ping():
	return "pong"

@frappe.whitelist(allow_guest=True)
def create_lead_api():
    try:
        data = frappe.local.form_dict
        lead_fn = data.get("firstname")

        if not data.get("mobileNo") or not lead_fn:
            frappe.throw("Missing required fields: 'Mobile No' and 'First Name'")

        existing_lead = frappe.db.get_value("CRM Lead", {"mobile_no": data["mobileNo"]},"first_name")
        if existing_lead:
            frappe.response["message"] = f"Thank you! {existing_lead} details have been already exists."
            #return "Lead Exists"
        else:
            lead = frappe.get_doc({
                "doctype": "CRM Lead",
                "first_name": lead_fn,
                "last_name": data["lastname"],
                "gender": data["gender"],
                #"email": data["email"],
                "mobile_no": data["mobileNo"],
                "status": "New",
                "source": "Website" })
            lead.insert(ignore_permissions=True)
            frappe.response["message"] = f"Thank you! {lead_fn} details have been securely saved."
                #return "Created"
    except Exception as e:
        frappe.response["message"] = f"Error: {str(e)}"
        #return "Not Created"