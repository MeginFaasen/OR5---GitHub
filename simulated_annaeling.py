import pandas as pd
import math
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import random
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

print(math.ceil(len(dfo)/3))

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
        
random_indelen(dfo)
print(f'Machine 1: {ma1} \n')
print(f'Machine 2: {ma2} \n')
print(f'Machine 3: {ma3} \n')