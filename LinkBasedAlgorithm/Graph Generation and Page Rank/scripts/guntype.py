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

# The guntype's dictionary
guntype = dict()
path = './jsonDir6049/*.json'
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
            state = data['itemOffered']['category']
            id = int((file.rsplit('/',1)[1]).split('.')[0])
            G.add_node(id)

	    # If state is not already present in the dictionary, create a new list and add guntype's to the value's list
            if state not in guntype:
                guntype[state] = [id]
	    # Else append the state to the value's list
            else:
                guntype[state].append(id)
	    
	    # Update the counter of the processed file for logging and tracking purposes
            count = count + 1
            if count%1000 == 0:
                print(count)

	# In case of exception, ignore and continue
        # Exception can occur due to the missing state location, id or other cases
        except Exception, e:
            continue

# For each state generate all the possible combinations of the guntype's
# Add all these combinations as the edge in the networkx graph
for key in guntype.keys():
    print(key)
    pairings = pairs(guntype[key])
    G.add_edges_from(pairings)

#print(nx.pagerank(G,0.85))

# Calculate page rank for the created graph and and write it to the result.json file
print('calculating page rank')
with open('./result.json', 'w') as outfile:
    json.dump(nx.pagerank(G,0.85), outfile)
