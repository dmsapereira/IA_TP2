import distanceMatrix as helper
import random

NITER = 1000


def getInitialTemp(matrix):
    maxDistance = matrix[1][0]
    minDistance = matrix[1][0]
    current = 0
    cities = matrix[0]

    for city1 in cities:
        for city2 in cities:
            if city1 == city2:
                continue
            else:
                current = helper.distance(matrix, city1,  city2)
                if current > maxDistance:
                    maxDistance = current
                elif current < minDistance:
                    minDistance = current

    return maxDistance - minDistance

def create_initial_solution(cities, iterations):
    path = []

    for i in  range(iterations):
        current = random.choice(cities)
        cities.remove(current)
        path.append(current)
    
    return path

def neighbor(path):
    i = random.randint(1, len(path) - 2)
    j = random.randint(1, len(path) - 2)

    if(i >= j):
        return neighbor(path)
    else:
        path1 = path[0:i + 1]
        print(path1)
        path2 = path[i + 1: j + 1]
        path2.reverse()
        print(path2) 
        path3 = path[j + 1:]
        print(path3)
        path1.extend(path2)
        path1.extend(path3)

    return path1

    



def solve():
    matrix = helper.readDistanceMatrix("distancias.txt")
    current = create_initial_solution(matrix, len(matrix[0]))
    best = current
    next = 0
    temp = getInitialTemp(matrix)

    #for iteration in range(0, NITER):