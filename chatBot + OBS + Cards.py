from twitchio.ext import commands, eventsub
from twitchio.client import Client
import pandas as pd
import random as rand
import time
import obspython as obs
import threading
import sys 

#--------------------------------Setup Code-----------------------------------------#
gl = pd.read_csv("https://raw.githubusercontent.com/gregknothe/OBS-Stuff/refs/heads/main/finalGameList.csv", sep="|")
rgl = pd.read_csv("https://raw.githubusercontent.com/GGSTFrameTrap/gameList/main/ranceGameList.csv", sep = "|")
mgl = pd.read_csv("https://raw.githubusercontent.com/gregknothe/OBS-Stuff/refs/heads/main/monuGameList.csv", sep="|")
cards = pd.read_csv("https://raw.githubusercontent.com/gregknothe/OBS-Stuff-v2/refs/heads/main/cardList.csv", sep="|").fillna("")
#cards = pd.read_csv("https://raw.githubusercontent.com/gregknothe/OBS-Stuff-v2/refs/heads/main/smallCardList.csv", sep="|").fillna("")
cards["id"] = cards["id"].astype(int)

ownedCards = pd.DataFrame(columns=["name", "id", "rarity", "imgURL", "setID", "game", "set", "date", "owner", "fav", "rawID"])

silver = r"C:\Users\Greg Knothe\Desktop\silverClaireAnimated.gif"
gold = r"C:\Users\Greg Knothe\Desktop\silverClaireAnimated.gif"
rainbow = r"C:\Users\Greg Knothe\Desktop\silverClaireAnimated.gif"
rance = r"C:\Users\Greg Knothe\Desktop\silverClaireAnimated.gif"

heyList = []
packList = []
modList = ["lastclaire", "greedx___", "asome26", "nastyplot", "botthewoz", "frendweeb", "gdom", "redditto", "sajam", "wooper_enthusiast",
           "joshgrilli", "sindercenpai", "hotashi", "linkl0nk", "chris_re5", "voidashe", "the_doc_", "abusywitch", "lament_03", "kyluneena",
           "jackpotfm", "nastyplot", "nbnhmr", "ailubee", "meowzykat", "squirrel147"]    

heyTimeStamp = time.time()
cooldown = 6
durration = 5

packTimeStamp = time.time()
cooldown2 = 7
durration2 = 6
packSize = 5
cardDurr = 2

hotkey_id = obs.OBS_INVALID_HOTKEY_ID

#Supresses error outputs (happens when someone types something other than !hey, so they kinda needa go tbh)
#class DevNull:
#    def write(self, msg):
#        pass
#sys.stderr = DevNull()

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

def drawCards(username):
    global cards
    global ownedCards
    unownedCards = cards[cards["owner"]==""]
    newCards = rand.sample(list(unownedCards.index), packSize)
    imgList = []
    for card in newCards:
        cards.at[card, "owner"] = username
        print(cards.columns)
        print(ownedCards.columns)
        ownedCards.loc[len(ownedCards)] = list(cards.loc[card])
        imgList.append(cards.loc[card, "imgURL"])
    ownedCards.to_csv("E:\Various Programs\Coding Projects\OBS Stuff v2\cardBackup.csv", sep="|", index=False)
    newCards = [x + 1 for x in newCards]
    cardString = ",".join(str(x) for x in newCards).replace(",", "%2C")
    return cardString, imgList[0], imgList[1], imgList[2], imgList[3], imgList[4]

def saveCards():
    global cards
    #cards.to_csv("E:/Various Programs/Coding Projects/OBS Stuff v2/cardList.csv", sep="|", index=False)
    cards.to_csv("E:/Various Programs/Coding Projects/OBS Stuff v2/cardList.csv", sep="|", index=False)
    return

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
    global heyTimeStamp
    if ctx.author.name not in heyList:
        if time.time() - heyTimeStamp >= cooldown:
            data = ohHey(ctx.author.name)
            await ctx.send(data[3])
            heyList.append(ctx.author.name)
            heyTimeStamp = time.time()
            display_game(data[0], data[1], data[2], ctx.author.name)
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

@bot.command(name="pack")
async def openCardPack(ctx):
    global packTimeStamp
    if ctx.author.name not in packList:
        if time.time() - packTimeStamp >= cooldown2:
            cards = drawCards(ctx.author.name)
            display_card(cards[1], cards[2], cards[3], cards[4], cards[5], ctx.author.name)
            packList.append(ctx.author.name)
            packTimeStamp = time.time()
            await ctx.send("Click to view your cards: gregknothe.github.io/OBS-Stuff-v2/g?i="+ cards[0] + " @" + ctx.author.name)
        else: 
            await ctx.send("!pack is on cooldown.🐛")
    else: 
        await ctx.send("You already used your !pack. @" + ctx.author.name)
    return

