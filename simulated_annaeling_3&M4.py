import pandas as pd
import math
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import random
import copy

import functies 
print('\033c')

# # Inladen van de Excel-sheets met 4 machines
# dfo = pd.read_excel('PaintShop - November 2026.xlsx', 'Orders')
# dfm = pd.read_excel('PaintShop - November 2026.xlsx', 'Machines')
# dfs = pd.read_excel('PaintShop - November 2026.xlsx', 'Setups')

# Inladen van de Excel-sheets met 3 machines
dfo = pd.read_excel('PaintShop - September 2026.xlsx', 'Orders')
dfm = pd.read_excel('PaintShop - September 2026.xlsx', 'Machines')
dfs = pd.read_excel('PaintShop - September 2026.xlsx', 'Setups')

# Voor sneller werk
surface_dict = dict(zip(dfo["Order"], dfo["Surface"]))
color_dict = dict(zip(dfo["Order"], dfo["Colour"]))
deadline_dict = dict(zip(dfo["Order"], dfo["Deadline"]))
penalty_dict = dict(zip(dfo["Order"], dfo["Penalty"]))
speed_dict = dict(zip(dfm["Machine"], dfm["Speed"]))

ma1 = []
ma2 = []
ma3 = []
if len(dfm)==4:
    ma4 = []

# Machines random indelen
def random_indelen(df):
    """
    """
    if len(dfm)==3:
        ceiling = math.ceil(len(df)/3)
        machines = [ma1, ma2, ma3]
    else:
        ceiling = math.ceil(len(df)/4)
        machines = [ma1, ma2, ma3, ma4]


    for i in df.index:
        ord_nr = dfo.loc[i, "Order"]
        machine = random.choice(machines)
        if len(machine) < ceiling:
            machine.append(ord_nr)
        else:
            machines.remove(machine)
            machine = random.choice(machines)
            if len(machine) < ceiling:
                machine.append(ord_nr)
            else:
                machines.remove(machine)
                machine = random.choice(machines)
                machine.append(ord_nr)
    if len(dfm)==3:
        return ma1, ma2, ma3
    else:
        return ma1, ma2, ma3, ma4

def setuptijd(newcol: str, machine: list) -> float:
    """
    Berekent de setup tijd door de nieuwe kleur te vergelijken met de oude kleur in de machine,
    als de machine nog geen order heeft toegewezen gekregen dan is de setuptijd automatisch nul.

    Returns:
        De setup tijd in een float.
    """
    if not machine:
        su_tijd = 0
    else:
        oldcol = color_dict[machine[-1]]
        if oldcol == newcol:
            su_tijd = 0
        else:
            su_tijd = dfs.loc[(dfs["From colour"] == oldcol) & (dfs["To colour"] == newcol), "Setup time"].item()
    return float(su_tijd)


def pen_cost(machines: list):
    """
    Berekent de penalty costs.

    Returns:
        

    """
    total_pen = 0
    for nr, m in enumerate(machines):
        eindtijd = 0
        verwerkte_orders = []
        machine_naam = f"M{nr + 1}" 
        speed = speed_dict[machine_naam]

        for o in m:
            surface = surface_dict[o]
            color = color_dict[o]
            su = setuptijd(color, verwerkte_orders)

            eindtijd = eindtijd + su + surface / speed
            tard = max(0, eindtijd - deadline_dict[o])
            pen = tard * penalty_dict[o]
            total_pen += pen
            verwerkte_orders.append(o)
        return total_pen
    
# simulated annealing  
random_indelen(dfo)
print('Initiele indeling:')
print(f'Machine 1: {ma1}')
print(f'Machine 2: {ma2}')
print(f'Machine 3: {ma3}')
if len(dfm)==4:
    print(f'Machine 4: {ma4}')

machines = [ma1, ma2, ma3]
if len(dfm)==4:
    machines.append(ma4)

huidige = pen_cost(machines)
best = huidige
print(f'Initiele penalty: {best:.2f}')
T = 500 #temperatuur
iteraties = 5000
alpha = 0.995

huidige_lijst = []
best_lijst = []
T_lijst = []

for i in range(iteraties):
    machine1 = random.choice(machines)
    machine2 = random.choice(machines)
    swap1 = random.choice(machine1)
    swap2 = random.choice(machine2)
    i1 = machine1.index(swap1)
    i2 = machine2.index(swap2)
    machine1[i1] = swap2
    machine2[i2] = swap1

    kandidaat = pen_cost(machines)
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

if len(dfm)==3:
    ma1, ma2, ma3 = beste_schema # herstel de beste indeling aan het eind
else:
    ma1, ma2, ma3, ma4 = beste_schema
# bouw_gantt(beste_schema) /
print(f'Beste schema penalty kosten: {pen_cost(beste_schema):.2f}')
print('Beste indeling:')
for nr, m in enumerate(beste_schema, start=1):
    print(f'Machine {nr}: {m}')

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