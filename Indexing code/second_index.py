__author__ = 'maheshkumarlunawat'
import tika
import solr
import os
import fnmatch
import json
import ast
from tika import parser
import urllib2
import subprocess
import re
import pycurl


segment_path='/Users/maheshkumarlunawat/Downloads/nutch-trunk/runtime/local/images/'
configfiles = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(segment_path)
    for f in fnmatch.filter(files, '*')]

html=['.html']
images=['.jpg','.png','.jpeg','.gif','.JPG','.PNG','.JPEG','.jpeg2','.ico','.tff','.tiff','.ICO','.GIF']
count=0

# create a connection to a solr server

s = solr.Solr('http://localhost:8888/solr')
for file_path in configfiles:
    print(file_path)
    if any(x in file_path for x in html):

        parsed = parser.from_file(file_path)
        index_dict={}

        # cTakes Parser Implementation

        procCtakes = subprocess.Popen(["curl", "-T", file_path, "-H","Content-Disposition: attachment; filename="+file_path+'"', "http://localhost:9998/rmeta"], stdout=subprocess.PIPE)
        (outCtakes, err) = procCtakes.communicate()
        dataCtakes=ast.literal_eval(outCtakes)
        if "Creation-Date" in dataCtakes[0]:
            index_dict["Creation-Date"]=dataCtakes[0]["Creation-Date"]
        if "Last-Modified" in dataCtakes[0]:
            index_dict["Last-Modified"]=dataCtakes[0]["Last-Modified"]
        if "Last-Save-Date" in dataCtakes[0]:
            index_dict["Last-Save-Date"]=dataCtakes[0]["Last-Save-Date"]


        # TIKA-Parser Metadata Implementation

        index_dict=ast.literal_eval(json.dumps(index_dict))
        s.add(index_dict)
        s.commit()
        if "metadata" in parsed.keys():
            dict=parsed["metadata"]
            # add a document to the index
            count=count+1
            index_dict["id"]=count
            if "og:locale" in dict.keys():
                index_dict["location"]=dict["og:locale"]
            if "og:updated_time" in dict.keys():
                index_dict["updated_time"]=dict["og:updated_time"]
            if "og:description" in dict.keys():
                index_dict["description"]=dict["og:description"]
            if "Content-Type" in dict.keys():
                index_dict["content_type"]=dict["Content-Type"].split(';')[0]
            if "title" in dict.keys():
                index_dict["title"]=dict["title"]
            if "resourceName" in dict.keys():
                index_dict["resourcename"]=dict["resourceName"]
        else:
            print("no indexing")

        # GEO-Topic Parser Implementation

        new_path=re.sub("(.html)", ".geot", file_path)
        os.rename(file_path,new_path)
        print(new_path)
        procGeo = subprocess.Popen(["curl", "-T", new_path, "-H","Content-Disposition: attachment; filename="+new_path+'"', "http://localhost:9998/rmeta"], stdout=subprocess.PIPE)
        (outGeo, err) = procGeo.communicate()
        dataGeo=ast.literal_eval(outGeo)
        if "Geographic_LATITUDE" in dataGeo[0]:
            index_dict["Geographic_LATITUDE"]=dataGeo[0]["Geographic_LATITUDE"]
        if "Geographic_LONGITUDE" in dataGeo[0]:
            index_dict["Geographic_LONGITUDE"]=dataGeo[0]["Geographic_LONGITUDE"]
        if "Geographic_NAME" in dataGeo[0]:
            index_dict["Geographic_NAME"]=dataGeo[0]["Geographic_NAME"]
        if "Optional_LATITUDE1" in dataGeo[0]:
            index_dict["Optional_LATITUDE1"]=dataGeo[0]["Optional_LATITUDE1"]
        if "Optional_LONGITUDE1" in dataGeo[0]:
            index_dict["Optional_LONGITUDE1"]=dataGeo[0]["Optional_LONGITUDE1"]
        if "Optional_NAME1" in dataGeo[0]:
            index_dict["Optional_NAME1"]=dataGeo[0]["Optional_NAME1"]

        index_dict=ast.literal_eval(json.dumps(index_dict))
        #print(index_dict)
        s.add(index_dict)
        s.commit()


    elif any(x in file_path for x in images):

        parsed = parser.from_file(file_path)
        index_dict={}

        # TIKA-Parser Metadata Implementation

        if "metadata" in parsed.keys():
            dict=parsed["metadata"]
            # add a document to the index
            count=count+1
            index_dict["id"]=count
            if "File Size" in dict.keys():
                index_dict["file_size"]=dict["File Size"]
            if "File Name" in dict.keys():
                index_dict["name"]=dict["File Name"]
            if "File Modified Date" in dict.keys():
                index_dict["updated_time"]=dict["File Modified Date"]
            if "Content-Type" in dict.keys():
                index_dict["content_type"]=dict["Content-Type"]
            if "Image Height" in dict.keys():
                index_dict["image_height"]=dict["Image Height"]
            if "Image Width" in dict.keys():
                index_dict["image_width"]=dict["Image Width"]
            if "resourceName" in dict.keys():
                index_dict["resourcename"]=dict["resourceName"]
        else:
            print("no indexing")

        # Tesseract OCR Parser

        procOCR = subprocess.Popen(["curl", "-T", file_path,"http://localhost:9998/tika ", "--header","Content-type: image/"+file_path.split('.')[1]], stdout=subprocess.PIPE)
        (outOCR, err) = procOCR.communicate()
        index_dict["OCR_text"]=outOCR

        # cTakes Parser Implementation

        procCtakes = subprocess.Popen(["curl", "-T", file_path, "-H","Content-Disposition: attachment; filename="+file_path+'"', "http://localhost:9998/rmeta"], stdout=subprocess.PIPE)
        (outCtakes, err) = procCtakes.communicate()
        dataCtakes=ast.literal_eval(outCtakes)
        if "Creation-Date" in dataCtakes[0]:
            index_dict["Creation-Date"]=dataCtakes[0]["Creation-Date"]
        if "Last-Modified" in dataCtakes[0]:
            index_dict["Last-Modified"]=dataCtakes[0]["Last-Modified"]
        if "Last-Save-Date" in dataCtakes[0]:
            index_dict["Last-Save-Date"]=dataCtakes[0]["Last-Save-Date"]

        # GEO-Topic Parser Implementation

        new_path=re.sub("(.jpg)|(.png)|(.jpeg)|(.gif)|(.JPG)|(.PNG)|(.JPEG)|(.jpeg2)|(.ico)|(.tff)|(.tiff)|(.ICO)|(.GIF)", ".geot", file_path)
        os.rename(file_path,new_path)
        print(new_path)
        procGeo = subprocess.Popen(["curl", "-T", new_path, "-H","Content-Disposition: attachment; filename="+new_path+'"', "http://localhost:9998/rmeta"], stdout=subprocess.PIPE)
        (outGeo, err) = procGeo.communicate()
        dataGeo=ast.literal_eval(outGeo)
        if "Geographic_LATITUDE" in dataGeo[0]:
            index_dict["Geographic_LATITUDE"]=dataGeo[0]["Geographic_LATITUDE"]
        if "Geographic_LONGITUDE" in dataGeo[0]:
            index_dict["Geographic_LONGITUDE"]=dataGeo[0]["Geographic_LONGITUDE"]
        if "Geographic_NAME" in dataGeo[0]:
            index_dict["Geographic_NAME"]=dataGeo[0]["Geographic_NAME"]
        if "Optional_LATITUDE1" in dataGeo[0]:
            index_dict["Optional_LATITUDE1"]=dataGeo[0]["Optional_LATITUDE1"]
        if "Optional_LONGITUDE1" in dataGeo[0]:
            index_dict["Optional_LONGITUDE1"]=dataGeo[0]["Optional_LONGITUDE1"]
        if "Optional_NAME1" in dataGeo[0]:
            index_dict["Optional_NAME1"]=dataGeo[0]["Optional_NAME1"]
        index_dict=ast.literal_eval(json.dumps(index_dict))
        s.add(index_dict)
        s.commit()
    else:
        print("no indexing")

