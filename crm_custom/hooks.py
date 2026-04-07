app_name = "crm_custom"
#app_name = "crm"
app_title = "MTBS CRM"
app_publisher = "MTBS"
app_description = "customized crm app"
app_email = "reagan.grand@gmail.com"
app_license = "mit"
#app_icon_url = "/assets/crm_custom/images/logo.svg"
#app_icon_title = "MTBS CRM"
#app_icon_route = "/crm"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
	{
# 		"name": "crm_custom",
# 		"logo": "/assets/crm_custom/logo.png",
# 		"title": "Crm Custom",
# 		"route": "/crm_custom",
# 		"has_permission": "crm_custom.api.permission.has_app_permission"

          "name": "crm",
		"logo": "/assets/crm_custom/images/logo.svg",
		"title": "MTBS CRM",
		"route": "/crm",
		"has_permission": "crm.api.check_app_permission",
	}
          
 ]
export_python_type_annotations = True
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/crm_custom/css/crm_custom.css"
# app_include_js = "/assets/crm_custom/js/crm_custom.js"

# include js, css files in header of web template
# web_include_css = "/assets/crm_custom/css/crm_custom.css"
# web_include_js = "/assets/crm_custom/js/crm_custom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "crm_custom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"CRM Deal" : "public/js/custom_fcrm_deal.js"}
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "crm_custom/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "crm_custom.utils.jinja_methods",
# 	"filters": "crm_custom.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "crm_custom.install.before_install"
# after_install = "crm_custom.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "crm_custom.uninstall.before_uninstall"
# after_uninstall = "crm_custom.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "crm_custom.utils.before_app_install"
# after_app_install = "crm_custom.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "crm_custom.utils.before_app_uninstall"
# after_app_uninstall = "crm_custom.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "crm_custom.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

#doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
#"CRM Deal": {        
 #       "before_update": "crm_custom.custom.crm_deal.validate"
#      }        
#}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"crm_custom.tasks.all"
# 	],
# 	"daily": [
# 		"crm_custom.tasks.daily"
# 	],
# 	"hourly": [
# 		"crm_custom.tasks.hourly"
# 	],
# 	"weekly": [
# 		"crm_custom.tasks.weekly"
# 	],
# 	"monthly": [
# 		"crm_custom.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "crm_custom.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
extend_doctype_class = {
# 	"Task": "crm_custom.custom.task.CustomTaskMixin"
     "CRM Lead": "crm_custom.custom.crm_lead.ExtendedCRMLead",
     "CRM Deal": "crm_custom.custom.crm_deal.ExtendedCRMDeal",
     "Contact": "crm_custom.custom.contact.ExtendedContact",
     "Quotation": "crm_custom.custom.quotation.ExtendedQuotation",
     #"ERPNext CRM Settings":"crm_custom.custom.erpnext_crm_settings.ExtendedERPNextCRMSettings",
 }

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "crm_custom.event.get_events"
     "crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings.get_quotation_url": "crm_custom.custom.override_whitelist.get_quotation_url",
     "crm.fcrm.doctype.crm_deal.crm_deal.create_deal": "crm_custom.custom.override_whitelist.create_deal",
     "crm.api.contact.get_linked_deals": "crm_custom.custom.override_whitelist.get_linked_deals"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "crm_custom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["crm_custom.utils.before_request"]
# after_request = ["crm_custom.utils.after_request"]

# Job Events
# ----------
# before_job = ["crm_custom.utils.before_job"]
# after_job = ["crm_custom.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"crm_custom.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

fixtures=[
     #{"dt":"Workspace","filters":[["module","IN",["FCRM"]]]},
     #{"dt":"Desktop Icon","filters":[["app","IN",["crm"]]]},
     #{"dt":"Workspace Sidebar","filters":[["name","IN",["Frappe CRM"]]]},
     #{"dt":"ERPNext CRM Settings"},
     #{"dt":"FCRM Settings"},
     #{"dt":"Website Settings"},
     #{"dt":"CRM Fields Layout","filters":[["name","IN",["Contact-Quick Entry","Contact-Side Panel","CRM Deal-Quick Entry","CRM Deal-Data Fields","CRM Deal-Side Panel","CRM Lead-Quick Entry","CRM Lead-Data Fields","CRM Lead-Side Panel"]]]}
     #{"dt":"CRM Lead Source","filters":[["name","IN",["Website","Deal"]]]},
    ]
