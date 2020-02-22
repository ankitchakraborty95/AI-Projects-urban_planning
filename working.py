import random
import numpy
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
                    if dist <=2 and dist!=0:
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
                    if dist <=2 and dist!=0:
                        score -= 4
                #print("C score because of c penalty", score)
                score -= 2 + orig_board[y][x]
                #print("C score because of building", score)
            x += 1
        x = 0
        y += 1
    return score

def find_all_coordinates(building: object, board: object) -> object:
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
# main genetic algorithm
def genetic_algorithm(ref_layout):
    population = gen_population(ref_layout)
    parents = get_parents(population)
    parent_1 = random.randint(0, len(parents)-1)
    parent_2 = parent_1
    while parent_2 == parent_1:
        parent_2 = random.randint(0, len(parents)-1)
    create_children(ref_layout[0], parents[parent_1][0], parents[parent_2][0])
    #for x in parents:
    #    for c in x[0]:
    #        print(c)
    #    print(x[1])
    pass

# Generates a random population and its score as a tuple
def gen_population(ref_layout):
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
def get_parents(pop):
    best_sort = get_best_fit([member[:] for member in pop])
    parents = []
    for top in range(0, elitism_factor):
        parents.append(best_sort[top])
    return parents
def culling_pop(pop):
    pop_copy = copy.deepcopy(pop)
    get_worst_fit(pop_copy)
    # print("worst sort")
    # print_board(get_worst_fit(pop_copy))
    for i in range(0,culling_factor):
        #print("removing",pop_copy[0])
        del pop_copy[0]
    return pop_copy

# Creates children based off 2 parents
# Simply cuts the 2D array in half between rows, and stitchs the other half on
def create_children(reference, mom, dad):
    height = len(mom)
    divide = int(height/2)
    mom_clone = copy.deepcopy(mom)
    dad_clone = copy.deepcopy(dad)
    # print("mom")
    # print_board(mom_clone)
    # print("dad")
    # print_board(dad_clone)
    child1 = []
    child2 = []
    for x in range(0, divide):
        child1.append(mom_clone[x])
        child2.append(dad_clone[x])
    for y in range(divide, height):
        child1.append(dad_clone[y])
        child2.append(mom_clone[y])
    x_list = find_all_coordinates('X',reference)
    s_list = find_all_coordinates('S',reference)
    for x in x_list:
        child1[x[0]][x[1]] = 'X'
        child2[x[0]][x[1]] = 'X'
    for s in s_list:
        child1[s[0]][s[1]] = 'S'
        child2[s[0]][s[1]] = 'S'
    # print("child 1")
    # print_board(child1)
    # print("child 2")
    # print_board(child2)

    child1_score = score_solution(reference, child1)
    child2_score = score_solution(reference, child2)
    return [(child1, child1_score), (child2, child2_score)]
def create_children_2(reference,mom,dad):
    reference_copy = copy.deepcopy(reference)
    # print("copy board")
    # print(reference_copy)
    mom_copy = copy.deepcopy(mom)
    dad_copy = copy.deepcopy(dad)
    # print("mom")
    # print_board(mom_copy)
    # print("dad")
    # print_board(dad_copy)
    child1 =copy.deepcopy(reference_copy)
    child2 =copy.deepcopy(reference_copy)
    i_temp_mom = find_all_coordinates('I',mom_copy)
    #print("i temp mom",i_temp_mom)
    i_temp_dad= find_all_coordinates('I', dad_copy)
    #print("i temp dad", i_temp_dad)
    n = random.randint(0,1)
    if(n==0):
        for cord in i_temp_mom:
            #print(" I taken from mom child 1")
            child1[cord[0]][cord[1]] = 'I'
    else:
        for cord in i_temp_dad:
            #print(" I taken from dad child 1")
            child1[cord[0]][cord[1]] = 'I'
    n = random.randint(0, 1)
    if (n == 0):
        for cord in i_temp_mom:
            #print(" I taken from mom child 2")
            child2[cord[0]][cord[1]] = 'I'
    else:
        for cord in i_temp_dad:
            #print(" I taken from dad child 2")
            child2[cord[0]][cord[1]] = 'I'
#############################################
    c_temp_mom = find_all_coordinates('C', mom_copy)
    #print("c temp mom", c_temp_mom)
    c_temp_dad = find_all_coordinates('C', dad_copy)
    #print("c temp dad", c_temp_dad)
    n = random.randint(0, 1)
    if (n == 0):
        for cord in c_temp_mom:
            #print("C taken from mom child 1")
            child1[cord[0]][cord[1]] = 'C'
    else:
        for cord in c_temp_dad:
            #print("C taken from dad child 1")
            child1[cord[0]][cord[1]] = 'C'
    n = random.randint(0, 1)
    if (n == 0):
        for cord in c_temp_mom:
            #print("C taken from mom child 2")
            child2[cord[0]][cord[1]] = 'C'
    else:
        for cord in c_temp_dad:
            #print("C taken from dad child 2")
            child2[cord[0]][cord[1]] = 'C'
