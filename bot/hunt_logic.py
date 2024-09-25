import random

async def on_hunt(hunter_hp, monster_hp, turn=1):
    
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
    monster_slain = False
    
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

async def on_potion(hunter_hp, monster_hp, potion_count, turn=1):
    
    # Checks for can_hunt ###################
    if hunter_hp == 0:
        print("hunter fainted")
        return False
    
    # if monster_hp == 0:
    #     print("monster slain")
    #     return False
    #########################################

    hunter_status = f"Consumed potion, healed 50 hp"
    new_hunter_hp = hunter_hp + 50

    if new_hunter_hp >= 100:
        new_hunter_hp = 100

    turn = turn + 1

    return new_hunter_hp, monster_hp, hunter_status, potion_count-1, turn



# Simulates the hunting logic for sword and shield
async def hunt_swordAndShield(hunter_hp, monster_hp, turn=1):
    
    # Checks for can_hunt ###################
    if hunter_hp == 0:
        print("hunter fainted")
        return False
    
    if monster_hp == 0:
        print("monster slain")
        return False
    #########################################

    hunter_dmg = 50 + 500
    monster_dmg = random.randint(20, 30) # TODO: change to actual bounds
    hunter_status = f"Dealt {hunter_dmg} damage to monster"
    monster_slain = False
    
    # attack logic
    monster_dmg = int(monster_dmg/2) # TODO: balance
    hunter_status = f"Blocked monster taking less damage ({monster_dmg}) & dealth {hunter_dmg} to monster"

    new_hunter_hp = hunter_hp - monster_dmg
    new_monster_hp = monster_hp - hunter_dmg
    hunter_status = hunter_status

    if new_monster_hp <= 0:
        new_monster_hp = 0
        hunter_status = "monster slain"
        monster_slain = True
    if new_hunter_hp <= 0:
        new_hunter_hp = 0
        if not monster_slain:
            hunter_status = "fainted"

    turn = turn + 1

    return new_hunter_hp, new_monster_hp, hunter_status, turn

