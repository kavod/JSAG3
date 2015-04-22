#!/usr/bin/env python
#encoding:utf-8

from jsonConfigParser import *

myDict = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": 
    	{
        "username": 
        	{
        		"title": "Username",
        		"type": "string"
        	},
    	"password": 
    		{
        		"title": "Password",
        		"$def": "#/definitions/password"
        	}
    	},
    "required": [ "username","password" ],
    "additionalProperties": False,
}

config = {'username':'niouf','password':'niorf'}

cp = jsonConfigParser(myDict)
cp.validate(config)
