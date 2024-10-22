from twitchio.ext import commands, eventsub
from twitchio.client import Client
import pandas as pd
import random as rand
import time
#--------------------------------Setup Code-----------------------------------------#
gl = pd.read_csv("https://raw.githubusercontent.com/gregknothe/OBS-Stuff/refs/heads/main/finalGameList.csv", sep="|")
rgl = pd.read_csv("https://raw.githubusercontent.com/GGSTFrameTrap/gameList/main/ranceGameList.csv", sep = "|")
mgl = pd.read_csv("https://raw.githubusercontent.com/gregknothe/OBS-Stuff/refs/heads/main/monuGameList.csv", sep="|")

cards = pd.read_csv()

heyList = []
modList = ["lastclaire", "greedx___", "asome26", "nastyplot", "botthewoz", "frendweeb", "gdom", "redditto", "sajam", "wooper_enthusiast",
           "joshgrilli", "sindercenpai", "hotashi", "linkl0nk", "chris_re5", "voidashe", "the_doc_", "abusywitch", "lament_03", "kyluneena",
           "jackpotfm", "nastyplot", "nbnhmr", "ailubee", "meowzykat", "squirrel147"]    

currTimeStamp = time.time()
cooldown = 6


#---------------------------------"Python" Code-------------------------------------#
def ohHey(username):
    if username == "life_jam":
        x = rand.randint(0,len(rgl.index))
        title, year, plat, img, rarity = rgl["name"][x], rgl["year2"][x], rgl["platform"][x], rgl["img"][x], rgl["rarity"][x]
        chatText = "Hey alright, it's my favorite " + title + " (" + plat[:25] + " " + str(int(year)) + ") streamer @" + username
    elif username == "monuminn":
        x = rand.randint(0,len(mgl.index))
        title, year, plat, img, rarity = mgl["name"][x], mgl["year2"][x], mgl["platform"][x], mgl["img"][x], mgl["rarity"][x]
        chatText = "Oh hey, it's my favorite " + title + " (" + plat[:25] + " " + str(int(year)) + ") streamer @" + username
    else:
        x = rand.randint(0,len(gl.index))
        title, year, plat, img, rarity = gl["name"][x], gl["year2"][x], gl["platform"][x], gl["img"][x], gl["rarity"][x]
        chatText = "Oh hey, it's my favorite " + title + " (" + plat[:25] + " " + str(int(year)) + ") streamer @" + username
    return title, img, rarity, chatText


#----------------------------------Chat Bot Code------------------------------------#
bot = commands.Bot(
    token='oauth:0nyov8e54o2d1ezitbcnvcbznrafcy',
    client_id=['hq2jby4wfk8p1rd2igt88y0wm0160i'],
    nick=['botthewoz'],
    prefix=['!'],
    initial_channels=['botthewoz']
)

@bot.command(name="hey", aliases=("Hey", "HEY"))
async def hey(ctx):
    global currTimeStamp
    if ctx.author.name not in heyList:
        if time.time() - currTimeStamp >= cooldown:
            await ctx.send(ohHey(ctx.author.name)[3])
            heyList.append(ctx.author.name)
            currTimeStamp = time.time()
        else:
            await ctx.send("!hey is on cooldown.🐛")
    else:
        await ctx.send("You already used your !hey. @" + ctx.author.name)
    return

@bot.command(name="hr")
async def heyRemove(ctx, *, text):
    if ctx.author.name in modList:
        try:
            heyList.remove(text.lower())
            await ctx.send("@" + text.lower() + " has been given another !hey.")
        except:
            await ctx.send("Something went wrong.😔")

if __name__ == "__main__":
    bot.run()

#---------------------------------OBS Code------------------------------------------#