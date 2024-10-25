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

silver = r"C:\Users\Greg Knothe\Desktop\silverClaireAnimated.gif"
gold = r"C:\Users\Greg Knothe\Desktop\silverClaireAnimated.gif"
rainbow = r"C:\Users\Greg Knothe\Desktop\silverClaireAnimated.gif"
rance = r"C:\Users\Greg Knothe\Desktop\silverClaireAnimated.gif"

heyList = []
modList = ["lastclaire", "greedx___", "asome26", "nastyplot", "botthewoz", "frendweeb", "gdom", "redditto", "sajam", "wooper_enthusiast",
           "joshgrilli", "sindercenpai", "hotashi", "linkl0nk", "chris_re5", "voidashe", "the_doc_", "abusywitch", "lament_03", "kyluneena",
           "jackpotfm", "nastyplot", "nbnhmr", "ailubee", "meowzykat", "squirrel147"]    

currTimeStamp = time.time()
cooldown = 6
durration = 5

hotkey_id = obs.OBS_INVALID_HOTKEY_ID

#Supresses error outputs (happens when someone types something other than !hey, so they kinda needa go tbh)
class DevNull:
    def write(self, msg):
        pass
sys.stderr = DevNull()

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
            data = ohHey(ctx.author.name)
            await ctx.send(data[3])
            heyList.append(ctx.author.name)
            currTimeStamp = time.time()
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
