import random
######tic tac toe environment #####


#========tic tac toe training code============
is_board_full = lambda board: (all(cell != '' for cell in board.copy()))
available_move = lambda board: [i for i,c in enumerate(board) if c == '']

win_combo = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

# def is_winner(player,board):
#     for c in win_combo:
#         if all(board[i]==player for i in c.copy()):
#             return True
#     return False
is_winner = lambda player,board: True in [all(board[i]==player for i in c.copy()) for c in win_combo.copy()]


################the original code :)#################
def _(network, is_agent_attack_x=True, fitness_seed:int=0) -> int:
    random.seed(fitness_seed)
    board = [""]*9
    cboard = [0]*9
    
    score = 0
    while not is_board_full(board):
        
        score -= 1
        x_move = dplay(network.run(cboard)) if is_agent_attack_x else random.choice(available_move(board))
        
        a = (1,-1) if is_agent_attack_x else (-1,1)
        
        if board[x_move] == "":
            board[x_move] = "x"
            cboard[x_move] = a[0]
            if is_winner("x",board):
                print("x won")
                score -= 20
                break
            if is_board_full(board):
                print("tie")
                break
            o_move = random.choice(available_move(board)) if is_agent_attack_x else dplay(network.run(cboard))
            #print(o_move)
            board[o_move] = "o"
            cboard[o_move] = a[1]
            if is_winner("o",board):
                print("o won")
                score += 100
                break
        else:
            print("oof wrong attack ",x_move,board[x_move])
            return score + 999
        for i in range(0,9,3):
            print(board[i:i+3])
    
    clear_board()
    return score
#========tic tac toe training code============

def play(player_x:callable, player_o:callable):
    #random.seed(0)
    board = [""]*9
    score_o = score_x = 0
    
    while not is_board_full(board):
        
        x_move = player_x(board)
        
        
        if board[x_move] == "":
            
            score_x -= 2
            board[x_move] = "x"
            if is_winner("x",board):
                
                score_x -= 1
                break
            if is_board_full(board):
                
                break
            o_move = player_o(board)
            
            
            if board[o_move] != "":
                
                
                score_o += 99
                break
            board[o_move] = "o"
            score_o -= 2
            if is_winner("o",board):
                
                
                score_o -= 1
                break
        else:
            score_x += 99
            break
    else:
        score_x -= 2
        score_o -= 2
        
    
    #print(score_o, score_x)
    return score_o, score_x
    

def a(board):
    b = [i if board[i] == "" else board[i] for i in range(9)]
    for i in range(3):
        print()
        [print(s, end=", ") for s in b[i*3:(i*3)+3]]
        print()
        
    return int(input())

def b(board):

    return random.choice(available_move(board))
    
if __name__ == "__main__":
    
    o, x = play(a, b)
    if o < x:
        print("o wins")
    elif o > x:
        print("x wins")
    else:
        print("its a tie")
#def qq():
#    ss = lambda x: x[1]
#    a = [(int,0)]*1_000
#    a.sort(key=ss)
#    play(b,b)
#    #print(a)
#from timeit import timeit

#s = timeit("qq()",number=1000,globals = globals())
#print(s,s/1000)
#       
        
    