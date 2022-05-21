import asyncio
from matplotlib.pyplot import spring

from wizwalker import Client
from wizwalker import XYZ
from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter.sprinty_client import MemoryReadError

potion_ui_buy = [
    "fillallpotions",
    "buyAction",
    "btnShopPotions",
    "centerButton",
    "fillonepotion",
    "buyAction",
    "exit"
]



async def is_visible_by_path(client: Client, path: list[str]):
	# FULL CREDIT TO SIROLAF FOR THIS FUNCTION
	# checks visibility of a window from the path
	root = client.root_window
	windows = await get_window_from_path(root, path)
	if windows == False:
		return False
	elif await windows.is_visible():
		return True
	else:
		return False

async def is_control_grayed(button):
    return await button.read_value_from_offset(688, "bool")

async def get_window_from_path(root_window, name_path):
    async def _recurse_follow_path(window, path):
        if len(path) == 0:
            return window

        for child in await window.children():
            if await child.name() == path[0]:
                found_window = await _recurse_follow_path(child, path[1:])
                if not found_window is False:
                    return found_window

        return False

    return await _recurse_follow_path(root_window, name_path)

async def auto_buy_potions_dungeon(client):
    # Head to home world gate
    await asyncio.sleep(0.1)
    await client.send_key(Keycode.HOME, 0.1)
    await client.send_key(Keycode.HOME, 0.1)
    await client.wait_for_zone_change()
    while not await client.is_in_npc_range():
        await client.send_key(Keycode.S, 0.1)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(1.2)
    tp_to_closest_mob = XYZ(-18.375408172607422, 376.6935729980469, 2.199798583984375)
    # Go to Wizard City
    leftButton = await get_window_from_path(
        client.root_window,
        ['WorldView','', 'messageBoxBG', 'ControlSprite', 'optionWindow', 'leftButton'])
    while not await is_control_grayed(leftButton):
        await client.mouse_handler.click_window(leftButton)
    await client.mouse_handler.click_window_with_name('wbtnWizardCity')
    await asyncio.sleep(0.6)
    await client.mouse_handler.click_window_with_name('teleportButton')
    await client.wait_for_zone_change()
    # Walk to potion vendor
    await client.goto(-0.5264079570770264, -3021.25244140625)
    await client.send_key(Keycode.W, 0.5)
    await client.wait_for_zone_change()
    await client.goto(11.836355209350586, -1816.455078125)
    await client.send_key(Keycode.W, 0.5)
    await client.wait_for_zone_change()
    await client.goto(-587.87927246093752, 404.43939208984375)
    await asyncio.sleep(1)
    await client.goto(-3965.254638671875, 1535.5472412109375)
    await asyncio.sleep(1)
    await client.goto(-4442.06005859375, 1001.5532836914062)
    await asyncio.sleep(1)
    while not await client.is_in_npc_range():
        await client.goto(-4442.06005859375, 1001.5532836914062)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(1.5)
    # Buy potions
    while True:
        try:
            for i in potion_ui_buy:
                await client.mouse_handler.click_window_with_name(i)
                await asyncio.sleep(0.8)
        except ValueError:
            continue
        break
    # Return
    await asyncio.sleep(.4)
    await client.send_key(Keycode.PAGE_UP, 0.1)
    await client.wait_for_zone_change()
    await client.send_key(Keycode.PAGE_DOWN, 0.1)
    await client.mouse_handler.click_window_with_name('ResumeInstanceButton')
    await client.wait_for_zone_change()
    await client.teleport(tp_to_closest_mob)

async def get_text(client, text):
    name, *_ = await client.root_window.get_windows_with_name(f"{text}")
    text = (await name.maybe_text())
    return text

async def get_objective(p) -> str:
    obj = await get_text(p, "txtGoalName")
    obj = obj.split("in ", 1)[0]
    obj = obj.lower()
    obj = obj.split("<center>", 1)[1]
    return obj


async def go_through_dialog(client):
    while not await client.is_in_dialog():
        await asyncio.sleep(0.1)
    while await client.is_in_dialog():
        await client.send_key(Keycode.SPACEBAR, 0.1)

