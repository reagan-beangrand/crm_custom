frappe.ui.form.on("CRM Deal", {    
	refresh(frm){
		console.log('extended-refresh');
	},
	/*custom_service_type(frm){
		console.log('extended-custom_service_type: ' + frm.doc.custom_service_type);
		let service_type = frm.doc.custom_service_type.trim().toLowerCase();
		debugger;
		if(service_type == 'bridal makeup')	{
			bridal_makeup_details(frm,false);
			class_details(frm,true);

		} else if(service_type == 'saree drape class (sd)' 
			|| service_type == 'master class (mc)'){
			class_details(frm,false);
			bridal_makeup_details(frm,true);
			//frm.set_df_property('custom_class_details', 'hidden', false);
			//frm.set_df_property('custom_bridal_makeup_details', 'hidden', true);
		} else{
			bridal_makeup_details(frm,false);
			class_details(frm,false);
		}
	},*/
    validate(frm){   
		console.log('extended-validate');     
        debugger;
		let service_type = frm.doc.custom_service_type.trim().toLowerCase();
		//Other than Bridal Makeup validation
		if(service_type!= 'bridal makeup'){
			if(frm.doc.custom_date_of_joining < frappe.datetime.get_today()){
				frappe.msgprint(__('You can not select past date in Date of Joining'));
				frappe.validated = false;
			}
		}
		//Bridal Makeup validation
		else { 
			
			if(frm.doc.custom_datetime < frappe.datetime.get_today()){
				frappe.msgprint(__('You can not select past date in DateTime'));
				frappe.validated = false;
			} else {
				let primary = frm.doc.custom_primary_mua;
				let secondary = frm.doc.custom_secondary_mua;
				if(primary != undefined && secondary != undefined){
						if(primary.toLowerCase() === secondary.toLowerCase()){
						frappe.msgprint('Primary and Secondary MUA should not be same person');
						frappe.validated = false;
					}			
				}

			}
		}
    }
})

function bridal_makeup_details(frm,ishidden) {
	frm.set_df_property('custom_bridal_makeup_details', 'hidden', ishidden);
	frm.set_df_property('custom_event', 'hidden', ishidden);
	frm.set_df_property('custom_datetime', 'hidden', ishidden);
	frm.set_df_property('custom_primary_mua', 'hidden', ishidden);
	frm.set_df_property('custom_secondary_mua', 'hidden', ishidden);
}

function class_details(frm,ishidden) {
	frm.set_df_property('custom_class_details', 'hidden', ishidden);
	frm.set_df_property('custom_course_name', 'hidden', ishidden);
	frm.set_df_property('custom_date_of_joining', 'hidden', ishidden);
	frm.set_df_property('custom_admission_number', 'hidden', ishidden);
	frm.set_df_property('custom_batch', 'hidden', ishidden);
}
