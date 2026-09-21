import pandas as pd
print('\033c')

dfo = pd.read_excel('PaintShop - September 2026.xlsx', 'Orders')
dfm = pd.read_excel('PaintShop - September 2026.xlsx', 'Machines')
dfs = pd.read_excel('PaintShop - September 2026.xlsx', 'Setups')
print(dfm.head())
print(dfs.head(12))

dfo = dfo.sort_values(by=["Deadline"], ascending=True)
print(dfo.head(10), '\n')

#for i in dfo.index:hooiiii