async def decide_heal_dungeon(client):
    if await client.needs_potion(health_percent=70, mana_percent=25):
        print(f'[{client.title}] Health is at {round((await client.calc_health_ratio()* 100), 2)}% and mana is at {round((await client.calc_mana_ratio() * 100), 2)}%. Need to recover.')
        if await client.has_potion():
            await client.use_potion()
            
        elif await client.stats.current_gold() >= 20000 and await client.stats.reference_level() > 5: 
            print(f"[{client.title}] Enough gold, buying potions")
            await auto_buy_potions_dungeon(client)

async def decide_heal(client):
    if await client.needs_potion(health_percent=70, mana_percent=25):
        print(f'[{client.title}] Health is at {round((await client.calc_health_ratio()* 100), 2)}% and mana is at {round((await client.calc_mana_ratio() * 100), 2)}%. Need to recover.')
        if await client.has_potion():
            await client.use_potion()
            
        elif await client.stats.current_gold() >= 20000 and await client.stats.reference_level() > 5: 
            print(f"[{client.title}] Enough gold, buying potions")
            await auto_buy_potions(client)
        

async def logout_and_in(client):
        print(f'[{client.title}] Logging out and in')
        await asyncio.sleep(0.6)
        await client.send_key(Keycode.ESC, 0.1)
        await asyncio.sleep(2)
        try:
            await client.mouse_handler.click_window_with_name('QuitButton')
        except ValueError:
            await client.send_key(Keycode.ESC, 0.1)
            await asyncio.sleep(2.5)
            await client.mouse_handler.click_window_with_name('QuitButton')
        await asyncio.sleep(2.5)
        if await client.root_window.get_windows_with_name('centerButton'):
            await asyncio.sleep(2.5)
            await client.mouse_handler.click_window_with_name('centerButton')
        await asyncio.sleep(8)
        await client.mouse_handler.click_window_with_name('btnPlay')
        await client.wait_for_zone_change()


async def tp_to_p1(client, p1):
    p1pos = await p1.body.position()
    await client.teleport(p1pos, wait_on_inuse=True)
    await asyncio.sleep(0.3)
    await client.send_key(Keycode.W, 0.1)
    await client.send_key(Keycode.D, 0.1)
    await asyncio.sleep(0.2)
    

async def auto_buy_potions(client):
    # Head to home world gate
    await asyncio.sleep(0.1)
    await client.send_key(Keycode.HOME, 0.1)
    await client.send_key(Keycode.HOME, 0.1)
    await client.wait_for_zone_change()
    while not await client.is_in_npc_range():
        await client.send_key(Keycode.S, 0.1)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(1.2)

    # Go to Wizard City
    leftButton = await get_window_from_path(
        client.root_window,
        ['WorldView','', 'messageBoxBG', 'ControlSprite', 'optionWindow', 'leftButton'])
    while not await is_control_grayed(leftButton):
        await client.mouse_handler.click_window(leftButton)
    await client.mouse_handler.click_window_with_name('wbtnWizardCity')
    await asyncio.sleep(0.15)
    await client.mouse_handler.click_window_with_name('teleportButton')
    await client.wait_for_zone_change()
    # Walk to potion vendor
    await client.goto(-0.5264079570770264, -3021.25244140625)
    await client.send_key(Keycode.W, 0.5)
    await client.wait_for_zone_change()
    await client.goto(11.836355209350586, -1816.455078125)
    await client.send_key(Keycode.W, 0.5)
    await client.wait_for_zone_change()
    await client.goto(-587.87927246093752, 404.43939208984375)
    await asyncio.sleep(1)
    await client.goto(-3965.254638671875, 1535.5472412109375)
    await asyncio.sleep(1)
    await client.goto(-4442.06005859375, 1001.5532836914062)
    await asyncio.sleep(1)
    while not await client.is_in_npc_range():
        await client.goto(-4442.06005859375, 1001.5532836914062)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(1)
    # Buy potions
    while True:
        try:
            for i in potion_ui_buy:
                await client.mouse_handler.click_window_with_name(i)
                await asyncio.sleep(0.8)
        except ValueError:
            continue
        break
    # Return
    await client.send_key(Keycode.PAGE_UP, 0.1)
    await client.wait_for_zone_change()
    await client.send_key(Keycode.PAGE_DOWN, 0.1)
