import io
# coding: utf-8
from urllib2 import *
from pprint import pprint

url='http://localhost:8984/solr/collection1/select?wt=json&indent=true&defType=edismax&qf=pgrk_keywords%5E200&stopwords=true&lowercaseOperators=true'
fopen=open("Linkqueries.txt","w")
d_items=open("destructive_items.txt","r")
queryStr='&q=text:"'

dItems=d_items.readlines()

for k in dItems:
	finalStr=queryStr+k.rstrip()+'"'
	fopen.write(finalStr + '\n')
	queryURL = url+finalStr
	conn = urlopen(queryURL)
	rsp = eval(conn.read())
	print "Destructive Items : " + k.rstrip() 
	print "Number of Matches : " + str(rsp['response']['numFound']) + '\n'
