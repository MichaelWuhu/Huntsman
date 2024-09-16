import random
import requests
import json  
import discord
import io
from PIL import Image
from discord_helpers import *

def setup_commands(bot):
    @bot.command()
    async def test(ctx):
        await ctx.send("test")

    @bot.command()
    async def hunt(ctx):
        
        # TEMP MONSTER DATA #############
        monsters_by_id = [17, 18, 21, 27, 36, 42, 60]
        # [great jagras, kulu-ya-ku, jyuratodus, pickle-monster, legiana, rathalos, zinogre]
        #################################
        
        # USER DATA #####################
        can_roll = True
        can_hunt = True
        #################################

        id = random.choice(monsters_by_id)  # change range id to number of monsters in API
        # TODO: add in a low/high rank status (changes probability)
        res = requests.get(f"https://mhw-db.com/monsters/{id}")
        monsters = json.loads(res.text)
        hunterRank = "low" # later change to below
    

        if can_roll:
            # TEMPORARY EMBED
            embed = discord.Embed(title="Monster Name", color=discord.Color.gold())
            embed.add_field(name="", value="React to Hunt", inline=False)
            embed.add_field(name="Hunter HP", value=f'💚: {100}', inline=True)
            embed.add_field(name="Monster HP", value=f'❤️: {2000}', inline=True)
            embed.set_image(url="attachment://image.png")
            embed.set_footer(text=f"Turn {1}")

            await send_card(ctx, embed=embed) 
            
