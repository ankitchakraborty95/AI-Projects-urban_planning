import random
import copy
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
                #print("X score PENALTY for i", score)
                # Commercial and residential zones within 2 tiles take a penalty of -20
                for coord in r_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 20
                #print("X score PENALTY for r", score)
                for coord in c_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 20
                #print("X score PENALTY for c", score)

            elif plot == 'S':
                # Residential zones within 2 tiles gain a bonus of 10 points
                for coord in r_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score += 10
                #print("S score being near residential", score)
            elif plot == 'I':
                # For each industrial tile within 2 squares, there is a bonus of 2 points
                for coord in i_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2 and not dist == 0:
                        score += 2
                #print("I score being near another I", score)
                score -= 2 + orig_board[y][x]
                #print("I score because of building", score)

            elif plot == 'R':
                # For each industrial site within 3 squares there is a penalty of 5 points
                for coord in i_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=3:
                        score -= 5
                #print("R score because of penalty I", score)
                # However, for each commercial site with 3 squares there is a bonus of 4 points
                for coord in c_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=3:
                        score += 4
                #print("R score because of commercial +", score)
                score -= 2 + orig_board[y][x]
                #print("R score because of building", score)

            elif plot == 'C':
                # For each residential tile within 3 squares, there is a bonus of 4 points
                for coord in r_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=3:
                        score += 4
                #print("C score because of r +", score)
                # For each commercial site with 2 squares, there is a penalty of 4 points
                for coord in c_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2 and not dist == 0:
                        score -= 4
                #print("C score because of c penalty", score)
                score -= 2 + orig_board[y][x]
                #print("C score because of building", score)
            x += 1
        x = 0
        y += 1
    return score

# Find all coordinates of instances of a building
def find_all_coordinates(building: object, board: object):
    coordinates = []
    y = 0
    x = 0
    for row in board:
        for plot in row:
            if plot == building:
                coordinates.append([y, x])
            x += 1
        x = 0
        y += 1
    return coordinates
###########################################################################################################################################################################
############################################################################################################################################################################

# Generates a random population and its score as a tuple
def gen_population(ref_layout,pop_size):
    population = []
    for x in range(0, pop_size):
        new_member = gen_rand_solution(ref_layout[0], ref_layout[1], ref_layout[2], ref_layout[3])
        #new_member = gen_rand_solution(ref_layout[0], random.randint(0,ref_layout[1]), random.randint(0,ref_layout[1]), random.randint(0,ref_layout[1]))
        member_score = score_solution(ref_layout[0], new_member)
        population.append((new_member, member_score))
    return population

# Gets the score from the tuple
def get_score(brd):
    return brd[1]

# Sorts the population based on the best score
def get_best_fit(pop):
    pop.sort(key = get_score, reverse=True)
    return pop

# Sorts the population based on the worst score
def get_worst_fit(pop):
    pop.sort(key=get_score)
    return pop

# Gets the set of parents from the population
def get_parents(pop,elitism_factor):
    best_sort = get_best_fit([member[:] for member in pop])
    parents = []
    for top in range(0, elitism_factor):
        parents.append(best_sort[top])
    return parents
def culling_pop(pop,culling_factor):
    pop_copy = copy.deepcopy(pop)
    get_worst_fit(pop_copy)
    for i in range(0,culling_factor):
        del pop_copy[0]
    return pop_copy

def print_board(board):
    for x in board:
        print(x)