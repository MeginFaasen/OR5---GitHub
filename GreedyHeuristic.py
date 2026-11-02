from functies import setuptijd

def greedy_EDD(data: dict) -> list:
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

        ec1 = e1 + su1 + surface / data["speed"]["M1"] # Eindtijd Checks
        ec2 = e2 + su2 + surface / data["speed"]["M2"]
        ec3 = e3 + su3 + surface / data["speed"]["M3"]
        if n == 4:
            ec4 = e4 + su4 + surface / data["speed"]["M4"]
        else:
            ec4 = float("inf")

        if ec1 == min(ec1, ec2, ec3, ec4):
            ma1.append(ord_nr)
            e1 = ec1
        elif ec2 == min(ec1, ec2, ec3, ec4):
            ma2.append(ord_nr)
            e2 = ec2
        elif ec3 == min(ec1, ec2, ec3, ec4):
            ma3.append(ord_nr)
            e3 = ec3
        else:
            ma4.append(ord_nr)
            e4 = ec4

    greedy_schema = [ma1, ma2, ma3]
    if n == 4:
        greedy_schema.append(ma4)

    return greedy_schema
