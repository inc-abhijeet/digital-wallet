import collections
import re
import cPickle as pickle

adjList = collections.defaultdict(set)
count = 0

#Checks to see if the row being read is valid. Regex for date format
date_re = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}')

#Read the input file
with open('../paymo_input/batch_payment.txt', 'r') as csvfile:

	#print "Creating graph..."
	for row in csvfile:
		tokens = row.split(',')
		if date_re.match(tokens[0]) is None:
			continue

		id1 = int(tokens[1])
		id2 = int(tokens[2])
		
		#undirected graph
		adjList[id1].add(id2)
		adjList[id2].add(id1)

	#print "Graph created"
	#print "-----------------"

#Create the graph.pk to be accessed by the feature files
with open('graph.pk', 'wb') as f:
	pickle.dump(adjList, f, -1)
