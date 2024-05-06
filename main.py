from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="h!", intents=intents)

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
    

# run bot
load_dotenv()
TOKEN = os.environ.get("TOKEN")
bot.run(TOKEN)
