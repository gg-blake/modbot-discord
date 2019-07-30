import discord
import random
import asyncio
import io
import aiohttp
import time
from PIL import Image

client = discord.Client()
trivia = None
pictoguesser = None
strated = False
native_channel = client.get_channel("557342916289232900")
genie = ""
genieDM = False
genieDM2 = False
ended = False
mute_enabled = False
begin_play = False
secret_msg = None
game_open = False
game_start = False
started = False
new = None
genie_confirm_open = False
image_link = None
finalized_question = False
genie_send_pic = False
new_question = False
questions = {
    1:("What is the closest star system to our own solar system?", ["Milky Way", "Alpha Centauri", "Proxima Centauri", "Epsilon Eridani"], "c"),
    2:("If you are having a cerebrovascular accident, you are having a what?", ["Stroke", "Kidney Failure", "Seizure", "Heart Attack"], "a"),
    3:("An oncologist studies what?", ["Autism", "Deez nutz", "Diabetes", "Cancer"], "d"),
    4:("As of March 16, 2019, How many films are currently included in the Marvel Cinematic Universe?", ["12", "19", "21", "17"], "b"),
}
letters = {
    "a":"🇦 ",
    "b":"🇧 ",
    "c":"🇨 ",
    "d":"🇩 ",
    "e":"🇪 ",
    "f":"🇫 ",
    "g":"🇬 ",
    "h":"🇭 ",
    "i":"🇮 ",
    "j":"🇯 ",
    "k":"🇰 ",
    "l":"🇱 ",
    "m":"🇲 ",
    "n":"🇳 ",
    "o":"🇴 ",
    "p":"🇵 ",
    "q":"🇶 ",
    "r":"🇷 ",
    "s":"🇸 ",
    "t":"🇹 ",
    "u":"🇺 ",
    "v":"🇻 ",
    "w":"🇼 ",
    "x":"🇽 ",
    "y":"🇾 ",
    "z":"🇿 ",
}

async def crop(image_path, coords, saved_location, channel):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)v
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    location = saved_location
    await client.send_file(channel, str(location))


async def search_game(ctx):
    global genieDM
    global genie
    global game_open
    global game_start
    global players
    game_open = True
    players_str = ""
    print(ctx.author.name)
    msg = await client.send_message(ctx.channel, "🕒60 secs left till game begins🕒")
    wait_time = 59
    for i in range(wait_time + 1):
        time.sleep(1)
        if wait_time - i < 10:
            await client.edit_message(msg, "🚨{} sec(s) left until the game begins🚨".format(wait_time - i))
        else:
            await client.edit_message(msg, "🕒{} sec(s) left until the game begins🕒".format(wait_time - i))
        await client.remove_reaction(msg, "💯", client.user)
    game_open = False
    players_id = [i.id for i in players]
    if len(players_id) < 1:
        return
    genie = random.choice(players_id)
    for member in msg.server.members:
        if member.id == genie:
            genie = member
    if len(players) > 0:
        for i in players:
            players_str += " " + i.name
        embed=discord.Embed(title="**The game has begun!**", color=0x0dcdfd)
        embed.add_field(name="Players", value=players_str, inline=True)
        embed.add_field(name="Pic Genie", value="**{}** has been selected to be the *Pic Genie*".format(str(genie)), inline=False)
        embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/409031437983940618/556636219552038934/wrench.jpg", text="The chosen Pic Genie will be notified through direct messages for further instruction on how to choose an image")
        await client.send_message(msg.channel, embed=embed)
        embed=discord.Embed(title="Pictoguesser")
        embed.set_author(name="Mod Bot Games", icon_url="https://cdn.discordapp.com/attachments/409031437983940618/556636219552038934/wrench.jpg")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/409031437983940618/556636219552038934/wrench.jpg")
        embed.add_field(name="(player), you've been selected to be the *Pic Genie*!", value="Please send me a picture of that you really love! THEN, type the secret name of the picture.", inline=False)
        embed.set_footer(text="Responses are still apt to penalty based on the rules from the server")
        await client.send_message(genie, embed=embed)
        genieDM = True
        pictoguesser = False
    return


