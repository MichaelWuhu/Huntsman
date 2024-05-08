import PIL.Image
import PIL.ImageOps
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

import random
import requests
import json

from MonsterImageScraper import *

from PIL import Image
import io

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
    id = random.randint(1, 20)  # change range id to number of monsters in API
    # add in a low/high rank status (changes probability)
    res = requests.get(f"https://mhw-db.com/monsters/{id}")
    response = json.loads(res.text)

    if can_roll:
        # await ctx.send(f"Name: {response['name']}")
        # await ctx.send(getMonsterImage(response['name']))
        await send_card(ctx, response["name"], getMonsterImage(response["name"]))


#########################################################################
#### HELPER METHODS ####
#########################################################################


# sends the info in a formatted card
async def send_card(ctx, name, image_url, image_width=200):
    image_data = resize_image(image_url, image_width)
    file = discord.File(io.BytesIO(image_data), filename="image.png")
    embed = discord.Embed(title=name, description="React with any emoji to claim!", color=discord.Color.gold())
    embed.set_image(url="attachment://image.png")
    await ctx.send(file=file, embed=embed)


# resizes an image for consistent width
def resize_image(image_url, base_width):
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))

    wpercent = base_width / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_width, hsize), Image.LANCZOS)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr


#########################################################################
#### END HELPER METHODS ####
#########################################################################

# run bot
load_dotenv()
TOKEN = os.environ.get("TOKEN")
bot.run(TOKEN)
