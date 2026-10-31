import copy

from functies import pen_cost

# Improved search
def improving_search(data: dict, beste_schema: list):
    machines = copy.deepcopy(beste_schema)   
    huidige = pen_cost(data, machines)
    
    lokaal_opt = True
    while lokaal_opt: #blijft doorgaan zolang de vorige ronde een verbetering vond
        lokaal_opt = False
        for m1 in range(len(machines)):
            for o1 in range(len(machines[m1])):
                for m2 in range(m1, len(machines)):
                    start = o1 + 1 if m2 == m1 else 0
                    for o2 in range(start, len(machines[m2])):
                        machine1 = machines[m1]
                        machine2 = machines[m2]
                        swap1 = machine1[o1]
                        swap2 = machine2[o2]
                        machine1[o1] = swap2
                        machine2[o2] = swap1

                        kandidaat = pen_cost(data, machines)
                        if kandidaat < huidige:   # geaccepteerd
                            huidige = kandidaat
                            lokaal_opt = True
                        else:                     # niet geaccepteerd
                            machine1[o1] = swap1
                            machine2[o2] = swap2

    return machines, huidige

    # print(f'Improved penalty cost: {best:.2f}')
    # for nr, m in enumerate(improved_schema, start=1):
    #     print(f'Machine {nr}: {m}\n')


# bouw_gantt(ma1, ma2, ma3) 



# print('Beste indeling:')
# print(f'Machine 1: {ma1}')
# print(f'Machine 2: {ma2}')
# print(f'Machine 3: {ma3}')
# print(f'Beste schema penalty kosten: {best:.2f}')

# gantt_df = pd.DataFrame.from_dict(gantt_rows)

# machines_labels = ["M1", "M2", "M3"]
# fig, ax = plt.subplots(figsize=(12, 4))

# for x, r in gantt_df.iterrows():
#     y = machines_labels.index(r["Machine"])
#     if r["Einde setup"] > r["Start setup"]:
#         ax.broken_barh([(r["Start setup"], r["Einde setup"] - r["Start setup"])],
#                        (y - 0.4, 0.8), facecolors="tab:purple")
#     ax.broken_barh([(r["Start order"], r["Einde order"] - r["Start order"])],
#                    (y - 0.4, 0.8), facecolors="tab:cyan", edgecolor="white")
#     ax.text((r["Start order"] + r["Einde order"]) / 2, y, r["Label"],
#             ha="center", va="center", color="black", fontsize=7)

# ax.set_yticks(range(len(machines_labels)))
# ax.set_yticklabels(machines_labels)
# ax.set_xlabel("Tijd")
# ax.legend(handles=[
#     Patch(facecolor="tab:purple", label="Setup"),
#     Patch(facecolor="tab:cyan", label="Order"),
# ])
# plt.show()
