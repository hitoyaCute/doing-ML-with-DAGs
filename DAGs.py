import random
#import numpy as np
from math import tanh,exp,sqrt,pi
from math import pow as mpow
random.seed(1)
def main():
    net = Network(2,2)
    for _ in range(0):
        net.mutate(5,5)
    #print(net.mutate(1,1,1))
    net.add_connection(0,3,2)
    net.add_connection(1,2,0.3)
    print(net.connections,"connections")
    print(net.nodes,"biases")
    print(net.order_nodes())
    print(net.forward([1.5,2.4]))
#play against the ai
def main():
    import tictactoe as rps
    from tictactoe import play
    agent = load("net.tt")
    
    def w(f):
        def inner(v):
            s = f(v)
            print(v,s)
            return s
        return inner
    rps.b = w(rps.b)
    
    
    def interpret(var):
        def _inv(environment:list):
            a,b = [int(i) for i in agent.forward([0 if i=='' else 1 if i==var else -1 for i in environment.copy()])]
            return ((a+1)*3)+b+1
        return _inv
    
    a = play(interpret("o"), rps.a)[0]
    print(a)
    


def load(file_dir:str):
    with open(file_dir, "rt") as data:
        
        
        dat = data.readline().strip().split(" ")
        inp,outp = [int(v) for v in dat[:2]]
        net = Network(inp,outp)
        for step in data:
            
            act, trgt, rs = step.strip().split(";")
            r1,r2,r3 = map(int,rs.split(" "))
            b_target,sn_target,dn_target = map(int,trgt.strip().split(' '))
            if act == "node":
                net.add_node(sn_target,dn_target,r1,r2,r3)
            elif act == "bias":
                net.change_bias(b_target,r1)
            else :
                net.add_connection(sn_target,dn_target,r1)
        return net


class Network:
    def __init__(self, inp:int, outp:int, hidfunc:str = "relu", outpfunc:str = "tanh"):
        """Initialize the network with fixed input and output layer"""
        self.inp = inp
        self.outp = outp
        #all of the nodes contains its biases
        self.nodes = [0 for _ in range(inp+outp)]
        self.connections = [{} for i in range(inp+outp)]
        self.hidfunc = hidfunc
        self.outpfunc = outpfunc
        self.dat = [(inp,outp, hidfunc,outpfunc)]
    def forward(self,inp:list[float,...]) -> list[float,...]:
        if len(inp) != self.inp:
            raise ValueError("invalid input lenght")
        outp = [0.0]*self.outp
        # nodes = [
        #     [#node0
        #         value,
        #         bias,
        #         [
        #             [dest_node,weights],
        #             ...#next set of weights
        #         ]
        #     ],
        #     ...#next set of nodes
        # ]
        
        #preparation of all nodes
        nodes = [[(inp[i] if i < self.inp else 0)+bias,[[i,weights] for weights in self.connections[i]]] for i,bias in enumerate(self.nodes)]
        
        ###########################SCOPES################################
        #[input_nodes   +    output_nodes            + hidden_nodes]
        #first self.inp + from self.inp to self.outp + the rest
        
        for nodeID in self.order_nodes():
            
            val = nodes[nodeID][0]
            
            #perform a value spreading and only input and hidden do this
            #the nodeID should be not a output node
            
            for i,w in self.connections[nodeID].items():
               nodes[i][0] += val * w
               #print(nodes[i][0],val,"a")
            
            #perform a activation func and only hidden and outp do this
            #                         if in output scope                  and not in hidden scope
            activator = self.outpfunc if nodeID < self.inp+self.outp and not nodeID < self.inp else self.hidfunc
            #if not in input scope
            if not nodeID < self.inp:
                if activator == "relu":
                    val = 0 if val < 0 else val
                elif activator == "sigmoid":
                    val = 1/(1+exp(-val))
                elif activator == "tanh":
                    val = tanh(val)
                elif activator == "softmax":
                    pass
                elif activator == "lrelu":
                    pass
                elif activator == "elu":
                    pass
                elif activator == "gelu":
                    val = 0.5*val*(1+(tanh(sqrt(2/pi)*(val+0.044715)*(mpow(val,3)))))
                nodes[nodeID][0] = val
                
            #if outside the inp    and inside the outp scope
            if self.inp-1 < nodeID < self.inp+self.outp:
                outp[nodeID-self.inp] = val
        
        return outp
    def add_node(self,srcs,dest,w1,w2,bias):
        nodeID = len(self.nodes)
        #add node to the list of bias
        self.nodes.append(bias)
        del self.connections[srcs][dest] #cut the existing connection
        #set new connections
        self.add_connection(srcs,nodeID,w1)
        self.add_connection(nodeID, dest, w2)
    def add_connection(self, node, dest, w = 1.0):
        
        if node < len(self.connections):
            self.connections[node][dest] = w
        else:
            self.connections.append({dest: w})
    def change_bias(self,srcs,bias):
        
        self.nodes[srcs] = bias
    def mutate(self,c_rate:int,b_rate:int=1,n_rate:int=1) -> "what mutation happens":
        """do a random mutation on the network None means give no probility that a action rate will be performed"""
        
        #create a list of how much a action will be done
        lst = ["connection"] * c_rate
        lst += ["node"] * n_rate
        lst += ["bias"] * b_rate
        #randomly select on what action will be done
        action = random.choice(lst)
        #bias change target
        b_target = random.randrange(len(self.nodes))
        
        nodes = self.order_nodes()
        
        #srcs connection node target index
        sn_target = random.choice(list(enumerate(nodes[:-self.outp])))
        #decendant connection node target after the ns_target index
        dn_target = random.choice(nodes[sn_target[0] if sn_target[1] > self.inp else self.inp:])
        sn_target = sn_target[1]
        
        #random values
        random.choice([0])
        r1, r2, r3 = [random.randint(-7,7) for i in [0,0,0]]
        
        if action == "node" and self.connections[sn_target]:
            #print(self.connections[sn_target])
            dn_target = random.choice(list(self.connections[sn_target].items()))[0]
            self.add_node(sn_target,dn_target,r1,r2,r3)
        elif action == "bias":
            self.change_bias(b_target,r1)
        else :
            action = "connection"
            self.add_connection(sn_target,dn_target,r1)
        
        x = action,(b_target,sn_target,dn_target),(r1,r2,r3)
        
        self.dat.append(x)
        return self
    def order_nodes(self):
        nodes = list(range(len(self.nodes)))
        return nodes[:self.inp]+nodes[self.outp+self.inp-2:]+nodes[self.inp:self.outp]
    def save(self, name):
        with open(name, "w") as file:
            for a in self.dat[0]:
                print(a,file=file,end=" ")
            for data in self.dat.copy()[1:] :
                print(f"\n{data[0]}",file = file, end="")
                [print(';'if j == 0 else "",a, file=file, end=' ',sep='') for i in (1,2) for j,a in enumerate(data[i])]
                
if __name__ == "__main__":
    main()