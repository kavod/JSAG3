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

schema = {"properties": {"keywords": {"items": {"order": 1, "type": "string", "description": "Keyword", "title": "Keyword"}, "order": 5, "type": "array", "description": "Search keywords", "title": "Search keywords"},"transmission": {"description": "Transmission configuration", "title": "Transmission configuration", "required": ["server", "port", "username", "slotNumber"], "properties": {"username": {"order": 3, "type": "string", "description": "Transmission username", "title": "Username"}, "slotNumber": {"description": "Maximum number of slots", "title": "Max slots", "default": 6, "minimum": 1, "type": "integer", "order": 5}, "password": {"$def": "#/def/password", "order": 4, "description": "Transmission password", "title": "Password"}, "port": {"description": "Transmission port", "title": "Port", "default": 50762, "minimum": 1, "type": "integer", "order": 2}, "server": {"order": 1, "format": "hostname", "description": "Transmission server", "title": "Server"}}, "type": "object", "order": 2}, "transfer": {"order": 3, "type": "string", "description": "Local directory for FTP transfer","placeholder":"Keep blank for disable", "title": "Local directory"}, "tracker": {"items": {"conditions": [{"then_prop": "login", "if_val": [null, "kickass"], "if_prop": "id", "then_status": "disabled"}], "properties": {"login": {"description": "Torrent provider login information", "title": "Torrent provider login info", "required": ["username"], "properties": {"username": {"order": 1, "type": "string", "description": "Torrent provider username", "title": "Torrent provider username"}, "password": {"$def": "#/def/password", "order": 2, "description": "Torrent provider password", "title": "Torrent provider password"}}, "type": "object", "order": 2}, "id": {"choices": {"tracker_id": {"kickass": "KickAss", "t411": "T411"}}, "$def": "#/choices/tracker_id", "order": 1, "description": "Torrent provider", "title": "Torrent provider"}}, "type": "object", "description": "Torrent provider configuration", "title": "Torrent provider"}, "order": 1, "type": "array", "description": "Torrent providers", "title": "Torrent providers"}, "smtp": {"description": "SMTP configuration", "title": "SMTP configuration", "type": "object", "order": 4, "conditions": [{"then_prop": "conf", "if_val": [false], "if_prop": "enable", "then_status": "disabled"}], "properties": {"enable": {"default": false, "order": 1, "type": "boolean", "description": "Email notification activation?", "title": "Email notification activation"}, "conf": {"description": "Email notification configuration", "title": "Email configuration", "required": ["server", "port", "ssltls", "sender"], "properties": {"username": {"order": 4, "type": "string", "description": "SMTP username [if required]", "title": "SMTP username"}, "sender": {"order": 6, "format": "email", "description": "Sender email for notifications", "title": "Sender email"}, "ssltls": {"default": false, "order": 3, "type": "boolean", "description": "SSL/TLS encryption", "title": "SSL/TLS encryption"}, "server": {"order": 1, "format": "hostname", "description": "SMTP server", "title": "Server"}, "password": {"$def": "#/def/password", "order": 5, "description": "SMTP password [if required]", "title": "SMTP password"}, "port": {"description": "SMTP port", "title": "Port", "default": 587, "minimum": 1, "type": "integer", "order": 2}}, "type": "object", "order": 2}}}}, "required": ["tracker", "transmission", "smtp"], "type": "object", "description": "Configuration", "title": "Configuration"};


function form_generate(id,schema)
{
	var node;
	if (getType(schema)=='object')
	{
		node = $("<fieldset>")
				.append($("<legend>").html(schema['title']));
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
			item_id = id + ((id.length>0) ? "_" + item['id'] : item['id']);
			node.append(form_generate(item_id,item['item']));
		});
		return node;
	}
	else if (getType(schema) == 'array')
	{
		return form_generate(id,schema['items']);
	}
	else if (getType(schema) == 'password')
	{
		node = $("<div>")
				.html(schema['title'])
				.append($("<input>")
					.attr("type","password")
					.attr("name",id));
		return node;
	}
	else if (getType(schema) == 'integer')
	{
		node = $("<div>")
				.html(schema['title'])
				.append($("<input>")
					.attr("type","number")
					.attr("name",id));
		return node;
	}
	else if (getType(schema) == 'email')
	{
		node = $("<div>")
				.html(schema['title'])
				.append($("<input>")
					.attr("type","email")
					.attr("name",id));
		return node;
	}
	else if (getType(schema) == 'choices')
	{
		nodeSelect = $("<select>")
					.attr("name",id);

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
				.html(schema['title'])
				.append(nodeSelect);
		return node;
	}
	else if (SIMPLE_TYPES.indexOf(getType(schema))>-1)
	{
		node = $("<div>")
				.html(schema['title'])
				.append($("<input>")
					.attr("name",id));
		return node
	}
}

$("#myForm").append(form_generate("",schema));

});
