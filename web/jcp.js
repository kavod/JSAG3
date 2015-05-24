$(function() {
$.ajaxSetup({
    // Disable caching of AJAX responses
    cache: false
});

SIMPLE_TYPES = ['string','password','choices','integer','hostname','boolean','file','email'];

function getType(input_schema,path)
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
}

schema = {"properties": {"prefer":{"choices": {"duckorrabbit": {"duck": "Duck", "rabbit": "Rabbit"}}, "$def": "#/choices/duckorrabbit", "order": 6, "description": "Indicate your prefered animal", "title": "What do you prefer?"},"keywords": {"items": {"order": 1, "type": "string", "description": "Keyword", "title": "Keyword"}, "order": 5, "type": "array", "description": "Search keywords", "title": "Search keywords"},"transmission": {"description": "Transmission configuration", "title": "Transmission configuration", "required": ["server", "port", "username", "slotNumber"], "properties": {"username": {"order": 3, "type": "string", "description": "Transmission username", "title": "Username"}, "slotNumber": {"description": "Maximum number of slots", "title": "Max slots", "default": 6, "minimum": 1, "type": "integer", "order": 5}, "password": {"$def": "#/def/password", "order": 4, "description": "Transmission password", "title": "Password"}, "port": {"description": "Transmission port", "title": "Port", "default": 50762, "minimum": 1, "type": "integer", "order": 2}, "server": {"order": 1, "format": "hostname", "description": "Transmission server", "title": "Server"}}, "type": "object", "order": 2}, "transfer": {"order": 3, "type": "string", "description": "Local directory for FTP transfer","placeholder":"Keep blank for disable", "title": "Local directory"}, "tracker": {"items": {"conditions": [{"then_prop": "login", "if_val": [null, "kickass"], "if_prop": "id", "then_status": "disabled"}], "properties": {"login": {"description": "Torrent provider login information", "title": "Torrent provider login info", "required": ["username"], "properties": {"username": {"order": 1, "type": "string", "description": "Torrent provider username", "title": "Torrent provider username"}, "password": {"$def": "#/def/password", "order": 2, "description": "Torrent provider password", "title": "Torrent provider password"}}, "type": "object", "order": 2}, "id": {"choices": {"tracker_id": {"kickass": "KickAss", "t411": "T411"}}, "$def": "#/choices/tracker_id", "order": 1, "description": "Torrent provider", "title": "Torrent provider"}}, "type": "object", "description": "Torrent provider configuration", "title": "Torrent provider"}, "order": 1, "type": "array", "description": "Torrent providers", "title": "Torrent providers"}, "smtp": {"description": "SMTP configuration", "title": "SMTP configuration", "type": "object", "order": 4, "conditions": [{"then_prop": "conf", "if_val": [false], "if_prop": "enable", "then_status": "disabled"}], "properties": {"enable": {"default": false, "order": 1, "type": "boolean", "description": "Email notification activation?", "title": "Email notification activation"}, "conf": {"description": "Email notification configuration", "title": "Email configuration", "required": ["server", "port", "ssltls", "sender"], "properties": {"username": {"order": 4, "type": "string", "description": "SMTP username [if required]", "title": "SMTP username"}, "sender": {"order": 6, "format": "email", "description": "Sender email for notifications", "title": "Sender email"}, "ssltls": {"default": false, "order": 3, "type": "boolean", "description": "SSL/TLS encryption", "title": "SSL/TLS encryption"}, "server": {"order": 1, "format": "hostname", "description": "SMTP server", "title": "Server"}, "password": {"$def": "#/def/password", "order": 5, "description": "SMTP password [if required]", "title": "SMTP password"}, "port": {"description": "SMTP port", "title": "Port", "default": 587, "minimum": 1, "type": "integer", "order": 2}}, "type": "object", "order": 2}}}}, "required": ["tracker", "transmission", "smtp","prefer"], "type": "object", "description": "Configuration", "title": "Configuration"};

config = {"transmission": {"username": "niouf", "slotNumber": 6, "password": "niorf", "port": 50762, "server": "front142.sdbx.co"}, "transfer": "/volume/Series", "tracker": [{"id": "kickass"}, {"login": {"username": "Niouf", "password": "moihlijh"}, "id": "t411"}], "smtp": {"enable": true, "conf": {"username": "niouf", "ssltls": true, "sender": "niouf@niouf.fr", "password": "niorf", "port": 587, "server": "smtp.gmail.com"}},"keywords":["niouf","niorf"]};

function form_generate(id,schema,required,config,str_format)
{
	if (typeof(required) === "undefined")
		required = false
	if (typeof(str_format) === "undefined")
		str_format = '%s: '

	myDefault = (typeof(config) === "undefined") ? (('default' in schema) ? schema['default'] : '') : config;

	var node;
	if (getType(schema)=='object')
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
			item_id = full_id(id,item['id']);
			required = ('required' in schema && schema['required'].indexOf(item['id'])> -1);
			value = (typeof(config) !== "undefined" && item['id'] in config) ? config[item['id']] : undefined;

			nodeItem = form_generate(item_id,item['item'],required,value);
			node.append(nodeItem);
			map[item['id']] = item_id;
		});
		return node;
	}
	else if (getType(schema) == 'array')
	{
		node = $("<fieldset>")
				.append($("<legend>").html(str_format.replace('%s',schema['title'])));
		$.each(config,function(index,item) {
			node.append(form_generate(id + '_' + (index+1),schema['items'],false,item,'%s '+(index+1)));
		});
		return node.append(form_generate(id,schema['items'],false,undefined,'Add %s'));
	}
	else if (getType(schema) == 'password')
	{
		node = $("<div>")
				.html(str_format.replace('%s',schema['title']))
				.append($("<input>")
					.attr("type","password")
					.attr("placeholder",schema['description'])
					.attr("name",id)
					.attr("id",id)
					.attr("value",myDefault)
					.prop("required",required));
		return node;
	}
	else if (getType(schema) == 'integer')
	{
		node = $("<div>")
				.html(str_format.replace('%s',schema['title']))
				.append($("<input>")
					.attr("type","number")
					.attr("placeholder",schema['description'])
					.attr("name",id)
					.attr("id",id)
					.attr("value",myDefault)
					.prop("required",required));
		return node;
	}
	else if (getType(schema) == 'email')
	{
		node = $("<div>")
				.html(str_format.replace('%s',schema['title']))
				.append($("<input>")
					.attr("type","email")
					.attr("placeholder",schema['description'])
					.attr("name",id)
					.attr("id",id)
					.attr("value",myDefault)
					.prop("required",required));
		return node;
	}
	else if (getType(schema) == 'boolean')
	{
		myDefault = (myDefault) ? "1" : "0";
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
		nodeSelect.val(myDefault);
		node = $("<div>")
				.html(str_format.replace('%s',schema['title']))
				.append(nodeSelect);
		return node;
	}
	else if (getType(schema) == 'choices')
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
		nodeSelect.val(myDefault);
		node = $("<div>")
				.html(str_format.replace('%s',schema['title']))
				.append(nodeSelect);
		return node;
	}
	else if (SIMPLE_TYPES.indexOf(getType(schema))>-1)
	{
		node = $("<div>")
				.html(str_format.replace('%s',schema['title']))
				.append($("<input>")
					.attr("name",id)
					.attr("id",id)
					.attr("placeholder",schema['description'])
					.attr("value",myDefault)
					.prop("required",required));
		return node
	}
}

