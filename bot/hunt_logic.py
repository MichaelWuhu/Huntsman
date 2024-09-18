import random

async def on_hunt(hunter_hp, monster_hp, turn=1):
    
    # print("hunter_hp: ", hunter_hp)
    # print("monster_hp: ", monster_hp)

    # Checks for can_hunt ###################
    if hunter_hp == 0:
        print("hunter fainted")
        return False
    
    if monster_hp == 0:
        print("monster slain")
        return False
    #########################################
    
    hunter_dmg = 50 + 500
    monster_dmg = random.randint(20, 30)
    hunter_status = f"Dealt {hunter_dmg} damage to monster"
    
    # attack logic
    if random.randint(1, 100) <= 15: # dodge chance
        monster_dmg = 0
        hunter_status += f"\n& dodged monster"
    elif random.randint(1, 100) <= 5: # miss chance
        hunter_dmg = 0
        hunter_status = f"Missed attack & took {monster_dmg} from monster"
    else:
        hunter_status += f"\n& took {monster_dmg} damage from monster"


    new_hunter_hp = hunter_hp - monster_dmg
    new_monster_hp = monster_hp - hunter_dmg
    hunter_status = hunter_status

    if new_monster_hp < 0:
        new_monster_hp = 0
        hunter_status = "monster slain"
        monster_slain = True
    if new_hunter_hp < 0:
        new_hunter_hp = 0
        if not monster_slain:
            hunter_status = "fainted"

    turn = turn + 1

    return new_hunter_hp, new_monster_hp, hunter_status, turn

# Simulates the hunting logic for sword and shield
async def hunt_swordAndShield(hunter, monster, turn=1):

    # User data
    # weapon = "swordAndShield" # weapon = user.weapon
    hunter_hp = 100 # hunter_hp = user.hp
    hunter_atk_stat = 100 # TODO: add in user stat from database
    weapon_dmg = 500 # TODO: adjust dmg
    hunter_dmg = weapon_dmg + hunter_atk_stat # add user atk stat
    dodge_chance = 20 # this is chance out of 100 # dodge_chance = user.dodge_chance

    # Monster data
    monster_hp = 2100 # monster_hp = monster.hp
    # monster_pot_dmg_low = (getMonsterHP(old_embed.title, "low") // 1000) * 10 # TODO: change low to rank argument
    # monster_pot_dmg_high = ((getMonsterHP(old_embed.title, "low") // 1000) + 1) * 10 # TODO: change low to rank argument
    monster_pot_dmg_low = 100
    monster_pot_dmg_high = 200
    monster_dmg = random.randint(monster_pot_dmg_low, monster_pot_dmg_high)
    # TODO: GET REST OF THE DATA
    

    # Checks for can_hunt ###################
    if hunter_hp == 0:
        print("hunter fainted")
        return False
    
    if monster_hp == 0:
        print("monster slain")
        return False
    #########################################

    



    snsOptions = ['stun', 'shield', 'dodge']

    hunter_move = f"Dealt {hunter_dmg} damage to monster"

    if random.randint(1, 100) <= 15: # %15 stun chance
        monster_dmg = 0
        hunter_move += "\n& stunned monster"
    elif random.randint(1, 100) <= 15: # %15 shield chance
        monster_dmg /= 2 # TODO: change value to make more sense
        hunter_move += "\n& blocked monster attack"
    elif random.randint(1, 100) <= dodge_chance: # %20 dodge chance
        monster_dmg = 0
        hunter_move += "\n& dodged monster attack"




    
    new_hunter_hp = int(hunter_hp - monster_dmg)
    new_monster_hp = int(monster_hp - hunter_dmg)
    
    turn += 1

    if new_hunter_hp < 0:
        new_hunter_hp = 0
    if new_monster_hp < 0:
        new_monster_hp = 0

    if new_monster_hp <= 0 and new_hunter_hp <= 0:
        return "hunted and fainted"
    elif new_monster_hp <= 0:
        return "hunted"
    elif new_hunter_hp <= 0:
        return "fainted"
    else:
        return "N/A"


