import asyncio
from pyrogram import client
from ubot.core.database import *

# Inisialisasi variabel global
jaseb_active = False
jaseb_text = "Pesan default"
jaseb_interval = 60  # Interval waktu dalam detik
jaseb_target = None

# Fungsi untuk memuat pengaturan dari database
async def load_jaseb_settings():
    global jaseb_text, jaseb_interval, jaseb_target
    jaseb_text = await jaseb_db.get_jaseb_text() or jaseb_text
    jaseb_interval = await jaseb_db.get_jaseb_interval() or jaseb_interval
    jaseb_target = await jaseb_db.get_jaseb_target() or jaseb_target

# Fungsi untuk menyimpan pengaturan ke database
async def save_jaseb_settings():
    await jaseb_db.set_jaseb_text(jaseb_text)
    await jaseb_db.set_jaseb_interval(jaseb_interval)
    await jaseb_db.set_jaseb_target(jaseb_target)

async def set_jaseb_active(active: bool, client):
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

async def set_jaseb_target(target: int):
    global jaseb_target
    jaseb_target = target
    await save_jaseb_settings()

async def jaseb_sender(client):
    global jaseb_active, jaseb_text, jaseb_interval, jaseb_target
    while jaseb_active:
        if jaseb_target:
            try:
                await client.send_message(jaseb_target, jaseb_text)
            except Exception as e:
                print(f"Error sending message: {e}")
        await asyncio.sleep(jaseb_interval)
