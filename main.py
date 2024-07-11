import time
import random
import tictactoe

from tictactoe import play,best_attack,trainf,create_best_posible_move

from DAGs import Network
from threading import Thread as t
#from concurrent.futures import ThreadPoolExecutor as Threader
from multiprocessing import Pool
pause = False
training= True
create_best_posible_move()

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
    a = [[0,1],[0,2],[2,3]];f = lambda x:x[0]


def train(generation=50000,seed=0):
    random.seed(seed)
    num_of_agent = 1000
    
    def evolve_agents(participants):
        print("evolving...")
        [net.mutate(50,25) for net in participants]

    
    #first initialize 1,000 agents
    agents = [Network(9,2) for _ in range(num_of_agent)]
    #[(agent.nodes.append(0), agent.connections.append({})) for agent in agents.copy() for _ in range(5)]
    #randomize the structure of a agent
    evolve_agents(agents)

    
    #loop
    s = lambda x : x[1]
    i = 0
    t1 = time.perf_counter()
    with Pool() as exct:
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
            
            evaluaties = list(exct.imap(fit, agents, chunksize=100))
                
                
            #step2 selection
            
            #random.shuffle(evaluaties)
            
            evaluaties.sort(key=s)
            print(f" max score : {evaluaties[0][1]} min score : {evaluaties[num_of_agent-1][1]} ,total_agent {len(agents)}")
            #print(f" state:{evaluaties[0][0].order_nodes(),evaluaties[0][0].connections}")
            
            evaluaties[0][0].save("net.tt")#i can't think of creative format or name ._.
            
            
            evaluaties = [i[0] for i in evaluaties]
            
            passers =  poprange(evaluaties,0,300)
            
            
            #step3 mutaion
            evolve_agents(evaluaties)
            agents = passers+evaluaties
            i+=1
            t2 = time.perf_counter()
            print(f"execution takes {t2-t1}s")
            t1 = t2
    print(agents[0].nodes)
    


    
def fit(agent):
    def interpret(var):
        def _inv(environment:list):
            a,b = [max((min((int(i),1)),-1)) for i in agent.forward([0 if i=='' else 1 if i==var else -1 for i in environment[:]])]
            return ((a+1)*3)+b+1#i found this was the problem lol 😂
        return _inv
    
    #a = play(interpret("o"), tictactoe.b)[0]
    def ai(f):
        def inner(board,attack="x"):
            return f(board)
        return inner
    b = trainf(interpret)
    #b = play(interpret("x"), ai(best_attack))[0]
    #b = play(tictactoe.b,interpret("x"))[1]
    return agent,b




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
    #main2()



[72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100, 33]
