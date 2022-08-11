# CISC6525 AI 
# Yuliya Akchurina 

""" 
Your assignment is to study the effects of four different heuristics on A* search of the Romania roadmap.
The heuristics are as follows, where (x1,y1 and (x2,y2) are the location so of the two cities
Heuristic #1: Straight Line Distance [ (x2-x1)^2 + (y2-y1)^2)^1/2
Heuristic #2: Manhattan Distance (x2-x1)+(y2-y1)
Heuristic #3: Sum of first two heuristics
Heuristic #4: Average of first two heuristics
1. Write a python program that implements A* search for the snippet of the roadmap we did in class
2. Select a set of 10 city pairs on the map, where there are multiple routes for each pair (as in Arad, Bucharest), 
and establish the optimal path by hand between each pair.
3. Evaluate A* using each heuristic on all 10 pairs, and count the number of optimal paths returned
4. Plot your results
5. Write a document with two sections. In the first section, document your code. In the second section, 
include your plot and explain  in detail your results. Are there any general conclusions you can draw?
Your ASTAR code should be written in a single python program which accepts as input a number from 1 to 4 
and then carries out the 10 searches you have selected using the correspondingly numbered of the 4 heuristics.

Your writeup MUST be written in PDF and BOTH writeup and python file can be submitted on blackboard.
remember: Your pythonfile MUSt run on Apporto using only what packages are already installed. 
"""

#
# ASTAR implementation
# for N&R Romania roadmap example
#
#
import math
import matplotlib.pyplot as plt  #for plotting barchart
#
# Part of the romania roadmapp
#
# coordinates of the cities on the map as
# **approximated** on paper and scaled
#
         
location = {'arad': [45.5, 279.5], 'zerind': [65.0, 325.0], 'sibiu': [175.5, 240.5], 
            'timisoara': [45.5, 182], 'oradea': [85.8, 364], 'lugoj': [124.8, 150.79999999999998], 
            'mehadia': [130, 104], 'drobeta': [124.8, 65.0], 'craiova': [227.5, 45.5], 
            'rimnicu': [208, 182], 'fagaras': [273.0, 234], 'pitesti': [305.5, 136.5], 
            'bucharest': [390, 91.0], 'giurgiu': [364, 26]}

#
# a portion of the map
#
map = [("arad","zerind",75),
       ("arad","sibiu",140),
       ("arad","timisoara",118),
       ("zerind","oradea",71),
       ("oradea","sibiu",151),
       ("timisoara","lugoj",111),
       ("lugoj","mehadia",70),
       ("mehadia","drobeta",75),
       ("drobeta","craiova",120),
       ("craiova","rimnicu",146),
       ("rimnicu","sibiu",80),
       ("craiova","pitesti",138),
       ("rimnicu","pitesti",97),
       ("sibiu","fagaras",99),
       ("pitesti","bucharest",101),
       ("fagaras","bucharest",211),
       ("giurgiu","bucharest",90)]

#
# the SLD table from N&R for comparison with the distance calculated
# from coordinates
#
SLDT = { "arad":366,
         "bucharest":0,
         "craiova":160,
         "drobeta":242,
         "eforie":161,
         "fagaras":176,
         "giurgiu":77,
         "hirsova":151,
         "iasi":226,
         "lugoj":244,
         "mehadia":241,
         "neamt":234,
         "oradea":380,
         "pitesti":100,
         "rimnicu":193,
         "sibiu":253,
         "timisoara":329,
         "zerind":374 }
#
# selects a map with a global variable
#
roadmap=map

#
# Successor fn: successor(state,action)=list of states arrived at after action in state
#
def successor(roadmap,city):
    """generate list of successors of startcity in roadmap"""
    # assumes format of roadmap and that city is a strong
    successorList=[]
    for mapentry in roadmap:
        if mapentry[0]==city:
            successorList.append( (mapentry[1], mapentry[2]) )
        elif mapentry[1]==city:
            successorList.append( (mapentry[0], mapentry[2]) )
    return successorList

#
# calculates straight line distance as a heuristic for ASTAR

