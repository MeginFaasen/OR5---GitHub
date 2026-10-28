from functies import setuptijd

def experiment_su(data: dict) -> list:
    """Zo min mogelijk setuptijd als greedy rule
    """
    n = data["n_machines"]

    ma1, ma2, ma3 = [], [], []
    ma4 = [] if n == 4 else None

    e1 = e2 = e3 = 0
    e4 = 0 if n == 4 else None

    dfo_sorted = data["dfo"].sort_values(by=["Deadline"], ascending=True)

    for i in dfo_sorted.index:
        newcol = dfo_sorted.loc[i, "Colour"]
        ord_nr = dfo_sorted.loc[i, "Order"]
        surface = dfo_sorted.loc[i, "Surface"]

        su1 = setuptijd(data, newcol, ma1)
        su2 = setuptijd(data, newcol, ma2)
        su3 = setuptijd(data, newcol, ma3)
        if n == 4:
            su4 = setuptijd(data, newcol, ma4)
        else:
            su4 = float("inf")

        if su1 == min(su1, su2, su3, su4):
            ma1.append(ord_nr)
            e1 = e1 + su1 + surface / data["speed"]["M1"]
        elif su2 == min(su1, su2, su3, su4):
            ma2.append(ord_nr)
            e2 = e2 + su2 + surface / data["speed"]["M2"]
        elif su3 == min(su1, su2, su3, su4):
            ma3.append(ord_nr)
            e3 = e3 + su3 + surface / data["speed"]["M3"]
        else:
            ma4.append(ord_nr)
            e4 = e4 + su4 + surface / data["speed"]["M4"]

    experiment_schema = [ma1, ma2, ma3]
    if n == 4:
        experiment_schema.append(ma4)

    return experiment_schema