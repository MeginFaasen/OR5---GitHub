import copy
from functies import pen_cost

# Improved search
def improving_search(data: dict, beste_schema: list):
    machines = copy.deepcopy(beste_schema)   
    huidige = pen_cost(data, machines)
    
    lokaal_opt = True
    while lokaal_opt: #blijft doorgaan zolang de vorige ronde een verbetering vond
        lokaal_opt = False
        for m1 in range(len(machines)):
            for p1 in range(len(machines[m1])):
                for m2 in range(m1, len(machines)):
                    start = p1 + 1 if m2 == m1 else 0
                    for p2 in range(start, len(machines[m2])):
                        machine1 = machines[m1]
                        machine2 = machines[m2]
                        swap1 = machine1[p1]
                        swap2 = machine2[p2]
                        machine1[p1] = swap2
                        machine2[p2] = swap1

                        kandidaat = pen_cost(data, machines)
                        if kandidaat < huidige:   # geaccepteerd
                            huidige = kandidaat
                            lokaal_opt = True
                        else:                     # niet geaccepteerd
                            machine1[p1] = swap1
                            machine2[p2] = swap2

    return machines
