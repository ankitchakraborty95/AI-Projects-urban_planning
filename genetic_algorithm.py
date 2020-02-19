from common_functions import *
pop_size = 100
parent_grp_size = 10

def genetic_algorithm(ref_layout):
    population = gen_population(ref_layout)
    parents = get_parents(population)
    for x in parents:
        for c in x[0]:
            print(c)
        print(x[1])
    pass

def gen_population(ref_layout):
    population = []
    for x in range(0, pop_size):
        new_member = gen_rand_solution(ref_layout[0], ref_layout[1], ref_layout[2], ref_layout[3])
        member_score = score_solution(ref_layout[0], new_member)
        population.append((new_member, member_score))
    return population

def get_score(brd):
    return brd[1]

def get_best_fit(pop):
    pop.sort(key = get_score, reverse=True)
    return pop

def get_worst_fit(pop):
    pop.sort(key=get_score)
    return pop

def get_parents(pop):
    best_sort = get_best_fit([member[:] for member in pop])
    parents = []
    for top in range(0, parent_grp_size):
        parents.append(best_sort[top])
    return parents
