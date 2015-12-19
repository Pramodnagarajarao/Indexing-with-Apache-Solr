import io
# coding: utf-8
from urllib2 import *
from pprint import pprint

url='http://localhost:8983/solr/collection1/select?wt=json&indent=true'
fopen=open("queries.txt","w")
statefile=open("tika-locations.txt","r")
year=['2015']
queryStr='&q=tika_location.geo_name:"'
#midStr='"+AND+geonames_address.fallsWithinState1stDiv.hasName.label:"'
#itemList=['Handguns','Rifles','Shotguns']
#outputfile=open("output.txt","w")
stateList=statefile.readlines()
#print type(stateList)

#item = {}
for k in stateList:
	seller = {}
	finalStr=queryStr+k.rstrip()+'"'+'&fl=itemOffered.model'
	fopen.write(finalStr + '\n')
	queryURL = url+finalStr
	conn = urlopen(queryURL)
	rsp = eval(conn.read())
	#yearMonth='2015-05-'+str(j).zfill(2)
	stateName = k.replace('%20', ' ')
	print "State : " + stateName + "Number of Matches : " + str(rsp['response']['numFound'])
	#print out the name field for each returned document
	if rsp['response']['numFound']>0:
		num=0
		newQry = queryURL + "&rows=" + str(rsp['response']['numFound'])
		conn2 = urlopen(newQry)
		rsp2 = eval(conn2.read())
		for x in range(0,rsp2['response']['numFound']):
			resultDict = rsp2['response']['docs'][x]
			if "itemOffered.model" in resultDict:
				sName = str(resultDict['itemOffered.model'])
				if sName in seller:
					seller[sName] = seller[sName] + 1
				else:
					seller[sName] = 1
		pprint(seller)
	print("\n")
