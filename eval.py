
filename = "main"
path = "strategies/" + filename

import pandas as pd

# strategies:
hard = pd.read_csv(path+"_hard.csv", index_col=0)
soft = pd.read_csv(path+"_soft.csv", index_col=0)
pair = pd.read_csv(path+"_pair.csv", index_col=0)

strats = [hard, soft, pair]
for df in strats:
    for ind in df.index:
        for col in df.columns: df.loc[ind][col] = eval(df.loc[ind][col])