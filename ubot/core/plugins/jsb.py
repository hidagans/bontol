import asyncio
from pyrogram import Client
from ubot.core.database import jaseb_db

# Inisialisasi variabel global
jaseb_active = False
jaseb_text = "Pesan default"
jaseb_interval = 60  # Interval waktu dalam detik
jaseb_targets = []

# Fungsi untuk memuat pengaturan dari database
async def load_jaseb_settings():
    global jaseb_text, jaseb_interval, jaseb_targets
    jaseb_text = await jaseb_db.get_jaseb_text() or jaseb_text
    jaseb_interval = await jaseb_db.get_jaseb_interval() or jaseb_interval
    jaseb_targets = await jaseb_db.get_jaseb_targets() or jaseb_targets

# Fungsi untuk menyimpan pengaturan ke database
async def save_jaseb_settings():
    await jaseb_db.set_jaseb_text(jaseb_text)
    await jaseb_db.set_jaseb_interval(jaseb_interval)
    await jaseb_db.set_jaseb_targets(jaseb_targets)

async def set_jaseb_active(active: bool, client: Client):
    global jaseb_active
    jaseb_active = active
    if active:
        asyncio.create_task(jaseb_sender(client))

async def set_jaseb_text(text: str):
    global jaseb_text
    jaseb_text = text
    await save_jaseb_settings()

async def set_jaseb_interval(interval: int):
    global jaseb_interval
    jaseb_interval = interval
    await save_jaseb_settings()

async def add_jaseb_target(target: int):
    global jaseb_targets
    # Memastikan ID grup atau channel memiliki awalan -100
    if not str(target).startswith("-100"):
        target = int(f"-100{target}")
    if target not in jaseb_targets:
        jaseb_targets.append(target)
        await save_jaseb_settings()

async def remove_jaseb_target(target: int):
    global jaseb_targets
    if target in jaseb_targets:
        jaseb_targets.remove(target)
        await save_jaseb_settings()

async def jaseb_sender(client: Client):
    global jaseb_active, jaseb_text, jaseb_interval, jaseb_targets
    while jaseb_active:
        for target in jaseb_targets:
            try:
                await client.send_message(target, jaseb_text)
            except Exception as e:
                print(f"Error sending message to {target}: {e}")
        await asyncio.sleep(jaseb_interval)
