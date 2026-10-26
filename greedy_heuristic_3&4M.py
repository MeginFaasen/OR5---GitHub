import pandas as pd
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
print('\033c')

# # Inladen van de Excel-sheets met 4 machines
# dfo = pd.read_excel('PaintShop - November 2026.xlsx', 'Orders')
# dfm = pd.read_excel('PaintShop - November 2026.xlsx', 'Machines')
# dfs = pd.read_excel('PaintShop - November 2026.xlsx', 'Setups')

# Inladen van de Excel-sheets met 3 machines
dfo = pd.read_excel('PaintShop - September 2026.xlsx', 'Orders')
dfm = pd.read_excel('PaintShop - September 2026.xlsx', 'Machines')
dfs = pd.read_excel('PaintShop - September 2026.xlsx', 'Setups')

# Dataframe sorteren op deadline
dfo = dfo.sort_values(by=["Deadline"], ascending=True) #greedy rule first deadline first

# Eindtijden 
e1 = 0
e2 = 0
e3 = 0
if len(dfm) == 4:
    e4 = 0

# Machine orders
ma1 = []   
ma2 = []
ma3 = []
if len(dfm) == 4:
    ma4 = []

# Voorbeireiding (dictionary voor) Gantt Chart, penalty cost & functies
gantt_rows = []

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

def pen_cost(eind, ind):
    """
    Berekent de penalty costs.

    Returns:
        
    """
    tard = max(0, eind - dfo.loc[ind, "Deadline"])
    pen = tard * dfo.loc[ind, "Penalty"]
    return pen

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

total_pen = 0

# Eindtijden berekenen en informatie opslaan voor de gantt chart
for i in dfo.index:
    newcol = dfo.loc[i, "Colour"]
    ord_nr = dfo.loc[i, "Order"]
    surface = dfo.loc[i, "Surface"]

    su1 = setuptijd(newcol, ma1)
    su2 = setuptijd(newcol, ma2)
    su3 = setuptijd(newcol, ma3)
    if len(dfm) == 4:
        su4 = setuptijd(newcol, ma4)

    ec1 = e1 + su1 + surface/dfm.loc[0, "Speed"]
    ec2 = e2 + su2 + surface/dfm.loc[1, "Speed"]
    ec3 = e3 + su3 + surface/dfm.loc[2, "Speed"]
    if len(dfm) == 4:
        ec4 = e4 + su4 + surface/dfm.loc[3, "Speed"]
    else:
        ec4 = 100000
    
    if ec1 == min(ec1, ec2, ec3, ec4):
        ma1.append(ord_nr)
        voeg_toe("M1", e1, su1, ec1, ord_nr)
        e1 = ec1
        total_pen += pen_cost(e1, i)
    
    elif ec2 == min(ec1, ec2, ec3, ec4):
        ma2.append(ord_nr)
        voeg_toe("M2", e2, su2, ec2, ord_nr)
        e2 = ec2
        total_pen += pen_cost(e2, i)

    elif ec3 == min(ec1, ec2, ec3, ec4):
        ma3.append(ord_nr)
        voeg_toe("M3", e3, su3, ec3, ord_nr)
        e3 = ec3
        total_pen += pen_cost(e3, i)

    else:
        ma4.append(ord_nr)
        voeg_toe("M4", e4, su4, ec4, ord_nr)
        e4 = ec4
        total_pen += pen_cost(e4, i)
    

print(f'Machine 1: {ma1} \n')
print(f'Machine 2: {ma2} \n')
print(f'Machine 3: {ma3} \n')
if len(dfm) == 4:
    print(f'Machine 4: {ma4} \n')
print(f'Totale penalty kosten greedy rule 1: {total_pen:.2f}')

# Schema visualiseren
gantt_df = pd.DataFrame.from_dict(gantt_rows)

machines = ["M1", "M2", "M3"]
if len(dfm) == 4:
    machines.append("M4")
beste_schema1 = [ma1, ma2, ma3]
if len(dfm) == 4:
    beste_schema1.append(ma4)
fig, ax = plt.subplots(figsize=(4 * len(dfo), len(dfo) + 1))

for x, r in gantt_df.iterrows():
    y = machines.index(r["Machine"])
    if r["Einde setup"] > r["Start setup"]:
        ax.broken_barh([(r["Start setup"], r["Einde setup"] - r["Start setup"])],
                       (y - 0.4, 0.8), facecolors="tab:purple")
    ax.broken_barh([(r["Start order"], r["Einde order"] - r["Start order"])],
                   (y - 0.4, 0.8), facecolors="tab:cyan", edgecolor="white")
    ax.text((r["Start order"] + r["Einde order"]) / 2, y, r["Label"],
            ha="center", va="center", color="black", fontsize=7)

ax.set_yticks(range(len(machines)))
ax.set_yticklabels(machines)
ax.set_xlabel("Tijd")
ax.legend(handles=[
    Patch(facecolor="tab:purple", label="Setup"),
    Patch(facecolor="tab:cyan", label="Order"),
])
plt.show()