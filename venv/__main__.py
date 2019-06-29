"""
GA Knapsack algorithm.
"""

# ----- Dependencies

from random import random

# One-linner for randomly choose a element in an array
# This one-linner is fastest than random.choice(x).
choice = lambda x: x[int(random() * len(x))]

# ----- Runtime configuration (edit at your convenience)

# Enter here the chance for an individual to mutate (range 0-1)
CHANCE_TO_MUTATE = 0.1

# Enter here the percent of top-grated individuals to be retained for the next generation (range 0-1)
GRADED_RETAIN_PERCENT = 0.2

# Enter here the chance for a non top-grated individual to be retained for the next generation (range 0-1)
CHANCE_RETAIN_NONGRATED = 0.05

# Number of individual in the population
POPULATION_COUNT = 100

# Maximum number of generation before stopping the script
GENERATION_COUNT_MAX = 10000

# ----- Do not touch anything after this line

# Number of top-grated individuals to be retained for the next generation
GRADED_INDIVIDUAL_RETAIN_COUNT = int(POPULATION_COUNT * GRADED_RETAIN_PERCENT)

# Array containing the names of all the objects.
NAMES = ['cat dish','laptop','Boxed Set of Knuth','assorted snacks','catnip','clothing','diamonds']

# Array containing the values of all the objects (same order as NAMES).
VALUES = [4, 40, 30, 6, 10, 7,70]

# Array containing the weights of all the objects (same order as NAMES).
WEIGHTS = [1, 4, 8, 2, 1, 5, 2]

# Heavy genetic constraint to avoid the individual to "compensate" heaviness penalty with value of heavy configuration
MAX_VAL = sum(VALUES)

# Total capacity of backpack
CAPACITY = 8

#
NUMBER_OF_OBJECTS = len(NAMES)

#
MIDDLE_LENGTH_OF_GENE_SEQ = NUMBER_OF_OBJECTS // 2

#

# ----- Genetic Algorithm code
# Note: An individual is simply an array of 1 & 0 (item picked or not picked).
# Because an individual is just an array of gens, a gene is either 1 or 0 in this case.
# And a population is nothing more than an array of individuals.

def get_random_digit():
    """ Return either 1 or 0 at random. """
    return choice([0, 1])


def get_random_individual():
    """ Create a new random individual. """
    return [get_random_digit() for _ in range(NUMBER_OF_OBJECTS)]


def get_random_population():
    """ Create a new random population, made of `POPULATION_COUNT` individual (array of arrays). """
    return [get_random_individual() for _ in range(POPULATION_COUNT)]


def get_individual_fitness(individual):
    """ Compute the fitness of the given individual. """
    """ Initialisation fitness. """
    fitness = 0
    """ Init stolen value. """
    total_value = 0
    """ Init weight stolen. """
    total_weight = 0
    """ Loop through the tuples to compute fitness of the given individual. """
    for gene, value, weight in zip(individual, VALUES, WEIGHTS):
        total_weight = total_weight + gene*weight
        total_value = total_value + gene*value
    fitness += total_value
    if total_weight > CAPACITY:
        fitness -= MAX_VAL
    return fitness


def average_population_grade(population):
    """ Return the average fitness of all individual in the population. """
    total = 0
    for individual in population:
        total += get_individual_fitness(individual)
    return total / POPULATION_COUNT


def grade_population(population):
    """ Grade the population. Return a list of tuples (individual, fitness) sorted from most graded to less graded. """
    graded_pop = []
    for individual in population:
        graded_pop.append((individual, get_individual_fitness(individual)))
    return sorted(graded_pop, key=lambda x: x[1], reverse=True)

def get_most_freq_individual_in_population(population):
    max_freq = 0
    most_freq_individual = population[0]
    for individual in population:
        curr_freq = population.count(individual)
        if curr_freq > max_freq:
            max_freq = curr_freq
            most_freq_individual = individual
    return most_freq_individual

def parse_individual(individual):
    """ Convert binary list to a tuple. """
    total_weight = 0
    total_value = 0
    objects_taken = []
    for gene, value, weight, name in zip(individual, VALUES, WEIGHTS, NAMES):
        if gene == 1:
            total_weight += weight
            total_value += value
            objects_taken.append(name)
    return (objects_taken, total_weight, total_value)

def evolve_population(population):
    """ Make the given population evolving to his next generation. """

    # Get individual sorted by grade (top first), the average grade and the solution (if any)
    raw_graded_population = grade_population(population)
    average_grade = 0
    graded_population = []
    for individual, fitness in raw_graded_population:
        average_grade += fitness
        graded_population.append(individual)
    average_grade /= POPULATION_COUNT

        # Filter the top graded individuals
    parents = graded_population[:GRADED_INDIVIDUAL_RETAIN_COUNT]

    # Randomly add other individuals to promote genetic diversity
    for individual in graded_population[GRADED_INDIVIDUAL_RETAIN_COUNT:]:
        if random() < CHANCE_RETAIN_NONGRATED:
            parents.append(individual)

    # Mutate some individuals
    for individual in parents:
        if random() < CHANCE_TO_MUTATE:
            place_to_modify = int(random() * NUMBER_OF_OBJECTS)
            individual[place_to_modify] = get_random_digit()

    # Crossover parents to create children
    parents_len = len(parents)
    desired_len = POPULATION_COUNT - parents_len
    children = []
    while len(children) < desired_len:
        father = choice(parents)
        mother = choice(parents)
        child = father[:MIDDLE_LENGTH_OF_GENE_SEQ] + mother[MIDDLE_LENGTH_OF_GENE_SEQ:]
        children.append(child)

    # The next generation is ready
    parents.extend(children)
    return parents, average_grade


# ----- Runtime code

def main():
    """ Main function. """
    print(choice([0, 1]))
    # Create a population and compute starting grade
    population = get_random_population()
    average_grade = average_population_grade(population)
    print('Starting grade: %.2f' % average_grade)

    # Make the population evolve
    i = 0
    log_avg = []
    while i < GENERATION_COUNT_MAX:
        population, average_grade = evolve_population(population)
        if i %250 == 0:
            print('Current grade: %.2f' % average_grade, '(%d generation)' % i)
        if i % 30 == 0:
            log_avg.append(average_grade)
        i += 1

    # Print the final stats
    average_grade = average_population_grade(population)
    print('Final grade: %.2f' % average_grade)


    print('- Last population was:')
    for number, individual in enumerate(population):
        print(number,individual)
    print('The most representative individual in last population was:')

    # Print final solution
    most_freq_individual = get_most_freq_individual_in_population(population)
    print(most_freq_individual)
    most_freq_individual = parse_individual(most_freq_individual)
    print('The final solution is:')
    print(most_freq_individual)

if __name__ == '__main__':
    main()