# Heuristic 1: Straight Line Distance- Euclidean Distance ((x2-x1)^2 + (y2-y1)^2)^1/2
def sld(city1,city2):
    """return the straight line distance from city1 to city 2"""
    #assumes a global location dictionary and that the cities are in it
    loc1=location[city1]
    loc2=location[city2]
    xdel = loc1[0]-loc2[0]
    ydel = loc1[1]-loc2[1]
    dist = math.sqrt( xdel*xdel + ydel*ydel )
    return dist

# Heuristic 2: Manhattan Distance |x2-x1|+|y2-y1|
def md(city1, city2):
    """return the Manhattan distance from city1 to city 2"""
    #assumes a global location dictionary and that the cities are in it
    loc1=location[city1]
    loc2=location[city2]
    xdel = loc2[0]-loc1[0]
    ydel = loc2[1]-loc1[1]
    mdist = abs(xdel) + abs(ydel)
    return mdist

# Heuristic 3: Sum of first two heuristics
def sumd(city1, city2):
    """return the Sum of first two heuristics distance from city1 to city 2"""
    #assumes a global location dictionary and that the cities are in it
    loc1=location[city1]
    loc2=location[city2]
    xdel = loc1[0]-loc2[0]
    ydel = loc1[1]-loc2[1]
    dist = math.sqrt( xdel*xdel + ydel*ydel )
    
    loc1=location[city1]
    loc2=location[city2]
    xdel = loc2[0]-loc1[0]
    ydel = loc2[1]-loc1[1]
    mdist = abs(xdel) + abs(ydel)
    sumdist = dist + mdist
    return sumdist

# Heuristic 4:  Average of first two heuristics
def avgd(city1, city2):
    """return the  Average of first two heuristics distance from city1 to city 2"""
    #assumes a global location dictionary and that the cities are in it
    loc1=location[city1]
    loc2=location[city2]
    xdel = loc1[0]-loc2[0]
    ydel = loc1[1]-loc2[1]
    dist = math.sqrt( xdel*xdel + ydel*ydel )
    
    loc1=location[city1]
    loc2=location[city2]
    xdel = loc2[0]-loc1[0]
    ydel = loc2[1]-loc1[1]
    mdist = abs(xdel) + abs(ydel)

    avgdist = (dist + mdist)/2
    return avgdist

#
# A* treesearch on the roadmap given a fringe =['name of start city',cost,[]] and
#  goal = 'name of goal city'
#

# function modified to accept heuristic as a parameter 
def ASTARtreesearch(frontier,goal, heuristic):
    """carry out a tree search for goal from node in fringe"""
    #finished = list() # list of already searched cities
    finished = []
    
    while len(frontier)>0:
        rootnode = frontier[0] # this is the strategy - pick min f(n)
        g = rootnode[1]
        h = heuristic(rootnode[0],goal)
        
        fmin = g + h # A* cost forfirst node, assume min
        for node in frontier:
            g = node[1]
            h = heuristic(node[0],goal)
            
            f = g + h # A* cost for each node in fringe
            if f<fmin:
                rootnode = node # smallest A* cost
                fmin = f
        frontier.remove(rootnode) # 'pop' minimum f(n) node from fringe
        root = rootnode[0]
        print("ASTAR Expands ",root," f=",fmin)
        if root == goal:
            print ('Found goal')
            return rootnode[2]+[goal]
            
        nextcitylist = successor(roadmap,root) # assumes global scope roadmap
        finished.append(root)

        for mapentry in nextcitylist:
            city = mapentry[0]
            stepcost=mapentry[1]
            if (not city in finished):
                newnode=[city,rootnode[1]+stepcost,rootnode[2]+[root]] # expand the path by one city
                frontier.append(newnode)# put them at the end
                
    return "No route to "+goal

# 10 citypairs for path finding
cities_list = [["oradea", "pitesti"], ["zerind" , "craiova"], ["timisoara", "sibiu"], 
["sibiu", "lugoj"], ["fagaras", "craiova"], ["drobeta", "oradea"], 
["rimnicu", "lugoj"], ["arad", "pitesti"], ["bucharest", "oradea"], 
["giurgiu", "timisoara"]] 

