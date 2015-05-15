#!/usr/bin/env python
#encoding:utf-8


   


def displayConf(parser,data,ident=''):
	for item in data.iteritems():
		if isinstance(item[1],dict):
			line = pattern.DICT.format(ident,item[0])
			print line
			displayConf(parser,item[1],' '+ident)
		elif isinstance(item[1],list):
			line = pattern.LIST.format(ident,"List of " + item[0])
			print line
			displayList(parser,item[0],item[1],ident)
		else:
			line = pattern.SIMPLE.format(ident,item[0],item[1])
			print line
			
def displayList(parser,title,data,ident):
	for key,item in enumerate(data):
		displayConf(parser,{"{0} {1}".format(title,str(key)):item},' '+ident)
		
displayConf({},{'slotNumber':1,'Transmission':{'username':2,'password':3},'Tracker':[{'provider':4},{'provider':5},{'provider':6}]})
