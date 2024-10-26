import pandas as pd
import os

def userCardFiles():
    df = pd.read_csv("cardList.csv", sep="|",).fillna("")
    for user in list(df["owner"].unique()):
        print(user)
        userDF = df[df["owner"]==user]
        userDF.to_csv("E:/Various Programs/Coding Projects/OBS Stuff v2/userDataFrames/"+user+".csv", sep="|", header=False)
    return

userCardFiles()