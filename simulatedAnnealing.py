import distanceMatrix as helper
import random
import time
from math import exp

# minimal proportion of accepted neighbours to change temperature
ACCEPT_NEIGHBOR_THRESHOLD = 0.1 
ACCEPTANCE_THRESHOLD = 0.01
TEMP_MULTIPLIER = 0.9

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

    i = random.randint(1, len(path) - 4)
    j = random.randint(1, len(path) - 2)

    while(i >= j or i + 1 == j):
        i = random.randint(1, len(path) - 4)
        j = random.randint(1, len(path) - 2)

    path1 = path[0:i + 1]
    path2 = path[i + 1: j + 1]
    path2.reverse()
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
    print("Minimum neighbors : " + str(n_accepted_neighbors) + ". Current accepted : " + str(accepted_neighbors))
    return  accepted_neighbors >= n_accepted_neighbors

def decay_temp(temp):
    return temp * TEMP_MULTIPLIER


def solve():
    n_iter = 10000
    current = create_initial_solution(len(matrix[0]))
    best = current
    next = 0
    temp = getInitialTemp()
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
            else:
                if getProb(d, temp):
                    accepted_neighbors +=1
                    current = next

            if(should_change_temp(n_iter, accepted_neighbors)):
                break
        if timetoStop(n_iter, accepted_neighbors) :
            print("Time Elapsed : " + str(int(round(time.time() * 1000)) - startTime) + "ms")
            return best 

        temp = decay_temp(temp)


            

    

solution = solve()
print(solution.path)
print(solution.cost)


