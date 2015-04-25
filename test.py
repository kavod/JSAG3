#!/usr/bin/env python
#encoding:utf-8

from jsonConfigParser import *

myDict_login = {
	"title": "Torrent provider login info",
	"description": "Torrent provider login information",
    "type": "object",
    "properties": 
    {
        "username": 
        {
    		"title": "Torrent provider username",
    		"description": "Torrent provider username",
    		"type": "string",
    		"order":1
        },
    	"password": 
    	{
    		"title": "Torrent provider password",
    		"description": "Torrent provider password",
    		"$def": "#/def/password",
    		"order":2
        }
    },
    "required": [ "username" ],
    "order":2
}

myDict_tracker = {
	"title": "Torrent provider",
	"description": "Torrent provider configuration",
    "type": "object",
    "properties": 
    {
        "id": 
        {
    		"title": "Torrent provider",
    		"description": "Torrent provider",
    		"$def": "#/choices/tracker_id",
    		"order":1,
    
			"choices": 
			{
				"tracker_id":
				{
					"t411":"T411",
					"kickass":"KickAss",
				}
			},
        },
    	"login": myDict_login
    },
    "conditions":
	[
		{ 
			"if_prop": "id", 
			"if_val": [None,'kickass'], 
			'then_prop':'login', 
			'then_status':'disabled' 
		}
	]
}

myDict_tracker_list = {
	"title":"Torrent providers",
    "description": "Torrent providers",
	"type":"array",
	"items": myDict_tracker,
	"order":1
}

myDict_transmission = {
	"title": "Transmission configuration",
    "description": "Transmission configuration",
    "type": "object",
    "properties": 
    {
        "server": 
        {
    		"title": "Server",
    		"description": "Transmission server",
    		"type": "string",
    		"format": "hostname",
    		"order":1
        },
        "port": 
        {
    		"title": "Port",
    		"description": "Transmission port",
    		"type": "integer",
    		"minimum":1,
    		"order":2,
    		"default": 50762
        },
        "username": 
        {
    		"title": "Username",
    		"description": "Transmission username",
    		"type": "string",
    		"order":3
        },
        "password": 
        {
        	"title": "Password",
    		"description": "Transmission password",
    		"$def": "#/def/password",
    		"order":4
        },
        "slotNumber": 
        {
        	"title": "Max slots",
    		"description": "Maximum number of slots",
    		"type": "integer",
    		"minimum":1,
    		"default":6,
    		"order":5
        },
    },
    "required": [ "server","port","username","slotNumber" ],
    "order":2
}

myDict_smtp_conf = {
	"title": "Transmission configuration",
    "description": "Transmission configuration",
    "type": "object",
    "properties": 
    {
        "server": 
        {
    		"title": "Server",
    		"description": "SMTP server",
    		"type": "string",
    		"format": "hostname",
    		"order":1
        },
        "port": 
        {
    		"title": "Port",
    		"description": "SMTP port",
    		"type": "integer",
    		"minimum":1,
    		"order":2,
    		"default": 587
        },
        "ssltls":
        {
        	"title": "SSL/TLS encryption",
        	"description": "SSL/TLS encryption",
        	"type": "boolean",
        	"default":False,
        	"order":3,
        },
        "username": 
        {
    		"title": "SMTP username",
        	"description": "SMTP username [if required]",
    		"type": "string",
    		"order":4
        },
        "password": 
        {
        	"title": "SMTP password",
        	"description": "SMTP password [if required]",
    		"$def": "#/def/password",
    		"order":5
        },
        "sender": 
        {
        	"title": "Sender email",
        	"description": "Sender email for notifications",
    		"type": "string",
    		"format": "email",
    		"order":6
        },
	},
	"required": ['server','port','ssltls','sender'],
	"order":2,
}

myDict_smtp = {
	"title": "SMTP configuration",
	"description": "SMTP configuration",
    "type": "object",
    "properties": 
    {
        "enable":
        {
        	"title": "Email notification activation",
        	"description": "Email notification activiation?",
        	"type": "boolean",
        	"default": False,
        	"order":1,
        },
        "conf":myDict_smtp_conf,
	},
    "conditions":
	[
		{ 
			"if_prop": "enable", 
			"if_val": [False], 
			'then_prop':'conf', 
			'then_status':'disabled' 
		}
	],
	"order":4,
}

myDict = {
	"title":"Configuration",
	"description":"Configuration",
    "type": "object",
    "properties": 
    {
        "tracker": myDict_tracker_list,
        "transmission": myDict_transmission,
        "transfer":
        {
        	"title": "Local directory",
        	"description": "Local directory for FTP transfer. [Keep blank for disable]",
        	"type":"string",
        	"order":3,
        },
        "smtp": myDict_smtp,
    },
    "required":['tracker','transmission','smtp']
}

config = {'transmission': {'username': 'niouf', 'slotNumber': 6, 'password': 'niorf', 'port': 50762, 'server': 'front142.sdbx.co'}, 'transfer': '/volume/Series', 'tracker': [{'id': 'kickass'}, {'login': {'username': 'Niouf', 'password': 'moihlijh'}, 'id': 't411'}], 'smtp': {'enable': True, 'conf': {'username': 'niouf', 'sender': 'niouf@niouf.fr', 'ssltls': True, 'server': 'smtp.gmail.com', 'password': 'niorf', 'port': 587}}}

cp = jsonConfigParser(myDict)
cp.validate(config)

value = jsonConfigValue(cp,config)
#print cp.cliCreate()
print cp.cliChange(config)
