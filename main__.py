import os
import asyncio
from typing import *

from wizwalker import ClientHandler, client
from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter
from wizwalker.memory import memory_objects
from wizwalker.memory.handler import HookHandler
from wizwalker import XYZ
from wizwalker.memory.memory_objects.client_object import DynamicClientObject


with open('accounts.txt') as fileVar:
    accounts = fileVar.read().splitlines()

creation_buttons = [
    'SkipButton',
    'SkipButton',
    'SkipButton',
    'SelectIceButton',
    'OKButton',
    'NextButton',
    'NextButton',
    'RandomButton',
    'DoneButton',
    'btnPlay'
]


async def set_completed(account):
    with open("completed.txt", "a") as file:
        file.write(account + "\n")

async def go_to_closest_mob(self, excluded_ids: Set[int] = None) -> bool:
    return await go_to_closest_of(self,await self.get_mobs(excluded_ids), False)

async def go_to_closest_of(self, entities: List[DynamicClientObject], only_safe: bool = False):
    if e := await self.find_closest_of_entities(entities, only_safe):
        ev = await e.location()
        await self.goto(ev.x, ev.y)
        return True
    return False

async def battleship(client):
        print("Combat Initiated")
        combat_handlers = []
        #Setting up the parsed configs to combat_handlers
        combat_handlers.append(SprintyCombat(client, CombatConfigProvider("configs/spellconfig.txt", cast_time=0.5 )))
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers]) # .wait_for_combat() to wait for combat to then go through the battles
        print ("Combat ended")
        await client.send_key(Keycode.D, 0.3)
        await asyncio.sleep(6.5)
        print ("Starting Second Battle")
        await go_to_closest_mob(client)
        # Battle:
        print ("Combat Initiated")
        combat_handlers = []
        # Setting up the parsed configs to combat_handlers
        combat_handlers.append(SprintyCombat(client, CombatConfigProvider("configs/spellconfig.txt", cast_time=0.5 )))
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers]) # .wait_for_combat() to wait for combat to then go through the battles
        print ("Combat ended")
        await asyncio.sleep(0.4)

async def bone_cages(client):
        await asyncio.sleep(1)
        await client.teleport(await client.quest_position.position())
        await asyncio.sleep(1.5)
        await client.send_key(Keycode.D, 0.1)
        await asyncio.sleep(0.5)
        await client.send_key(Keycode.X, 0.6)
        await asyncio.sleep(0.5)
        await client.teleport(await client.quest_position.position())
        await asyncio.sleep(1.5)
        await client.send_key(Keycode.D, 0.1)
        await asyncio.sleep(1.5)
        await client.send_key(Keycode.X, 0.6)

async def go_through_dialog(client):
    while not await client.is_in_dialog():
        await asyncio.sleep(0.1)
    while await client.is_in_dialog():
        await client.send_key(Keycode.SPACEBAR, 0.1)


async def main(sprinter):
    for account in accounts:
        username, password = account.split(':')
        
        print ("Launching Wizard101")
        ClientHandler.start_wiz_client()
        while len(clients := sprinter.get_new_clients()) == 0:
            await asyncio.sleep(0.5)
        client = clients[0]
        client.login(username, password)


        print ("Activating Some Hooks")
        await client.hook_handler.activate_root_window_hook()
        await client.hook_handler.activate_render_context_hook()
        await client.mouse_handler.activate_mouseless()
        client.title = "Level5Bot"

        print ("Starting character creation")
        await client.send_key(Keycode.W)
        for i in range(30):
            await client.send_key(Keycode.SPACEBAR)
        await asyncio.sleep(1)
        for button in creation_buttons:
            print (f"Clicking on {button}")
            await client.mouse_handler.click_window_with_name(button)
            await client.send_key(Keycode.SPACEBAR)
            await asyncio.sleep(2)
        print ("Leaving and rejoining to skip tutorial")
        await asyncio.sleep(2.5)
        os.system("taskkill /f /im  WizardGraphicalClient.exe")
               
        print ("Launching Wizard101")
        ClientHandler.start_wiz_client()
        while len(clients := sprinter.get_new_clients()) == 0:
            await asyncio.sleep(0.5)
        client = clients[0]
        client.login(username, password)


        print ("Activating Some Hooks")
        await client.hook_handler.activate_root_window_hook()
        await client.hook_handler.activate_render_context_hook()
        await client.mouse_handler.activate_mouseless()
        client.title = "Level5Bot"

        await asyncio.sleep(3)
        await client.send_key(Keycode.W)
        await asyncio.sleep(3)
        await client.send_key(Keycode.ENTER)
        await asyncio.sleep(5)
        await client.mouse_handler.click_window_with_name('SkipButton')
        await client.mouse_handler.click_window_with_name('SkipButton')
        await asyncio.sleep(1)
        await client.mouse_handler.click_window_with_name('leftButton')
        await level_2(client)
        await level_3(client)
        await level_4(client)
        await level_5(client)
        await set_completed(account)


