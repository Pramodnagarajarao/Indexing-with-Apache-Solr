import json
import glob
import networkx as nx

# Given a list of elements in a dictionary, 
# return a list of pair of all the possible combination of the elements
def pairs(listSource):
    resultPairs = []
    for node1 in range(len(listSource)):
        for node2 in range(node1+1,len(listSource)):
            resultPairs.append([listSource[node1], listSource[node2]])
    return resultPairs

# The locations dictionary
locations = dict()
guntype = dict()
keyword = dict()
manufacturer = dict()
pairingDict = dict()

path = './jsonDir100/*.json'
files=glob.glob(path)
count = 0

# Creating the networkx graph
G=nx.Graph()

print('Beginning of processing the json files')
for file in files:
    with open(file) as data_file:
        data = json.load(data_file)
        try:
	    # Check for the required field in the json file
            # If id is present add it to the graph
            state = data['geonames_address'][0]['fallsWithinState1stDiv']['hasName']['label']
            id = int((file.rsplit('/',1)[1]).split('.')[0])
            G.add_node(id)

	    # If state is not already present in the dictionary, create a new list and add location to the value's list
            if state not in locations:
                locations[state] = [id]
	    # Else append the state to the value's list
            else:
                locations[state].append(id)


	    state = data['itemOffered']['category']
            id = int((file.rsplit('/',1)[1]).split('.')[0])
            G.add_node(id)

            # If state is not already present in the dictionary, create a new list and add guntype's to the value's list
            if state not in guntype:
                guntype[state] = [id]
            # Else append the state to the value's list
            else:
                guntype[state].append(id)


            # Check for the required field in the json file
            # If id is present add it to the graph
            state = data['itemOffered']['keywords']
            id = int((file.rsplit('/',1)[1]).split('.')[0])
            G.add_node(id)

            for s in state:
                # If state is not already present in the dictionary, create a new list and add keyword's to the value's list
                if s not in keyword:
                    keyword[s] = [id]
                # Else append the state to the value's list
                else:
                    keyword[s].append(id)
	    
	    # Check for the required field in the json file
            # If id is present add it to the graph
            state = data['itemOffered']['manufacturer']
            id = int((file.rsplit('/',1)[1]).split('.')[0])
            G.add_node(id)

            # If state is not already present in the dictionary, create a new list and add manufacturer's to the value's list
            if state not in manufacturer:
                manufacturer[state] = [id]
            # Else append the state to the value's list
            else:
                manufacturer[state].append(id)
            
            # Update the counter of the processed file for logging and tracking purposes
            count = count + 1
            if count%1000 == 0:
                print(count)

	# In case of exception, ignore and continue
        # Exception can occur due to the missing state location, id or other cases
        except Exception, e:
            continue

# For each state generate all the possible combinations of the locations
# Add all these combinations as the edge in the networkx graph
for key in locations.keys():
    pairings = pairs(locations[key])
    for p in pairings:
        strP = str(p[0]) + ':' + str(p[1])
        # print strP
        if strP in pairingDict:
            pairingDict[strP] = pairingDict[strP]+1
        else:
            pairingDict[strP] = 1

for key in guntype.keys():
    pairings = pairs(guntype[key])
    for p in pairings:
        strP = str(p[0]) + ':' + str(p[1])
        if strP in pairingDict:
            pairingDict[strP] = pairingDict[strP]+1
        else:
            pairingDict[strP] = 1

for key in keyword.keys():
    pairings = pairs(keyword[key])
    for p in pairings:
        strP = str(p[0]) + ':' + str(p[1])
        if strP in pairingDict:
            pairingDict[strP] = pairingDict[strP]+1
        else:
            pairingDict[strP] = 1

for key in manufacturer.keys():
    pairings = pairs(manufacturer[key])
    for p in pairings:
        strP = str(p[0]) + ':' + str(p[1])
        if strP in pairingDict:
            pairingDict[strP] = pairingDict[strP]+1
        else:
            pairingDict[strP] = 1


#print(nx.pagerank(G,0.85))

# Calculate page rank for the created graph and and write it to the result.json file
#print('calculating page rank')
with open('./result100.json', 'w') as outfile:
    json.dump(locations, outfile)

with open('./resultLink.json', 'w') as outfile:
    json.dump(pairingDict, outfile)
