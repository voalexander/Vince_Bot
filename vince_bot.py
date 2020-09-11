# Vince Bot
import os
import random
import time
import datetime

import google_sheets
import discord
from discord.ext import commands
from dotenv import load_dotenv

time.sleep(10)
vinceQuotes = google_sheets.getQuotes()
lastUsed = datetime.datetime(2000, 1,1)
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
google_doc = os.getenv('GOOGLE_DOC')

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
# Bot runs at bottom of file

def randomVinceQuote():
    global vinceQuotes
    global lastUsed
    duration = datetime.datetime.now() - lastUsed
    print("Time since: " + str(duration.seconds))
    if duration.seconds > 30: # Time buffer to prevent hitting googlesheets API
        # Pull new quotes from google sheets
        print("Pulled new")
        lastUsed = datetime.datetime.now()
        vinceQuotes = google_sheets.getQuotes()
        return random.choice(vinceQuotes)
    else:
        # Pull stored quotes
        return random.choice(vinceQuotes)

# Set discord status
@bot.event
async def on_ready():
    print(f'{bot.user.name} connected to Discord')
    await bot.change_presence(activity=discord.Game(name="Hi I'm VinceBot!"))

# Get random quote
@bot.command(name="vince", help="me vince")
async def vince_quote(ctx):
    await ctx.send(randomVinceQuote())

# Get random quote
@bot.command(name="Vince", help="me Vince")
async def Vince_quote(ctx):
    await ctx.send(randomVinceQuote())

# Get a specific quote
@bot.command(name="vincent")
async def vincent_quote(ctx, arg: int):
    global vinceQuotes
    if not (arg < 0 or arg > (len(vinceQuotes))):
        await ctx.send(vinceQuotes[arg - 1])

# Add quotes to public googledoc
@bot.command(name="addQuote", help="Gives link to add Quotes")
async def getLink(ctx):
    await ctx.send(google_doc)

# Add quotes to public googledoc
@bot.command(name="addquote", help="Gives link to add quotes")
async def getLink1(ctx):
    await ctx.send(google_doc)

# Display help command
@bot.command(name='help')
async def help(ctx):
    toPrint = "```css\nHi! I'm Vince-bot, for all your Vince quote needs.\n"
    toPrint += "my commands are\n\n"
    toPrint += "[!vince], [!addquote], [help], [!vincent { quote number }], [!listquotes]"
    await ctx.send(toPrint)

# Sends user DM of all quotes registered
@bot.command(name='listquotes')
async def listQuotes(ctx):
    global vinceQuotes
    vinceQuotes = google_sheets.getQuotes()
    num = 1
    toPrint = ""
    for x in vinceQuotes:
        toPrint += str(num) + ": " + x + "\n"
        num += 1
    # Need to split for ever 1990 characters to avoid discord DM character limit
    split = [toPrint[i:i+1990] for i in range(0, len(toPrint), 1990)]
    for x in split:
        await ctx.author.send("```css\n" + x + "```")

# Start bot
bot.run(token)
