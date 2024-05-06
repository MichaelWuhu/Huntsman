from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

import random
import requests
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="h!", intents=intents)

can_roll = True

# on rdy
@bot.event
async def on_ready():
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1
    
    print("Bot is in " + str(guild_count) + " servers")


# test command
@bot.command()
async def test(ctx):
    await ctx.send("test")
    
@bot.command()
async def hunt(ctx):
    random_number = random.randint(1, 20)
    # add in a low/high rank status (changes probability)
    res = requests.get(f"https://mhw-db.com/monsters/{random_number}")
    print(res)
    response = json.loads(res.text)
    print(response)

    if can_roll:
        await ctx.send(f"Name: {response['name']}")

# run bot
load_dotenv()
TOKEN = os.environ.get("TOKEN")
bot.run(TOKEN)
