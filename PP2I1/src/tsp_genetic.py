import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
import tsplib95

class TSPSolver:
    """Class to instantiate a TSP solver, through a genetic algorithm.
    It allows you to use your own distance function, choose the population size and the mutation rate.
    """
    def __init__(self,coordinates_list : list[tuple[float,float]] ,n_population : int, mutation_rate : float,dist_function : callable):
        self.n_cities = len(coordinates_list)
        self.n_population = n_population
        self.mutation_rate = mutation_rate
        self.coordinates_list = coordinates_list
        self.dist_function = dist_function
        self.names_list = np.array([i for i in range(1,self.n_cities + 1)])
        self.cities_dict = {x:y for x,y in zip(self.names_list,coordinates_list)}
        
    def computeDistance(self,city_a : int, city_b : int) -> float:
        """Computes the distance between two cities
        Args:
            city_a (int): City A
            city_b (int): City B
        Returns:
            float: Distance between city A and city B
        """
        return self.dist_function(self.cities_dict[city_a], self.cities_dict[city_b])

    def genesis(self, cities_list : list[int]) -> npt.NDArray:
        """
        Generates the initial population of the genetic algorithm
        Args:
            cities_list : List of cities to be visited
        Returns:
            npt.NDArray: Initial population 
        """
        return np.array([cities_list[np.random.permutation(self.n_cities)] for i in range(self.n_population)])
    
    def evalPermutationFitness(self, city_list : npt.ArrayLike) -> float:
        """
        Evaluates the fitness of a permutation of cities
        Args:
            city_list : List of cities to be visited
        Returns:
            float: Fitness of the permutation
        """
        total = 0
        for i in range(self.n_cities - 1):
            a = city_list[i]
            b = city_list[i + 1]
            total += self.computeDistance(a,b)
        return total
    
    def getAllFitness(self, population_set : npt.NDArray) -> npt.NDArray:
        """
        Gets the fitness of all the permutations in the population
        Args:
            population_set : Population of permutations
        Returns:
            fitness_list : Fitness of all the permutations
        """
        fitness_list = np.zeros(self.n_population)
        for i in range(self.n_population):
            fitness_list[i] = self.evalPermutationFitness(population_set[i])
        return fitness_list
    
    def selectProgenitor(self, population_set : npt.NDArray, fitness_list : npt.ArrayLike) -> npt.ArrayLike:
        """
        Selects two progenitors from the population that best minimize the sum of the distances between the cities
        Args:
            population_set : Population of permutations
            fitness_list : Fitness of all the permutations
        Returns:
            progenitor_list : List of progenitors
        """
        total_fit = fitness_list.sum()
        prob_list = fitness_list/total_fit
        # A progenitor can mate with itself, so we can't use a permutation (duplicates not allowed)
        progenitor_list_a = np.random.choice(range(len(population_set)), len(population_set),p=prob_list, replace=True)
        progenitor_list_b = np.random.choice(range(len(population_set)), len(population_set),p=prob_list, replace=True)
        progenitor_list_a = population_set[progenitor_list_a]
        progenitor_list_b = population_set[progenitor_list_b]
        return np.array([progenitor_list_a,progenitor_list_b])

    def mateProgenitors(self, prog_a : npt.ArrayLike, prog_b : npt.ArrayLike) -> npt.ArrayLike:
        """
        Mates two progenitors, generating an offspring
        Args:
            prog_a : Progenitor A
            prog_b : Progenitor B
        Returns:
            offspring : offspring of the two progenitors
        """
        offspring = prog_a[0:5]
        for city in prog_b:
            if not city in offspring:
                offspring = np.concatenate((offspring,[city]))
        return offspring

    def matePopulation(self, progenitor_list : npt.ArrayLike) -> npt.NDArray:
        """
        Mates the population of progenitors, generating a new population
        Args:
            progenitor_list : List of progenitors
        Returns:
            new_population_set : newly generated population
        """
        new_population_set = []
        for i in range(progenitor_list.shape[1]):
            prog_a, prog_b = progenitor_list[0][i], progenitor_list[1][i]
            offspring = self.mateProgenitors(prog_a, prog_b)
            new_population_set.append(offspring)
        return new_population_set
    
    def mutateOffspring(self, offspring : npt.ArrayLike) -> npt.ArrayLike:
        """
        Randomly mutates a certain number of cities in the offspring depending on the mutation rate.
        Args:
            offspring : Offspring to be mutated
        Returns:
            offspring : Mutated offspring
        """
        for i in range(int(self.n_cities * self.mutation_rate)):
            a = np.random.randint(0,self.n_cities)
            b = np.random.randint(0,self.n_cities)
            offspring[a], offspring[b] = offspring[b], offspring[a]
        return offspring
    
    def mutatePopulation(self, new_population_set : npt.ArrayLike) -> npt.NDArray:
        """
        Randomly mutates the population set.
        Args:
            new_population_set : Population to be mutated
        Returns:
            mutated_pop : Mutated population
        """
        mutated_pop = []
        for offspring in new_population_set:
            mutated_pop.append(self.mutateOffspring(offspring))
        return mutated_pop
    
    def solve(self,n_generation : int) -> list[int,float,npt.ArrayLike]:
        """
        TSP solver using a genetic algorithm approach.
        Args:
            n_generation : Number of generations to be run (the more the better for precision, but the slower the algorithm)
        Returns:
            best_solution : Best solution found by the algorithm
        """
        #initialization phase
        population_set = self.genesis(self.names_list)
        fitness_list = self.getAllFitness(population_set)
        progenitor_list = self.selectProgenitor(population_set,fitness_list)
        new_population_set = self.matePopulation(progenitor_list)
        mutated_pop = self.mutatePopulation(new_population_set)
        best_solution = [-1,np.inf,np.array([])]
        for i in range(n_generation - 1):
            fitness_list = self.getAllFitness(population_set)
            if fitness_list.min() < best_solution[1]:
                best_solution[0] = i
                best_solution[1] = fitness_list.min()
                best_solution[2] = np.array(mutated_pop)[fitness_list.min() == fitness_list]
            progenitor_list = self.selectProgenitor(population_set,fitness_list)
            new_population_set = self.matePopulation(progenitor_list)
            mutated_pop = self.mutatePopulation(new_population_set)
        return best_solution

def distance_function(city_1 : list[int,int],city_2 : list[int,int]) -> float:
    return ((city_1[0] - city_2[0])**2 + (city_1[1] - city_2[1])**2)**0.5

data = tsplib95.load('berlin52.tsp')
cities = list(data.get_nodes())
coords = list(data.node_coords.values())

tsp = TSPSolver(coords,1000,0.3,distance_function)

xs = [coord[0] for coord in coords]
ys = [coord[1] for coord in coords]
plt.scatter(xs,ys)

res = tsp.solve(1000)
arr = res[2]

xs = [coords[i-1][0] for i in arr[0]]
ys = [coords[i-1][1] for i in arr[0]]
plt.plot(xs,ys)

print(res)
plt.show()