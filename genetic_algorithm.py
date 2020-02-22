from common_functions import *
pop_size = 400
elitism_factor = 10
culling_factor = 3
time_limit = 10.0

# main genetic algorithm
def genetic_algorithm(ref_layout):
    start_time = time.perf_counter()
    input_board = ref_layout
    initial_pop = gen_population(input_board, pop_size)
    curr_pop = copy.deepcopy(initial_pop)

    run = True
    while (run):
        elitism_pop = get_parents(curr_pop, elitism_factor)
        next_gen_pop = []
        #######elitism pop############
        for x in elitism_pop:
            next_gen_pop.append(x)
        #########pop after culling#########33
        pop_after_culling = culling_pop(curr_pop, culling_factor)
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
        curr_pop = next_gen_pop
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        if (time_limit-0.1 < execution_time <= time_limit+0.1):
            print("execution time", execution_time)
            run = False

    get_best_fit(curr_pop)
    print("best score found")
    for x in curr_pop[0][0]:
        print(x)
    print(curr_pop[0][1])