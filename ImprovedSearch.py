import random
import copy

from functies import pen_cost

# Improved search
def improving_search(data: dict, beste_schema: list, iteraties: int):
    machines = copy.deepcopy(beste_schema)   
    huidige = pen_cost(data, machines)
    best = huidige
    improved_schema = copy.deepcopy(machines)

    for i in range(iteraties):
        machine1 = random.choice(machines)
        machine2 = random.choice(machines)
        swap1 = random.choice(machine1)
        swap2 = random.choice(machine2)
        i1 = machine1.index(swap1)
        i2 = machine2.index(swap2)
        machine1[i1] = swap2
        machine2[i2] = swap1

        kandidaat = pen_cost(data, machines)
        if kandidaat < huidige:  # geaccepteerd
            huidige = kandidaat
            if kandidaat < best:
                best = kandidaat
                improved_schema = copy.deepcopy(machines)
        else:  # niet geaccepteerd
            machine1[i1] = swap1
            machine2[i2] = swap2

    print(f'Improved penalty cost: {best:.2f}')
    for nr, m in enumerate(improved_schema, start=1):
        print(f'Machine {nr}: {m}\n')

    return improved_schema, best

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
