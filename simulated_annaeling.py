import pandas as pd
import math
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import random
import copy
print('\033c')

# Inladen van de Excel-sheets
dfo = pd.read_excel('PaintShop - September 2026.xlsx', 'Orders')
dfm = pd.read_excel('PaintShop - September 2026.xlsx', 'Machines')
dfs = pd.read_excel('PaintShop - September 2026.xlsx', 'Setups')
print(dfm.head())
print(dfs.head(12))

ma1 = []
ma2 = []
ma3 = []

# Machines random indelen
def random_indelen(df):
    """
    """
    ceiling = math.ceil(len(df)/3)
    machines = [ma1, ma2, ma3]

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
    return ma1, ma2, ma3

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
        oldcol = dfo.loc[dfo["Order"] == machine[-1], "Colour"].item()
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
    for m in machines:
        huidigetijd = 0
        eindtijd = 0
        verwerkte_orders = []

        for o in m:
            surface = dfo.loc[dfo["Order"] == o, "Surface"].item()
            color = dfo.loc[dfo["Order"] == o, "Colour"].item()
            su = setuptijd(color, verwerkte_orders)

            if m == ma1:
                eindtijd += huidigetijd + su + surface/dfm.loc[dfm["Machine"]== 'M1', "Speed"].item()
                tard = max(0, eindtijd - dfo.loc[dfo["Order"] == o, "Deadline"].item())
                pen = tard * dfo.loc[dfo["Order"] == o, "Penalty"].item()

            elif m == ma2:
                eindtijd += huidigetijd + su + surface/dfm.loc[dfm["Machine"]== 'M2', "Speed"].item()
                tard = max(0, eindtijd - dfo.loc[dfo["Order"] == o, "Deadline"].item())
                pen = tard * dfo.loc[dfo["Order"] == o, "Penalty"].item()

            else:
                eindtijd += huidigetijd + su + surface/dfm.loc[dfm["Machine"]== 'M3', "Speed"].item()
                tard = max(0, eindtijd - dfo.loc[dfo["Order"] == o, "Deadline"].item())
                pen = tard * dfo.loc[dfo["Order"] == o, "Penalty"].item()
            total_pen += pen
            verwerkte_orders.append(o)
    return total_pen
    
        
random_indelen(dfo)
print(f'Machine 1: {ma1} \n')
print(f'Machine 2: {ma2} \n')
print(f'Machine 3: {ma3} \n')

machines = [ma1, ma2, ma3]
huidige = pen_cost(machines)
best = huidige
print(f'Initiele penalty: {best:.2f}')
T = 500 #temperatuur
iteraties = 1000
alpha = 0.999

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
    acceptatie = math.exp(-delta/T)
    if delta < 0 or random.random() < acceptatie: # de move wordt geaccepteerd
        huidige = kandidaat
        if kandidaat < best:
            best = kandidaat
            beste_schema = machines.copy()
    else: # De move wordt niet geaccepteerd
        machine1[i1] = swap1 # swap terug draaien
        machine2[i2] = swap2
    T *= alpha

ma1, ma2, ma3 = beste_schema   # herstel de beste indeling aan het eind
print(f'Beste schema penalty kosten: {best:.2f}')
print('Beste indeling:')
print(f'Machine 1: {ma1}')
print(f'Machine 2: {ma2}')
print(f'Machine 3: {ma3}')
