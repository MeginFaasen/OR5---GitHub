
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
