import math
import random
import copy

from functies import pen_cost

# Machines random indelen
def random_indelen(data: dict) -> list:
    """
    """
    n = data["n_machines"] 

    ma1, ma2, ma3 = [], [], []
    ma4 = [] if n == 4 else None
    machines = [ ma1, ma2, ma3]
    if n == 4:
        machines.append(ma4)

    ceiling =  math.ceil(len(data["surface"]) / n)

    for o in data["surface"].keys():
        beschikbaar = []
        for m in machines:
            if len(m) < ceiling:
                beschikbaar.append(m)
        machine = random.choice(beschikbaar)
        machine.append(o)
    return machines

    
# simulated annealing 
def simulated_annealing(data: dict, start_schema: list, T: float, iteraties: int, alpha: float, iteraties_per_T: int = 1):
    machines = copy.deepcopy(start_schema)
    huidige = pen_cost(data, machines)
    best = huidige
    beste_schema = copy.deepcopy(machines)
    huidige_lijst, best_lijst, T_lijst = [], [], []

    for i in range(iteraties):
        machine1 = random.choice(machines)
        machine2 = random.choice(machines)
        swap1 = random.choice(machine1)
        swap2 = random.choice(machine2)
        i1 = machine1.index(swap1)
        i2 = machine2.index(swap2)
        machine1[i1] = swap2
        machine2[i2] = swap1

        kandidaat = pen_cost(data, machines)
        delta = kandidaat - huidige
        if delta < 0:
            geaccepteerd = True
        else:
            acceptatie = math.exp(-delta / T)
            geaccepteerd = random.random() < acceptatie

        if geaccepteerd:
            huidige = kandidaat
            if kandidaat < best:
                best = kandidaat
                beste_schema = copy.deepcopy(machines)
        else:
            machine1[i1] = swap1   # swap terugdraaien
            machine2[i2] = swap2

        if (i + 1) % iteraties_per_T == 0:   
            T *= alpha

        huidige_lijst.append(huidige)
        best_lijst.append(best)
        T_lijst.append(T)

    return beste_schema, best, huidige_lijst, best_lijst, T_lijst
