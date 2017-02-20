from random import random, uniform, randrange, shuffle, choice

# The options right now are more or less optimum.

knapsack_items = [
(382745, 825594),
(799601, 1677009),
(909247, 1676628),
(729069, 1523970),
(467902, 943972),
(44328, 97426),
(34610, 69666),
(698150, 1296457),
(823460, 1679693),
(903959, 1902996),
(853665, 1844992),
(551830, 1049289),
(610856, 1252836),
(670702, 1319836),
(488960, 953277),
(951111, 2067538),
(323046, 675367),
(446298, 853655),
(931161, 1826027),
(31385, 65731),
(496951, 901489),
(264724, 577243),
(224916, 466257),
(169684, 369261)
]
# First Weight, Second Value
knapsack_capacity = 6404180

global_max = ['', 0]

population = []

penalty = 100
chromosome_length = 24
population_size = 100
mutation_rate = 0.041
mutation_percentage = 0.6
crossover_rate = 0.8
number_of_elits = 10
number_of_generations = 5000


def find_i_maxs(array, i):
    maxs = []
    arr = list(array)
    for j in range(i):
        maxs.append(max(arr))
        del arr[arr.index(maxs[j])]
    return maxs


def find_i_mins(array, i):
    mins = []
    arr = list(array)
    for j in range(i):
        mins.append(min(arr))
        del arr[arr.index(mins[j])]
    return mins


def create_random_individual():
    ind = ''
    for i in range(chromosome_length):
        rand = random()
        if rand < 0.5:
            ind += '0'
        else:
            ind += '1'
    return ind


def create_random_generation():
    generation = []
    for i in range(population_size):
        ind = create_random_individual()
        generation.append(ind)
    return generation


def fitness(individual):
    global knapsack_items, knapsack_capacity, population
    while True:
        weight = 0 
        value = 0
        for index in range(chromosome_length):
            if individual[index] == '1':
                weight += knapsack_items[index][0]
                value += knapsack_items[index][1]
        if weight > knapsack_capacity:
            return penalty
            # I tried some solutions to this problem
            # 1 - As you see giving a penalty point so low they don't survive
            # 2 - Generating a random individual
            # 3 - Assigning the global max individual
            # 4 - Mutating then assigning the global max individual
            # 5 - Assigning a random individual from population
            # 6 - Assigning a mutated random individual from population
            # Among those I didn't make a statictical graph but a completely
            # random individual seemed fine. I got good results with it and
            # also it was not allowing individuals that don't satisfy the
            # constraints.
        else:
            if value > global_max[1]:
                global_max[0] = individual
                global_max[1] = value
            return value



sum_of_fitness = 0
def sum_fitness(population):
    global sum_of_fitness
    for ind in population:
        sum_of_fitness += fitness(ind)


def selection_rate(individual):
    fit_ind = fitness(individual)
    return fitness(individual) / sum_of_fitness


def crossover(population):
    mating_pool = []
    new_population = []
    selection_rates = []
    elits = []
    for ind in population:
        selection_rates.append(selection_rate(ind))
    best_rates = find_i_maxs(selection_rates, number_of_elits)
    for rate in best_rates:
        index = selection_rates.index(rate)
        elits.append(population[index])
    for elit in elits:
        mating_pool.append(elit)
    worst_rates = find_i_mins(selection_rates, number_of_elits)
    for rate in worst_rates:
        index = selection_rates.index(rate)
        del selection_rates[index]
        del population[index]
    sum_of_rates = sum(selection_rates)
    for i in range(population_size - number_of_elits):
        rand = uniform(0, sum_of_rates)
        rate_sum = 0
        for index, rate in enumerate(selection_rates):
            rate_sum += rate
            if rand < rate_sum:
                mating_pool.append(population[index])
                break
    while mating_pool:
        first_index = randrange(0, len(mating_pool))
        second_index = randrange(0, len(mating_pool))
        while first_index is second_index:
            second_index = randrange(0, len(mating_pool))
        rand = random()
        if rand < crossover_rate:
            rand = randrange(0, chromosome_length + 1)
            parts = []
            parts.append(mating_pool[first_index][0:rand])
            parts.append(mating_pool[first_index][rand:chromosome_length])
            parts.append(mating_pool[second_index][0:rand])
            parts.append(mating_pool[second_index][rand:chromosome_length])
            new_population.append(parts[0] + parts[3])
            new_population.append(parts[1] + parts[2])
        else:
            new_population.append(mating_pool[first_index])
            new_population.append(mating_pool[second_index])

        if first_index > second_index:
            del mating_pool[first_index]
            del mating_pool[second_index]
        elif second_index > first_index:
            del mating_pool[second_index]
            del mating_pool[first_index]
    shuffle(new_population)
    return new_population


def mutate_individual(individual):
    new_ind = ''
    for ch in individual:
        rand = random()
        if rand < mutation_rate:
            if ch is '0':
                new_ind += '1'
            else:
                new_ind += '0'
        else:
            if ch is '0':
                new_ind += '0'
            else:
                new_ind += '1'
    return new_ind


def mutate(population):
    inds_to_mutate = int(population_size * mutation_percentage)
    new_population = []
    for mutated_inds in range(inds_to_mutate):
        rand_index = randrange(0, len(population))
        new_ind = mutate_individual(population[rand_index])           
        mutated_inds += 1
        new_population.append(new_ind)
        del population[rand_index]
    for ind in population:
        new_population.append(ind)
    shuffle(new_population)
    return new_population


def main():
    global population
    population = create_random_generation()
    for i in range(number_of_generations):
        sum_fitness(population)
        population = crossover(population)
        population = mutate(population)
        best = ''
        best_fit = 0
        for ind in population:
            if fitness(ind) > best_fit:
                best_fit = fitness(ind)
                best = ind
        print(best, '--> Best of generation ' + str(i + 1))
    print('Global max ->', global_max[0])


if __name__ == '__main__':
    main()