@client.event
async def on_message(message):
    global mute_enabled
    global started
    global letters
    global new
    global secret_msg
    global players
    global finalized_question
    global saved_location
    global image_link
    global new_question
    global genie_confirm_open
    global native_channel
    global begin_play
    global genieDM
    global genieDM2
    global genie
    global trivia
    global pictoguesser
    passed = False
    # we do not want the bot to reply to itself
    if message.author == client.user:
        if trivia:
            await client.add_reaction(message, "🇦")
            await client.add_reaction(message, "🇧")
            await client.add_reaction(message, "🇨")
            await client.add_reaction(message, "🇩")
            trivia = False
        elif pictoguesser:
            await client.add_reaction(message, "💯")
            pictoguesser = False
        elif trivia == None:
            client.send_message(message.channel, "Failure to enable trivia.")
        return

    if message.content.upper().startswith('$HELP'):
        await client.send_message(message.channel, "Becoming a Certified Good Boi will allow you to embed links and send and share files. To register for a Good Boi Certification, type '!register'! Once you begin the registration process, you must be a responsible member of the community. No funny business. During the 7 day waiting period, a strike or infringement upon any of the #rules will result in the permanent incompletion of the Certification process\n$register (register for Good-Boi certification)\n$goodboicheck (check if you are Good-Boi certified)\n$gimmevbuck (accept your good boi certification)")

    if message.content.upper().startswith('$BESTLANGUAGE'):
        await client.send_message(message.channel, "**Python is good but Lua is too**")

    if message.content.lower().startswith('$trivia'):
        thisQuestion = questions[random.randrange(1, 5)]
        myDesc = thisQuestion[0]
        embed = discord.Embed(title="Trivia Time", description=myDesc+"\n", color=0x13fb1f)
        a = thisQuestion[1][0]
        b = thisQuestion[1][1]
        c = thisQuestion[1][2]
        d = thisQuestion[1][3]
        embed.add_field(name=':regional_indicator_a:' , value=a, inline=False)
        embed.add_field(name=':regional_indicator_b:' , value=b, inline=False)
        embed.add_field(name=':regional_indicator_c:' , value=c, inline=False)
        embed.add_field(name=':regional_indicator_d:' , value=d, inline=False)
        trivia = True
        await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith('$pg') and not started:
        started = True
        new = []
        native_channel = message.channel
        embed = discord.Embed(title="**Pictoguesser**", description="*A game a about visual pattern recognition*", color=0x49f3f3)
        embed.set_author(name="Mod Bot Games", icon_url="https://cdn.discordapp.com/attachments/409031437983940618/556636219552038934/wrench.jpg")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/409031437983940618/556636030917148679/morgan.png")
        embed.add_field(name="⚔️How to Win⚔️", value="*Guess the picture's name using key components of the photo*", inline=False)
        embed.add_field(name="🚫Requirements🚫", value="*Friends (2+)*", inline=False)
        embed.add_field(name="🛠️Created By🛠️", value="LesbianChodeGamer#2270", inline=False)
        pictoguesser = True
        global players
        global playerNum
        playerNum = 1
        players = []
        msg = await client.send_message(message.channel, embed=embed)
        client.loop.create_task(search_game(msg))

    if message.content.lower().startswith('$group'):
        await client.send_message(message.channel, players)

    if genieDM and str(message.channel) == 'Direct Message with ' + message.author.name:
        if message.content.endswith('.jpg') or message.content.endswith('.png'):
            try:
                global pgembed
                pgembed = discord.Embed()
                image_link = message.content
                pgembed.set_image(url=image_link)
                await client.send_message(genie, embed=pgembed)
                genieDM = False
                genieDM2 = True
                await client.send_message(genie, "Epic! Now type in a message!")
            except:
                embed=discord.Embed(title=" ")
                embed.set_author(name="There was a issue with processing that file", icon_url="https://cdn.discordapp.com/attachments/409031437983940618/556636219552038934/wrench.jpg")
                await client.send_message(genie, embed=embed)
            return

    if genieDM2 and str(message.channel) == 'Direct Message with ' + message.author.name:
        secret_msg = message.content
        embed=discord.Embed(title="**Your secret message is:**", description="```{}```".format(secret_msg), color=0xff1515)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/409031437983940618/556636219552038934/wrench.jpg")
        embed.add_field(name="type $y to confirm, $n to cancel", value="​​​​", inline=True)
        embed.set_footer(text="Keep it safe, keep it close...")
        await client.send_message(genie, embed=embed)
        await client.send_message(native_channel, "the genie has finished!")
        genieDM2 = False
        genie_confirm_open = True
        return

    if genie_confirm_open:
        if message.content.startswith('$y'):
            await client.send_message(native_channel, "pillow time, nibba!")
            genie_confirm_open = False
            new_question = True
        elif message.content.startswith('$n'):
            genie_confirm_open = False
            genieDM2 = True
            return

    if new_question:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_link) as resp:
                if resp.status != 200:
                    return await channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
        image_path = data
        x1 = 0
        y1 = 0
        x2 = 500
        y2 = 500
        coords = (x1, y1, x2, y2)
        saved_location = "crop.jpg"
        await client.loop.create_task(crop(image_path, coords, saved_location, native_channel))
        new_question = False
        finalized_question = True

    if finalized_question and message.author.name in [user.name for user in players]:
        emoji_filler = ""
        list1 = []
        for i in secret_msg:
            list1.append(i)
        if ' ' in list1:
            list1.remove(' ')
        secret_msg = ""
        for i in list1:
            secret_msg += i
        msg = set([])
        for i in message.content.lower():
            msg.add(i)
        print("My word:", msg)
        key = set([])
        for i in secret_msg:
            key.add(i)
        print("The genie's word", key)
        together = msg & key
        print("Shared letters:", together)
        for i in together:
            if i not in new:
                new.append(i)
        for i in secret_msg:
            if i in new:
                emoji_filler += letters[i]
            else:
                emoji_filler += "🔵"
        print("New words:", new)
        embed=discord.Embed(title=emoji_filler, color=0xff0000)
        embed.set_author(name="(Genie Player)", icon_url="https://cdn.discordapp.com/attachments/409031437983940618/556636219552038934/wrench.jpg")
        await client.send_message(native_channel, embed=embed)
        await client.send_file(native_channel, saved_location)
        if "🔵" not in emoji_filler:
            print(message.author.name, "wins!")

    if message.content.lower().startswith('$mute') or mute_enabled:
        mute_enabled = True
        if message.author.name == "HangmanBot":
            await client.delete_message(message)


    if message.content.lower().startswith('$unmute'):
        mute_enabled = False


@client.event
async def on_reaction_add(reaction, user):
    global game_open
    global players
    global playerNum
    if reaction.emoji == "💯" and user.name != "Mod Bot" and game_open:
        players.append(user)
        pJoin = discord.Embed(color=0x2506fd)
        pJoin.set_footer(icon_url=user.avatar_url, text="{} has joined the party!".format(user.name))
        await client.send_message(reaction.message.channel, embed=pJoin)
        playerNum += 1


@client.event
async def on_reaction_remove(reaction, user):
    global game_open
    global players
    global playerNum
    if reaction.emoji == "💯" and user.name != "Mod Bot" and game_open:
        players.remove(user)
        pJoin = discord.Embed(color=0x2506fd)
        pJoin.set_footer(icon_url=user.avatar_url, text="{} has left the party!".format(user.name))
        await client.send_message(reaction.message.channel, embed=pJoin)
        playerNum -= 1


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    trivia = None
    pictoguesser = None


while True:
    try:
        client.run('NTA2NDUwNDQ3ODcyMjk0OTE0.D140VQ.AQpjT7zTFpJzvUmYt3I0mYgFOOc')
    except:
        pass
