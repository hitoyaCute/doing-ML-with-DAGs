import time
import random
import tictactoe
from tictactoe import play
from DAGs import Network
from threading import Thread as t
from concurrent.futures import ThreadPoolExecutor as Threader
pause = False
training= True

def main():
    a = t(target=train)
    
    a.start()
    ask()
    a.stop()
    
def ask():
    while True:
        a = input("stop - stop the training\npause\nplay").lower()
        if a == "s":
            training = False
            break
        if a == "":
            pause = True
        if a == "l":
            training = True
            pause = False



def train(generation=500000000000000,seed=2):
    random.seed(99)
    num_of_agent = 200
    
    def evolve_agents(participants):
        print("evolving...")
        return [net.mutate(20,7) for net in participants]

    
    #first initialize 1,000 agents
    agents = [Network(9,2) for _ in range(num_of_agent)]
    
    #randomize the structure of a agent
    agents = evolve_agents(agents)

    
    #loop
    s = lambda x : x[1]
    i = 0
    while True :
        if i == generation-1:
            break
        if pause:
            time.sleep(0.2)
            continue
        if not training:
        	break
        
        print(f'generation {i}' )
        
        
        #step1 evaluate
        with Threader(200) as exct:
            evaluaties = list(exct.map(fit, agents))
            
            
        #step2 selection
        evaluaties.sort(key=s)
        print(f" max score : {evaluaties[0][1]} min score : {evaluaties[num_of_agent-1][1]}")
        print(f" state:{agents[0].order_nodes(),agents[0].connections}")
        agents[0].save("net.tt")#i can't think of creative format or name ._.
        evaluaties = [i[0] for i in evaluaties]
        
        passers =  poprange(evaluaties,60)
        
        
        #step3 mutaion
        evaluaties = evolve_agents(evaluaties)
        agents = passers+evaluaties
        i+=1
    print(agents[0].nodes)
    


    
def fit(agent):
    def interpret(var):
        def _inv(environment:list):
            a,b = [int(i) for i in agent.forward([0 if i=='' else 1 if i==var else -1 for i in environment.copy()])]
            return (a+1*3)+b+1
        return _inv
    
    a = play(interpret("o"), tictactoe.b)[0]
    
    #b = play(tictactoe.b , interpret("x"))[1]
    return agent,a




def poprange(lst, start, end=None):
    if not end:
        end = len(lst)-1
    # if start < 0 or end >= len(lst) or start > end or isinstance(start,int):
    #     raise ValueError("Invalid start or end index")
    result = lst[start:end+1]
    del lst[start:end+1]
    return result
if __name__ == "__main__":
    main()
