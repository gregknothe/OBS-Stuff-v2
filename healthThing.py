import pandas as pd

name = ["sol", "ky", "may", "axl", "chipp", "pot", "faust", "millia", "zato", "ram", "leo", "nago", 
        "gio", "anji", "ino", "gold", "jacko", "chaos", "baiken", "test", "bridget", "sin", "bed", "asuka (shield)", "asuka", 
        "johnny", "elphelt", "aba", "slayer", "dizzy"]
oldEHP = [541, 533, 533, 481, 447, 585, 499, 449, 470, 488, 548, 585, 503, 552, 488, 570, 477, 499,
          507, 496, 477, 505, 527, 676, 338, 557, 487, 559, 566, 536]
newDef = [.93, .95, 1, 1.03, 1.18, .87, .96, 1.14, 1.01, 1, .95, .92, .98, 1,
          1.01, .89, 1.06, 1.01, 1.04, .98, 1.07, .96, .82, .75, 1.5, .93, 1.04,
          .9, .92, 1.09]
newGuts = [2,2,4,1,4,4,0,2,0,1,3,3,1,5,1,3,2,0,4,1,2,3,0,0,0,3,2,2,1,5]

zero = [.97, .92, .89, .84, .75, .66, .56]
one = [.96, .91, .87, .82, .73, .63, .53]
two = [.95, .90, .85, .80, .70, .60, .50]
three = [.94, .80, .83, .78, .67, .57, .47]
four = [.93, .88, .81, .76, .64, .53, .44]
five = [.92, .87, .79, .74, .60, .50, .41]

def getGutsValue(gut, stage):
        if gut == 0:
            match stage:
                case 100: return 1
                case 70: return zero[0]
                case 60: return zero[1]
                case 50: return zero[2]
                case 40: return zero[3]
                case 30: return zero[4]
                case 20: return zero[5]
                case 10: return zero[6]
        if gut == 1: 
            match stage:
                case 100: return 1
                case 70: return one[0]
                case 60: return one[1]
                case 50: return one[2]
                case 40: return one[3]
                case 30: return one[4]
                case 20: return one[5]
                case 10: return one[6]
        if gut == 2:
            match stage:
                case 100: return 1
                case 70: return two[0]
                case 60: return two[1]
                case 50: return two[2]
                case 40: return two[3]
                case 30: return two[4]
                case 20: return two[5]
                case 10: return two[6]
        if gut == 3:
            match stage:
                case 100: return 1
                case 70: return three[0]
                case 60: return three[1]
                case 50: return three[2]
                case 40: return three[3]
                case 30: return three[4]
                case 20: return three[5]
                case 10: return three[6]
        if gut == 4:
            match stage:
                case 100: return 1
                case 70: return four[0]
                case 60: return four[1]
                case 50: return four[2]
                case 40: return four[3]
                case 30: return four[4]
                case 20: return four[5]
                case 10: return four[6]
        if gut == 5:
            match stage:
                case 100: return 1
                case 70: return five[0]
                case 60: return five[1]
                case 50: return five[2]
                case 40: return five[3]
                case 30: return five[4]
                case 20: return five[5]
                case 10: return five[6]
        
ehp = []
for x in range(len(newDef)):
    y1 = (420 * .3) / (getGutsValue(newGuts[x], 100)* newDef[x])
    y2 = (420 * .1) / (getGutsValue(newGuts[x], 70)* newDef[x])
    y3 = (420 * .1) / (getGutsValue(newGuts[x], 60)* newDef[x])
    y4 = (420 * .1) / (getGutsValue(newGuts[x], 50)* newDef[x])
    y5 = (420 * .1) / (getGutsValue(newGuts[x], 40)* newDef[x])
    y6 = (420 * .1) / (getGutsValue(newGuts[x], 30)* newDef[x])
    y7 = (420 * .1) / (getGutsValue(newGuts[x], 20)* newDef[x])
    y8 = (420 * .1) / (getGutsValue(newGuts[x], 10)* newDef[x])
    yx = y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8
    ehp.append(yx)

df = pd.DataFrame({"name": name, "oldehp": oldEHP, "ehp": ehp})
df["diffEHP"] = df["ehp"] - df["oldehp"] 
        
d = 1.06
q = 126/(d * getGutsValue(5, 100))
r = 42/(d * getGutsValue(5, 70))
t = 42/(d * getGutsValue(5, 60))
y = 42/(d * getGutsValue(5, 50))
u = 42/(d * getGutsValue(5, 40))
i = 42/(d * getGutsValue(5, 30))
o = 42/(d * getGutsValue(5, 20))
p = 42/(d * getGutsValue(5, 10))

j = q + r + t + y + u + i + o + p

print(df.sort_values(by=["ehp"], ascending=False))



