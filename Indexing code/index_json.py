__author__ = 'maheshkumarlunawat'
import tika
import solr
import os
import fnmatch
import json
import ast
import json
from pprint import pprint


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


segment_path='/Users/maheshkumarlunawat/sample/'
configfiles = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(segment_path)
    for f in fnmatch.filter(files, '*.json')]
count=1
# create a connection to a solr server
s = solr.Solr('http://localhost:8983/solr')
for file_path in configfiles:
    print(file_path)
    with open(file_path) as data_file:
        index_dict = {}
        index_dict["id"] = count
        count = count + 1
        data = json.load(data_file)
        flattenedDict=flattenDict(data)
        flattenedDict['id'] = count
        count = count + 1
        del flattenedDict['@context']
        flattenedDict['price_item'] = flattenedDict['price']
        del flattenedDict['price']
        index_dict=ast.literal_eval(json.dumps(flattenedDict))
        s.add(index_dict)
        s.commit()