##################################################3
    r_temp_mom = find_all_coordinates('R', mom_copy)
    #print("r temp mom", r_temp_mom)
    r_temp_dad = find_all_coordinates('R', dad_copy)
    #print("r temp dad", r_temp_dad)
    n = random.randint(0, 1)
    if (n == 0):
        for cord in r_temp_mom:
            #print("R taken from mom child 1")
            child1[cord[0]][cord[1]] = 'R'
    else:
        for cord in r_temp_dad:
            #print("R taken from dad child 1")
            child1[cord[0]][cord[1]] = 'R'
    n = random.randint(0, 1)
    if (n == 0):
        for cord in r_temp_mom:
            #print("R taken from mom child 2")
            child2[cord[0]][cord[1]] = 'R'
    else:
        for cord in r_temp_dad:
            #print("R taken from dad child 2")
            child2[cord[0]][cord[1]] = 'R'
    # print("child 1","mom",mom_copy,"dad",dad_copy)
    # print_board(child1)
    # print("child 2","mom",mom_copy,"dad",dad_copy)
    # print_board(child2)
    while(check_board(child1)==False):
        mutate_board(child1)
    while (check_board(child2) == False):
        mutate_board(child2)
    child1_score = score_solution(reference_copy, child1)
    child2_score = score_solution(reference_copy, child2)
    return [(child1, child1_score), (child2, child2_score)]
def check_board(board):
    r_coord = find_all_coordinates('R', board)
    c_coord = find_all_coordinates('C', board)
    i_coord = find_all_coordinates('I', board)
    if(len(r_coord)==0 or len(i_coord)==0 or len(c_coord)==0):
        return False
    else:
        return True
def mutate_board(board):
    i_cord = find_all_coordinates('I',board)
    if(len(i_cord)==0):
        t = True
        while(t):
            row = random.randint(0,(len(board)-1))
            col = random.randint(0,(len(board[0])-1))
            if(board[row][col]!='X' and board[row][col]!='S' and board[row][col]!='C' and board[row][col]!='R'):
                board[row][col]='I'
                t=False
    c_cord = find_all_coordinates('C', board)
    if (len(c_cord) == 0):
        t = True
        while (t):
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board[0]) - 1)
            if (board[row][col] != 'X' and board[row][col] != 'S' and board[row][col] != 'I' and board[row][
                col] != 'R'):
                board[row][col] = 'C'
                t = False
    r_cord = find_all_coordinates('R', board)
    if (len(r_cord) == 0):
        t = True
        while (t):
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board[0]) - 1)
            if (board[row][col] != 'X' and board[row][col] != 'S' and board[row][col] != 'I' and board[row][
                col] != 'C'):
                board[row][col] = 'R'
                t = False
    return board

def print_board(board):
    for x in board:
        print(x)
######################################################################################################################################################################
pop_size = 400
elitism_factor = 10
culling_factor = 3
input_board = read_File(r"H:\\WPI\spring 20\AI\ASSIGNMENT 1\urban 2.txt")
print_board(input_board)
initial_pop = gen_population(input_board)
curr_pop = copy.deepcopy(initial_pop)
print("initial pop")
print_board(initial_pop)

#############
start_time = time.perf_counter()

run =True
while(run):
    elitism_pop = get_parents(curr_pop)
    next_gen_pop = []
    #######elitism pop############
    # print("elitism pop")
    # print_board(elitism_pop)
    for x in elitism_pop:
        next_gen_pop.append(x)
    # print("next gen")
    # print_board(next_gen_pop)
    #########pop after culling#########33
    pop_after_culling = culling_pop(curr_pop)
    # print("pop after culling")
    # print_board(pop_after_culling)
    children_count = pop_size - elitism_factor
    i = 0
    while (children_count > 0):
        if (children_count != 1):
            child = create_children_2(input_board[0], pop_after_culling[i][0], pop_after_culling[i + 1][0])
            next_gen_pop.append(child[0])
            next_gen_pop.append(child[1])
            i = i + 2
            children_count = children_count - 2
        else:
            child = create_children_2(input_board[0], pop_after_culling[i][0], pop_after_culling[i + 1][0])
            next_gen_pop.append(child[0])
            i = i + 1
            children_count = children_count - 1
    # print("next gen")
    # print_board(next_gen_pop)
    curr_pop = next_gen_pop
    end_time = time.perf_counter()
    #print("end time",end_time)
    execution_time = end_time-start_time
    #run = run-1
    if(9.9<execution_time<=10.2):
        print("time is up baby")
        print("execution time",execution_time)
        run = False


# print("final best pop")
# print_board(curr_pop)
get_best_fit(curr_pop)
print("best score found",curr_pop[0])





