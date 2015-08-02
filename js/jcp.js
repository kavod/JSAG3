/**
 * Usage:
 *
 *  * jcp.create_form(node,id,schema,data);
 *  	Will insert a form based on the schema defaulted with the data
 *  @param {node} node: reference to a node element which will contain the generated <FORM>
 *      Note that all existing contents of the node element will be erased
 *  @param {string} id: ID property of the generated form.
 *  @param {Object} schema: object containing the JSONschema describing the form structure.
 *  @param {Object=} data: object containing the current data content of the form (optional).
 *      It is highly recommended to NOT communicate clear content of password fields (replace with genetic values as ****)
 */

;jcp = {

	SIMPLE_TYPES: ['string','password','choices','integer','hostname','boolean','file','email'],
	SCHEMA: {},
	VALUES: {},

	getType: function (input_schema,path)
	{
		if (typeof(path) === "undefined")
			path = [];
		configParser = input_schema;
		if (path.length > 0)
		{
			$.each(path,function(index,level)
			{
				if (level === parseInt(level,10))
					configParser = configParser["items"]; 
				else
					configParser = configParser["properties"][level];
			});
		}

		if ('type' in configParser)
			return configParser['type'];
		if ('format' in configParser)
			return configParser['format'];
		if ('$def' in configParser)
		{
			defRegex = /^#\/def\/(\w+)/i;
			myType = defRegex.exec(configParser['$def']);
			if (myType)
			{
				return myType[1];
		 	}
			else
			{
				defRegex = /^#\/choices\/(\w+)$/i;
				myType = defRegex.exec(configParser['$def']);
				if (myType)
					return "choices";
			}
		}
		return "";
	},


	form_generate: function (id,schema,required,config,str_format,level)
	{
		if (typeof(required) === "undefined")
			required = false
		if (typeof(str_format) === "undefined")
			str_format = '%s: '
		if (typeof(level) === "undefined")
			level = 0;

		myDefault = (typeof(config) === "undefined") ? (('default' in schema) ? schema['default'] : '') : config;

		var node;
		if (jcp.getType(schema)=='object')
		{
			node = $("<fieldset>")
					.attr('id',id)
					.append($("<legend>").html(str_format.replace('%s',schema['title'])));
			sortedItems = [];
			$.each(schema['properties'],function(index,item)
			{
				sortedItems.push({'id':index,'order':item['order'],'item':item});
			});

			sortedItems = sortedItems.sort(function (a, b) {
				if (!('order' in a)) a['order'] = 0;
				if (!('order' in b)) b['order'] = 0;
			
				return a['order']> b['order'] ;
			});

			map = [];
			$.each(sortedItems,function(index,item)
			{
				item_id = jcp.full_id(id,item['id']);
				required = ('required' in schema && schema['required'].indexOf(item['id'])> -1);
				value = (typeof(config) !== "undefined" && item['id'] in config) ? config[item['id']] : undefined;

				nodeItem = jcp.form_generate(item_id,item['item'],required,value,'%s',level+1);
				node.append(nodeItem);
				map[item['id']] = item_id;
			});
			return node;
		}
		else if (jcp.getType(schema) == 'array')
		{
			node = $("<fieldset>")
					.attr('id',id)
					.append($("<legend>").html(str_format.replace('%s',schema['title'])));
			/*newNode = $('<form>')
						.append(jcp.form_generate(id + '_',schema['items'],true,undefined,'Add %s',level+1)
							.append($('<input>')
								.attr('type','button')
								.attr('value','Add')
								.on('click',function(event) {
										$('#' + id + '_submit').click();
									})
								)
							.append($('<input>')
								.attr('type','submit')
								.css('display','none')
								.attr('id',id + '_submit')
								)
							)
						.attr('id','new_' + id)
						.on('submit',function(event) {
							defRegex = /^(.*)_([0-9]+)$/i;
							myID = defRegex.exec($('#'+event.target.id).prev()[0].id);
							jcp.getFromJSON(jcp.VALUES,id).push(jcp.getFromJSON($('#'+event.target.id).serializeObject(),id)[0]);
							jcp.updateForms();
							$('#'+event.target.id)[0].reset();
							event.preventDefault();
						})
						.addClass('new');
			node.append(newNode);*/
			newNode = $('<a href></a>')
						.html('Add %s'.replace('%s',schema['title']))
						.attr('id','new_' + id)
						.addClass('new')
						.on('click',function(event) {
							event.preventDefault();
							defRegex = /^(.*)_([0-9]+)$/i;
							myID = defRegex.exec($('#'+event.target.id).prev()[0].id);
							jcp.getFromJSON(jcp.VALUES,id).push(
								jcp.getFromJSON(
										$('<form>')
										.append(jcp.form_generate(id + '_',schema['items'],true,undefined,'Add %s',level+1))
										.serializeObject()
									,id+'_0')
								);
							jcp.updateForms();
						});
			node.append(newNode);
			return node;
		}
		else if (jcp.getType(schema) == 'password')
		{
			node = $("<div>")
					.append($("<label>")
						.html(str_format.replace('%s',schema['title']))
						.addClass('nv'+level)
						.attr('for',id)
						)
					.append($("<input>")
						.attr("type","password")
						.attr("placeholder",schema['description'])
						.attr("name",jcp.idToName(id))
						.attr("id",id)
						.prop("required",required));
			return node;
		}
		else if (jcp.getType(schema) == 'integer')
		{
			inputNode = $("<input>")
						.attr("type","number")
						.attr("placeholder",schema['description'])
						.attr("name",jcp.idToName(id))
						.attr("id",id)
						.prop("required",required);
			if ('minimum' in schema)
				inputNode.attr("min",('exclusiveMinimum' in schema && schema['exclusiveMinimum']) ? parseInt(schema['minimum']) + 1 : schema['minimum']);
			
			if ('maximum' in schema)
				inputNode.attr("max",('exclusiveMaximum' in schema && schema['exclusiveMaximum']) ? parseInt(schema['maximum']) - 1 : schema['maximum']);
	
	
			node = $("<div>")
					.append($("<label>").html(str_format.replace('%s',schema['title']))
						.addClass('nv'+level)
						.attr('for',id)
						)
					.append(inputNode);
			return node;
		}
		else if (jcp.getType(schema) == 'email')
		{
			node = $("<div>")
					.append($("<label>").html(str_format.replace('%s',schema['title']))
						.addClass('nv'+level)
						.attr('for',id)
						)
					.append($("<input>")
						.attr("type","email")
						.attr("placeholder",schema['description'])
						.attr("name",jcp.idToName(id))
						.attr("id",id)
						.prop("required",required));
			return node;
		}
		else if (jcp.getType(schema) == 'boolean')
		{
			nodeSelect = $("<input>")
						.attr('type','checkbox')
						.attr("name",jcp.idToName(id))
						.attr("id",id);


			/*choices = {"0":"No","1":"Yes"};
			$.each(choices,function(key,value) {
				nodeSelect.append($("<option>")
							.attr("value",key)
							.html(value)
							);
			});*/
			node = $("<div>")
					.append($("<label>").html(str_format.replace('%s',schema['title']))
						.addClass('nv'+level)
						.attr('for',id)
						)
					.append(nodeSelect);
			return node;
		}
		else if (jcp.getType(schema) == 'choices')
		{
			nodeSelect = $("<select>")
						.attr("name",jcp.idToName(id))
						.attr("id",id)
						.prop("required",required);
					
			nodeSelect.append($("<option>")
						.attr("value","")
						.html(schema['description'])
						);

			defRegex = /^#\/choices\/(\w+)/i;
			myType = defRegex.exec(schema['$def']);
			if (myType)
			{
				choices = schema['choices'][myType[1]];
				$.each(choices,function(key,value) {
					nodeSelect.append($("<option>")
								.attr("value",key)
								.html(value)
								);
				});
			}
			node = $("<div>")
					.append($("<label>").html(str_format.replace('%s',schema['title']))
						.addClass('nv'+level)
						.attr('for',id)
						)
					.append(nodeSelect);
			return node;
		}
		else if (jcp.SIMPLE_TYPES.indexOf(jcp.getType(schema))>-1)
		{
			node = $("<div>")
					.append($("<label>").html(str_format.replace('%s',schema['title']))
						.addClass('nv'+level)
						.attr('for',id)
						)
					.append($("<input>")
						.attr("name",jcp.idToName(id))
						.attr("id",id)
						.attr("placeholder",schema['description'])
						.prop("required",required));
			return node
		}
	},

	form_setValue: function (id,schema,config,level)
	{
		if (typeof(level) === "undefined")
			level = 0;

		myDefault = (typeof(config) === "undefined") ? (('default' in schema) ? schema['default'] : '') : config;

		var node;
		if (jcp.getType(schema)=='object')
		{
			sortedItems = [];
			$.each(schema['properties'],function(index,item)
			{
				sortedItems.push({'id':index,'order':item['order'],'item':item});
			});

			sortedItems = sortedItems.sort(function (a, b) {
				if (!('order' in a)) a['order'] = 0;
				if (!('order' in b)) b['order'] = 0;
			
				return a['order']> b['order'] ;
			});

			$.each(sortedItems,function(index,item)
			{
				item_id = jcp.full_id(id,item['id']);
				value = (typeof(config) !== "undefined" && item['id'] in config) ? config[item['id']] : undefined;

				jcp.form_setValue(item_id,item['item'],value,level+1);
			});
		}
		else if (jcp.getType(schema) == 'array')
		{
			$('#' + id +'>:not(.new):not(legend)').remove();
			node = $('#' + id +'>.new');
			$.each(config,function(index,item) {
				node.before(
					jcp.form_generate(id + '_' + index,schema['items'],true,item,'%s '+(index+1),level+1)
						.append($('<input>')
							.attr('type','button')
							.attr('value','Delete')
							.on('click',function(event) {
									jcp.getFromJSON(jcp.VALUES,id).splice(index,1);
									jcp.updateForms();
								})
						)
				);
			});
		
			$.each(config,function(index,item) {
				jcp.form_setValue(id + '_' + (index),schema['items'],item,level+1);
			});
		}
		else if (jcp.getType(schema) == 'password')
		{
			$('#' + id ).val(myDefault);
		}
		else if (jcp.getType(schema) == 'integer')
		{
			$('#' + id ).val(myDefault);
		}
		else if (jcp.getType(schema) == 'email')
		{
			$('#' + id ).val(myDefault);
		}
		else if (jcp.getType(schema) == 'boolean')
		{
			//myDefault = (myDefault) ? "1" : "0";
			nodeSelect = $('#' + id );
			nodeSelect.prop("checked",myDefault);
		}
		else if (jcp.getType(schema) == 'choices')
		{
			nodeSelect = $('#' + id );
			nodeSelect.val(myDefault);
		}
		else if (jcp.SIMPLE_TYPES.indexOf(jcp.getType(schema))>-1)
		{
			$('#' + id ).val(myDefault);
		}
	},

	create_events: function(id,schema,config)
	{
		var max_left;
		var cut_left;
		if (jcp.getType(schema)=='object')
		{
			max_left = 0;
			sortedItems = [];
			$.each(schema['properties'],function(index,item)
			{
				sortedItems.push({'id':index,'order':item['order'],'item':item});
			});

			sortedItems = sortedItems.sort(function (a, b) {
				if (!('order' in a)) a['order'] = 0;
				if (!('order' in b)) b['order'] = 0;
			
				return a['order']> b['order'] ;
			});

			map = [];
			$.each(sortedItems,function(index,item)
			{
				value = (typeof(config) !== "undefined" && item['id'] in config) ? config[item['id']] : undefined;
				item_id = jcp.full_id(id,item['id']);
				cur_left = jcp.create_events(item_id,item['item'],value);
				max_left = (max_left < cur_left) ? cur_left : max_left;
				map[item['id']] = item_id;
			});

			if ("conditions" in schema)
			{
				$.each(schema['conditions'],function(key,val) 										  
				{
					myevent = Object.create(val);
					myevent['if_val'] = val['if_val'].slice(0);
					index = myevent['if_val'].indexOf(null)
					if (index!=-1)
					{
						myevent['if_val'][index] = "";
					}
					myevent['map'] = map;
					myevent['if_prop'] = jcp.full_id(id,myevent['if_prop']);
					myevent['then_prop'] = jcp.full_id(id,myevent['then_prop']);
					$('#'+myevent['if_prop']).on("change",myevent,jcp.show_hide);
					jcp.show_hide({"data":myevent});
				});
			}
			return max_left;
		}
		else if (jcp.getType(schema) == 'array')
		{
			max_left = 0;
			$.each(config,function(index,item) {
				cur_left = jcp.create_events(id + '_' + (index),schema['items'],item);
				max_left = (max_left < cur_left) ? cur_left : max_left;
			});
			/*cur_left = jcp.create_events(id + '_',schema['items'],undefined);
			max_left = (max_left < cur_left) ? cur_left : max_left;*/
		}
		else
		{
			return $('#'+id).offset()['left'];
		}
	},

	create_form: function (node,id,schema,config)
	{
		if (typeof(config) === 'undefined')
			config = {};
		node.html('');
		newNode = $("<form>")
				.append(jcp.form_generate(id,schema,false,config))
				.append($('<input>')
					.attr('type','submit')
					.attr('id',id + '_submit')
					);
		node.append(newNode);
		jcp.SCHEMA[id] = schema;
		jcp.VALUES[id] = config;
		
		jcp.updateForms();
		
		return newNode;
	},
	
	updateForms: function()
	{
		for (key in jcp.VALUES)
		{
			jcp.form_setValue(key,jcp.SCHEMA[key],jcp.VALUES[key]);
			jcp.create_events(key,jcp.SCHEMA[key],jcp.VALUES[key]);
			jcp.align_values(jcp.SCHEMA[key],jcp.VALUES[key]);
		}
	},
	
/*	schema_to_form: function(node,jcp_path,id)
	{
		schema_path = jcp_path + 'schema/' + id
		values_path = jcp_path + 'values/' + id
		$.getJSON( schema_path, function( data ) {
			var schema = data;
			$.getJSON( values_path, function( data ) {
				jcp.create_form(node,id,schema,data);
			});
		});
	},*/

	show_hide: function(event)
	{
		var if_field = $('#'+event.data['if_prop'])[0];
		value = if_field.type == 'checkbox' ? if_field.checked : if_field.value;
	
		if(event.data['if_val'].indexOf(value)>-1)
		{
			$('#'+event.data['then_prop']).hide();
			$('#'+event.data['then_prop'] + " *[required]").addClass("hidden_required_field");
			$('#'+event.data['then_prop'] + " .hidden_required_field").prop('required',false);
		} else
		{
			$('#'+event.data['then_prop'] + " .hidden_required_field").prop('required',true);
			$('#'+event.data['then_prop'] + " .hidden_required_field").removeClass("hidden_required_field");
			$('#'+event.data['then_prop']).show();
		}
	},

	align_values: function (schema,config)
	{
		var maxLabelNv = Array(9);
		for(var i = 1 ; i < 10 ; i++)
			$("label.nv" + i.toString()).css('width','auto');
		var maxInput = jcp.maxLeft("input,select");
		for(var i = 1 ; i < 10 ; i++)
			maxLabelNv[i] = jcp.maxLeft("label.nv" + i.toString());
		$("label").css('display','inline-block');
		for(var i = 1 ; i < 10 ; i++)
			$("label.nv" + i.toString()).css('width',maxInput-maxLabelNv[i]+10);
	},

	maxLeft: function (selector)
	{
		return Math.max.apply(null, $(selector).map(function ()
		{
			return $(this).offset()['left'];
		}).get());
	},

	full_id: function (path,id)
	{
		return path + ((path.length>0) ? "_" + id : id)
	},
	
	idToName: function(myString) 
	{
		while(myString!=myString.replace(new RegExp("^([^_]+)_([^_]*)(.*)$"),"$1[$2]$3")) 
			myString=myString.replace(new RegExp("^([^_]+)_([^_]*)(.*)$"),"$1[$2]$3");
		return myString 
	},
	
	getFromJSON: function(json,myString) 
	{
		regex_str = "^([^_]+)_(.*)$";
	
		result = json;
		var reg = myString.match(new RegExp(regex_str));
		while(reg) 
		{
			myString=myString.replace(new RegExp(regex_str),"$2");
			result = result[reg[1]];
			reg = myString.match(new RegExp(regex_str));
		}
		return result[myString];
	}
};
