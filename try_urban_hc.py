import random
import numpy as np
import math
import time

# Read a text file and generate a board representation as a 2D array
def read_File(fname):
    board = []
    line_num = 0
    i_max = 0
    c_max = 0
    r_max = 0
    with open(fname, 'r', encoding='utf-8-sig') as layout:
        for line in layout:
            trantab = str.maketrans(dict.fromkeys(',\n'))
            cleaned_line = line.translate(trantab)
            line_array = [char for char in cleaned_line]
            for x in range(0, len(line_array)):
                if is_intstring(line_array[x]):
                    line_array[x] = int(line_array[x])
            if line_num == 0:
                i_max = line_array[0]
            elif line_num == 1:
                c_max = line_array[0]
            elif line_num == 2:
                r_max = line_array[0]
            else:
                board.append(line_array)
            line_num+=1
    return [board, i_max, c_max, r_max]

# checks the max width of the layout
def check_max(layout):
    max = 0
    for line in layout:
        if len(line) > max:
            max = len(line)
    return max

# checks if the provided index is out of bounds or not
def is_inRange (s, i):
    try:
        b = s[i]
        return True
    except IndexError:
        return False

# checks if the provided string is an int
def is_intstring (s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Should have 4 possibilities, I - Industrial,  C - Commerce, R - Residential, or no development
def gen_rand_solution(board, indust, comm, resid):
    sol_board = [plot[:] for plot in board]
    height = len(board) -1
    width = len(board[0]) -1
    i = 0
    for x in range(0, indust):
        rand_y = random.randint(0, height)
        rand_x = random.randint(0, width)
        while not is_intstring(sol_board[rand_y][rand_x]):
            rand_y = random.randint(0, height)
            rand_x = random.randint(0, width)
        sol_board[rand_y][rand_x] = 'I'
    for x in range(0, comm):
        rand_y = random.randint(0, height)
        rand_x = random.randint(0, width)
        while not is_intstring(sol_board[rand_y][rand_x]):
            rand_y = random.randint(0, height)
            rand_x = random.randint(0, width)
        sol_board[rand_y][rand_x] = 'C'
    for x in range(0, resid):
        rand_y = random.randint(0, height)
        rand_x = random.randint(0, width)
        while not is_intstring(sol_board[rand_y][rand_x]):
            rand_y = random.randint(0, height)
            rand_x = random.randint(0, width)
        sol_board[rand_y][rand_x] = 'R'
    return sol_board

def score_solution(orig_board, sol_board):
    score = 0
    x = 0
    y = 0
    r_coord = find_all_coordinates('R', sol_board)
    c_coord = find_all_coordinates('C', sol_board)
    i_coord = find_all_coordinates('I', sol_board)
    for row in sol_board:
        for plot in row:
            if plot == 'X':
                # Industrial zones within 2 tiles take a penalty of -10
                for coord in i_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 10
                # Commercial and residential zones within 2 tiles take a penalty of -20
                for coord in r_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 20
                for coord in c_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 20
            elif plot == 'S':
                # Residential zones within 2 tiles gain a bonus of 10 points
                for coord in r_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score += 10
            elif plot == 'I':
                # For each industrial tile within 2 squares, there is a bonus of 2 points
                for coord in i_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score += 2
                score -= 2 + orig_board[y][x]
            elif plot == 'R':
                # For each industrial site within 3 squares there is a penalty of 5 points
                for coord in i_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=3:
                        score -= 5
                # However, for each commercial site with 3 squares there is a bonus of 4 points
                for coord in c_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=3:
                        score += 4
                score -= 2 + orig_board[y][x]
            elif plot == 'C':
                # For each residential tile within 3 squares, there is a bonus of 4 points
                for coord in r_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=3:
                        score += 4
                # For each commercial site with 2 squares, there is a penalty of 4 points
                for coord in c_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 4
                score -= 2 + orig_board[y][x]
            x += 1
        x = 0
        y += 1
    return score

def find_all_coordinates(building, board):
    coordinates = []
    y = 0
    x = 0
    for row in board:
        for plot in row:
            if plot == building:
                coordinates.append((y, x))
            x += 1
        x = 0
        y += 1
    return coordinates

# Move one zone and get next board with the highest score based on current board
def find_next_best_board(board):
    high_score = -1000000000
    high_board = []
    succ_board = []
    dimension = np.shape(orig_board)
    for x in range(0,dimension[1]-1):
        for y in range(0,dimension[0]-1):
            # find zones
            if board[x][y] == 'I' or board[x][y] == 'R' or board[x][y] == 'C':
                # choose one zone and calculate scores on all empty tiles.
                for i in range(0,dimension[1]-1):
                    for j in range(0,dimension[0]-1):
                        # check if this tile is empty, empty tile is int. 
                        if is_intstring(board[i][j]):
                            # copy curernt board so it will not be affected
                            succ_board = [plot[:] for plot in board]
                            # move this zone to the empty tile
                            succ_board[i][j] = board[x][y]
                            succ_board[x][y] = orig_board[x][y]
                            succ_score = score_solution(orig_board, succ_board)
                            
                            # update highest score and its board
                            if succ_score > high_score:
                                high_score = succ_score
                                high_board = [plot[:] for plot in succ_board]
        
    return [high_board, high_score]
        

# fname = input("Enter file name : ")
# fname = 'urban_1.txt'
# Original(empty) board with numbers of RIC: [board, i_max, c_max, r_max]
# read_File = read_File(fname)
# Original board and RIC 
# orig_board = read_File[0]
# indust = read_File[1]
# comm = read_File[2]
# resid = read_File[3]
# print("Original board:")
# print(orig_board)
# sol_board = gen_rand_solution(orig_board, indust, comm, resid)
# print('random board')
# print(sol_board)
# next_move = find_next_best_board(sol_board)
# next_board = next_move[0]
# next_score = next_move[1]
# print("next high score"+ str(next_score))
# print(next_board)

#######################################################################################
# Hill climbing with simulated annealing
# T is temperature, cool is cooling factor.

def hc_annealing(orig_board):
    
    maxTime = 10
    startTime = time.time()
    best_score_all = []
    steps = 0
    restart = 0
    # keep track of best boards and their scores in all rounds of simulated annealing
    best_scores= []
    best_boards= []
   
 
    
    while (time.time() - startTime < maxTime):
        # start or restart to generate a new random board and take it as current board
        sol_board = gen_rand_solution(orig_board, indust, comm, resid)
        sol_score = score_solution(orig_board, sol_board)
        current_board = [plot[:] for plot in sol_board]
        current_score = sol_score

        # track the best score and board before restart
        best_score = current_score
        best_board = [plot[:] for plot in current_board]

        T=1.0e+5000
        cool=0.99
        sidemoves = 50

        #########Use simulated annealing to decide if next board should be accepted.#####
        while T > 0.1:
            
            # check neighbor with the highest score based on this board
            next_move = find_next_best_board(current_board)
            next_board = next_move[0]
            next_score = next_move[1]
            
            # probability of accepting board with lower score        
            p = pow(math.e, (next_score-current_score)/T) 

            # if next score is higher, accept
            if next_score > current_score:
                current_board = [plot[:] for plot in next_board]
                current_score = next_score
                # update best score and board
                best_board = [plot[:] for plot in current_board]
                best_score = current_score
                # print('move up')

            # if next score is lower but acceptance possibility is high, accept
            elif next_score < current_score and p > random.random():
                current_board = [plot[:] for plot in next_board]
                current_score = next_score
                # print('move dwon')

            # take sidemoves if they are the same.
            elif next_score == current_score:
                if sidemoves > 0:
                    current_board = [plot[:] for plot in next_board]
                    current_score = next_score
                    sidemoves -= 1
                    # print('side walk')
                else:
                    print('hit plataeu')
                    break

            if time.time() - startTime > maxTime:
                print('Timeout!')
                break

            else:
                break

            # Decrease the temperature
            T = T*cool
            steps += 1
            
            
        # print('total steps: ' + str(steps))
        # restart
        restart += 1
   
            

        # save the best score before restart.
        best_scores.append(best_score)
        best_boards.append(best_board)

    print('Temoerature = ' + str(T))
    print('Restart '+ str(restart) + ' times')   

    
    # best score of all time
    best_score_all = np.max(best_scores)
    # index of the first best score is the index of first best board because they were appended to two arrays at the same time.
    index_position = best_scores.index(best_score_all)
    best_board_all = best_boards[index_position]
    return [best_score_all, best_board_all]
    
######################################################################################


# fname = input("Enter file name : ")
fname = 'urban_2.txt'
read_File = read_File(fname)
# Original board and RIC 
orig_board = read_File[0]
indust = read_File[1]
comm = read_File[2]
resid = read_File[3]
print("Original board:")
print(orig_board)
print("Having a nice cardio hill climbing for 10 second...")
result = hc_annealing(orig_board)
final_score = result[0]
final_board = result[1]
print("Highest score: " + str(final_score))
print('First board that achieved this score:')
print(final_board)




