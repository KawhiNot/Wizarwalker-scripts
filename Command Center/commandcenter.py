import asyncio
from time import time

from wizwalker.extensions.wizsprinter import WizSprinter
from wizwalker.constants import Keycode
from wizwalker.extensions.scripting.utils import teleport_to_friend_from_list
from SlackFighter import SlackFighter
from utils import decide_heal_dungeon , logout_and_in , go_through_dialog , tp_to_p1 , decide_heal

async def setup(client):
    print(f"[{client.title}] Activating Hooks")
    await client.activate_hooks()
    await client.mouse_handler.activate_mouseless()
    await client.send_key(Keycode.PAGE_DOWN, 0.1)

async def mouseless(client):
    await client.mouse_handler.activate_mouseless()


async def main(sprinter):
    # Register clients
    sprinter.get_new_clients()
    clients = sprinter.get_ordered_clients()
    p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
    for i, p in enumerate(clients, 1):
        p.title = "p" + str(i)

    # Hook activation
    await asyncio.gather(*[setup(p) for p in clients])
    
    Total_Count = 0
    total = time()
    while True:

        await asyncio.sleep(1)
        await asyncio.gather(*[decide_heal(p) for p in clients])

        start = time()
        # Entering Dungeon
        for p in clients:
            for p in clients:
                await asyncio.sleep(0.1)
                await p1.send_key(Keycode.A, 0.4)
                await asyncio.sleep(1.5)
            await asyncio.gather(*[p.send_key(Keycode.A, 0.4) for p in clients[1:]]) #sending a for other clients
            await asyncio.sleep(1)
            while await p1.is_in_npc_range():
                await asyncio.sleep(1)
                await p1.send_key(Keycode.X, 0.1)
                await p1.wait_for_zone_change()
            print(f"[{p.title}] Teleporting to P1")
            await asyncio.gather(*[p.send_key(Keycode.F, 0.1) for p in clients[1:]]) #sending f for other clients
            await asyncio.sleep(1)
            await asyncio.gather(*[teleport_to_friend_from_list(p, icon_list=2, icon_index=0) for p in clients[1:]]) #Fish Icon in friends list
            await asyncio.gather(*[p.wait_for_zone_change() for p in clients[1:]])
            await asyncio.sleep(1.4)
            await asyncio.gather(*[go_through_dialog(p) for p in clients])
            await asyncio.sleep(0.7)
            await p1.tp_to_closest_mob()
            await asyncio.sleep(0.1)
            await p1.send_key(Keycode.W, 0.1)
            await asyncio.sleep(1)
            await asyncio.gather(*[tp_to_p1(p, p1) for p in clients])
            await asyncio.sleep(0.3)
            # Battle
            print("Starting First Battle")
            battles = []
            for client in clients:
                battles.append(SlackFighter(client))
            while True:
                if await SlackFighter(p1).is_fighting():
                    await asyncio.gather(*[battle.wait_for_combat() for battle in battles])
                    print("Combat Ended")
                    break
                await asyncio.sleep(0.1)
            await asyncio.gather(*[mouseless(p) for p in clients])
            await asyncio.sleep(4)
            await asyncio.gather(*[go_through_dialog(p) for p in clients])
            await asyncio.sleep(1)
            await p1.send_key(Keycode.W, 0.3)
            await asyncio.gather(*[p.send_key(Keycode.W, 0.3) for p in clients[1:]]) #sending W for other clients
            await asyncio.sleep(0.5)
            # Checking for healing
            await asyncio.gather(*[decide_heal_dungeon(p) for p in clients])
            await asyncio.sleep(7.5)
            for p in clients:
                await p1.tp_to_closest_mob()
                await asyncio.sleep(1)
                await p1.send_key(Keycode.W, 0.1)
            await asyncio.gather(*[tp_to_p1(p, p1) for p in clients])
            # Battle
            print("Starting Second Battle")
            battles = []
            for client in clients:
                battles.append(SlackFighter(client))
            while True:
                if await SlackFighter(p1).is_fighting():
                    await asyncio.gather(*[battle.wait_for_combat() for battle in battles])
                    print("Combat Ended")
                    break
                await asyncio.sleep(0.1)
            await asyncio.gather(*[mouseless(p) for p in clients])
            await asyncio.sleep(4)
            await asyncio.gather(*[logout_and_in(p) for p in clients])

            # Time
            Total_Count += 1
            print("------------------------------------------------------")
            print("The Total Amount of Runs: ", Total_Count)
            print("Time Taken for run: ", round((time() - start) / 60, 2), "minutes")
            print("Total time elapsed: ", round((time() - total) / 60, 2), "minutes")
            print("Average time per run: ", round(((time() - total) / 60) / Total_Count, 2), "minutes")
            print("------------------------------------------------------")



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
