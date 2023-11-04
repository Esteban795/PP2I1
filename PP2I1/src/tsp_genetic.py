import numpy as np

import matplotlib.pyplot as plt
import tsplib95
from typing import Callable

#City_List,size_population=1000,elite_size=75,mutation_Rate=0.01,generation=1000,num_selected=500
class TSPSolver:

    def __init__(self,coords : list[tuple[float,float]], pop_size : int, dist_function : Callable,mutation_rate : float = 0.01,elite_size : int = 75) -> None:
        self.coords = coords
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.dist_function = dist_function
        self.elite_size = elite_size
    
    def generateInitPopulation(self) -> list[list[int]]:
        """
        Generates the initial population of the genetic algorithm
        Returns:
            npt.NDArray: Initial population 
        """
        return [np.random.permutation(len(self.coords)) for i in range(self.pop_size)]

    def getDistance(self, city_1 : tuple[int,int], city_2 : tuple[int,int]) -> float:
        """
        Calculates the distance between two cities
        Args:
            city_1 (tuple[int,int]): First city
            city_2 (tuple[int,int]): Second city
        Returns:
            float: Distance between the two cities
        """
        return self.dist_function(city_1,city_2)
    
    def getPopulationScore(self,population : list[list[int]]) -> list[float]:  
        """
        Calculates the fitness score for each individual in the population
        Args:
            population (list[list[int]]): Population to calculate the fitness scores of
        Returns:
            list[float]: Fitness scores of the population
        """
        return [self.getFitness(route) for route in population]
    
    def getFitness(self,route):
        """
        Calculates the fitness of a route
        Args:
            route : Route to calculate the fitness of
        Returns:
            float: Fitness of the route
        """
        fitness_score = 0
        for i in range(len(route)):
            j = (i + 1) % len(route)
            fitness_score += self.getDistance(self.coords[route[i]],self.coords[route[j]])
        return fitness_score
    
    def makeCrossover(self, parent_1 : list[int], parent_2 : list[int]) -> list[int]:
        """
        Makes a crossover between two parents
        Args:
            parent_1 : First parent
            parent_2 : Second parent
        Returns:
            list[int]: Child route
        """
        childP1 = [0 for i in range(len(parent_1))]
        geneA = int(np.random.random() * len(parent_1))
        geneB = int(np.random.random() * len(parent_1))
        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)
        for i in range(startGene, endGene):
            childP1.append(parent_1[i])
        childP2 = [item for item in parent_2 if item not in childP1]
        return childP1 + childP2

    #Centre Inverse Mutation (CIM)
    def applyCIM(self,route : list[int]) -> list[int]:
        """
        Applies the CIM (Centre Inverse Mutation) mutation to a route
        Args:
            route : Route to apply the mutation to
        Returns:
            list[int]: Route after the mutation
        """
        index = len(route) // 2
        first_half = route[:index][::-1]
        second_half = route[index:][::-1]
        return first_half + second_half
    
    def selectBestResults(self, population_ranked : list[int]) -> list[list[int]]:
        """
        Selects the best results from a ranked population
        Args:s
            population_ranked: Ranked population 
        Returns:
            list[list[int]]: Best results from the ranked population
        """
        return [population_ranked[i][0] for i in range(self.elite_size)]
    
    def sortElitistRoutes(self, population : list[list[int]]) -> list[list[int]]:
        """
        Sorts the population by elitism (best fitness score)
        Args:
            population : Population to sort
        Returns:
            list[(i,fitness_score)]: Sorted population
        """
        return sorted([(i,self.getFitness(population[i])) for i in range(len(population))],key=lambda x: x[1],reverse=False)
    
    def breedPopulation(self, mating_pool : list[list[int]]) -> list[list[int]]:
        """
        breeds the population together.
        Args:
            mating_pool : Mating pool
        """
        return [self.makeCrossover(mating_pool[i],mating_pool[i + 1]) for i in range(len(mating_pool) - 1)]

    def mutatePopulation(self,children : list[list[int]]) -> list[list[int]]:
        """
        mutate the population by applying the CIM mutation
        Args :
            children : children
        Returns : 
            list[list[int]] : a list of the mutated children
        """
        return [self.applyCIM(children[i]) for i in range(10)]

    def matingPool(self, population : list[list[int]], selection_results : list[int]) -> list[list[int]]:
        """
        Creates a mating pool from a population
        Args:
            population : Population to create the mating pool from
            selection_results : Selection results
        Returns:
            list[list[int]]: Mating pool
        """
        return [population[selection_results[i]] for i in range(len(selection_results))]

    def generateNextGeneration(self, population : list[list[int]]) -> list[list[int]]:
        """
        Generates the next generation
        Args:
            population : Population to generate the next generation from
        Returns:
            list[list[int]]: Next generation
        """
        population_ranked = self.sortElitistRoutes(population)
        selection_results = self.selectBestResults(population_ranked)
        mating_pool = self.matingPool(population,selection_results)
        children = self.breedPopulation(mating_pool)
        next_generation = self.mutatePopulation(children)
        del children[:10]
        children.extend(next_generation)
        return children

    def solve(self,n_generations : int) -> list[list[int]]:
        """
        Solves the TSP problem
        Args:
            n_generations (int): Number of generations to run the algorithm for
        Returns:
            list[list[int]]: Best route found by the algorithm
        """
        population = self.generateInitPopulation()
        for i in range(n_generations):
            pop = self.generateNextGeneration(population)
            population.extend(pop)
            del population[:self.elite_size]
            print("Generation=",i)         
        ranked = sorted(self.sortElitistRoutes(pop))[0]
        print("RANK_",ranked)
        print(f"Best Route :{population[ranked[0]]} ")
        print(f"best route distance {ranked[1]}")
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.show()
        return ranked, pop


cityList= [(33, 89), (9, 81), (40, 126), (80, 96), (120, 124), (127, 110), (93, 67), (89, 140), (186, 104), (136, 192), (131, 169), (179, 181), (120, 7), (184, 130), (111, 185), (120, 187), (110, 193), (1, 27), (68, 5), (194, 173), (139, 52), (97, 74), (198, 11), (164, 60), (45, 145)]

tsp = TSPSolver(cityList,1000,lambda x,y : np.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2))

res = tsp.solve(300)
print(res)