function create_events(id,schema,config)
{
	if (getType(schema)=='object')
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

		map = [];
		$.each(sortedItems,function(index,item)
		{
			value = (typeof(config) !== "undefined" && item['id'] in config) ? config[item['id']] : undefined;
			item_id = full_id(id,item['id']);
			create_events(item_id,item['item'],value);
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
				myevent['if_prop'] = full_id(id,myevent['if_prop']);
				myevent['then_prop'] = full_id(id,myevent['then_prop']);
				$('#'+myevent['if_prop']).on("change",myevent,show_hide);
				show_hide({"data":myevent});
			});
		}
	}
	else if (getType(schema) == 'array')
	{
		$.each(config,function(index,item) {
			create_events(id + '_' + (index+1),schema['items'],item);
		});
		create_events(id,schema['items'],undefined);
	}
}

function create_form(schema,config)
{
	if (typeof(config) === 'undefined')
		config = {};
	node = $("<form>")
			.append(form_generate("",schema,false,config))
			.append($("<input>").attr("type","submit"));
	return node
}

show_hide = function(event)
{
	console.log($('#'+event.data['if_prop'])[0].value);
	if(event.data['if_val'].indexOf($('#'+event.data['if_prop'])[0].value)>-1)
	{
		console.log($('#'+event.data['then_prop']));
		$('#'+event.data['then_prop']).hide();
	} else
	{
		$('#'+event.data['then_prop']).show();
	}
}

$("#myForm").append(create_form(schema,config));
create_events("",schema,config);



function full_id(path,id)
{
	return path + ((path.length>0) ? "_" + id : id)
}
});
