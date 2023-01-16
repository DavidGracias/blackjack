import modules.Blackjack as Blackjack

from os.path import exists
filename = "main"
path = "strategies/" + filename

import pandas as pd

if True or not (exists(path+"_hard.csv") and exists(path+"_soft.csv") and exists(path+"_pair.csv")):
    columns = range(1, 10+1)
    hard    = pd.DataFrame(columns=columns, index=range(5, 20+1))
    soft    = pd.DataFrame(columns=columns, index=range(2, 10+1))
    pair    = pd.DataFrame(columns=columns, index=range(1, 10+1))

    for df in [hard, soft, pair]:
        for ind in df.index:
            for col in df.columns: df.loc[ind][col] = ( (0,0), (0,0), (0,0), (0,0))

    hard.to_csv(path+"_hard.csv")
    soft.to_csv(path+"_soft.csv")
    pair.to_csv(path+"_pair.csv")



# strategies:
hard = pd.read_csv(path+"_hard.csv", index_col=0)
soft = pd.read_csv(path+"_soft.csv", index_col=0)
pair = pd.read_csv(path+"_pair.csv", index_col=0)

strats = [hard, soft, pair]
for df in strats:
    for ind in df.index:
        for col in df.columns: df.loc[ind][col] = eval(df.loc[ind][col])

game = Blackjack.Blackjack(isSim=(path, strats))
game.addPlayer("Bot")

mult = 1
while True:

    game.newRound()

    if game.numRounds % int(1e5) == 0:
        # print(f"{mult}0k simulations ran")
        
        strats[0].to_csv(path+"_hard.csv")
        strats[1].to_csv(path+"_soft.csv")
        strats[2].to_csv(path+"_pair.csv")

        mult += 1
    
    # if game.numRounds % int(1e6) == 0:
    #     break