import pandas as pd
import random as rand
import time

startTime = time.time()

cards = pd.read_csv("https://raw.githubusercontent.com/gregknothe/OBS-Stuff-v2/refs/heads/main/cardGamble/finalFile.csv", sep="|")
cards["owner"] = ""

ownedCards = pd.DataFrame(columns=["name", "id", "rarity", "imgURL", "setID", "game", "set", "date", "owner"])

downloadTime = time.time()

def drawCards(user):
    unownedCards = cards[cards["owner"]==""]
    newCards = rand.sample(list(unownedCards.index), 5)
    for card in newCards:
        cards.at[card, "owner"] = user
        ownedCards.loc[len(ownedCards)] = list(cards.loc[card])
    ownedCards.to_csv("cardBackup.csv", sep="|", index=False)
    return

def saveCards():
    cards.to_csv("finalFile.csv", sep="|", index=False)
    return

drawCards("asome")
#drawCards("monte")
#drawCards("claire")
#print(cards[cards["owner"]!=""].sort_values(by="owner"))
saveCards()

drawTime = time.time()

print(ownedCards)

print("download time: " + str(downloadTime-startTime))
print("draw time: " + str(drawTime-downloadTime))