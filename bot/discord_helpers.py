import discord
from PIL import Image
import io
import random
import requests

from hunt_logic import *


async def send_card(ctx, file, embed):

    # TODO: replace emojis with mh emojis
    hunt_button = discord.ui.Button(label="HUNT", style=discord.ButtonStyle.secondary, emoji="⚔️") 
    special_button = discord.ui.Button(label="SPECIAL", style=discord.ButtonStyle.primary, emoji="🔮")
    potion_button = discord.ui.Button(label="POTION", style=discord.ButtonStyle.success, emoji="🍄")
    view = discord.ui.View(timeout=120)
    view.add_item(hunt_button)
    view.add_item(special_button)
    view.add_item(potion_button)

    async def hunt_callback(interaction):
        await interaction.response.defer()
        embed = interaction.message.embeds[0]
        hunter_hp, monster_hp, turn = get_embed_values(embed)
        
        hunt = await on_hunt(hunter_hp=hunter_hp, monster_hp=monster_hp, turn=turn)
        print(f"hunt: {hunt}")
        if hunt:
            await edit_card(interaction.message, embed, hunt[0], hunt[1], hunt[2], hunt[3])

        # await interaction.channel.send(f'{hunted}')
        # hunt_button.disabled = True # TODO: not working

    async def special_callback(interaction):
        await interaction.response.defer()
        embed = interaction.message.embeds[0]
        hunter_hp, monster_hp, turn = get_embed_values(embed)

        user_weapon = "swordAndShield" # TODO: get acutal weapon
        special = await eval(f"hunt_{user_weapon} (hunter_hp={hunter_hp}, monster_hp={monster_hp}, turn={turn})")

        print(f"special: {special}")
        if special:
            await edit_card(interaction.message, embed, special[0], special[1], special[2], special[3])

    async def potion_callback(interaction):
        await interaction.response.defer()
        embed = interaction.message.embeds[0]
        hunter_hp, monster_hp, turn = get_embed_values(embed)
        potion_count = 10 # TODO: get actual potion count

        # await interaction.channel.send(f'**{interaction.user.display_name}** pressed item button')
        # potion_button.disabled = True # TODO: not working

        potion = await on_potion(hunter_hp=hunter_hp, monster_hp=monster_hp, potion_count=potion_count, turn=turn)
        print(f"potion: {potion}")
        if potion:
            await edit_card(interaction.message, embed, potion[0], potion[1], potion[2], potion[4])
            # potion_count_in_db = potion[3] # TODO: update potion count in database
            
    

    hunt_button.callback = hunt_callback
    special_button.callback = special_callback
    potion_button.callback = potion_callback

    await ctx.send(file=file, embed=embed, view=view)


async def edit_card(message, embed, hunter_hp, monster_hp, status, turn):
    new_embed = create_embed(embed.title, status, hunter_hp, monster_hp, turn)
    await message.edit(embed=new_embed)


# create embed
def create_embed(title, status, hunterHP, monsterHP, turn=1):
    embed = discord.Embed(title=title, color=discord.Color.gold())
    embed.add_field(name="", value=status, inline=False)
    embed.add_field(name="Hunter HP", value=f'💚: {hunterHP}', inline=True)
    embed.add_field(name="Monster HP", value=f'❤️: {monsterHP}', inline=True)
    embed.set_image(url="attachment://image.png")
    embed.set_footer(text=f"Turn {turn}")
    return embed

def get_embed_values(embed):
    hunter_hp_parts = embed.fields[1].value.split(':')
    hunter_hp = int(hunter_hp_parts[1].strip())

    monster_hp_parts = embed.fields[2].value.split(':')
    monster_hp = int(monster_hp_parts[1].strip())

    turn = int(embed.footer.text.split(' ')[1])

    return hunter_hp, monster_hp, turn


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












# sends the info in a formatted card
async def old_send_card(ctx, monster_name, monster_rank, image_url, image_width=200):
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