import csv
import cPickle as pickle

#read pickle dump file here
with open('graph.pk', 'rb') as f:
	adjList = pickle.load(f)

count = 0
#print "Feature 2 initialized..."
#Write the output to this file
outputfile = open('../paymo_output/output2.txt','w')

with open('inputData.txt', 'r') as inputfile:
	for inputRow2 in inputfile:
			tokens = inputRow2.split(',')
			id1 = int(tokens[0])
			id2 = int(tokens[1])
			flag = 0
			
			#check for degree 1 friends
			if (id2 in adjList[id1]):
				flag = 1
			
			#check for degree 2 friends
			for friends in adjList[id1]:
				if id2 in adjList[friends]:
					#if two degree friends then break out of the loop and set the flag
					flag = 1
					count = count + 1
					break
				else:
					count = count + 1
			if (flag):
				outputfile.write("trusted\n")
			else:
				outputfile.write("unverified\n")
		
inputfile.close()
outputfile.close()

#print "Output2.txt ready"
#print "-----------------"