async def level_2(client):
        await asyncio.sleep(4)
        print ("Walking And Talking To Ambrose")
        await client.send_key(Keycode.W, 1.5)
        await asyncio.sleep(0.3)
        await client.send_key(Keycode.X, 0.3)
        await asyncio.sleep(0.3)
        await go_through_dialog(client)
        await asyncio.sleep(3)
        print ("Talking To Gamma")
        await go_through_dialog(client)
        print ("Walking To Connelly")
        await client.send_key(Keycode.W, 1.7)
        await asyncio.sleep(0.3)
        await client.send_key(Keycode.X, 0.3)
        await asyncio.sleep(0.3)
        print ("Talking To Connelly")
        await go_through_dialog(client)
        await asyncio.sleep(0.3)
        await go_through_dialog(client)
        await asyncio.sleep(0.3)
        print ("Activating Quest And Duel Hooks")
        await client.hook_handler.activate_quest_hook()
        await client.hook_handler.activate_player_hook()
        await client.hook_handler.activate_client_hook()
        await client.hook_handler.activate_duel_hook()
        await asyncio.sleep(2)
        print ("Teleporting To Lost Souls")
        await client.teleport(await client.quest_position.position())
        await asyncio.sleep(1.5)
        await go_to_closest_mob(client)
        await asyncio.sleep(1)
        await battleship(client)
        print ("Talking To The Lost Souls")
        await go_through_dialog(client)
        await asyncio.sleep(0.4)
        print ("Teleporting To Connelly")
        await asyncio.sleep(0.4)
        await client.teleport(await client.quest_position.position())
        await asyncio.sleep(1)
        await client.send_key(Keycode.D, 0.3)
        print ("Talking To Connelly")
        await client.send_key(Keycode.X, 0.4)
        await go_through_dialog(client)
        await asyncio.sleep(4)
        print ("Teleporting And Talking With Ceren")
        await client.teleport(await client.quest_position.position())
        await asyncio.sleep(0.3)
        await client.send_key(Keycode.D, 0.2)
        await asyncio.sleep(0.7)
        await client.send_key(Keycode.X, 0.1)
        await go_through_dialog(client)
        print ("Level 2 Done!")


async def level_3(client):
        await go_through_dialog(client)
        await asyncio.sleep(1.5)
        await client.teleport(await client.quest_position.position())
        await asyncio.sleep(2)
        print ("Teleporting To Skeletal Pirates")
        await client.teleport(await client.quest_position.position())
        await asyncio.sleep(1.5)
        await go_to_closest_mob(client)
        await asyncio.sleep(1)
        await battleship(client)
        print ("Talking To Skeletal Pirates")
        await asyncio.sleep(0.4)
        await go_through_dialog(client)
        await asyncio.sleep(0.4)
        print ("Teleporting To Ceren")
        await asyncio.sleep(2)
        await client.teleport(await client.quest_position.position())
        await asyncio.sleep(1)
        await client.send_key(Keycode.D, 0.2)
        await asyncio.sleep(0.4)
        await client.send_key(Keycode.X, 0.1)
        await asyncio.sleep(1)
        await go_through_dialog(client)
        print ("Level 3 Done!")


async def level_4(client):
        await asyncio.sleep(0.8)
        await go_through_dialog(client)
        await asyncio.sleep(3)
        print ("Teleporting To Lady Oriel")
        await asyncio.sleep(3)
        await client.teleport(XYZ(-29550, 19501, 162))
        await asyncio.sleep(5)
        await client.send_key(Keycode.W, 1)
        await go_through_dialog(client)
        await asyncio.sleep(3)
        await client.teleport(await client.quest_position.position())
        await asyncio.sleep(3)
        print ("Talking To Lady Oriel")
        await asyncio.sleep(1)
        await client.send_key(Keycode.D, 0.2)
        await asyncio.sleep(0.5)
        await client.send_key(Keycode.X, 0.6)
        await asyncio.sleep(1)
        await go_through_dialog(client)
        await asyncio.sleep(1)
        await go_through_dialog(client)
        await asyncio.sleep(3)
        await client.teleport(XYZ(588.1171875, -3368.130859375, 162.33975219726562))
        await asyncio.sleep(5)
        print ("Teleporting To Bone Cages")
        await bone_cages(client)
        await asyncio.sleep(3)
        print ("Teleporting To Dark Fairies")
        await client.teleport(await client.quest_position.position())
        await asyncio.sleep(2)
        await go_to_closest_mob(client)
        await asyncio.sleep(1)
        await battleship(client)
        print ("Talking To Dark Fairies")
        await go_through_dialog(client)
        await asyncio.sleep(3)
        print ("Opening The Other Two Bone Cages")
        await bone_cages(client)
        await asyncio.sleep(1)
        print ("Teleporting To Lady Oriel")
        await asyncio.sleep(1.5)
        await client.teleport(XYZ(-29550, 19501, 162))
        await asyncio.sleep(0.3)
        await client.wait_for_zone_change()
        print ("Talking To Fairies And Lady Oriel")
        await asyncio.sleep(0.8)
        await client.send_key(Keycode.W, 1)
        await asyncio.sleep(0.5)
        await go_through_dialog(client)
        await asyncio.sleep(1.5)
        await go_through_dialog(client)
        await asyncio.sleep(3)
        await client.teleport(await client.quest_position.position())
        await client.send_key(Keycode.W, 0.2)
        await asyncio.sleep(1)
        await client.send_key(Keycode.X, 0.2)
        await go_through_dialog(client)
        await asyncio.sleep(1)
        await go_through_dialog(client)
        print ("Level 4 Done!")


