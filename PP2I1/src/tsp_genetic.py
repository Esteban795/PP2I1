import numpy as np
import matplotlib.pyplot as plt
from typing import Callable
import random


class TSPSolver:

    def __init__(self,coords : list[tuple[float,float]], pop_size : int, dist_function : Callable, mutation_rate : float = 0.01, elite_size = 75) -> None:
        self.coords = coords
        self.pop_size = pop_size
        self.dist_func = dist_function
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size

    def createGenesis(self) -> list[list[int]]:
        """
        Creates the first generation of routes randomly
        Args :
            None
        Returns :
            list : list of routes
        """
        return [np.random.permutation(len(self.coords)) for i in range(self.pop_size)]

    def getFitness(self,route : list[int]) -> float:
        """
        Calculates individual fitness for a route.
        Args :
            route : list of cities' numbers in a certain order
        Returns :
            float : fitness of the route
        """
        score = 0
        for i in range(len(route)):
            score += self.dist_func(self.coords[route[i]], self.coords[route[(i+1)%len(route)]])
        return score

    def makeCrossover(self,route1 : list[int],route2 : list[int]) -> list[int]:
        """
        Performs crossover between two routes.
        Args :
            route1 : list of cities' numbers in a certain order
            route2 : list of cities' numbers in a certain order
        Returns :
            list : list of cities' numbers in a certain order
        """
        gene1 = int(random.random() * len(route1))
        gene2 = int(random.random() * len(route1))
        start_gene = min(gene1,gene2)
        end_gene = max(gene1,gene2)
        child1 = [] * len(route1)
        for i in range(start_gene,end_gene):
            child1.append(route1[i])
        child2 = [item for item in route2 if item not in child1]
        return child1 + child2

    def applyMutation(self,route : list[int]) -> list[int]:
        """
        Mutates a route with a certain probability.
        It applies Centre Inversion Mutation.
        """
        if random.random() < self.mutation_rate:
            return route
        route_one = route[:len(route)//2][::-1]
        route_two = route[len(route) //2:][::-1]
        return route_one + route_two
        
    def selectFittest(self,pop_ranked : list[tuple[int,float]]) -> list[int]:
        """
        Selects the best routes from the population.
        Args :
            `pop_ranked` : list of tuples (route, fitness) sorted by fitness
        Returns :
            list : list of the first `elite_size` routes
        """
        return [pop_ranked[i][0] for i in range(self.elite_size)]

    def getElitistRoutes(self,population : list[list[int]]) -> list[tuple[int,float]]:
        """
        Sorts the population by fitness.
        Args :
            population : list of routes
        Returns :
            list : list of tuples (route_index, fitness) sorted by fitness
        """
        return sorted([(i,self.getFitness(population[i])) for i in range(len(population))],key = lambda x: x[1],reverse=False)
    
    def breedPopulation(self,mating_pool : list[list[int]]) -> list[list[int]]:
        """
        Breeds the population with itself. Each member reproduces with the following one.
        Args : 
            mating_pool : list of routes
        Returns :
            list : list of children
        """
        return [self.makeCrossover(mating_pool[i],mating_pool[i + 1]) for i in range(len(mating_pool) - 1)] 

    def mutatePopulation(self,children : list[list[int]]) -> list[list[int]]:
        """
        Mutates the first 10 children of the population.
        Args :
            children : list of routes
        Returns :
            list : list of mutated children
        """
        return [self.applyMutation(children[i]) for i in range(10)]

    def getMatingPool(self,population : list[list[int]], selection_results : list[list[int]]) -> list[list[int]]:
        """
        Selects the routes from the population according to the selection results (which mean they are currently
        the fittest routes).
        """
        return [population[selection_results[i]] for i in range(len(selection_results))]

    def getNextGeneration(self,current_population : list[list[int]]) -> list[list[int]]:
        """
        Applies the whole genetic algorithm to the current population.
        Args :
            current_population : list of routes
        Returns :   
            list : list of the next generation's routes
        """
        population_rank = self.getElitistRoutes(current_population)
        selection_result = self.selectFittest(population_rank)
        mating_pool = self.getMatingPool(current_population,selection_result)
        children = self.breedPopulation(mating_pool)
        next_generation = self.mutatePopulation(children)
        del children[:10]
        children.extend(next_generation)
        return children

    def solve(self,n_generations : int) -> tuple[list[int],float]:
        """
        Algorithm's main method.
        Args :
            n_generations : number of generations to be created
        Returns :
            tuple : (route, fitness) of the best route
        """
        pop = []
        population= self.createGenesis()
        for i in range(n_generations):
            pop = self.getNextGeneration(population)
            population.extend(pop)
            del population[:74]           
            print("Generation=",i)
        rank_= sorted(self.getElitistRoutes(pop))[0]
        return population[rank_[0]],rank_[1]