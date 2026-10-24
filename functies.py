
import pandas as pd
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
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