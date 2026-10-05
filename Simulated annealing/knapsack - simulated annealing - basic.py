# SIMULATED ANNEALING + DISCRETE IMPROVING SEARCH FOR KNAPSACK

# GenAI usage declaration cf. Me & My Machine classification: PIGGYBACKER - Mostly Made By GenAI
# This product was mostly created by Al. There was some basic prompting, reprompting and curating of results. Al did all the heavy lifting.
# The OR5 teacher did an initial check on the correctness of the code, but the correctness of the code has not been verified. 
# TO DO: You need to run test cases and verify that the results are as expected, i.e., validate the correctness of the code.

import math
import random


# problem data
items = ["A", "B", "C", "D", "E"]
weight = [4, 2, 3, 5, 1]
value = [12, 10, 9, 15, 4]
capacity = 8


def calculate_objective(solution):
    total_value = 0
    for item in solution:
        total_value += value[item]
    return total_value

# ---
# PHASE 0: RANDOM FEASIBLE STARTING SOLUTION
# ---

remaining = list(range(len(items)))
random.shuffle(remaining)

solution = []
current_weight = 0

for item in remaining:
    if current_weight + weight[item] <= capacity:
        solution.append(item)
        current_weight += weight[item]

# ---
# PHASE 1: SIMULATED ANNEALING: exchange moves
# A neighbor replaces one selected item by one unselected item.
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

    unselected = []
    for item in range(len(items)):
        if item not in current_solution:
            unselected.append(item)

    # randomly generate a feasible exchange neighbor
    while True:

        position = random.randrange(len(current_solution))
        new_item = random.choice(unselected)

        neighbor = current_solution.copy()
        neighbor[position] = new_item

        neighbor_weight = 0
        for item in neighbor:
            neighbor_weight += weight[item]

        if neighbor_weight <= capacity:
            break

    # evaluate the neighbor
    neighbor_objective = calculate_objective(neighbor)
    improvement = neighbor_objective - current_objective

    # accept an improving move, or sometimes a non-improving move
    if improvement >= 0 or random.random() < math.exp(improvement / temperature):
        current_solution = neighbor
        current_objective = neighbor_objective

        # update incumbent solution
        if current_objective > best_objective:
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
# PHASE 2: DISCRETE IMPROVING SEARCH: best improvement with exchange moves
# Start from the best solution found by Simulated Annealing.
# ---

current_solution = sa_solution.copy()
current_objective = calculate_objective(current_solution)

while True:

    best_neighbor = None
    best_objective = current_objective

    unselected = []
    for item in range(len(items)):
        if item not in current_solution:
            unselected.append(item)

    # generate and evaluate all feasible exchange neighbors
    for position in range(len(current_solution)):
        for new_item in unselected:

            neighbor = current_solution.copy()
            neighbor[position] = new_item

            neighbor_weight = 0
            for item in neighbor:
                neighbor_weight += weight[item]

            if neighbor_weight <= capacity:
                neighbor_objective = calculate_objective(neighbor)

                if neighbor_objective > best_objective:
                    best_neighbor = neighbor
                    best_objective = neighbor_objective

    # stop if no improving neighbor exists
    if best_neighbor is None:
        break

    # move to best neighbor
    current_solution = best_neighbor
    current_objective = best_objective


# show results
sa_weight = 0
for item in sa_solution:
    sa_weight += weight[item]

final_weight = 0
for item in current_solution:
    final_weight += weight[item]

print("SA selected items:", [items[item] for item in sa_solution])
print("SA total weight:", sa_weight)
print("SA total value:", sa_objective)

print()
print("Locally optimal selected items:", [items[item] for item in current_solution])
print("Locally optimal total weight:", final_weight)
print("Locally optimal total value:", current_objective)
