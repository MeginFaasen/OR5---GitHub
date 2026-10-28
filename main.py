from functies import laad_data, pen_cost, plot_SA, export_excel
from GreedyHeuristic import greedy_EDD
from SimulatedAnnaeling import random_indelen, simulated_annealing
from ImprovedSearch import improving_search
from experiment import experiment_su
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

    #experiment zo min mogelijk setuptijd
    experiment_schema = experiment_su(data)
    print(f'Experiment setuptijd penalty: {pen_cost(data, experiment_schema):.2f}')

    #experiment -> Improved search
    experiment_improved, experiment_improved_pen = improving_search(data, experiment_schema, iteraties=1000)
    print(f'experiment + DIS penalty: {experiment_improved_pen:.2f}')

    # experiment -> simulated annealing
    exp_sa_schema, exp_sa_pen, huidige_lijst, best_lijst, T_lijst = simulated_annealing(
    data, experiment_schema, T=500, iteraties=5000, alpha=0.999
    )
    print(f'SA penalty: {exp_sa_pen:.2f}')
    plot_SA(huidige_lijst, best_lijst, T_lijst)

    #het aller beste schema zoeken
    beste_pen = min(
        pen_cost(data, greedy_schema),
        pen_cost(data, greedy_improved), 
        pen_cost(data, sa_schema), 
        pen_cost(data, sa_improved),
        pen_cost(data, experiment_schema), 
        pen_cost(data, experiment_improved),
        pen_cost(data, exp_sa_schema),
        )
    if beste_pen == pen_cost(data, greedy_schema):
        beste_schema = greedy_schema
        print(f'Het beste schema is geworden: Greedy!')
    elif beste_pen == pen_cost(data, greedy_improved):
        beste_schema = greedy_improved
        print(f'Het beste schema is geworden: Greedy improved!')
    elif beste_pen == pen_cost(data, sa_schema):
        beste_schema = sa_schema
        print(f'Het beste schema is geworden: simulated annealing!')
    elif beste_pen == pen_cost(data, sa_improved):
        beste_schema = sa_improved
        print(f'Het beste schema is geworden: simaluted improved!')
    elif beste_pen == pen_cost(data, experiment_schema):
        beste_schema = experiment_schema
        print(f'Het beste schema is geworden: experiment minste setuptijd!')
    elif beste_pen == experiment_improved_pen:
        beste_schema = experiment_improved
        print(f'Het beste schema is geworden: experiment minste setuptijd improved search!')
    else:
        beste_schema = exp_sa_schema
        print(f'Het beste schema is geworden: experiment minste setuptijd en dan nog SA!')
    export_excel(data, beste_schema, bestand)

    return greedy_schema, greedy_improved, sa_schema, sa_improved, experiment_schema, experiment_improved

if __name__ == "__main__": # wordt ALLEEN uitgevoerd als je main.py zelf start
    main('PaintShop - November 2026.xlsx')   
    # main('PaintShop - September 2026.xlsx')