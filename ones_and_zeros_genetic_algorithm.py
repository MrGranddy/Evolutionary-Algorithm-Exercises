from random import random, uniform, randrange

population_size = 100
size_of_string = 20
crossover_rate = 1.0
mutation_rate = 0.05
num_of_generations = 100
max_individual = ''
max_fitness = 0

def fitness(individual):
	global max_individual
	global max_fitness
	point = 0
	for ch in range(0, size_of_string // 2):
		if individual[ch] is '1':
			point += 1
	for ch in range(size_of_string // 2, size_of_string):
		if individual[ch] is '0':
			point += 1
	if not max_individual:
		max_individual = individual
		max_fitness = point
	if max_fitness < point:
		max_individual = individual
		max_fitness = point
	return point

def selection_rate(population, individual):
	total_fitness = 0
	for ind in population:
		total_fitness += fitness(ind)
	return fitness(individual) / total_fitness

def crossover(population):
	mating_pool = []
	new_population = []
	rates = []
	for individual in population:
		rates.append(selection_rate(population ,individual))
	sum_of_rates = sum(rates)
	for i in range(population_size):
		rand = uniform(0, sum_of_rates)
		rate_sum = 0
		for index, rate in enumerate(rates):
			rate_sum += rate
			if rand < rate_sum:
				mating_pool.append(population[index])
				break
	while mating_pool:
		mating_pool_len = len(mating_pool)
		first_index = randrange(mating_pool_len)
		temp = randrange(mating_pool_len)
		while temp is first_index:
			temp = randrange(mating_pool_len)
		second_index = temp
		cut_index = randrange(size_of_string) + 1
		parts = []
		parts.append(mating_pool[first_index][0:cut_index])
		parts.append(mating_pool[second_index][0:cut_index])
		parts.append(mating_pool[first_index][cut_index:size_of_string])
		parts.append(mating_pool[second_index][cut_index:size_of_string])
		new_population.append(parts[0] + parts[3])
		new_population.append(parts[1] + parts[2])
		if first_index > second_index:
			del mating_pool[first_index]
			del mating_pool[second_index]
		else:
			del mating_pool[second_index]
			del mating_pool[first_index]

	return new_population

def mutate(population):
	for individual in population:
		new_individual = ''
		for gene in individual:
			if mutation_rate > random():
				if gene is '1':
					new_individual += '0'
				else:
					new_individual += '1'
			else:
				new_individual += gene

	

def main():
	global max_individual
	population = []
	for p in range(population_size):
		temp = ''
		for i in range(size_of_string):
			rand = random()
			if rand < 0.5:
				temp += '1'
			else:
				temp += '0'
		population.append(temp)
	for i in range(num_of_generations):
		population = crossover(population)
		mutate(population)
		print('Max Individual -> ' + max_individual)

if __name__ == '__main__':
	main()
