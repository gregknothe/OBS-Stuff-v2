import pandas as pd

cards = pd.read_csv("https://raw.githubusercontent.com/gregknothe/OBS-Stuff-v2/refs/heads/main/cardList.csv", sep="|").fillna("")
cards.at[1, "owner"] = "BotTheWoz"

owner1 = cards.iloc[1]["owner"]
print(owner1)
