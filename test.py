#!/usr/bin/env python
#encoding:utf-8

from jsonConfigParser import *

myDict_login = {
	"title": "Torrent provider login information",
    "type": "object",
    "properties": 
    {
        "username": 
        {
    		"title": "Username",
    		"type": "string",
    		"order":1
        },
    	"password": 
    	{
    		"title": "Password",
    		"$def": "#/def/password",
    		"order":2
        }
    },
    "required": [ "username" ],
    "order":2
}

myDict_tracker = {
	"title": "Torrent provider configuration",
    "type": "object",
    "properties": 
    {
        "id": 
        {
    		"title": "Torrent provider",
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
	"type":"array",
	"items": myDict_tracker,
	"order":1
}

myDict_transmission = {
	"title": "Transmission configuration",
    "type": "object",
    "properties": 
    {
        "server": 
        {
    		"title": "Transmission server",
    		"type": "string",
    		"format": "hostname",
    		"order":1
        },
        "port": 
        {
    		"title": "Transmission port",
    		"type": "integer",
    		"minimum":1,
    		"order":2,
    		"default": 50762
        },
        "username": 
        {
    		"title": "Transmission username",
    		"type": "string",
    		"order":3
        },
        "password": 
        {
        	"title": "Transmission password",
    		"$def": "#/def/password",
    		"order":4
        },
        "slotNumber": 
        {
        	"title": "Maximum number of slots",
    		"type": "integer",
    		"minimum":1,
    		"default":6,
    		"order":5
        },
    },
    "required": [ "server","port","username","slotNumber" ],
    "order":2
}

myDict = {
	"title":"Configuration",
    "type": "object",
    "properties": 
    {
        "tracker": myDict_tracker_list,
        "transmission": myDict_transmission,
    }
}

config = {"tracker":[{'id':'t411','login':{'username':'niouf','password':'niorf'}}]}

cp = jsonConfigParser(myDict)
#cp.validate(config)

value = jsonConfigValue(cp,config)
print cp.cliCreate()
