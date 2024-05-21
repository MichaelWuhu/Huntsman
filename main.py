import PIL.Image
import PIL.ImageOps
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

import random
import requests
import json

from MonsterWebScraper import *

from PIL import Image
import io

import re

# import datetime

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
    monsters = json.loads(res.text)
    rank = "low" # later change to below
    
    # hunter_rank = getHunterRank(ctx.user)
    # if hunter_rank >= 


    if can_roll:
        message = await send_card(ctx, monsters["name"], rank, getMonsterImage(monsters["name"])) # switch to hunter point system later
        # await message.add_reaction("👍")

# TODO: remove
# @bot.event
# async def on_reaction_add(reaction, user):
#     if user.bot:
#         return
#     channel = reaction.message.channel
#     message_creation_time = reaction.message.created_at
#     current_time = datetime.datetime.now(datetime.timezone.utc)

#     # only allow reactions to messages created within the last minute 
#     # print(current_time)
#     # print(message_creation_time)
#     # print(current_time - message_creation_time)
#     # print((current_time - message_creation_time).total_seconds())
#     if (current_time - message_creation_time).total_seconds() > 60:
#         return

#     if reaction.emoji == "👍" and can_hunt:
#         await channel.send(f'**{user.display_name}** reacted with {reaction.emoji}')
#         # can_hunt = False
#         if try_hunt(user=user):
#             await channel.send(f'**{user.display_name}** successfully hunted the monster!')
#             return


async def on_hunt(message, user):
    if user.bot:
        return
    
    if not can_hunt:
        return False
    
    # TODO: remove
    # channel = message.channel
    # message_creation_time = message.created_at
    # current_time = datetime.datetime.now(datetime.timezone.utc)
    # if (current_time - message_creation_time).total_seconds() > 60:
    #     return 



    # weapon = user.weapon
    # weapons = ['SWORDANDSHIELD', 'GREATSWORD', 'LONGSWORD', 'LANCE', 'BOW']
    weapon = "SWORDANDSHIELD"
    old_embed = message.embeds[0]
    
    # print(old_embed.fields[1])
    hunter_hp_parts = old_embed.fields[1].value.split(':')
    hunter_hp = int(hunter_hp_parts[1].strip())


    monster_hp_parts = old_embed.fields[2].value.split(':')
    monster_hp = int(monster_hp_parts[1].strip())

    monster_dmg = getMonsterHP(old_embed.title, "low") / 100 # TODO: change low to rank argument
    # TODO: just an IDEA but subtract defense from monster_dmg
    hunter_move = f"Took {monster_dmg} damage"
    
        
    if weapon == "SWORDANDSHIELD":
        # user_atk_stat = db.getUserAtkStat() # TODO: add in user stat from database
        weapon_dmg = 500
        snsOptions = ['stun', 'shield', 'dodge']
        if random.randint(1, 100) <= 5: # %5 stun chance
            atk_move = random.choice(snsOptions)
            print(atk_move)
            if atk_move == "stun":
                monster_dmg = 0
                hunter_move = "Stunned monster"
            elif atk_move == "shield":
                monster_dmg /= 2 # TODO: change value to make more sense
                hunter_move = "Blocked monster attack"
            elif atk_move == "dodge":
                monster_dmg = 0
                hunter_move = "Dodged monster attack"
        
    # universal dmg (no special weapon effects)
    if random.randint(1, 100) <= 10: # %10 dodge chance
        print("dodged")
        hunter_move = "dodged"
        monster_dmg = 0

    

    new_hunter_hp = int(hunter_hp - monster_dmg)
    new_monster_hp = int(monster_hp - weapon_dmg)

    if new_hunter_hp < 0:
        new_hunter_hp = 0
    if new_monster_hp < 0:
        new_monster_hp = 0

    embed = create_embed(old_embed.title, hunter_move, new_hunter_hp, new_monster_hp)
    # embed.set_field_at(2) # monster hp

    await message.edit(embed=embed)

    if new_monster_hp <= 0:
        return "hunted"
    elif new_hunter_hp <= 0:
        return "fainted"
    else:
        return "N/A"
    


#########################################################################
#### HELPER METHODS ####
#########################################################################

# sends the info in a formatted card
async def send_card(ctx, monster_name, monster_rank, image_url, image_width=200):
    image_data = resize_image(image_url, image_width)
    file = discord.File(io.BytesIO(image_data), filename="image.png")
    
    hunter_hp_value = 100
    monster_hp_value = getMonsterHP(monster_name, monster_rank)
    

    embed = create_embed(monster_name, "React to Hunt", hunter_hp_value, monster_hp_value)
    
    hunt_button = discord.ui.Button(label="HUNT", style=discord.ButtonStyle.secondary, emoji="⚔️")
    view = discord.ui.View(timeout=60)
    view.add_item(hunt_button)

    async def callback(interaction):
        await interaction.response.defer()
        hunted = await on_hunt(interaction.message, interaction.user)
        if hunted == "hunted":
            await interaction.channel.send(f'**{interaction.user.display_name}** hunted the monster 🗡️')
        elif hunted == "fainted":
            await interaction.channel.send(f'**{interaction.user.display_name}** fainted 💀')
            # await interaction.channel.send(f'**{interaction.user.display_name}** pressed button') # TODO: maybe just leave blank
        return
    
    hunt_button.callback = callback

    message = await ctx.send(file=file, embed=embed, view=view)
    return message

# create embed
def create_embed(title, status, hunterHP, monsterHP):
    embed = discord.Embed(title=title, color=discord.Color.gold())
    embed.add_field(name="", value=status, inline=False)
    embed.add_field(name="Hunter HP", value=f'💚: {hunterHP}', inline=True)
    embed.add_field(name="Monster HP", value=f'❤️: {monsterHP}', inline=True)
    embed.set_image(url="attachment://image.png")
    return embed


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



# TODO: remove this and make it 100% chance of hunting monster
# rn its just % chance
# def try_hunt():
#     random_num = random.randint(1, 100)
#     print(random_num)
#     if random_num <= 40: # 40% Chance of success in hunting monster
#         return True
#     else:
#         return False

#########################################################################
#### END HELPER METHODS ####
#########################################################################



# run bot
load_dotenv()
TOKEN = os.environ.get("TOKEN")
bot.run(TOKEN)
