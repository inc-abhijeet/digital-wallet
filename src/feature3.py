import csv
import cPickle as pickle

#read pickle dump file here
with open('graph.pk', 'rb') as f:
	adjList = pickle.load(f)

count = 0


#print "Feature 3 initialized..."
outputfile = open('../paymo_output/output3.txt','w')


with open('inputData.txt', 'r') as inputfile:
	for row in inputfile:
		try:
			tokens = row.split(',')
			id1 = int(tokens[0])
			id2 = int(tokens[1])
			flag = 0

			if (id2 in adjList[id1]):
				flag = 1

			for friends in adjList[id1]:
				#print friends
				if id2 in adjList[friends]:
					#print friends
					flag = 1
					count = count + 1
					break
				else:
					for friend in adjList[friends]:
						#print friend
						if id2 in adjList[friend]:
							flag = 1
							break
						else:
							for person in adjList[friend]:
								if id2 in adjList[person]:
									flag = 1
									break

			if (flag):
				outputfile.write("trusted\n")
			else:
				outputfile.write("unverified\n")
		except (ValueError, IndexError):
			continue

#print "Output3.txt ready"
outputfile.close()

