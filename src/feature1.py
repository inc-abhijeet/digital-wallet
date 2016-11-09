import csv
import cPickle as pickle

#read pickle dump file here
with open('graph.pk', 'rb') as f:
	adjList = pickle.load(f)

count = 0
#print "Feature 1 initialized..."
outputfile = open('../paymo_output/output1.txt','w')

with open('inputData.txt', 'r') as inputfile:
	for row in inputfile:
		
		tokens = row.split(',')
		id1 = int(tokens[0])
		id2 = int(tokens[1])

		#check for degree 1 friends
		if id1 in adjList:
			if id2 in adjList[id1]:
				outputfile.write("trusted\n")
				count = count + 1
			else:
				outputfile.write("unverified\n")
				count = count + 1
		
	
inputfile.close()
outputfile.close()
#print "Output1.txt ready"
#print "-----------------"
