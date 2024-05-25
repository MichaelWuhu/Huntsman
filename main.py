import PIL.Image
import PIL.ImageOps
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

import random
import requests
import json

from MonsterHelperMethods import *

from PIL import Image
import io

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
    

    if can_roll:
        await send_card(ctx, monsters["name"], rank, getMonsterImage(monsters["name"])) # switch to hunter point system later
        monster_name = monsters["name"]
        element = getMonsterElement(monster_name)
        print(f"{monster_name}'s element: {element}")


async def on_hunt(message, user):
    if user.bot:
        return

    # weapon = user.weapon
    # weapons = ['SWORDANDSHIELD', 'GREATSWORD', 'LONGSWORD', 'LANCE', 'BOW']
    weapon = "GREATSWORD"
    old_embed = message.embeds[0]

    turn = int(old_embed.footer.text.split(' ')[1])
    print(turn)

    used_special = False

    prev_status = old_embed.fields[0].value
    
    hunter_hp_parts = old_embed.fields[1].value.split(':')
    hunter_hp = int(hunter_hp_parts[1].strip())

    monster_hp_parts = old_embed.fields[2].value.split(':')
    monster_hp = int(monster_hp_parts[1].strip())

    if hunter_hp == 0 or monster_hp == 0:
        print("can't hunt")
        return False

    monster_pot_dmg_low = (getMonsterHP(old_embed.title, "low") // 1000) * 10 # TODO: change low to rank argument
    monster_pot_dmg_high = ((getMonsterHP(old_embed.title, "low") // 1000) + 1) * 10 # TODO: change low to rank argument
    monster_dmg = random.randint(monster_pot_dmg_low, monster_pot_dmg_high)
    # print(f"monster dmg = {monster_dh!mg}")
    hunter_move = f"Took {monster_dmg} damage from monster" # TODO: just an IDEA but subtract defense from monster_dmg
    
    if weapon == "SWORDANDSHIELD":
        # user_atk_stat = db.getUserAtkStat() # TODO: add in user stat from database
        weapon_dmg = 50000 # TODO: adjust dmg
        hunter_dmg = weapon_dmg # add user atk stat
        snsOptions = ['stun', 'shield', 'dodge']
        if random.randint(1, 100) <= 5: # %5 stun chance
            used_special = True
            hunter_move = f"Dealt {hunter_dmg} damage to monster"
            atk_move = random.choice(snsOptions)
            print(atk_move)
            if atk_move == "stun":
                monster_dmg = 0
                hunter_move += "\n& stunned monster"
            elif atk_move == "shield":
                monster_dmg /= 2 # TODO: change value to make more sense
                hunter_move += "\n& blocked monster attack"
            elif atk_move == "dodge":
                monster_dmg = 0
                hunter_move += "\n& dodged monster attack"
    
    if weapon == "GREATSWORD":
        # user_atk_stat = db.getUserAtkStat() # TODO: add in user stat from database
        weapon_dmg = 1000 # TODO: adjust dmg
        hunter_dmg = weapon_dmg # add user atk stat
        used_special = True
        if turn % 2 == 1: # every other turn
            hunter_dmg = 0
            hunter_move += "\nCharging up"
        elif turn % 3 == 0: # every 3rd turn
            hunter_dmg *= 2
            hunter_move += f"\nTrue charged slash did {hunter_dmg} damage to monster"
        else:
            hunter_move += f"\nDealt {hunter_dmg} damage to monster"

    if weapon == "LONGSWORD":
        # user_atk_stat = db.getUserAtkStat() # TODO: add in user stat from database
        weapon_dmg = 800 # TODO: adjust dmg
        hunter_dmg = weapon_dmg # add user atk stat

        if "Parried" in prev_status:
            hunter_dmg = int(hunter_dmg * 1.5)
            hunter_move += f"\nParry follow-up did {hunter_dmg} damage to monster"
            used_special = True
        elif random.randint(1, 100) <= 50: # 5% parry chance
            monster_dmg = 0
            hunter_dmg = 0
            hunter_move = "Parried monster attack"
            used_special = True
           

    # universal dmg (no special weapon effects)
    if not used_special:
        if random.randint(1, 100) <= 10: # %10 dodge chance
            hunter_move = f"Dealt {hunter_dmg} damage to monster"
            print("dodged via global 10%")
            hunter_move += "\n& dodged monster attack"
            monster_dmg = 0
        else:
            hunter_move += f"\n& dealt {hunter_dmg} damage to monster"

    new_hunter_hp = int(hunter_hp - monster_dmg)
    new_monster_hp = int(monster_hp - hunter_dmg)

    if new_hunter_hp < 0:
        new_hunter_hp = 0
    if new_monster_hp < 0:
        new_monster_hp = 0
    
    turn += 1
    embed = create_embed(old_embed.title, hunter_move, new_hunter_hp, new_monster_hp, turn)
    # embed.set_field_at(2) # monster hp

    await message.edit(embed=embed)

    if new_monster_hp <= 0 and new_hunter_hp <= 0:
        return "hunted and fainted"
    elif new_monster_hp <= 0:
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
        if hunted == "hunted and fainted":
            await interaction.channel.send(f'**{interaction.user.display_name}** hunted the monster 🗡️ but...')
            await interaction.channel.send(f'**{interaction.user.display_name}** also fainted 💀')
            amount_dropped_low = (getMonsterHP(monster_name, monster_rank) // 1000) * 10
            amount_dropped_high = ((getMonsterHP(monster_name, monster_rank) // 1000) + 1) * 10
            amount_dropped = random.randint(amount_dropped_low, amount_dropped_high)
            element = getMonsterElement(monster_name)
            element_emoji = getMonsterElementEmoji(element)
            await interaction.channel.send(f'**{monster_name}** dropped {element_emoji} **{amount_dropped} {element} parts** {element_emoji}')
        elif hunted == "hunted":
            await interaction.channel.send(f'**{interaction.user.display_name}** hunted the monster 🗡️')  
            amount_dropped_low = (getMonsterHP(monster_name, monster_rank) // 1000) * 10
            amount_dropped_high = ((getMonsterHP(monster_name, monster_rank) // 1000) + 1) * 10
            amount_dropped = random.randint(amount_dropped_low, amount_dropped_high)
            element = getMonsterElement(monster_name)
            element_emoji = getMonsterElementEmoji(element)
            await interaction.channel.send(f'**{monster_name}** dropped {element_emoji} **{amount_dropped} {element} parts** {element_emoji}')
        elif hunted == "fainted":
            await interaction.channel.send(f'**{interaction.user.display_name}** fainted 💀')
            # await interaction.channel.send(f'**{interaction.user.display_name}** pressed button') # TODO: maybe just leave blank
        return
    
    hunt_button.callback = callback

    message = await ctx.send(file=file, embed=embed, view=view)
    return message

# create embed
def create_embed(title, status, hunterHP, monsterHP, turn=1):
    embed = discord.Embed(title=title, color=discord.Color.gold())
    embed.add_field(name="", value=status, inline=False)
    embed.add_field(name="Hunter HP", value=f'💚: {hunterHP}', inline=True)
    embed.add_field(name="Monster HP", value=f'❤️: {monsterHP}', inline=True)
    embed.set_image(url="attachment://image.png")
    embed.set_footer(text=f"Turn {turn}")
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
