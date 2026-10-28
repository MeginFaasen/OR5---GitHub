from functies import setuptijd

# # Voorbeireiding (dictionary voor) Gantt Chart, penalty cost & functies
# gantt_rows = []


# def voeg_toe(machine_naam, begin, su, einde, order_naam):
#     """Slaat het setup-blok en het order-blok van één order op voor de Gantt-chart."""
#     gantt_rows.append({
#         "Machine": machine_naam,
#         "Start setup": begin,
#         "Einde setup": begin + su,
#         "Start order": begin + su,
#         "Einde order": einde,
#         "Label": order_naam,
#     })

# # total_pen = 0

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

# print(f'Machine 1: {ma1} \n')
# print(f'Machine 2: {ma2} \n')
# print(f'Machine 3: {ma3} \n')
# if len(dfm) == 4:
#     print(f'Machine 4: {ma4} \n')
# print(f'Totale penalty kosten greedy rule 1: {pen_cost(greedy_schema) :.2f}')

# # Schema visualiseren
# gantt_df = pd.DataFrame.from_dict(gantt_rows)

# machines = ["M1", "M2", "M3"]
# if len(dfm) == 4:
#     machines.append("M4")
# beste_schema1 = [ma1, ma2, ma3]
# if len(dfm) == 4:
#     beste_schema1.append(ma4)
# fig, ax = plt.subplots(figsize=(4 * len(dfo), len(dfo) + 1))

# for x, r in gantt_df.iterrows():
#     y = machines.index(r["Machine"])
#     if r["Einde setup"] > r["Start setup"]:
#         ax.broken_barh([(r["Start setup"], r["Einde setup"] - r["Start setup"])],
#                        (y - 0.4, 0.8), facecolors="tab:purple")
#     ax.broken_barh([(r["Start order"], r["Einde order"] - r["Start order"])],
#                    (y - 0.4, 0.8), facecolors="tab:cyan", edgecolor="white")
#     ax.text((r["Start order"] + r["Einde order"]) / 2, y, r["Label"],
#             ha="center", va="center", color="black", fontsize=7)

# ax.set_yticks(range(len(machines)))
# ax.set_yticklabels(machines)
# ax.set_xlabel("Tijd")
# ax.legend(handles=[
#     Patch(facecolor="tab:purple", label="Setup"),
#     Patch(facecolor="tab:cyan", label="Order"),
# ])
# plt.show()