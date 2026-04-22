import frappe

@frappe.whitelist(allow_guest=True)
def ping():
	return "pong"

@frappe.whitelist(allow_guest=True)
def create_lead_api():
    try:
        data = frappe.local.form_dict

        if not data.get("mobileNo") or not data.get("firstname"):
            frappe.throw("Missing required fields: 'Mobile No' and 'First Name'")

        existing_lead = frappe.db.exists("CRM Lead", {"mobile_no": data["mobileNo"]})
        if existing_lead:
            frappe.response["message"] = f"Lead already exists: {existing_lead}"
            #return "Lead Exists"
        else:
            lead = frappe.get_doc({
                "doctype": "CRM Lead",
                "first_name": data["firstname"],
                "last_name": data["lastname"],
                "gender": data["gender"],
                #"email": data["email"],
                "mobile_no": data["mobileNo"],
                "status": "New",
                "source": "Website"
        })
        lead.insert(ignore_permissions=True)
        frappe.response["message"] = f"Lead created: {lead.name}"
        #return "Created"
    except Exception as e:
        frappe.response["message"] = f"Error: {str(e)}"
        #return "Not Created"