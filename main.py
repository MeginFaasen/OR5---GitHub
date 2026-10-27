import pandas as pd
import math
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import random
import copy

from functies import plot_SA
from GreedyHeuristic import greedy_EDD
print('\033c')

# Inladen van de Excel-sheets met 4 machines
dfo = pd.read_excel('PaintShop - November 2026.xlsx', 'Orders')
dfm = pd.read_excel('PaintShop - November 2026.xlsx', 'Machines')
dfs = pd.read_excel('PaintShop - November 2026.xlsx', 'Setups')

# # Inladen van de Excel-sheets met 3 machines
# dfo = pd.read_excel('PaintShop - September 2026.xlsx', 'Orders')
# dfm = pd.read_excel('PaintShop - September 2026.xlsx', 'Machines')
# dfs = pd.read_excel('PaintShop - September 2026.xlsx', 'Setups')

# Voor sneller werk
surface_dict = dict(zip(dfo["Order"], dfo["Surface"]))
color_dict = dict(zip(dfo["Order"], dfo["Colour"]))
deadline_dict = dict(zip(dfo["Order"], dfo["Deadline"]))
penalty_dict = dict(zip(dfo["Order"], dfo["Penalty"]))
speed_dict = dict(zip(dfm["Machine"], dfm["Speed"]))

ma1 = []
ma2 = []
ma3 = []
if len(dfm)==4:
    ma4 = []
def main():
    greedy_EDD()

if __name__ == "__main__":
    main('PaintShop - November 2026.xlsx')   # wordt ALLEEN uitgevoerd als je main.py zelf start
    # main('PaintShop - September 2026.xlsx')