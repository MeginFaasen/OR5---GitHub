# SIMULATED ANNEALING + DISCRETE IMPROVING SEARCH FOR BIN PACKING

# GenAI usage declaration cf. Me & My Machine classification: PIGGYBACKER - Mostly Made By GenAI
# This product was mostly created by Al. There was some basic prompting, reprompting and curating of results. Al did all the heavy lifting.
# The OR5 teacher did an initial check on the correctness of the code, but the correctness of the code has not been verified. 
# TO DO: You need to run test cases and verify that the results are as expected, i.e., validate the correctness of the code.

import math
import random


# problem data
items = ["A", "B", "C", "D", "E", "F", "G"]
size = [4, 8, 1, 4, 2, 5, 3]
capacity = 10


def calculate_objective(solution):
    return len(solution)

# ---
# PHASE 0: RANDOM FEASIBLE STARTING SOLUTION
# ---

remaining = list(range(len(items)))
random.shuffle(remaining)

solution = []

for item in remaining:

    # place the item in the first bin where it fits
    item_placed = False

    for bin in solution:

        bin_load = 0
        for bin_item in bin:
            bin_load += size[bin_item]

        if bin_load + size[item] <= capacity:
            bin.append(item)
            item_placed = True
            break

    # create a new bin if necessary
    if not item_placed:
        solution.append([item])

# ---
# PHASE 1: SIMULATED ANNEALING: relocate moves
# A neighbor moves one item from one bin to another bin.
# ---

initial_temperature = 1000
max_iterations = 1000000
iterations_per_temperature = 1000
alpha = 0.9

current_solution = [bin.copy() for bin in solution]
current_objective = calculate_objective(current_solution)

best_solution = [bin.copy() for bin in current_solution]
best_objective = current_objective

temperature = initial_temperature
iteration = 0
iterations_at_temperature = 0

while iteration < max_iterations:

    # randomly generate a feasible relocate neighbor
    while True:

        source_bin = random.randrange(len(current_solution))
        target_bin = random.randrange(len(current_solution))

        if target_bin == source_bin:
            continue

        item_position = random.randrange(len(current_solution[source_bin]))
        item = current_solution[source_bin][item_position]

        target_bin_load = 0
        for target_item in current_solution[target_bin]:
            target_bin_load += size[target_item]

        if target_bin_load + size[item] <= capacity:

            neighbor = [bin.copy() for bin in current_solution]

            neighbor[target_bin].append(item)
            neighbor[source_bin].pop(item_position)

            # remove an empty bin
            if len(neighbor[source_bin]) == 0:
                neighbor.pop(source_bin)

            break

    # evaluate the neighbor
    neighbor_objective = calculate_objective(neighbor)
    improvement = current_objective - neighbor_objective

    # accept an improving move, or sometimes a non-improving move
    if improvement >= 0 or random.random() < math.exp(improvement / temperature):
        current_solution = neighbor
        current_objective = neighbor_objective

        # update incumbent solution
        if current_objective < best_objective:
            best_solution = [bin.copy() for bin in current_solution]
            best_objective = current_objective

    iteration += 1
    iterations_at_temperature += 1

    # reduce the temperature after a fixed number of iterations
    if iterations_at_temperature == iterations_per_temperature:
        temperature *= alpha
        iterations_at_temperature = 0


# save Simulated Annealing solution
sa_solution = [bin.copy() for bin in best_solution]
sa_objective = best_objective

# ---
# PHASE 2: DISCRETE IMPROVING SEARCH: best improvement with relocate moves
# Start from the best solution found by Simulated Annealing.
# ---

current_solution = [bin.copy() for bin in sa_solution]
current_objective = calculate_objective(current_solution)

while True:

    best_neighbor = None
    best_objective = current_objective

    # generate and evaluate all feasible relocate neighbors
    for source_bin in range(len(current_solution)):
        for item_position in range(len(current_solution[source_bin])):

            item = current_solution[source_bin][item_position]

            for target_bin in range(len(current_solution)):

                if target_bin == source_bin:
                    continue

                target_bin_load = 0
                for target_item in current_solution[target_bin]:
                    target_bin_load += size[target_item]

                if target_bin_load + size[item] <= capacity:

                    neighbor = [bin.copy() for bin in current_solution]

                    neighbor[target_bin].append(item)
                    neighbor[source_bin].pop(item_position)

                    # remove an empty bin
                    if len(neighbor[source_bin]) == 0:
                        neighbor.pop(source_bin)

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
print("SA bins:", [[items[item] for item in bin] for bin in sa_solution])
print("SA number of bins:", sa_objective)

print()
print("Locally optimal bins:", [[items[item] for item in bin] for bin in current_solution])
print("Locally optimal number of bins:", current_objective)
