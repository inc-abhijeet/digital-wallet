import re

#Regex for valid date format as a sanity check for a valid row being read
date_re = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}')
#Input data for each feature file so as to avoid more time consumption in reading and traversing every column of stream_payment
outputfile = open('inputData.txt','w')

with open('../paymo_input/stream_payment.txt', 'r') as csvfile:
	#print "Creating input data..."
	for row in csvfile:
		tokens = row.split(',')
		if date_re.match(tokens[0]) is None:
			continue

		#read id1 and id2
		outputfile.write(tokens[1])
		outputfile.write(",")
		outputfile.write(tokens[2])
		outputfile.write("\n")		

#print "Created input data"
#print "-----------------"
