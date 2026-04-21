import frappe


@frappe.whitelist()
def create_lead_api():
    data = frappe.form_dict

    if not data.get("mobileNo") or not data.get("firstname"):
        frappe.throw("Missing required fields: 'mobileNo' and 'firstname'")

    existing_lead = frappe.db.exists("CRM Lead", {"email": data["email"]})
    if existing_lead:
        frappe.response["message"] = f"Lead already exists: {existing_lead}"
    else:
        lead = frappe.get_doc({
            "doctype": "CRM Lead",
            "first_name": data["firstname"],
            "email": data["email"],
            "mobile_no": data["mobileNo"],
            "status": "New",
            "source": "Website"
    })
    lead.insert(ignore_permissions=True)
    frappe.response["message"] = f"Lead created: {lead.name}"