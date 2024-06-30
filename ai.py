import random
import numpy as np
from math import tanh,exp
from copy import deepcopy
from collections import defaultdict, deque

random.seed(0)

def main():
    dag = Network(2,2)
    dag.mutate(1)
    a = [2,2]
    dag.add_connection(1,3,1)
    print(dag.inp,dag.outp,dag.hidden_nodes,dag.connections)
    print(dag.predict(a))


    

class Network:
    def __init__(self, inp, outp):
        self.inp = inp
        self.outp = [[0,"tanh"] for _ in range(outp)]
        self.hidden_nodes = []
        self.connections = {}
    def predict(self, env:list):
        '''create a prediction based on the structure of the network\nenv is a list of measurement from the environment'''
        outp = [0.0]*len(self.outp)
        #storing the final values
        values = {}
        #values = {descendantID: {parentID: val} for parentID,val in enumerate(env) for _,descendantID in self.connections[parentID].items() if parentID in self,connections}
        for parentID,val in enumerate(env):
            if parentID in self.connections:
                for descendantID,w in self.connections[parentID].items():
                    if descendantID in values:
                        values[descendantID][parentID] = val
                    else:
                        values[descendantID] = {parentID: val}
        
        #how many out node
        outn = len(self.outp)
        
        #step 1 get the order of operation
        srtd = self.topoSort()
        print(srtd)
        for i in srtd[self.inp:]:
            
            #check is its a output node by knowing if node index(i) is less than outn
            #index format is input_nodes,output_nodes,hidden_nodes
            a_outp_node = not i < self.inp
            
            #holder of biases
            
            node = self.outp[i-self.inp-1] if a_outp_node else self.hidden_nodes[i-(outn+self.inp)-1]
            # if i in self.connections:
            #     print(i,node,values[i],self.connections[i],"lll")
            
            
            #calculate the final value
            val = sum(
                [
                    (
                        0 if descendantID not in values else
                        0 if i not in values[descendantID] else values[descendantID][i]
                    ) * w
                    for descendantID,w in self.connections[i].items()
                ]
            ) + node[0] if i in self.connections else 0
            
            #activator chunk
            activator = node[1]
            if activator == "relu":
                val = 0 if val < 0 else val
            elif activator == "sigmoid":
                val = 1/(1+exp(-val))
            elif activator == "tanh":
                val = tanh(val)
            elif activator == "softmax":
                pass
            
            #stuff that will tell what value a node will get
            print(val)
            if not a_outp_node:
                for dest,_ in self.connections[i].items():
                    if i in values:
                        values[dest][i] = val
                    else:
                        values[dest] = {i: val}
            
            else:
                outp[i-self.inp] = val
        
        return outp
        
    def mutate(self, new_connection_rate: int, new_node_rate: int = 0, new_bias_rate: int = 0):
        """do a random mutation on the network None means give no probability that a action rate will be performed"""
        
        #create a list of how much a action will be done
        lst = ["connection"] * new_connection_rate
        lst += ["node"] * new_node_rate
        lst += ["bias"] * new_bias_rate
        
        #randomly select on what action will be done
        action = random.choice(lst)
        
        hidden = len(self.hidden_nodes)
        outp = len(self.outp)
        #create a list on IDs of all nodes
        total_nodes = self.inp+outp+hidden
        nodes_ID = list(range(total_nodes))
        
        #get a random poiting node
        node = random.choice(nodes_ID)
        #this is a node that will be use as head for a connection
        srcs_node = random.choice(nodes_ID[:self.inp] + nodes_ID[self.inp+outp:])
        #get a random dest from outp to hidden where dest is always the descendant of the srcs_node
        dest =  nodes_ID[(srcs_node if srcs_node < self.inp-1 else self.inp)-1:]
        dest_node = random.choice(dest)
        
        #create a random bias and wieghts
        r1,r2,r3 = [random.randint(-7,7) for _ in (1,2,3)]
        
        print(action,srcs_node,dest_node,r1)
        if action == "node" and self.connections:
            self.add_node(srcs_node, dest_node, w1, w2, w3)
            #this should be same as connection option
        elif action == "bias":
            self.bias(node, w1)
            #get a random node from hidden to output
        else:
            self.add_connection(srcs_node, dest_node, r1)
            #random node from input to hidden, from the index of the chosen hidden to output where index cant be pointing at inp node
    def add_node(self, node: int, dest: int, bias = 0.0, w1 = 1.0, w2 = 1.0, activator: str = "relu"):
        """adds new node by spiting connection assuming/n     that you call this and there is connection exist else err"""
        
        #step 1 add the hidden_node on the node list
        self.hidden_nodes.append([bias,activator])
        new_node_id = len(self.hidden_nodes)-1
        
        self.add_connection(node, new_node_id, w1)
        self.add_connection(new_node_id, dest, w2)
    def add_connection(self, node:int, dest:int, w = 1.0):
        if node in self.connections:
            self.connections[node][dest] = w
        else:
            self.connections[node] = {dest: w}
    def change_bias(self, node:int, bias = 0.0):
        #if the node is a hidden node or a output
        layer = self.hidden_nodes if node > len(self.outp) else self.outp
        layer[node] = bias
    
    def topoSort(self):
        edge = self.connections
        list_of_all_node  = range(self.inp+len(self.outp+self.hidden_nodes))
        # Add all nodes from list_of_all_node to the edge dictionary if they don't already exist
        for node in list_of_all_node:
            if node not in edge:
                edge[node] = {}
    
        # Initialize a dictionary to count in-degrees of all nodes
        in_degree = {node: 0 for node in list_of_all_node}
    
        # Calculate in-degrees
        for node in edge:
            for neighbor in edge[node]:
                if neighbor in in_degree:
                    in_degree[neighbor] += 1
    
        # Initialize a queue and add all nodes with in-degree 0
        queue = [node for node in in_degree if in_degree[node] == 0]
    
        topo_sorted_list = []
    
        while queue:
            current_node = queue.pop(0)
            topo_sorted_list.append(current_node)
    
            for neighbor in edge[current_node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
    
        if len(topo_sorted_list) == len(list_of_all_node):
            return topo_sorted_list
        else:
            raise Exception("Graph has a cycle")
    
    # def topoSort(self):
    #     # Step 1: Initialize the graph and in-degree dictionary
    #     graph = defaultdict(list)
    #     in_degree = defaultdict(int)
        
    #     # Step 2: Populate the graph and in-degree based on input_data
    #     for index, descendants in self.connections.items():
    #         if descendants:
    #             for descendant in descendants:
    #                 if not descendant:
    #                     continue
                    
    #                 graph[index].append(descendant)
    #                 in_degree[descendant] += 1
            
    #         # Make sure all nodes appear in the in-degree dictionary
    #         if index not in in_degree:
    #             in_degree[index] = 0
        
    #     # Step 3: Find all nodes with no incoming edges (in-degree 0)
    #     zero_in_degree_nodes = deque(
    #         [node for node in in_degree if in_degree[node] == 0]
    #     )
        
    #     # Step 4: Perform the topological sort
    #     topo_sorted = []
    #     while zero_in_degree_nodes:
    #         current_node = zero_in_degree_nodes.popleft()
    #         topo_sorted.append(current_node)
            
    #         # Decrease the in-degree of each descendant
    #         for neighbor in graph[current_node]:
    #             in_degree[neighbor] -= 1
    #             if in_degree[neighbor] == 0:
    #                 zero_in_degree_nodes.append(neighbor)
        
    #     # Step 5: Check if topological sort is possible (no cycle)
    #     # print(topo_sorted)
    #     # if len(topo_sorted) == len(self.connections):
    #     #     return topo_sorted
    #     # else:
    #     #     raise ValueError("topological sorting is impossible")
        # return topo_sorted


if __name__ == "__main__":
    main()
