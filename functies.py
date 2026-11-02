import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def laad_data(bestandsnaam: str) -> dict:
    """Laad alle data in en geeft dictionaries terug voor sneller gebruik.

        Returns: 
            Dict
    """
    dfo = pd.read_excel(bestandsnaam, 'Orders')
    dfm = pd.read_excel(bestandsnaam, 'Machines')
    dfs = pd.read_excel(bestandsnaam, 'Setups')

    return {
        "surface": dict(zip(dfo["Order"], dfo["Surface"])), #bijv. ORD23: 280
        "colour": dict(zip(dfo["Order"], dfo["Colour"])),
        "deadline": dict(zip(dfo["Order"], dfo["Deadline"])),
        "penalty": dict(zip(dfo["Order"], dfo["Penalty"])),
        "speed": dict(zip(dfm["Machine"], dfm["Speed"])),
        "setup": {(rij["From colour"], rij["To colour"]): rij["Setup time"] for _, rij in dfs.iterrows()}, #bijv. ("green", "red"): 6
        "n_machines": len(dfm),
        "dfo": dfo,
    }


def setuptijd(data: dict, newcol: str, machine: list) -> float:
    """
    Berekent de setup tijd door de nieuwe kleur te vergelijken met de oude kleur in de machine,
    als de machine nog geen order heeft toegewezen gekregen dan is de setuptijd automatisch nul.
    """
    if not machine:
        su_tijd = 0
    else:
        oldcol = data["colour"][machine[-1]]
        if oldcol == newcol:
            su_tijd = 0
        else:
            su_tijd = data["setup"][oldcol, newcol]
    return float(su_tijd)

def pen_cost(data: dict, machines: list) -> float:
    """
    Berekent de penalty costs.

    Returns:
        float van de penalty kosten

    """
    total_pen = 0
    for nr, m in enumerate(machines):
        eindtijd = 0
        verwerkte_orders = []
        machine_naam = f"M{nr + 1}" 
        speed = data["speed"][machine_naam]

        for o in m:
            surface = data["surface"][o]
            color = data["colour"][o]
            su = setuptijd(data, color, verwerkte_orders)

            eindtijd = eindtijd + su + surface / speed
            tard = max(0, eindtijd - data["deadline"][o])
            pen = tard * data["penalty"][o]
            total_pen += pen
            verwerkte_orders.append(o)
    return total_pen

def plot_SA(huidige_lijst: list, best_lijst: list, T_lijst: list):
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(huidige_lijst, color="tab:cyan", label="huidige oplossing", linewidth=0.8)
    ax1.plot(best_lijst, color="#A020F0", label="beste oplossing", linewidth=1.2)
    ax1.set_xlabel("Iteratie")
    ax1.set_ylabel("Penalty cost")

    ax2 = ax1.twinx()
    ax2.plot(T_lijst, color="tab:gray", label="temperatuur")
    ax2.set_ylabel("Temperatuur")

    lijnen1, labels1 = ax1.get_legend_handles_labels()
    lijnen2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lijnen1 + lijnen2, labels1 + labels2, loc="upper right")

    ax1.set_title("Voortgang van Simulated Annealing")
    plt.show()

def export_excel(data: dict, machines: list, bestandsnaam: str):
    """
    Schrijft het schema in een Excel-bestand met werkblad 'Schedule',
    in het door de opdracht voorgeschreven 11-kolommenformaat.
    Werkt generiek voor elk aantal machines.
    """
    n = data["n_machines"]
    bestandsnaam = f"PaintShop Beste Schema {n}M.xlsx"
    rijen = []

    for nr, m in enumerate(machines):
        machine_naam = f"M{nr + 1}"
        speed = data["speed"][machine_naam]
        eindtijd = 0
        verwerkt = []

        for seq, o in enumerate(m, start=1):
            su = setuptijd(data, data["colour"][o], verwerkt)
            start = eindtijd + su
            proces = data["surface"][o] / speed
            einde = start + proces
            tard = max(0, einde - data["deadline"][o])
            cost = tard * data["penalty"][o]

            rijen.append({
                "Order": o,
                "Machine": machine_naam,
                "SeqNo": seq,
                "Setup": su,
                "Start": start,
                "Process": proces,
                "End": einde,
                "Deadline": data["deadline"][o],
                "Tardiness": tard,
                "Penalty": data["penalty"][o],
                "Cost": cost,
            })

            eindtijd = einde
            verwerkt.append(o)

    schedule_df = pd.DataFrame(rijen)
    with pd.ExcelWriter(bestandsnaam, engine="openpyxl") as writer:
        schedule_df.to_excel(writer, sheet_name="Schedule", index=False)

    print(f'Schedule geëxporteerd naar {bestandsnaam} ({len(schedule_df)} rijen)')

#visualiseren
def bouw_gantt(data: dict, machines: list) -> list:
    """Bouwt voor elke order een setup-blok en een order-blok voor de Gantt-chart."""
    gantt_rows = []
    for nr, m in enumerate(machines):
        machine_naam = f"M{nr + 1}"
        speed = data["speed"][machine_naam]
        eindtijd = 0
        verwerkte_orders = []

        for o in m:
            su = setuptijd(data, data["colour"][o], verwerkte_orders)
            begin = eindtijd
            eindtijd = begin + su + data["surface"][o] / speed

            gantt_rows.append({
                "Machine": machine_naam,
                "Start setup": begin,
                "Einde setup": begin + su,
                "Start order": begin + su,
                "Einde order": eindtijd,
                "Label": o,
            })
            verwerkte_orders.append(o)
    return gantt_rows


def plot_gantt(gantt_rows: list, titel: str = ""):
    """Tekent de planning: per machine een rij, setup in paars en orders in cyaan."""
    gantt_df = pd.DataFrame.from_dict(gantt_rows)
    machines_labels = sorted(gantt_df["Machine"].unique())
    fig, ax = plt.subplots(figsize=(12, 1 + len(machines_labels)))

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
    ax.set_title(titel)
    ax.legend(handles=[Patch(facecolor="tab:purple", label="Setup"),
                       Patch(facecolor="tab:cyan", label="Order")])
    plt.show()