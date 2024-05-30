import numpy as np
from math import tanh
import time

import random


deepcopy = (
    lambda x: [deepcopy(x[_]) for _, i in enumerate(x)]
    if isinstance(x, (list, tuple))
    else x
)


# activation functions
inp = lambda x: x

relu = lambda x: max(0, x)


def node(ingoing_data: list[["weights","value"], ...],bias: float,activator: callable ) -> float:
    return activator(sum([weight * value for weight, value in ingoing_data]) + bias)

def agent_sort_by_score(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2][1]  # Choosing the middle element as the pivot
        left = [x for x in arr if x[1] > pivot]
        middle = [x for x in arr if x[1] == pivot]
        right = [x for x in arr if x[1] < pivot]
        return agent_sort_by_score(left) + middle + agent_sort_by_score(right)
        



from collections import defaultdict, deque

class network:
    """DAGs based network"""

    def __init__(self, ins: int, outs: int) -> None:
        """will make new network with input and output nodes only with no conection and biases set to 0"""
        self.nodes = [[0, inp, [[None, 0]]] for _ in range(ins)] + [
            [0, tanh, [[None, 0]]] for _ in range(outs)
        ]

        

    def ev(self, inputs: list[int, ...]) -> list[int, ...]:
        """evaluate and returns the final value of output neuron"""

        out = []

        # dict to store the list of value from parent neuron on name of on decendant neuron
        value = {}

        # puting the emvironment mesurements to input neuron
        #for i,val in enumerate(inputs):
#            value[i] = [0,val]

        for nodeID in self.topoSort():
        	
            bias, func, connections = self.nodes[nodeID]

            connector = [[0,inputs[nodeID]]] if func == inp else value[nodeID] if nodeID in value else [[0,0]]
            
            if connections and func != tanh:
            	continue
            	
            
            output = round(node(connector, bias, func),3)
            
            if func == tanh:
                out.append(output)
                continue  # to avoid runing the part because we know there is no more neuron
            

            # this part will save the output to the list of output on name of decendance so it can use it directly
            for dest, wieght in deepcopy(connections):
                if dest:  # if destination node is not None
                    if dest in value:
                        value[dest] += [output, wieght]
                    else:
                        value[dest] = [[output, wieght]]
        return out

    def add_hiden_node(
        self,
        bias: float,
        srcs: list["parent_node: int, weight: float"],
        dest: list["decendant_node: int, weight: float"],
    ) -> None:
        # adds new connection from parent node to new node
        self.nodes[srcs[0]][2].append([len(self.nodes), srcs[1]])

        # make new node with connection to decendant node
        self.nodes.append((bias, relu, [dest]))

    def add_connection(self, nodeID: int, dest: int, weight: float = 1.0) -> None:

        existing_connections = deepcopy(self.nodes[nodeID][2])
        temp = []
        notfound = True
        for node, i in existing_connections:
            if node == dest:
                notfound = False
                out = weight
            else:
                out = i
            temp.append([node, out])
        if notfound:
            temp.append([dest, weight])

        return temp

    def change_bias(self, nodeId: int, bias: float):
        self.nodes[nodeId][0] = bias

    def topoSort(self):
        # Step 1: Initialize the graph and in-degree dictionary
        graph = defaultdict(list)
        in_degree = defaultdict(int)

        # Step 2: Populate the graph and in-degree based on input_data
        for index, (*a, descendants) in enumerate(self.nodes):
            if descendants:
                for descendant in descendants:
                    if not descendant:
                        continue
                    graph[index].append(descendant[0])
                    in_degree[descendant[0]] += 1

            # Make sure all nodes appear in the in-degree dictionary
            if index not in in_degree:
                in_degree[index] = 0

        # Step 3: Find all nodes with no incoming edges (in-degree 0)
        zero_in_degree_nodes = deque(
            [node for node in in_degree if in_degree[node] == 0]
        )

        # Step 4: Perform the topological sort
        topo_sorted = []
        while zero_in_degree_nodes:
            current_node = zero_in_degree_nodes.popleft()
            topo_sorted.append(current_node)

            # Decrease the in-degree of each descendant
            for neighbor in graph[current_node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    zero_in_degree_nodes.append(neighbor)

        # Step 5: Check if topological sort is possible (no cycle)
        if len(topo_sorted) == len(self.nodes):
            return topo_sorted
        else:
            return ("Cycle detected, topological sort not possible",list(range(len(self.nodes))))[1]

def play(agent:network) -> int:
	"""play against the agent where it's opponent is a randomized move and return the score"""
	"""the scoring will be based +1 if it attacks on block that has no other attack"""
	"""else -1, +2 if tie,-5 if loose,+10 if wins,- amount of total attack made"""
	

#def sort_by_score(agents:list[list['agent:network',"score:int"]]) -> list[list[int,int]]:
#	"""sort agents by it's score"""
#	print(agents)
#	
#	l = len(agents)
#	s=  agents
#	while True:
#		agents1 = deepcopy(agents)
#		agents = []
#		for agentID,(_,score) in enumerate(agents1):
#			jmbl = False
#			#print(agentID, (agentID+2)%l,l)
#			a = agents1[agentID]
#			b = agents1[(agentID+2)%l]
#			
#			if a[1] > b[1]:
#				temp = a
#			else:
#				jmbl = True
#				temp = b
#			agents.append(temp)
#			#print(agents)
#		if not jmbl:
#			break
#			
#	return agents

def pop_range(lst, start, end):
#    if start < 0 or end >= len(lst) or start > end or isinstance(start,int):
#        raise ValueError("Invalid start or end index")
    result = lst[start:end+1]
    del lst[start:end+1]
    return result




random.seed(2)
print(agent_sort_by_score([[0, random.randint(-10,10)] for _ in range(5)]))
random.seed(2)
a = [[0, random.randint(-10,10)] for _ in range(5)]
a = sorted(a,key= lambda x: x[1], reverse=True)
print(a)

from timeit import timeit

num = 1_000

#print(timeit("agent_sort_by_score(a)", number=num, globals=globals()))
#print(timeit("sorted(a,key= lambda x: x[1], reverse=True)", number=num, globals=globals()))
#print(timeit("a.sort(key= lambda x: x[1], reverse=True);s = a", number=num, globals=globals()))


flat2D = lambda x: [a for q in x for a in q]
###################


x = "x"
o = "o"
n = ""

i = [[x,n,x],
     [o,o,x],
     [n,n,n]]
     
s = [[-1.0 if x == a else 1.0 if o == a else 0.001 for a in q] for q in i]

s = flat2D(s)

seed = 99999

inputs = 9
outputs = 2

HLayer = [8,9,5]

dag = network(inputs,outputs)

print("input:",i,"translated:",s,sep="\n")

total = sum(HLayer)+inputs+outputs
for nodeLen in HLayer:
	for i in range(nodeLen):
		pass

random.seed(seed)
for i in range(inputs):
	for j in range(outputs):
		dag.add_connection(i,j,random.randint(-5,5))


random.seed(seed)
for i in dag.topoSort():
	dag.change_bias(i,random.randint(-5,5))


print("output\n  ",dag.ev(s))
#print("nodes",dag.nodes)
print(f"total nodes {len(dag.nodes)}")

random.seed(seed)
print(random.randint(0,5))
