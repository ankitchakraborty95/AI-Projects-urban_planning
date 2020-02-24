import random
import numpy as np
import math
import time
from statistics import mean 
from common_functions import *

# ask for user input
# fname = input("Enter file name : ")

# program time starts here
start_time = time.perf_counter()
# max time of this program is 10s
maxTime = 10


# Move one zone and get next board with the highest score based on current board
def find_next_best_board(board, orig_board):
    high_score = -1000000000
    high_board = []
    succ_board = []
    dimension = np.shape(orig_board)
    for x in range(0,dimension[0]):
        for y in range(0,dimension[1]):
            # find zones
            if board[x][y] == 'I' or board[x][y] == 'R' or board[x][y] == 'C':
                # choose this zone and look for all empty tiles.
                for i in range(0,dimension[0]):
                    for j in range(0,dimension[1]):
                        # check if this tile is empty. empty tile is int. 
                        if is_intstring(board[i][j]):
                            # make change on a copy of curernt board
                            succ_board = [plot[:] for plot in board]
                            # move this zone to the empty tile by swapping location.
                            succ_board[i][j] = board[x][y]
                            succ_board[x][y] = orig_board[x][y]
                            succ_score = score_solution(orig_board, succ_board)
                            
                            # update highest score and its board
                            if succ_score > high_score:
                                high_score = succ_score
                                high_board = [plot[:] for plot in succ_board]
        
    return [high_board, high_score]


#######################################################################################
# Hill climbing with simulated annealing

def hc_annealing(orig_board, indust, comm, resid):
    
    best_score_all = 0
    # to save the board and time when the first highest score is achieved.
    first_best_board = 0
    first_best_time = 0
   
    # keep track of best boards and their scores in all rounds of simulated annealing
    best_scores= []
    best_boards= []
    best_times = []

    # keep track of numbers of restart
    restart = 0

    while time.perf_counter() - start_time < maxTime:

        # T is temperature, cool is cooling factor.
        T=500
        cool=0.95
        
        # generate a new random board and pass it to current board
        sol_board = gen_rand_solution(orig_board, indust, comm, resid)
        sol_score = score_solution(orig_board, sol_board)
        current_board = [plot[:] for plot in sol_board]
        current_score = sol_score
        
        # track the best score and board and time before restart
        best_score = current_score
        best_board = [plot[:] for plot in current_board]
        best_time = time.perf_counter()
 
        #Use simulated annealing to decide if next board should be accepted.
        while T > 0.1 and time.perf_counter() - start_time < maxTime:
            
            # check neighbor with the highest score based on this board
            next_move = find_next_best_board(current_board, orig_board)
            next_board = next_move[0]
            next_score = next_move[1]

            # probability of accepting board with lower score        
            p = pow(math.e, (next_score-current_score)/T) 

            # if next score is higher, accept
            if next_score > current_score:
                current_board = [plot[:] for plot in next_board]
                current_score = next_score
                # update best score and board and time whenever there's higher score
                best_time = time.perf_counter()
                best_board = [plot[:] for plot in current_board]
                best_score = current_score
             

            # if next score is lower but acceptance possibility is high, accept
            elif next_score < current_score and p > random.random():
                current_board = [plot[:] for plot in next_board]
                current_score = next_score

            else:
                
                break
            
            # Decrease the temperature
            T = T*cool

            # save the best score, board, time after annealing and before restart.
            best_scores.append(best_score)
            best_boards.append(best_board) 
            best_times.append(best_time) 
    
        # restart
        restart += 1
        
    print("Started at " + str(500) + ' degree, with cooling factor ' + str(cool) + ', simulated annealing restarted ' + str(restart) + " times")  
    
    # best score of all time
    best_score_all = np.max(best_scores)

    # index of the first best score is the index of first best board
    #  because they were appended to arrays at the same time.
    index_position = best_scores.index(best_score_all)
    first_best_board = best_boards[index_position]
    first_best_time = best_times[index_position]
    return [best_score_all, first_best_board, first_best_time]
    
######################################################################################