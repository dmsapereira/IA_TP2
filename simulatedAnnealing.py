import distanceMatrix as helper
import random
import time
from math import exp

# minimal proportion of accepted neighbours to change temperature
ACCEPTANCE_THRESHOLD = 0.005
ACCEPT_NEIGHBOR_THRESHOLD = 0.05
N_ITER_GEOMETRIC_MULTIPLIER = 1.05
N_ITER_LINEAR_CONSTANT = 1000 
GEO_TEMP_MULTIPLIER = 0.95
GRADUAL_TEMP_MULTIPLIER =  0.01


matrix = helper.readDistanceMatrix("distancias.txt")

class Solution:

    def __init__(self):
        self.path = []
        self.cost = 0

    def addCity(self, city):
        if self.path:
            self.cost += helper.distance(matrix, self.path[-1], city)
        self.path.append(city)

    def finishPath(self):
        self.cost += helper.distance(matrix, self.path[-1], self.path[0])

    def chosen_one(self, iteration, temp):
        self.iteration = iteration
        self.temp = temp

    




def getInitialTemp():
    maxDistance1 = int(matrix[1][0][0])
    minDistance1 = int(matrix[1][0][0])
    maxDistance2 = int(matrix[1][0][0])
    minDistance2 = int(matrix[1][0][0])

    current = 0
    cities = matrix[0]

    for city1 in cities:
        for city2 in cities:
            if city1 == city2:
                continue
            else:
                current = helper.distance(matrix, city1,  city2)
                if current > maxDistance2:
                    if current > maxDistance1:
                        maxDistance2 = maxDistance1
                        maxDistance1 = current
                    else:
                        maxDistance2 = current 
                
                elif current < minDistance2:
                    if current < minDistance1:
                        minDistance2 = minDistance1
                        minDistance1 = current
                    else:
                        minDistance2 = current

    return maxDistance1 + maxDistance2 - minDistance1 - minDistance2

def getProb(d, temp):
    threshold = exp(-d/temp)
    roll = random.random()
    return roll <= threshold

def create_initial_solution(n):
    solution = Solution()
    cities = list(matrix[0])

    for i in range(n):
        current = random.choice(cities)
        cities.remove(current)
        solution.addCity(current)
    
    solution.finishPath()

    return solution


def neighbor(solution):
    path = solution.path

    i = random.randint(0, len(path) - 3)
    j = random.randint(0, len(path) - 1)

    while(i >= j or i + 1 == j):
        i = random.randint(1, len(path) - 4)
        j = random.randint(1, len(path) - 2)

    path1 = path[0:i + 1]
    path2 = path[i + 1: j + 1]
    path2.reverse()
    if j == (len(path) - 1):
        path3 = []
    else:
        path3 = path[j + 1:]
    path1.extend(path2)
    path1.extend(path3)

    result = Solution()
    for city in path1:
        result.addCity(city)

    result.finishPath()

    return result

def timetoStop(n_iter, accepted_neighbors):
    return accepted_neighbors/n_iter < ACCEPTANCE_THRESHOLD

def should_change_temp(current_n_iter, accepted_neighbors):
    n_accepted_neighbors = current_n_iter * ACCEPT_NEIGHBOR_THRESHOLD
    return  accepted_neighbors >= n_accepted_neighbors

def decay_temp(temp, mode):
    if mode == "GEO":
        return temp * GEO_TEMP_MULTIPLIER
    return temp / (1 + GRADUAL_TEMP_MULTIPLIER *temp)

def change_n_iter(n_iter, mode):
    if mode == "CONST":
        return n_iter 
    elif mode == "GEO":
        return n_iter * N_ITER_GEOMETRIC_MULTIPLIER
    else:
        return n_iter + N_ITER_LINEAR_CONSTANT





def solve():

    temp = input("Initial Temp (AUTO | <value>) :").strip()
    if temp == "AUTO":
        temp = getInitialTemp()
        print(temp)

    n_iter_mode = input("Iteration number mode (LINEAR | GEO | ONE | SMART | CONST) : ").upper().strip()

    if n_iter_mode == "ONE":
        temp_mode = "GRADUAL"

    temp_mode = "GEO"

    n_iter = 10000
    first = create_initial_solution(len(matrix[0]))
    current = first
    best = current
    worst = current
    next = 0
    startTime = int(round(time.time() * 1000))

    while(True):
        accepted_neighbors = 0
        for iteration in range(n_iter):
            next = neighbor(current) 
            d = next.cost - current.cost
            if d < 0:
                current = next
                accepted_neighbors += 1
                if current.cost < best.cost:
                    best = current
                    best.chosen_one(iteration, temp)
                elif getProb(d, temp):
                    accepted_neighbors +=1
                    current = next


            if worst.cost - next.cost < 0:
                worst = next

            if(n_iter_mode == "ONE"):
                break
            elif(n_iter_mode == "SMART" and should_change_temp(n_iter, accepted_neighbors)):
                break

        if timetoStop(n_iter, accepted_neighbors) :
            print("Time Elapsed : " + str(int(round(time.time() * 1000)) - startTime) + "ms")
            last = current
            break 

        if n_iter_mode != ("CONST" or "SMART"):
            n_iter =  change_n_iter(n_iter, n_iter_mode)
        temp = decay_temp(temp, temp_mode)

    print("First : " , first.path)
    print("Last : " , last.path)
    print("Worst : " , worst.path)
    print("Best")
    print("\t Iteration : " , best.iteration)
    print("\t Temp : " , best.temp)
    print("\t Path : " , best.path)
    print("\t Cost : " , best.cost)
    return best

            

    

solution = solve()


