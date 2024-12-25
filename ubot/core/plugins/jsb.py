import asyncio
from pyrogram import Client
from ubot.core.database import jaseb_db

# Fungsi untuk memuat pengaturan dari database
async def load_jaseb_settings(user_id):
    return await jaseb_db.get_jaseb_settings(user_id)

# Fungsi untuk menyimpan pengaturan ke database
async def save_jaseb_settings(user_id, jaseb_status, text, interval, targets):
    await jaseb_db.set_jaseb_settings(user_id, jaseb_status, text, interval, targets)

async def set_jaseb_active(user_id, active: bool, client: Client):
    jaseb_status, jaseb_text, jaseb_interval, jaseb_targets = await load_jaseb_settings(user_id)
    jaseb_status = "on" if active else "off"
    await save_jaseb_settings(user_id, jaseb_status, jaseb_text, jaseb_interval, jaseb_targets)
    if active:
        asyncio.create_task(jaseb_sender(user_id, client))

async def set_jaseb_text(user_id, text: str):
    jaseb_status, jaseb_text, jaseb_interval, jaseb_targets = await load_jaseb_settings(user_id)
    jaseb_text = text
    await save_jaseb_settings(user_id, jaseb_status, jaseb_text, jaseb_interval, jaseb_targets)

async def set_jaseb_interval(user_id, interval: int):
    jaseb_status, jaseb_text, jaseb_interval, jaseb_targets = await load_jaseb_settings(user_id)
    jaseb_interval = interval
    await save_jaseb_settings(user_id, jaseb_status, jaseb_text, jaseb_interval, jaseb_targets)

async def add_jaseb_target(user_id, target: int):
    jaseb_status, jaseb_text, jaseb_interval, jaseb_targets = await load_jaseb_settings(user_id)
    if not str(target).startswith("-100"):
        target = int(f"-100{target}")
    if target not in jaseb_targets:
        jaseb_targets.append(target)
        await save_jaseb_settings(user_id, jaseb_status, jaseb_text, jaseb_interval, jaseb_targets)

async def remove_jaseb_target(user_id, target: int):
    jaseb_status, jaseb_text, jaseb_interval, jaseb_targets = await load_jaseb_settings(user_id)
    if target in jaseb_targets:
        jaseb_targets.remove(target)
        await save_jaseb_settings(user_id, jaseb_status, jaseb_text, jaseb_interval, jaseb_targets)

async def jaseb_sender(user_id, client: Client):
    jaseb_status, jaseb_text, jaseb_interval, jaseb_targets = await load_jaseb_settings(user_id)
    while jaseb_status == "on":
        for target in jaseb_targets:
            try:
                await client.send_message(target, jaseb_text)
            except Exception as e:
                print(f"Error sending message to {target}: {e}")
        await asyncio.sleep(jaseb_interval)