@bot.command(name="pr")
async def packRemove(ctx, *, text):
    if ctx.author.name in modList:
        try:
            packList.remove(text.lower())
            await ctx.send("@" + text.lower() + " has been given another !pack.")
        except:
            await ctx.send("Something went wrong.😔")

@bot.command(name="fav")
async def favoriteCard(ctx, *, text):
    global cards
    text = text.split(" ")
    #print(int(text[0]))
    #print(type(int(text[0])))
    #print(cards["id"][1])
    #print(type(cards["id"][1]))
    #print(339981 == cards["id"][1])
    #print(cards.index[cards["id"]==int(text[0])][0])
    #await ctx.send(currIndex)
    #await ctx.send(cards["name"][2])
    #print(cards.loc[cards["id"] == int(text[0]), "owner"].values[0])
    try: 
        if int(text[1]) not in [1,2,3,4,5]:
            await ctx.send("Invalid Favorite Value: must be between 1 and 5.")
            return
    except:
        await ctx.send("You forgot to add a Favorite Value (between 1 and 5).")
        return
    print(ctx.author.name)
    print(text[0])
    print(cards["owner"][int(text[0])-1])
    try:
        if ctx.author.name == str(cards["owner"][int(text[0])-1]):
            ownedCards = cards[cards["owner"]==ctx.author.name]
            try:
                favCard = ownedCards[ownedCards["fav"]==int(text[1])]
                await ctx.send("Card being overwritten: " + str(favCard.index[0]))
                cards.loc[int(favCard.index[0]), "fav"] = 0
            except:
                await ctx.send("Value not already saved.")
            cards.loc[int(text[0])-1, "fav"] = int(text[1])
            await ctx.send("["+ str(text[0]) + "] " + str(cards["name"][int(text[0])-1]) + " has been set to Fav #" + str(text[1]) + ".")
        else:
            await ctx.send("You do not own that card.🐛")
    except:
        await ctx.send("Something went wrong.😔")

@bot.command(name="trade")
async def trade(ctx, *, text):
    try:
        if ctx.author.name in modList:
            id1 = int(text.split(" ")[0])-1
            id2 = int(text.split(" ")[1])-1
            #print(id1)
            #print(id2)
            owner1 = cards.iloc[id1]["owner"]
            owner2 = cards.iloc[id2]["owner"]
            #print(owner1)
            #print(owner2)
            cards.at[id1, "owner"] = owner2
            cards.at[id2, "owner"] = owner1
            cards.at[id1, "fav"] = 0
            cards.at[id2, "fav"] = 0
            #print(cards.at[id1, "owner"])
            #print(cards.at[id2, "owner"])
            await ctx.send("trade: (" + owner1 + ") " + str(id1+1) + " <-> (" + owner2 + ") " + str(id2+1))
    except:
        await ctx.send("Something went wrong.😔")
    

@bot.command(name="save")
async def saveFile(ctx):
    if ctx.author.name in modList:
        saveCards()
        await ctx.send("Card file saved. PogChamp")
    return

if __name__ == "__main__":
    bot.run()

#---------------------------------OBS Code------------------------------------------#
def display_game(title, img, rarity, username):

    #Getting required info from !hey command.
    settings = obs.obs_data_create()
    scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())

    #Updating the gacha.
    raritySource = obs.obs_get_source_by_name("gachaRarity")
    if rarity == "silver":
        obs.obs_data_set_string(settings, "file", silver)
    elif rarity == "gold":
        obs.obs_data_set_string(settings, "file", gold)
    elif rarity == "rainbow":
        obs.obs_data_set_string(settings, "file", rainbow)
    else:
        obs.obs_data_set_string(settings, "file", rance)

    obs.obs_source_update(raritySource, settings)

    #Updating the Title.
    titleSource = obs.obs_get_source_by_name("titleText")
    obs.obs_data_set_string(settings, "text", title)
    obs.obs_source_update(titleSource, settings)

    #Updating the Game Image.
    imgSource = obs.obs_get_source_by_name("gameImage")
    obs.obs_data_set_string(settings, "url", img)
    obs.obs_source_update(imgSource, settings)

    #Updating the User Name.
    userSource = obs.obs_get_source_by_name("usernameText")
    obs.obs_data_set_string(settings, "text", username)
    obs.obs_source_update(userSource, settings)

    #Hopefully plays the shenmue sound
    pullSource = obs.obs_get_source_by_name("pullSound")
    obs.obs_source_media_play_pause(pullSource, True)

    #Toggling the visibility of the group with a wait statement inbetween.
    groupSource = obs.obs_get_source_by_name("ohHeyGroup")
    group = obs.obs_scene_sceneitem_from_source(scene, groupSource)
    obs.obs_sceneitem_set_visible(group, True)

    #Hides the visuals after set durration time.
    def hide_group():
        obs.obs_sceneitem_set_visible(group, False)

        #Releasing the sources.
        obs.obs_data_release(settings)
        obs.obs_source_release(raritySource)
        obs.obs_source_release(titleSource)
        obs.obs_source_release(imgSource)
        obs.obs_source_release(userSource)
        obs.obs_source_release(groupSource)
        obs.obs_source_release(pullSource)
        obs.obs_scene_release(scene)

    threading.Timer(durration, hide_group).start()


