#!/usr/bin/env python
#encoding:utf-8

from jsonConfigParser import *

myDict_login = {
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
    "required": [ "username","password" ],
    "order":2
}

myDict_tracker = {
    "type": "object",
    "properties": 
    {
        "id": 
        {
    		"title": "ID",
    		"type": "string",
    		"order":1
        },
    	"login": myDict_login
    },
    "required": [ "id" ],
}

myDict_tracker_list = {
	"type":"array",
	"items": myDict_tracker,
	"order":1
}

myDict = {
    "type": "object",
    "properties": 
    {
        "tracker": myDict_tracker_list
    },
    "required": [ "tracker" ],
}

config = {"tracker":[{'id':'t411','login':{'username':'niouf','password':'niorf'}}]}

cp = jsonConfigParser(myDict)
#cp.validate(config)

value = jsonConfigValue(cp,config)
print cp.cliCreate()
