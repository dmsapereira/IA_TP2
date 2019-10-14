import distanceMatrix as helper
import random
from math import exp

N_ITER = 1000
matrix = helper.readDistanceMatrix("distancias.txt")

class Solution:
    def __init__(self):
        self.path = []
        self.cost = 0

    def addCity(self, city):
        if self.path:
            self.cost += helper.distance(matrix, self.path[-1], city)
        self.path.append(city)
    




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
    path = Solution()
    cities = list(matrix[0])

    for i in range(n):
        current = random.choice(cities)
        cities.remove(current)
        path.addCity(current)

    return path


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

    return result


def solve():
    current = create_initial_solution(len(matrix[0]))
    best = current
    next = 0
    temp = getInitialTemp(matrix)

    while(True):
        for iteration in range(N_ITER):
            next = neighbor(current) 
            d = next.cost - current.cost
            if d < 0:
                current = next
                if current.cost < best.cost:
                    best = current
            else:
                if getProb(d, temp):
                    current = next
            

    

"""current = create_initial_solution(len(matrix[0]))
print(getInitialTemp())
print(current.cost)
print(neighbor(current).cost)"""