def correctURL(url):
    if "https://api.ccgtrader.co.uk/" in url:
        return url + "?key=card-medium"
    else: 
        return url

def display_card(img1, img2, img3, img4, img5, username):

    #Getting required info from !pack command.
    settings = obs.obs_data_create()
    scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())

    #Updating the card1 Image.
    imgSource1= obs.obs_get_source_by_name("card1")
    obs.obs_data_set_string(settings, "url", correctURL(img1))
    obs.obs_source_update(imgSource1, settings)

    #Updating the card2 Image.
    imgSource2 = obs.obs_get_source_by_name("card2")
    obs.obs_data_set_string(settings, "url", correctURL(img2))
    obs.obs_source_update(imgSource2, settings)

    #Updating the card3 Image.
    imgSource3 = obs.obs_get_source_by_name("card3")
    obs.obs_data_set_string(settings, "url", correctURL(img3))
    obs.obs_source_update(imgSource3, settings)

    #Updating the card4 Image.
    imgSource4 = obs.obs_get_source_by_name("card4")
    obs.obs_data_set_string(settings, "url", correctURL(img4))
    obs.obs_source_update(imgSource4, settings)

    #Updating the card5 Image.
    imgSource5 = obs.obs_get_source_by_name("card5")
    obs.obs_data_set_string(settings, "url", correctURL(img5))
    obs.obs_source_update(imgSource5, settings)

    #Updating the User Name.
    userSource = obs.obs_get_source_by_name("usernameCard")
    obs.obs_data_set_string(settings, "text", username)
    obs.obs_source_update(userSource, settings)

    #Toggling the visibility of the group with a wait statement inbetween.
    groupSource = obs.obs_get_source_by_name("cardGroup")
    group = obs.obs_scene_sceneitem_from_source(scene, groupSource)
    obs.obs_sceneitem_set_visible(group, True)

    def hide_card1():
        obs.obs_source_set_enabled(imgSource1, False)
    
    def hide_card2():
        obs.obs_source_set_enabled(imgSource2, False)
    
    def hide_card3():
        obs.obs_source_set_enabled(imgSource3, False)
    
    def hide_card4():
        obs.obs_source_set_enabled(imgSource4, False)
    
    def hide_card5():
        obs.obs_source_set_enabled(imgSource5, False)
    
    threading.Timer(cardDurr*1, hide_card1).start()
    threading.Timer(cardDurr*2, hide_card2).start()
    threading.Timer(cardDurr*3, hide_card3).start()
    threading.Timer(cardDurr*4, hide_card4).start()
    threading.Timer(cardDurr*5, hide_card5).start()


    #Hides the visuals after set durration time.
    #Need to set all back to visible after they disappear
    def hide_group2():
        obs.obs_sceneitem_set_visible(group, False)

        obs.obs_source_set_enabled(imgSource1, True)
        obs.obs_source_set_enabled(imgSource2, True)
        obs.obs_source_set_enabled(imgSource3, True)
        obs.obs_source_set_enabled(imgSource4, True)
        obs.obs_source_set_enabled(imgSource5, True)

        #Releasing the sources.
        obs.obs_data_release(settings)
        obs.obs_source_release(imgSource1)
        obs.obs_source_release(imgSource2)
        obs.obs_source_release(imgSource3)
        obs.obs_source_release(imgSource4)
        obs.obs_source_release(imgSource5)
        obs.obs_source_release(userSource)
        obs.obs_source_release(groupSource)
        obs.obs_scene_release(scene)

    threading.Timer(cardDurr*6, hide_group2).start()


#Description of the script in the script menu, crazy.
def script_description():
    return "Active the bot via the 'Twitch Chat Bot Start' hotkey."

#Adds ability to save hotkey, since it doesn't by default?
def script_save(settings):
    global hotkey_id
    hotkey_save_array = obs.obs_hotkey_save(hotkey_id)
    obs.obs_data_set_array(settings, "Twitch Chat Bot Start", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

#More hotkey stuff, automatically runs when the script is started.
def script_load(settings):
    global hotkey_id
    def callback(pressed):
        if pressed:
            return bot.run()
    hotkey_id = obs.obs_hotkey_register_frontend("htk_hotkey2", "Twitch Chat Bot Start", callback)
    hotkey_save_array = obs.obs_data_get_array(settings, "Twitch Chat Bot Start")
    obs.obs_hotkey_load(hotkey_id, hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

#Not sure what this stuff does, but its required, and is 100% the source of closing crashes. 
def script_update(settings):
    dog = "dog"
    return

def script_properties():
    cat = "cat"
    return

#Make pages look better
