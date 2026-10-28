import pandas as pd
import math
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
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
def simulated_annealing(data: dict, start_schema: list, T: float, iteraties: int, alpha: float):
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
        T *= alpha

        huidige_lijst.append(huidige)
        best_lijst.append(best)
        T_lijst.append(T)

    return beste_schema, best, huidige_lijst, best_lijst, T_lijst

# # bouw_gantt(beste_schema) /
# print(f'Beste schema penalty kosten: {pen_cost(beste_schema):.2f}')
# print('Beste indeling:')
# for nr, m in enumerate(beste_schema, start=1):
#     print(f'Machine {nr}: {m}')

# plot_SA(huidige_lijst, best_lijst, T_lijst)

# #gantt visualisatie
# gantt_df = pd.DataFrame.from_dict(gantt_rows)

# machines_labels = [f"M{idx+1}" for idx in range(len(beste_schema))]
# fig, ax = plt.subplots(figsize=(12, 4))

# for x, r in gantt_df.iterrows():
#     y = machines_labels.index(r["Machine"])
#     if r["Einde setup"] > r["Start setup"]:
#         ax.broken_barh([(r["Start setup"], r["Einde setup"] - r["Start setup"])],
#                        (y - 0.4, 0.8), facecolors="tab:purple")
#     ax.broken_barh([(r["Start order"], r["Einde order"] - r["Start order"])],
#                    (y - 0.4, 0.8), facecolors="tab:cyan", edgecolor="white")
#     ax.text((r["Start order"] + r["Einde order"]) / 2, y, r["Label"],
#             ha="center", va="center", color="black", fontsize=7)

# ax.set_yticks(range(len(machines_labels)))
# ax.set_yticklabels(machines_labels)
# ax.set_xlabel("Tijd")
# ax.legend(handles=[
#     Patch(facecolor="tab:purple", label="Setup"),
#     Patch(facecolor="tab:cyan", label="Order"),
# ])
# plt.show()