async def level_5(client):
        await asyncio.sleep(3)
        await client.teleport(XYZ(588.1171875, -3368.130859375, 162.33975219726562))
        await asyncio.sleep(5)
        print ("Teleporting And Talking To Ceren")
        await asyncio.sleep(1)
        await client.teleport(await client.quest_position.position())
        await client.send_key(Keycode.W, 0.1)
        await asyncio.sleep(2)
        await client.send_key(Keycode.X, 0.2)
        await go_through_dialog(client)
        await asyncio.sleep(0.3)
        await go_through_dialog(client)
        await asyncio.sleep(0.3)
        await client.send_key(Keycode.PAGE_DOWN, 0.1)
        await asyncio.sleep(0.3)
        print ("Teleporting To And Fighting Rattlebones")
        await asyncio.sleep(1)
        await client.teleport(XYZ(-16490.9921875, 18904.318359375, 33.5146484375))
        await asyncio.sleep(3)
        await client.send_key(Keycode.D, 0.4)
        await asyncio.sleep(1)
        await client.send_key(Keycode.W, 0.6)
        await asyncio.sleep(0.3)
        await client.wait_for_zone_change()
        await asyncio.sleep(0.3)
        await client.send_key(Keycode.W, 0.3)
        await asyncio.sleep(0.3)
        await go_through_dialog(client)
        await client.send_key(Keycode.W, 1.5)
        await asyncio.sleep(0.3)
        # Battle:
        print("Combat Initiated")
        combat_handlers = []
        # Setting up the parsed configs to combat_handlers
        combat_handlers.append(SprintyCombat(client, CombatConfigProvider('configs/spellconfig.txt', cast_time=0.5 )))
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers]) # .wait_for_combat() to wait for combat to then go through the battles
        print("Combat ended")
        await asyncio.sleep(0.5)
        await go_through_dialog(client)
        await asyncio.sleep(4)
        print ("Teleporting Back To Ceren")
        await client.send_key(Keycode.PAGE_UP, 0.1)
        await asyncio.sleep(2.5)
        await go_through_dialog(client)
        await asyncio.sleep(0.5)
        await client.send_key(Keycode.X, 0.1)
        await go_through_dialog(client)
        await asyncio.sleep(0.3)
        await go_through_dialog(client)
        await asyncio.sleep(1)
        print ("Teleporting To Commons")
        await client.send_key(Keycode.END, 0.2)
        await asyncio.sleep(3)
        await client.wait_for_zone_change()
        await asyncio.sleep(3)
        await client.teleport(await client.quest_position.position())
        await asyncio.sleep(0.3)
        await client.send_key(Keycode.A, 0.2)
        await asyncio.sleep(3)
        await client.send_key(Keycode.UP_ARROW, 1.5)
        await asyncio.sleep(0.3)
        await client.send_key(Keycode.X, 0.2)
        await go_through_dialog(client)
        await asyncio.sleep(0.3)
        await client.send_key(Keycode.S, 2)
        await asyncio.sleep(3)
        print ("Teleporting To Ambrose")
        await asyncio.sleep(3)
        await client.teleport(await client.quest_position.position())
        await client.send_key(Keycode.A, 0.2)
        await asyncio.sleep(3.5)
        await client.send_key(Keycode.W, 1.6)
        await asyncio.sleep(0.3)
        await client.send_key(Keycode.X, 0.4)
        await asyncio.sleep(0.6)
        await go_through_dialog(client)
        await asyncio.sleep(0.3)
        await go_through_dialog(client)
        await asyncio.sleep(0.3)
        print ("Level 5 Done!")


# Error Handling
async def run():
    sprinter = WizSprinter()

    try:
        await main(sprinter)
    except:
        import traceback

        traceback.print_exc()

    await sprinter.close()


# Start
if __name__ == "__main__":
    asyncio.run(run())
