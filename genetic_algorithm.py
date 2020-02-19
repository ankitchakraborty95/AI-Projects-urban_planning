from common_functions import *
pop_size = 100
parent_grp_size = 10

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
    for top in range(0, parent_grp_size):
        parents.append(best_sort[top])
    return parents

# Creates children based off 2 parents
# Simply cuts the 2D array in half between rows, and stitchs the other half on
def create_children(reference, mom, dad):
    height = len(mom)
    divide = int(height/2)
    mom_clone = [momgene[:] for momgene in mom]
    dad_clone = [dadgene[:] for dadgene in dad]
    child1 = []
    child2 = []
    for x in range(0, divide):
        child1.append(mom_clone[x])
        child2.append(dad_clone[x])
    for y in range(divide, height):
        child1.append(dad_clone[y])
        child2.append(mom_clone[y])
    child1_score = score_solution(reference, child1)
    child2_score = score_solution(reference, child2)
    return [(child1, child1_score), (child2, child2_score)]
