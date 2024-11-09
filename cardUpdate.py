import pandas as pd
import os

def userCardFiles():
    df = pd.read_csv("cardList.csv", sep="|",).fillna("")
    userList = []
    uniqueUser = list(df["owner"].unique())
    uniqueUser = filter(None, uniqueUser)
    for user in uniqueUser:
        print(user)
        userList.append(user)
        userDF = df[df["owner"]==user]
        userDF.to_csv("E:/Various Programs/Coding Projects/OBS Stuff v2/userDataFrames/"+user+".csv", sep="|", header=False, index=False)
    userListDF = pd.DataFrame(filter(None, userList))
    userListDF.to_csv("E:/Various Programs/Coding Projects/OBS Stuff v2/userDataFrames/userList.csv", sep="|", header=False, index=False)
    return

userCardFiles()

#df = pd.read_csv("cardList.csv", sep="|").fillna("")
#df["id"] = df["id"].astype("int")
#print(df)

#print(df.index[df.index == 119446])
#print(df["owner"][21166])
