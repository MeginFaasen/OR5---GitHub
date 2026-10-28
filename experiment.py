from functies import setuptijd
import math as m

def experiment_su(data: dict) -> list:
    """Zo min mogelijk setuptijd als greedy rule
    """
    n = data["n_machines"]
    ceiling =  m.ceil(len(data["surface"]) / n)

    ma1, ma2, ma3 = [], [], []
    ma4 = [] if n == 4 else None

    e1 = e2 = e3 = 0
    e4 = 0 if n == 4 else None

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

        if all(len(ma) >= ceiling for ma in [ma1, ma2, ma3] + ([ma4] if n == 4 else [])):
            raise ValueError("Alle machines hebben hun maximale capaciteit bereikt!")

        if su1 == min(su1, su2, su3, su4):
            ma1.append(ord_nr)
            e1 = e1 + su1 + surface / data["speed"]["M1"]
        elif su2 == min(su1, su2, su3, su4):
            ma2.append(ord_nr)
            e2 = e2 + su2 + surface / data["speed"]["M2"]
        elif su3 == min(su1, su2, su3, su4):
            ma3.append(ord_nr)
            e3 = e3 + su3 + surface / data["speed"]["M3"]
        elif su4 == min(su1, su2, su3, su4):
            ma4.append(ord_nr)
            e4 = e4 + su4 + surface / data["speed"]["M4"]

    experiment_schema = [ma1, ma2, ma3]
    if n == 4:
        experiment_schema.append(ma4)

    return experiment_schema