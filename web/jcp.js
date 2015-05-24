;jcp = {

	SIMPLE_TYPES: ['string','password','choices','integer','hostname','boolean','file','email'],

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
			return node.append(jcp.form_generate(id + '_0',schema['items'],false,undefined,'Add %s',level+1).addClass('new'));
		}
		else if (jcp.getType(schema) == 'password')
		{
			node = $("<div>")
					.append($("<label>")
						.html(str_format.replace('%s',schema['title']))
						.addClass('nv'+level)
						)
					.append($("<input>")
						.attr("type","password")
						.attr("placeholder",schema['description'])
						.attr("name",id)
						.attr("id",id)
						.prop("required",required));
			return node;
		}
		else if (jcp.getType(schema) == 'integer')
		{
			inputNode = $("<input>")
						.attr("type","number")
						.attr("placeholder",schema['description'])
						.attr("name",id)
						.attr("id",id)
						.prop("required",required);
			if ('minimum' in schema)
				inputNode.attr("min",('exclusiveMinimum' in schema && schema['exclusiveMinimum']) ? parseInt(schema['minimum']) + 1 : schema['minimum']);
			
			if ('maximum' in schema)
				inputNode.attr("max",('exclusiveMaximum' in schema && schema['exclusiveMaximum']) ? parseInt(schema['maximum']) - 1 : schema['maximum']);
	
	
			node = $("<div>")
					.append($("<label>").html(str_format.replace('%s',schema['title']))
						.addClass('nv'+level)
						)
					.append(inputNode);
			return node;
		}
		else if (jcp.getType(schema) == 'email')
		{
			node = $("<div>")
					.append($("<label>").html(str_format.replace('%s',schema['title']))
						.addClass('nv'+level)
						)
					.append($("<input>")
						.attr("type","email")
						.attr("placeholder",schema['description'])
						.attr("name",id)
						.attr("id",id)
						.prop("required",required));
			return node;
		}
		else if (jcp.getType(schema) == 'boolean')
		{
			nodeSelect = $("<select>")
						.attr("name",id)
						.attr("id",id)
						.prop("required",required);


			choices = {"0":"No","1":"Yes"};
			$.each(choices,function(key,value) {
				nodeSelect.append($("<option>")
							.attr("value",key)
							.html(value)
							);
			});
			node = $("<div>")
					.append($("<label>").html(str_format.replace('%s',schema['title']))
						.addClass('nv'+level)
						)
					.append(nodeSelect);
			return node;
		}
		else if (jcp.getType(schema) == 'choices')
		{
			nodeSelect = $("<select>")
						.attr("name",id)
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
						)
					.append(nodeSelect);
			return node;
		}
		else if (jcp.SIMPLE_TYPES.indexOf(jcp.getType(schema))>-1)
		{
			node = $("<div>")
					.append($("<label>").html(str_format.replace('%s',schema['title']))
						.addClass('nv'+level)
						)
					.append($("<input>")
						.attr("name",id)
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
				node.before(jcp.form_generate(id + '_' + (index+1),schema['items'],false,item,'%s '+(index+1),level+1));
			});
		
			$.each(config,function(index,item) {
				jcp.form_setValue(id + '_' + (index+1),schema['items'],item,level+1);
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
			myDefault = (myDefault) ? "1" : "0";
			nodeSelect = $('#' + id );
			nodeSelect.val(myDefault);
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
				cur_left = jcp.create_events(id + '_' + (index+1),schema['items'],item);
				max_left = (max_left < cur_left) ? cur_left : max_left;
			});
			cur_left = jcp.create_events(id + '_0',schema['items'],undefined);
			max_left = (max_left < cur_left) ? cur_left : max_left;
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
		node.append($("<form>")
				.append(jcp.form_generate(id,schema,false,config))
				.append($("<input>").attr("type","button").attr("id","reset"))
				.append($("<input>").attr("type","submit")));
		jcp.form_setValue(id,schema,config);
		jcp.create_events(id,schema,config);
		jcp.align_values(schema,config);
	},

	show_hide: function(event)
	{
		if(event.data['if_val'].indexOf($('#'+event.data['if_prop'])[0].value)>-1)
		{
			$('#'+event.data['then_prop']).hide();
		} else
		{
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
	}
};
