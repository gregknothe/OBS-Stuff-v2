import pandas as pd
import os

def userCardFiles():
    df = pd.read_csv("cardList.csv", sep="|",).fillna("")
    userList = []
    for user in list(df["owner"].unique()):
        print(user)
        userList.append(user)
        userDF = df[df["owner"]==user]
        userDF.to_csv("E:/Various Programs/Coding Projects/OBS Stuff v2/userDataFrames/"+user+".csv", sep="|", header=False, index=False)
    userListDF = pd.DataFrame(filter(None, userList))
    userListDF.to_csv("E:/Various Programs/Coding Projects/OBS Stuff v2/userDataFrames/userList.csv", sep="|", header=False, index=False)
    return

userCardFiles()