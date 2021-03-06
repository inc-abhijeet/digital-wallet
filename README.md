# digital-wallet

# Table of Contents

1. [Features implemented] (README.md#features-implemented)
2. [Implementation details] (README.md#implmentation-details)
3. [Algorithm] (README.md#algorithm)
4. [Work flow] (README.md#work-flow)
5. [Repo directory structure](README.md#repo-directory-structure)
6. [Output of run tests] (README.md#output-of-run-tests)

##Features implemented

Digital wallet warns the user for the following three features:

###Feature 1
When anyone makes a payment to another user, they'll be notified if they've never made a transaction with that user before.

###Feature 2
When anyone outside the "second degree friends network" tries to make a payment.

###Feature 3
This feature warns the user only when they're outside the "4th degree friends network".


##Implmentation details

The source code is handcrafted in Python. 

###Graph creation
The initial stage is to create a graph from batch_payment.txt. If users have interacted before then an edge is added between those users and is stored in an adjacency list. List was chosen over matrix for faster computation and better memory usage. The graph is created once and dumped into a file called graph.pk with the help of pickle. This file is then accessed by three features and makes it faster as compared to building the graph each time a feature is called. 

###Preparing the input data
Since all the three features are primariliy concerned with the two id's (column 1 and 2, indexed 0) in the stream_payment.txt this file is accessed only once by createInputData and it outputs the two id's to a comma separated inputData.txt. This is then accessed by all the three features for testing purposes. It saves time as the stream_payment need not be opened and traversed always, since we are only interested in the column 1 and 2 of this file.

##Algorithm
For now the three features have been implmented pretty straight forward. However, feature 3 is pretty time consuming. A better algorithm that could be used was Flyod Warshall. However, the time complexity for this algorithm is O(N^3) where N is the number of the nodes. Which is what the present implmentation of feature 3 potrays as well. Recursion is also not a pleasing option for feature 3.

However an algorithm that I did come up with is a modification of Breath First Search and Minimum Spanning tree and Least Common Ancestor.

One direct way would be to select a root in the graph and then apply BFS while maintaining a hop count for each of the nodes from this root. For any two given nodes (id1 and id2), we know the distance of these nodes from the root and we can compute the LCA of these two nodes (ancestor). Using the formula we can compute the degree of two nodes, 

distance(root, id1) + distance(root, id2) - 2 * distance(root, ancestor)

..................................................................^ LCA............

Then a simple check of this degree with the degree required by a given feature should mark the two users as trusted or unverified. However, for the LCA to be calculated the graph will have to be a tree. But, through experimentations I figured out that the given dataset does not produce a tree and hence it is not possible to use the above algorithm directly. 

No algorithm can be directly applied to such a huge dataset for high degree friends as it is really time consuming and slow. But there are approximations that can be implemented. Like if two users have interacted a great number of times (T, this T should be derived through experimentations.) then that edge is of higher importance to use than those edges where the users have hardly interacted with each other. Such are the edges that can be ignored when constructing the Minimum Spanning Tree. This is the pre-processing which will construst the approximated tree. BFS is now run on this tree while keeping a track of the number of hops from a given node to the rest of the nodes in the tree. Finally the above formula is applied for any two given pairs of users to determine if they are trusted or unverified depeding on their degree.
However, there may be components in the approximated tree. So the above algorithm will now be applied for each component in this tree. 

To better enhance this algorithm we can compute a threshold for the degree "N". This can be computed through heuristics. Any degree above N will have the above algorithm applied to it and any degree below this threshold will be run through Floyd Warshall algorithm.

##Work flow
1. createGraph.py
 1. Reads batch_payment.txt row by row
 2. Creates an adjacency list, edge added if two id's have had a transaction.
 3. Pickle package use to dump this adjacency list to graph.pk
2. createInputData.py
 1. Reads stream_payment.txt row by row.
 2. Writes column 1 and column 2 (id1 and id2, 0 indexed columns) to comma separated inputData.txt
3. feature1.py
 1. Imports the adjacency list from graph.pk through pickle package.
 2. Reads inputData.txt row by row.
 3. For each id1 and id2 pair for each row checks to see if they are degree 1 friends and marks them as trusted else unverified
 4. Takes constant time lookup
 5. Stores output in ../paymo_output/output1.txt
4. feature2.py
 1. Imports the adjacency list from graph.pk through pickle package.
 2. Reads inputData.txt row by row.
 3. For each id1 and id2 pair for each row checks to see if they are degree 2 friends and marks them as trusted else unverified
 4. Takes linear time lookup
 5. Writes output to ../paymo_output/output2.txt
5. feature3.py
 1. Imports the adjacency list from graph.pk through pickle package.
 2. Reads inputData.txt row by row.
 3. For each id1 and id2 pair for each row checks to see if they are degree 4 friends and marks them as trusted else unverified
 4. Takes cube time lookup
 5. Stores output in ../paymo_output/output3.txt

##Repo directory structure

	├── README.md 
	├── run.sh
	├── src
	│  	└── createGraph.py
	│  	└── createInputData.py
	│  	└── feature1.py
	│  	└── feature2.py
	│  	└── feature3.py
	│  	└── graph.pk
	│  	└── inputData.txt
	├── paymo_input
	│   └── batch_payment.txt
	|   └── stream_payment.txt
	├── paymo_output
	│   └── output1.txt
	|   └── output2.txt
	|   └── output3.txt
	└── insight_testsuite
	 	   ├── run_tests.sh
		   └── tests
	        	└── test-1-paymo-trans
        		│   ├── paymo_input
        		│   │   └── batch_payment.txt
        		│   │   └── stream_payment.txt
        		│   └── paymo_output
        		│       └── output1.txt
        		│       └── output2.txt
        		│       └── output3.txt



##Output of run tests
	[PASS]: test-1-paymo-trans (output1.txt)
	[PASS]: test-1-paymo-trans (output2.txt)
	[PASS]: test-1-paymo-trans (output3.txt)

