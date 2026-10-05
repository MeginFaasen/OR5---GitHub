# SIMULATED ANNEALING + DISCRETE IMPROVING SEARCH FOR TSP

# GenAI usage declaration cf. Me & My Machine classification: PIGGYBACKER - Mostly Made By GenAI
# This product was mostly created by Al. There was some basic prompting, reprompting and curating of results. Al did all the heavy lifting.
# The OR5 teacher did an initial check on the correctness of the code, but the correctness of the code has not been verified. 
# TO DO: You need to run test cases and verify that the results are as expected, i.e., validate the correctness of the code.

import math
import random


# problem data
cities = ["A", "B", "C", "D"]

distance = [
    [0, 4, 7, 3],
    [4, 0, 2, 6],
    [7, 2, 0, 5],
    [3, 6, 5, 0]
]


def calculate_objective(solution):
    total_distance = 0

    for i in range(len(solution) - 1):
        total_distance += distance[solution[i]][solution[i + 1]]

    return total_distance

# ---
# PHASE 0: RANDOM FEASIBLE STARTING SOLUTION
# ---

remaining = list(range(1, len(cities)))
random.shuffle(remaining)

solution = [0]

for city in remaining:
    solution.append(city)

# return to starting city
solution.append(solution[0])

# ---
# PHASE 1: SIMULATED ANNEALING: 2-opt moves
# A neighbor is created by reversing part of the route.
# ---

initial_temperature = 1000
max_iterations = 1000000
iterations_per_temperature = 1000
alpha = 0.9

current_solution = solution.copy()
current_objective = calculate_objective(current_solution)

best_solution = current_solution.copy()
best_objective = current_objective

temperature = initial_temperature
iteration = 0
iterations_at_temperature = 0

while iteration < max_iterations:

    # randomly generate a 2-opt neighbor
    i = random.randrange(1, len(current_solution) - 2)
    j = random.randrange(i + 1, len(current_solution) - 1)

    neighbor = current_solution.copy()

    # 2-opt move: reverse the segment from i to j
    neighbor[i:j + 1] = reversed(neighbor[i:j + 1])

    # evaluate the neighbor
    neighbor_objective = calculate_objective(neighbor)
    improvement = current_objective - neighbor_objective

    # accept an improving move, or sometimes a non-improving move
    if improvement >= 0 or random.random() < math.exp(improvement / temperature):
        current_solution = neighbor
        current_objective = neighbor_objective

        # update incumbent solution
        if current_objective < best_objective:
            best_solution = current_solution.copy()
            best_objective = current_objective

    iteration += 1
    iterations_at_temperature += 1

    # reduce the temperature after a fixed number of iterations
    if iterations_at_temperature == iterations_per_temperature:
        temperature *= alpha
        iterations_at_temperature = 0


# save Simulated Annealing solution
sa_solution = best_solution.copy()
sa_objective = best_objective

# ---
# PHASE 2: DISCRETE IMPROVING SEARCH: best improvement with 2-opt moves
# Start from the best solution found by Simulated Annealing.
# ---

current_solution = sa_solution.copy()
current_objective = calculate_objective(current_solution)

while True:

    best_neighbor = None
    best_objective = current_objective

    # generate and evaluate all 2-opt neighbors
    for i in range(1, len(current_solution) - 2):
        for j in range(i + 1, len(current_solution) - 1):

            neighbor = current_solution.copy()

            # 2-opt move: reverse the segment from i to j
            neighbor[i:j + 1] = reversed(neighbor[i:j + 1])

            neighbor_objective = calculate_objective(neighbor)

            if neighbor_objective < best_objective:
                best_neighbor = neighbor
                best_objective = neighbor_objective

    # stop if no improving neighbor exists
    if best_neighbor is None:
        break

    # move to best neighbor
    current_solution = best_neighbor
    current_objective = best_objective


# show results
print("SA route:", [cities[city] for city in sa_solution])
print("SA total distance:", sa_objective)

print()
print("Locally optimal route:", [cities[city] for city in current_solution])
print("Locally optimal total distance:", current_objective)
