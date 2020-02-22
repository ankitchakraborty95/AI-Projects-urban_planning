import random
import numpy
import copy
import time
from common_functions import *

# Read a text file and generate a board representation as a 2D array
######################################################################################################################################################################
pop_size = 400
elitism_factor = 10
culling_factor = 3
input_board = read_File(r"/home/ankit/git/AI/assignment_1/urban/urban_1.txt")
print_board(input_board)
initial_pop = gen_population(input_board,pop_size)
curr_pop = copy.deepcopy(initial_pop)
print("initial pop")
print_board(initial_pop)

#############
start_time = time.perf_counter()

run =True
while(run):
    elitism_pop = get_parents(curr_pop,elitism_factor)
    next_gen_pop = []
    #######elitism pop############
    # print("elitism pop")
    # print_board(elitism_pop)
    for x in elitism_pop:
        next_gen_pop.append(x)
    # print("next gen")
    # print_board(next_gen_pop)
    #########pop after culling#########33
    pop_after_culling = culling_pop(curr_pop,culling_factor)
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





