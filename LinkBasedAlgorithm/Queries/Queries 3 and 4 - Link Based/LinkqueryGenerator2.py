import io
# coding: utf-8
from urllib2 import *

url='http://localhost:8984/solr/collection1/select?wt=json&indent=true&defType=edismax&qf=pgrk_manufacturer%5E200+AND+pgrk_guntype%5E100&stopwords=true&lowercaseOperators=true'
fopen=open("Linkqueries.txt","w")
statefile=open("tika-locations.txt","r")
year=['2015']
queryStr='&q=tika_location.geo_name:"'
#midStr='"+AND+geonames_address.fallsWithinState1stDiv.hasName.label:"'
#itemList=['Handguns','Rifles','Shotguns']
#outputfile=open("output.txt","w")
stateList=statefile.readlines()
#print type(stateList)
#seller = {}
#item = {}
for k in stateList:
	finalStr=queryStr+k.rstrip()+'"'+'&fl=seller.description%2Cseller.contactPoint.name%2Cseller.contactPoint.telephone.name%2CitemOffered.model%2CitemOffered.itemCondition'
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
			print "Seller Information : "
			if "seller.contactPoint.name" in resultDict:
				print "Name : " + str(resultDict['seller.contactPoint.name'])
			if "seller.description" in resultDict:
				print "Description : " + str(resultDict['seller.description'])
			if "seller.contactPoint.telephone.name" in resultDict:
				print "Ph No. : " + str(resultDict['seller.contactPoint.telephone.name'])
			print "Item Information : "
			if "itemOffered.model" in resultDict:
				print "Model : " + str(resultDict['itemOffered.model'])
			if "itemOffered.itemCondition" in resultDict:
				print "Condition : " + str(resultDict['itemOffered.itemCondition'])
			print("\n")
