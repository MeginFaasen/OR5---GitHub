from functies import laad_data, pen_cost, plot_SA, export_excel
from GreedyHeuristic import greedy_EDD
from SimulatedAnnaeling import random_indelen, simulated_annealing
from ImprovedSearch import improving_search
print('\033c')

def main(bestand):
    data = laad_data(bestand)

    #Greedy Heuristiek
    greedy_schema = greedy_EDD(data)
    print(f'Greedy penalty: {pen_cost(data, greedy_schema):.2f}')

    #Greedy -> Improved search
    greedy_improved, greedy_improved_pen = improving_search(data, greedy_schema, iteraties=1000)
    print(f'Greedy + DIS penalty: {greedy_improved_pen:.2f}')

    #Simulated Annealing
    random_schema = random_indelen(data)
    sa_schema, sa_pen, huidige_lijst, best_lijst, T_lijst = simulated_annealing(
        data, random_schema, T=500, iteraties=5000, alpha=0.999
    )
    print(f'SA penalty: {sa_pen:.2f}')
    plot_SA(huidige_lijst, best_lijst, T_lijst)

    #Simulated annealing -> improved search
    sa_improved, sa_improved_pen = improving_search(data, sa_schema, iteraties=1000)
    print(f'SA + DIS penalty: {sa_improved_pen:.2f}')

    #het aller beste schema zoeken
    beste_pen = min(pen_cost(data, greedy_schema), pen_cost(data, greedy_improved), pen_cost(data, sa_schema), pen_cost(data, sa_improved))
    if beste_pen == pen_cost(data, greedy_schema):
        beste_schema = greedy_schema
        print(f'Het beste schema is geworden: Greedy!')
    if beste_pen == pen_cost(data, greedy_improved):
        beste_schema = greedy_improved
        print(f'Het beste schema is geworden: Greedy improved!')
    if beste_pen == pen_cost(data, sa_schema):
        beste_schema = sa_schema
        print(f'Het beste schema is geworden: simulated annealing!')
    if beste_pen == pen_cost(data, sa_improved):
        beste_schema = sa_improved
        print(f'Het beste schema is geworden: simaluted improved!')
    

    export_excel(data, beste_schema, bestand)

    return greedy_schema, greedy_improved, sa_schema, sa_improved

if __name__ == "__main__": # wordt ALLEEN uitgevoerd als je main.py zelf start
    main('PaintShop - November 2026.xlsx')   
    # main('PaintShop - September 2026.xlsx')