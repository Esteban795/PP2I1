import tsplib95 #"@author of external package: Michael Ritter. Need to pip install this package"
import random
import math
import time
import matplotlib.pyplot as plt
from typing import Callable

class TSPSolver:

    def __init__(self,coords : list[list[float]],dist_func : Callable) -> None:
        self.dist_func = dist_func
        self.coords = coords
        

    def getRouteCost(self,route : list[int]) -> float:
        """
        Calculates cost/fitness for the solution/route.
        Args :
            route : list of integers representing the order of cities to visit
        Returns :
            fitness : float representing the fitness of the solution
        """
        distance = 0
        for i in range(len(route)):
            distance += self.dist_func(self.coords[route[i]], self.coords[route[(i + 1) % len(route)]])
        fitness = 1 / distance
        return fitness
        
    def getNeighbors(self,route : list[int]) -> list[int]: 
        """
        Returns neighbor of your solution.
        Args :
            route : list of integers representing the order of cities to visit
        Returns :
            neighbor : list of integers representing the order of cities to visit, with a spcific change applied depending on a random chosen function
        """
        neighbor = route[::]
        func = random.randint(0,3) #randomly selects a function to apply to the route to get a neighbor
        match func:
            case 0:
                self.inverseSubroute(neighbor)
            case 1:
                self.insertNode(neighbor)
            case 2:
                self.swapNodes(neighbor)
            case 3:
                self.swapRoutes(neighbor)
        return neighbor

    def inverseSubroute(self,route: list[int]) -> list[int]:
        """
        Inverse a subroute from node i to j. 
        Args :
            route : list of integers representing the order of cities to visit
        Returns :
            route : list of integers representing the order of cities to visit, with the modified subroute
        Example : 
        route = [1,2,3,4,5,6]
        Let's say node 2 and 5 are selected.
        The function returns [1,4,3,2,5,6]
        """
        node_one = random.choice(route)
        node_two = random.choice([x for x in route if x != node_one]) #selects another random index that is not the same as node_one
        mini = min(node_one,node_two)
        maxi = max(node_one,node_two)
        route[mini:maxi] = route[mini:maxi][::-1] #reverse the subroute from mini to maxi
        return route

    def insertNode(self,route : list[int]) -> list[int]:
        """
        Randomly selects two nodes, i and j, and inserts node j into the route after node i.
        Args :
            route : list of integers representing the order of cities to visit
        Returns :
            route : list of integers representing the order of cities to visit, with the modified subroute

        """
        node_j = random.choice(route)
        route.remove(node_j) #to make sure we avoid selecting j again
        node_i = random.choice(route)
        index = route.index(node_i)
        route.insert(index, node_j)
        return route

    def swapNodes(self,route : list[int]) -> list[int]:
        """
        Randomly selects two nodes, i and j, and swaps their positions in the route.
        Args :
            route : list of integers representing the order of cities to visit
        Returns :
            route : new list of integers representing the order of cities to visit
        """
        pos_one = random.randint(0, len(route) - 1)
        pos_two = random.randint(0, len(route) - 1)
        route[pos_one], route[pos_two] = route[pos_two], route[pos_one]
        return route

    def swapRoutes(self,route : list[int]) -> list[int]:
        """
        Randomly selects two nodes, i and j, and insert the subroute from i to j into another randomly chosen position.
        Args :
            route : list of integers representing the order of cities to visit
        Returns :
            route : new list of integers representing the order of cities to visit
        """
        subroute_a = random.randint(0, len(route) - 1)
        subroute_b = random.randint(0, len(route) - 1)
        mini = min(subroute_a,subroute_b)
        maxi = max(subroute_a,subroute_b)
        subroute = route[mini:maxi]
        del route[ mini:maxi]
        insert_pos = random.choice(range(len(route)))
        for i in subroute:
            route.insert(insert_pos,i)
        return route

    def simulatedAnnealing(self):
        """
        Performs simulated annealing to find a solution
        Args :
            None
        Returns :
            best_route, best_route_distance : list of integers representing the order of cities to visit, and the distance of the route
        """
        initial_temp = 5000
        alpha = 0.90
        current_temp = initial_temp
        solution = list(range(len(self.coords)))
        same_solution = 0
        same_cost_diff = 0
        while same_solution < 1500 and same_cost_diff < 15000: #terminates once a candidate has been selected 1500 times and the same fitness score has occurred 15000 times
            neighbor = self.getNeighbors(solution)
            # Check if neighbor is better than current best
            cost_diff = self.getRouteCost(neighbor) - self.getRouteCost(solution)

            # if the new solution is better, accept it
            if cost_diff > 0:
                solution = neighbor
                same_solution = 0
                same_cost_diff = 0
            elif cost_diff == 0: #same cost, so we just increment the counter
                solution = neighbor
                same_solution = 0
                same_cost_diff += 1
                
            # if the new solution is not better, accept it with a probability of e^(-cost/temp)
            else:
                if random.uniform(0, 1) <= math.exp(cost_diff / current_temp):
                    solution = neighbor
                    same_solution = 0
                    same_cost_diff = 0
                else:
                    same_solution += 1
                    same_cost_diff += 1
            # decrement the temperature
            current_temp = current_temp * alpha
        return solution, 1/self.getRouteCost(solution)

def distance(a,b):
    """Calculates the distance between two cities"""
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

#Change tsp file name to run on separate tsp datasets
data = tsplib95.load('berlin52.tsp')
cities = list(data.node_coords.values())
best_route_distance = []
best_route = []
convergence_time = []   
start = time.time()
solver = TSPSolver(cities, distance)
route, route_distance = solver.simulatedAnnealing()
print(route,route_distance)
time_elapsed = time.time() - start
best_route_distance.append(route_distance)
best_route.append(route)
convergence_time.append(time_elapsed)
#Plot Routes
xs = [cities[i][0] for i in route]
ys = [cities[i][1] for i in route]

plt.scatter(xs,ys)
# 'bo-' means blue color, round points, solid lines
plt.plot(xs,ys,'y--')
plt.xlabel('X Coordinates')
plt.ylabel('Y Coordinates')
plt.show()