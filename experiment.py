from functies import setuptijd
import math as m

def experiment_su(data: dict) -> list:
    """Greedy rule: minimaliseer setuptijd; bij gelijkspel kies de snelste machine.
    """
    n = data["n_machines"]
    ceiling =  m.ceil(len(data["surface"]) / n)

    ma1, ma2, ma3 = [], [], []
    ma4 = [] if n == 4 else None

    dfo_sorted = data["dfo"].sort_values(by=["Deadline"], ascending=True)

    for i in dfo_sorted.index:
        newcol = dfo_sorted.loc[i, "Colour"]
        ord_nr = dfo_sorted.loc[i, "Order"]
        surface = dfo_sorted.loc[i, "Surface"]

        su1 = setuptijd(data, newcol, ma1) if len(ma1) < ceiling else float("inf")
        su2 = setuptijd(data, newcol, ma2) if len(ma2) < ceiling else float("inf")
        su3 = setuptijd(data, newcol, ma3) if len(ma3) < ceiling else float("inf")

        if n == 4:
            su4 = setuptijd(data, newcol, ma4) if len(ma4) < ceiling else float("inf")
        else:
            su4 = float("inf")

        proces1 = surface / data["speed"]["M1"]
        proces2 = surface / data["speed"]["M2"]
        proces3 = surface / data["speed"]["M3"]
        proces4 = surface / data["speed"]["M4"] if n == 4 else float("inf")

        min_su = min(su1, su2, su3, su4)
        kandidaten = []
        if su1 == min_su:
            kandidaten.append((proces1, 1))
        if su2 == min_su:
            kandidaten.append((proces2, 2))
        if su3 == min_su:
            kandidaten.append((proces3, 3))
        if su4 == min_su:
            kandidaten.append((proces4, 4))

        kandidaten.sort()
        keuze = kandidaten[0][1]

        if keuze == 1:
            ma1.append(ord_nr)
        elif keuze == 2:
            ma2.append(ord_nr)
        elif keuze == 3:
            ma3.append(ord_nr)
        else:
            ma4.append(ord_nr)
            
    experiment_schema = [ma1, ma2, ma3]
    if n == 4:
        experiment_schema.append(ma4)

    return experiment_schema