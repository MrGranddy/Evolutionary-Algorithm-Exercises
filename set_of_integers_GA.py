from random import random, uniform, randrange, shuffle

# The options right now are more or less optimum.

chromosome_length = 30
population_size = 100
mutation_rate = 0.04
mutation_percentage = 0.75
crossover_rate = 0.9
number_of_elits = 20
number_of_generations = 40


def find_i_maxs(array, i):
    """ Description:
            This function takes an array and returns global max to 'i'th max.

        Example:
            a = [10, 23, 242, 23, 12] so if I call find_i_maxs(a, 3)
            it will return the array [242, 23, 23] notice that this
            array is sorted from max to min.

        Args:
            array (list): The list what you want its max values.

            i (int): The number of maxs you want.

        Returns:
            maxs (list): The list containing maxs.
    """
    maxs = []
    arr = list(array)
    for j in range(i):
        maxs.append(max(arr))
        del arr[arr.index(maxs[j])]
    return maxs


def find_i_mins(array, i):
    """ Description:
            This function takes an array and returns global min to 'i'th min.

        Example:
            a = [10, 23, 242, 23, 12] so if I call find_i_mins(a, 3)
            it will return the array [10, 12, 23] notice that this
            array is sorted from min to max.

        Args:
            array (list): The list what you want its min values.

            i (int): The number of mins you want.

        Returns:
            mins (list): The list containing mins.
    """
    mins = []
    arr = list(array)
    for j in range(i):
        mins.append(min(arr))
        del arr[arr.index(mins[j])]
    return mins


def bit_to_int(bit_string):
    """ Description:
            This function takes a bit_string. In this form the bit_string
            must be the one third size of the chromosomes because each
            chromosome has 3 numbers in it. Then the function converts
            that part to a number.

        Example:
            For example in this default form, my chromosomes are 30 bits long
            so the numbers are 10 bits long, this means they represent 1024
            numbers. The function converts the 1000110001 string to
            512 + 32 + 16 + 1 = 561 then extracts 511 = 50. It does that
            because in this program I want to store numbers like
            -512 < x <= 512 rather than 0 <= x < 1024

            bit_to_int('1111111111') = 512
            bit_to_int('1101001111') = 335

        Args:
            bit_string (string): The bit string which will be converted
            to integer.

        Returns:
            num (int): The number equivalent to the bit_string.
    """
    num = 0
    for i in range(0, chromosome_length // 3):
        if bit_string[i] is '0':
            num *= 2
        else:
            num = num * 2 + 1
    num = num - 511
    return num


def create_random_generation():
    """ Description:
            This function creates a random generation.

        Example:
            population = create_random_generation()
            Now there are random individuals in list population.
            All the sizes are decided from the options on the top.

        Args:
            No arguments.

        Returns:
            generation (list): The list containing random individuals.
    """
    generation = []
    for i in range(population_size):
        ind = ''
        for j in range(chromosome_length):
            rand = random()
            if rand < 0.5:
                ind += '0'
            else:
                ind += '1'
        generation.append(ind)
    return generation


def fitness(individual):
    """ Description:
            This function calculates the fitness value for the given
            individual. Notice this for this GA example, the higher the
            fitness is the worst is the individual.
            The fitness is calculated by taking squares of the 3 numbers in the
            individual than summing them.

        Example:
            fitness('100000000010000000001000000000')
            = 512 ** 2 + 512 ** 2 + 512 ** 2 = 786432

        Args:
            individual (string) = The individual which is given for its
            fitness to be calculated

        Returns:
            ans (int) = The fitness value of the individual.
    """
    num1 = bit_to_int(individual[0:10])
    num2 = bit_to_int(individual[10:20])
    num3 = bit_to_int(individual[20:30])
    ans = num1 ** 2 + num2 ** 2 + num3 ** 2

    # This exception is here because later when calculating selection rate 
    # it would cause a division by zero error.
    if ans is 0:
        return 1

    return ans


sum_of_fitness = 0
def sum_fitness(population):
    """ Description:
            This function sums the fitness values for the given population.
            Then assigns the value to the variable above, sum_of_fitness.
        Example:
            sum_fitness(population)
            print(sum_of_fitness)
            $ 1241415322 --> output
        Args:
            population (list): The list containing individuals which
            I want to sum their fitness values.

        Returns:
            No returns.
    """
    global sum_of_fitness
    for ind in population:
        sum_of_fitness += fitness(ind)


def selection_rate(individual):
    """ Description:
            This function calculates the probability for an individual to
            be selected to the mating_pool.
            As you see the bigger your fitness value is the less likely to
            be selected you get.

        Example:
            selection_rate('111111111111111111111111111111') = 0.1231e-6

        Args:
            individual (string) = The individual which its selection rate
            is to be calculated.

        Returns:
            Returns the calculated selection rate
            -> (sum_of_fitness / fitness(individual))
    """
    fit_ind = fitness(individual)
    return sum_of_fitness / fitness(individual)


def crossover(population):
    """ Description:
            This funtion does the crossover operation on the given population.
            Basically it takes pairs of individuals then make them produce
            offsprings.

        Example:
            selection_rate('111111111111111111111111111111') = 0.1231e-6

        Args:
            individual (string) = The individual which its selection rate
            is to be calculated.

        Returns:
            Returns the calculated selection rate
            -> (sum_of_fitness / fitness(individual))
    """
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


def mutate(population):
    inds_to_mutate = int(population_size * mutation_percentage)
    new_population = []
    for mutated_inds in range(inds_to_mutate):
        rand_index = randrange(0, len(population))
        new_ind = ''
        for ch in population[rand_index]:
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
        mutated_inds += 1
        new_population.append(new_ind)
        del population[rand_index]
    for ind in population:
        new_population.append(ind)
    return new_population


def main():
    population = create_random_generation()
    for i in range(number_of_generations):
        sum_fitness(population)
        population = crossover(population)
        population = mutate(population)
        best = ''
        best_fit = 786440
        for ind in population:
            if fitness(ind) < best_fit:
                best_fit = fitness(ind)
                best = ind
        print(bit_to_int(best[0:10]),
            bit_to_int(best[10:20]),
            bit_to_int(best[20:30]),
            '-> Generation ' + str(i + 1) + ' the best.')


if __name__ == '__main__':
    main()