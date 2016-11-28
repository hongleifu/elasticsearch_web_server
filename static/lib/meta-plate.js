function edit_table_button_click() {
	var obj = {};
	obj.apply_id = $("#apply_id").val();
	obj.table_id = $("#table_id").val();
	obj.reviewer_id = $("#reviewer_id").val();
	obj.host_id = $("#host_id").val();
	obj.db_id = $("#db_id").val();
	obj.name = $("#name").val();
	obj.comments = $("#comments").val();
	obj.apply_desc = $("#apply_desc").val();
	obj.fields = [];
	$("#fields_table").find("tr").each(function(){
		var ele = {};	
		ele.id = $(this).find("#id").val();	
		ele.name = $(this).find("#name").val();	
		ele.field_type = $(this).find("#field_type").val();	
		ele.is_primary = $(this).find("#is_primary").val();	
		ele.is_partition = $(this).find("#is_partition").val();	
		ele.comments = $(this).find("#comments").val();	
		obj.fields.push(ele);
	});
	jsonStr = JSON.stringify(obj);
	$("#form_json_text").val(jsonStr);
	$("#edit_table_form").attr("action","/edit_table?operate=submit")
	$("#edit_table_form").submit()
}
