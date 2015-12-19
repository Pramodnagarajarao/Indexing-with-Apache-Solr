__author__ = 'maheshkumarlunawat'
import tika
import solr
import os
import fnmatch
import json
import ast
import json
import yaml
from pprint import pprint
import sunburnt


def flattenDict(d, result=None):
    if result is None:
        result = {}
    for key in d:
        value = d[key]
        if isinstance(value, dict):
            value1 = {}
            for keyIn in value:
                value1[".".join([key,keyIn])]=value[keyIn]
            flattenDict(value1, result)
        elif isinstance(value, (list, tuple)):
            for indexB, element in enumerate(value):
                if isinstance(element, dict):
                    value1 = {}
                    index = 0
                    for keyIn in element:
                        newkey = ".".join([key,keyIn])
                        value1[".".join([key,keyIn])]=value[indexB][keyIn]
                        index += 1
                    for keyA in value1:
                        flattenDict(value1, result)
        else:
            result[key]=value
    return result

class mydict(dict):
	def __str__(self):
		return json.dumps(self)
	def __repr__(self):
        	return json.dumps(self)

#segment_path='out/'
#configfiles = [os.path.join(dirpath, f)
#    for dirpath, dirnames, files in os.walk(segment_path)
#    for f in fnmatch.filter(files, '*')]


si = sunburnt.SolrInterface("http://localhost:8984/solr/")


#configfiles=['/Users/maheshkumarlunawat/Downloads/nutch-trunk/runtime/local/images/0d/0a/0da0febadf46bc910f358452a424495f_f8e2472114553b23b9afc3e2e184826f.jpg']
#html=['.html']
#images=['.jpg','.png','.jpeg','.gif','.JPG','.PNG','.JPEG','.jpeg2','.ico','.tff','.tiff','.ICO','.GIF']
#count=1
# create a connection to a solr server
#s = solr.Solr('http://localhost:8983/solr')
pagerank_guntype=json.load(open("/home/presha/Downloads/linkbased/resultJSONs/guntype6049.json","r"))
pagerank_keywords=json.load(open("/home/presha/Downloads/linkbased/resultJSONs/keywords6049.json","r"))
pagerank_locations=json.load(open("/home/presha/Downloads/linkbased/resultJSONs/locations6049.json","r"))
pagerank_manufacturer=json.load(open("/home/presha/Downloads/linkbased/resultJSONs/manufacturer6049.json","r"))

for x in range(1,190167):
    file_path = '/home/presha/Downloads/linkbased/jsonDir6049/' + str(x) + '.json'
    #print(file_path)
    if os.path.isfile(file_path):
	print (file_path)
	with open(file_path) as data_file:
		index_dict = {}
		#print count
		#count = count + 1    
    		data = json.load(data_file)
		flattenedDict=flattenDict(data)
		flattenedDict["id"] = x
		del flattenedDict["@context"]
		if 'price' in flattenedDict.keys():
			flattenedDict["price_item"] = flattenedDict["price"]
			del flattenedDict["price"]
		if str(x) in pagerank_guntype:
			flattenedDict['pgrk_guntype'] = pagerank_guntype[str(x)]
		if str(x) in pagerank_keywords:	
			flattenedDict['pgrk_keywords'] = pagerank_keywords[str(x)]
		if str(x) in pagerank_locations:
			flattenedDict['pgrk_locations'] = pagerank_locations[str(x)]
		if str(x) in pagerank_manufacturer:
			flattenedDict['pgrk_manufacturer'] = pagerank_manufacturer[str(x)]
		str_json = json.dumps(flattenedDict)
		index_dict = ast.literal_eval(str_json)
	    	si.add(index_dict)
	    	si.commit()

    else:
	print "No File with such name"
    
	
#	if "a" in flattenedDict.keys():
#            index_dict["a"]=flattenedDict["a"]
#        if "File Name" in flattenedDict.keys():
#            index_dict["uri"]=flattenedDict["uri"]
#        if "File Modified Date" in flattenedDict.keys():
#            index_dict["price_item"]=flattenedDict["price_item"]
#        if "Content-Type" in flattenedDict.keys():
#            index_dict["identifier.a"]=flattenedDict["identifier.a"]
#        if "Image Height" in flattenedDict.keys():
#            index_dict["priceCurrency"]=flattenedDict["priceCurrency"]
#        if "Image Width" in flattenedDict.keys():
#            index_dict["seller.a"]=flattenedDict["seller.a"]
#        if "resourceName" in flattenedDict.keys():
#            index_dict["publisher.uri"]=flattenedDict["publisher.uri"]
        #index_dict=ast.literal_eval(json.dumps(index_dict))
	#for key, value in flattenedDict.iteritems():
	
	#print str_json
	#x = str(str_json)
	#print x
#	json_acceptable_string = str_json.replace("'", "\"")
	#print index_dict
	#newdict = '{%s}' % ', '.join(['"%s": "%s"' % (k, v) for k, v in index_flattenDict.items()])
	#index_dict = mydict(flattenedDict)
	#print flattenedDict
	#print type(index_dict)

