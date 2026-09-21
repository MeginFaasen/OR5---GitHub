import pandas as pd
print('\033c')

dfo = pd.read_excel('PaintShop - September 2026.xlsx', 'Orders')
dfm = pd.read_excel('PaintShop - September 2026.xlsx', 'Machines')
dfs = pd.read_excel('PaintShop - September 2026.xlsx', 'Setups')
print(dfm.head())
print(dfs.head(12))

dfo = dfo.sort_values(by=["Deadline"], ascending=True)
print(dfo.head(10), '\n')
e1 = 0
e2 = 0
e3 = 0
ma1 = []
ma2 = []
ma3 = []

for i in dfo.index:
    ec1 = e1 + (dfo.loc[i, "Surface"]/dfm.loc[0, "Speed"]) #+ setuptijd
    ec2 = e2 + (dfo.loc[i, "Surface"]/dfm.loc[1, "Speed"]) #+ setuptijd
    ec3 = e3 + (dfo.loc[i, "Surface"]/dfm.loc[2, "Speed"]) #+ setuptijd
    if ec1 == min(ec1, ec2, ec3):
        ma1.append(dfo.loc[i, "Order"])
        e1 += ec1
    elif ec2 ==min(ec1, ec2, ec3):
        ma2.append(dfo.loc[i, "Order"])
        e2 += ec2
    else:
        ma3.append(dfo.loc[i, "Order"])
        e3 += ec3
print(f'Machine 1: {ma1} \n')
print(f'Machine 2: {ma2} \n')
print(f'Machine 3: {ma3} \n')

# eindtijd = eindtijd + surface/machinatijd + setuptijd