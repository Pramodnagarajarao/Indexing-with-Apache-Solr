import io
# coding: utf-8
from urllib2 import *

url='http://localhost:8984/solr/collection1/select?wt=json&indent=true&defType=edismax&qf=pgrk_locations%5E200+AND+pgrk_keywords%5E100&stopwords=true&lowercaseOperators=true'
fopen=open("Linkqueries.txt","w")
statefile=open("us-states.txt","r")
year=['2015']
queryStr='&q=availabilityStarts:"'
midStr='"+AND+geonames_address.fallsWithinState1stDiv.hasName.label:"'
itemList=['Handguns','Rifles','Shotguns']
#outputfile=open("output.txt","w")
stateList=statefile.readlines()
#print type(stateList)
for k in stateList:
	for j in range(01,31):
		finalStr=queryStr+'2015-05-'+str(j).zfill(2)+'T00'+midStr+k.rstrip()+'"'
		fopen.write(finalStr + '\n')
		queryURL = url+finalStr
		conn = urlopen(queryURL)
		rsp = eval(conn.read())
		yearMonth='2015-05-'+str(j).zfill(2)
		stateName = k.replace('%20', ' ')
		print "\nYear-Month : " + yearMonth + "  State : " + stateName + "Number of Matches : " + str(rsp['response']['numFound'])
		#print out the name field for each returned document
		if rsp['response']['numFound']>0:
			num=0
			for l in itemList:
				fopen.write(queryURL+'+AND+itemOffered.category:"'+l+'"')
				conn2 = urlopen(queryURL+'+AND+itemOffered.category:"'+l+'"')
				
				rsp2 = eval(conn2.read())
				print l+ " : " + str(rsp2['response']['numFound'])
				num=num+rsp2['response']['numFound']
			print "Undefined : "+ str(rsp['response']['numFound']-num)