#predetermined optimal paths between the 10 citypairs
optimal_path = [["oradea", "sibiu", "rimnicu", "pitesti"], 
                ["zerind", "arad", "sibiu", "rimnicu", "craiova"], 
                ["timisoara", "arad", "sibiu"], 
                ["sibiu", "arad", "timisoara", "lugoj"], 
                ["fagaras", "sibiu", "rimnicu", "craiova"], 
                ["drobeta", "craiova", "rimnicu", "sibiu", "oradea"], 
                ["rimnicu", "craiova", "drobeta", "mehadia", "lugoj"], 
                ["arad", "sibiu", "rimnicu", "pitesti"], 
                ["bucharest", "pitesti", "rimnicu", "sibiu", "oradea"], 
                ["giurgiu", "bucharest", "pitesti", "rimnicu", "sibiu", "arad", "timisoara"]]

# dictionary of 4 heuristic functions to choose from
heuristic_dict = {1:sld, 2:md, 3:sumd, 4:avgd}

heuristic_list = []  # use to store the pathways found by heuristic search
accuracy_list = []  # use to store boolean outputs of the path comparison to the optimal path
prediction_accuracy = []  #use to store the numeric prediction accuracy results 
heuristics_accuracy = []

#Part 1: run all 4 heuristics with ASTARtreesearch function to get the results for analysis and plotting
for key in heuristic_dict.keys():
    print(f" \nHEURISTIC {key} COMPUTE PATH {heuristic_dict[key]}")

    ctr = 0
    for start, end in cities_list:
        frontier=[[start,0, []]]
        goal=end
        print(frontier[0][0], " to ", goal)
        heuristic_route = ASTARtreesearch(frontier, goal, heuristic_dict[key])
        print(heuristic_route)
        #heuristic_list.append(heuristic_route)

        accuracy_list.append(optimal_path[ctr] == heuristic_route)
        ctr+=1
        #print(f"accuracy_list in loop {accuracy_list}")

    heuristics_accuracy.append(accuracy_list)
    accuracy_list = []

print(f"\nHeuristics_accuracy {heuristics_accuracy}\n")    
#print(f"heuristics_accuracy {len(heuristics_accuracy)}")

accuracy = []
quantity = []
for list in heuristics_accuracy:
    accuracy.append(sum(bool(x) for x in list))
    quantity.append(len(list))

#PLOT the results on comparison heuristic paths to the optimal paths
data = accuracy
plt.bar(["Str Line Dist", "Manhattan Dist", "Sum", "Average"], data, color='royalblue', edgecolor = 'navy', linewidth = 1.5, alpha=0.9)
plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
plt.xlabel('Heuristic Function')
plt.ylabel('Optimal path count')
plt.title(f'Optimal paths found for {len(optimal_path)} city pairs by heuristic')
plt.show()

#Part2: user selects a heuristic to use in ASTARtreesearch
#selection = input("\nType in a number from 1 to 4 to select a heuristic for path search \n 1 = Straight Line Distance, \n 2 = Manhattan Distance \n 3 = Sum of Straight Line Distance and Manhattan Distance \n 4 = Average of Straight Line Distance and Manhattan Distance \n\n User Input: ")
selection = 0
while int(selection) not in heuristic_dict.keys():
    selection = input("Type in a number from 1 to 4 to select a heuristic for path search \n 1 = Straight Line Distance, \n 2 = Manhattan Distance \n 3 = Sum of Straight Line Distance and Manhattan Distance \n 4 = Average of Straight Line Distance and Manhattan Distance \n\nUser Input: ")
else: 
    print(f"\nYou selected {selection}\n")

#call the ASTARtreesearch function to obtain the pathways for the 10 citypairs with user selected heuristic
for start, end in cities_list:
    frontier=[ [start,0, []] ]
    goal=end
    print( frontier[0][0], " to ", goal )
    heuristic_route = ASTARtreesearch(frontier, goal, heuristic_dict[int(selection)] )
    print(heuristic_route)
    heuristic_list.append(heuristic_route)
    
#compare the results of the user input ASTARtreesearch with the predetermined optimal(shortest) path between city pairs 
for i in range(len(optimal_path)):
    print(optimal_path[i] == heuristic_list[i])
    print(f'optimal path:   {optimal_path[i]}')
    print(f'heuristic path: {heuristic_list[i]}')
    accuracy_list.append(optimal_path[i] == heuristic_list[i])

print(f'\nAccuracy list: \n{accuracy_list}')
prediction_accuracy.append(sum(accuracy_list))
print(f'Prediction_accuracy {prediction_accuracy}')
