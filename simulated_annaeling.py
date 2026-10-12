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

#Visualiseren
gantt_rows = []

def voeg_toe(machine_naam, begin, su, einde, order_naam):
    """Slaat het setup-blok en het order-blok van één order op voor de Gantt-chart."""
    gantt_rows.append({
        "Machine": machine_naam,
        "Start setup": begin,
        "Einde setup": begin + su,
        "Start order": begin + su,
        "Einde order": einde,
        "Label": order_naam,
    })

def bouw_gantt(ma1, ma2, ma3):
    machines_dict = {"M1": ma1, "M2": ma2, "M3": ma3}
    for naam, orders in machines_dict.items():
        eindtijd = 0
        verwerkte_orders = []
        speed = dfm.loc[dfm["Machine"] == naam, "Speed"].item()

        for o in orders:
            surface = dfo.loc[dfo["Order"] == o, "Surface"].item()
            color = dfo.loc[dfo["Order"] == o, "Colour"].item()
            su = setuptijd(color, verwerkte_orders)

            begin = eindtijd
            eindtijd = begin + su + surface / speed

            voeg_toe(naam, begin, su, eindtijd, o)
            verwerkte_orders.append(o)

    
# simulated annealing  
random_indelen(dfo)
print('Initiele indeling:')
print(f'Machine 1: {ma1}')
print(f'Machine 2: {ma2}')
print(f'Machine 3: {ma3}')

machines = [ma1, ma2, ma3]
huidige = pen_cost(machines)
best = huidige
print(f'Initiele penalty: {best:.2f}')
T = 500 #temperatuur
iteraties = 5000
alpha = 0.995

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

ma1, ma2, ma3 = beste_schema   # herstel de beste indeling aan het eind
bouw_gantt(ma1, ma2, ma3) 
print(f'Beste schema penalty kosten: {best:.2f}')
print('Beste indeling:')
print(f'Machine 1: {ma1}')
print(f'Machine 2: {ma2}')
print(f'Machine 3: {ma3}')

gantt_df = pd.DataFrame.from_dict(gantt_rows)

machines_labels = ["M1", "M2", "M3"]
fig, ax = plt.subplots(figsize=(12, 4))

for x, r in gantt_df.iterrows():
    y = machines_labels.index(r["Machine"])
    if r["Einde setup"] > r["Start setup"]:
        ax.broken_barh([(r["Start setup"], r["Einde setup"] - r["Start setup"])],
                       (y - 0.4, 0.8), facecolors="tab:purple")
    ax.broken_barh([(r["Start order"], r["Einde order"] - r["Start order"])],
                   (y - 0.4, 0.8), facecolors="tab:cyan", edgecolor="white")
    ax.text((r["Start order"] + r["Einde order"]) / 2, y, r["Label"],
            ha="center", va="center", color="black", fontsize=7)

ax.set_yticks(range(len(machines_labels)))
ax.set_yticklabels(machines_labels)
ax.set_xlabel("Tijd")
ax.legend(handles=[
    Patch(facecolor="tab:purple", label="Setup"),
    Patch(facecolor="tab:cyan", label="Order"),
])
plt.show()
