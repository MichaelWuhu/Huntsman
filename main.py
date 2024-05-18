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
can_hunt = True

monsters_by_id = [17, 18, 21, 27, 36, 42, 60]
# [great jagras, kulu-ya-ku, jyuratodus, pickle-monster, legiana, rathalos, zinogre]

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
    id = random.choice(monsters_by_id)  # change range id to number of monsters in API
    # TODO: add in a low/high rank status (changes probability)
    res = requests.get(f"https://mhw-db.com/monsters/{id}")
    response = json.loads(res.text)

    if can_roll:
        message = await send_card(ctx, response["name"], getMonsterImage(response["name"]))
        await message.add_reaction("👍")


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    channel = reaction.message.channel
    if reaction.emoji == "👍" and can_hunt:
        await channel.send(f'**{user.display_name}** reacted with {reaction.emoji}')
        if try_hunt(user=user):
            await channel.send(f'**{user.display_name}** successfully hunted the monster!')


#########################################################################
#### HELPER METHODS ####
#########################################################################


# sends the info in a formatted card
async def send_card(ctx, name, image_url, image_width=200):
    image_data = resize_image(image_url, image_width)
    file = discord.File(io.BytesIO(image_data), filename="image.png")
    temp_description = (f'💚: {"100"}')
    embed = discord.Embed(title=name, description=temp_description, color=discord.Color.gold())
    embed.set_image(url="attachment://image.png")
    message = await ctx.send(file=file, embed=embed)
    return message


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


# rn its just % chance
def try_hunt(user):
    random_num = random.randint(1, 100)
    if random_num <= 40: # 40% Chance of success in hunting monster
        return True
    else:
        return False

#########################################################################
#### END HELPER METHODS ####
#########################################################################

# run bot
load_dotenv()
TOKEN = os.environ.get("TOKEN")
bot.run(TOKEN)
