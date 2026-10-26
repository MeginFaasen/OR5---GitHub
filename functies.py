
import pandas as pd
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import pandas as pd
import math
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import random
import copy
print('\033c') 


dfo = pd.read_excel('PaintShop - September 2026.xlsx', 'Orders')
dfm = pd.read_excel('PaintShop - September 2026.xlsx', 'Machines')
dfs = pd.read_excel('PaintShop - September 2026.xlsx', 'Setups')

MACHINE_NAMEN = ["M1", "M2", "M3"]

def setuptijd(newcol: str, machine: list) -> float:
    """
    Berekent de setup tijd door de nieuwe kleur te vergelijken met de oude kleur in de machine,
    als de machine nog geen order heeft toegewezen gekregen dan is de setuptijd automatisch nul.
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

def plot_SA(huidige_lijst: list, best_lijst: list, T_lijst: list):
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(huidige_lijst, color="tab:blue", label="huidige oplossing", linewidth=0.8)
    ax1.plot(best_lijst, color="tab:orange", label="beste oplossing", linewidth=1.2)
    ax1.set_xlabel("Iteratie")
    ax1.set_ylabel("Penalty cost")

    ax2 = ax1.twinx()
    ax2.plot(T_lijst, color="tab:green", label="temperatuur")
    ax2.set_ylabel("Temperatuur")

    lijnen1, labels1 = ax1.get_legend_handles_labels()
    lijnen2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lijnen1 + lijnen2, labels1 + labels2, loc="upper right")

    ax1.set_title("Voortgang van Simulated Annealing")
    plt.show()


# Improved search   
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

            if m == machines[0]:
                eindtijd += huidigetijd + su + surface/dfm.loc[dfm["Machine"]== 'M1', "Speed"].item()
                tard = max(0, eindtijd - dfo.loc[dfo["Order"] == o, "Deadline"].item())
                pen = tard * dfo.loc[dfo["Order"] == o, "Penalty"].item()

            elif m == machines[1]:
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

#visualiseren
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

def bouw_gantt(machines: list):
    if len(machines)==3:
        machines_dict = {"M1": ma1, "M2": ma2, "M3": ma3}
    else: 
        machines_dict = {"M1": ma1, "M2": ma2, "M3": ma3, "M4": ma4}

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
