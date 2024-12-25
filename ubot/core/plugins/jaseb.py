import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from ubot import get_arg
from ubot.core.database import jaseb_db
from ubot.core.helpers.client import PY

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

@PY.UBOT("setjaseb", SUDO=True)
async def set_jaseb(client: Client, message: Message):
    global jaseb_active
    arg = get_arg(message)
    if arg == "on":
        jaseb_active = True
        await message.reply_text("Jaseb diaktifkan.")
        asyncio.create_task(jaseb_sender(client))
    elif arg == "off":
        jaseb_active = False
        await message.reply_text("Jaseb dinonaktifkan.")
    else:
        await message.reply_text("Gunakan perintah .setjaseb on/off")

@PY.UBOT("setjasebtext", SUDO=True)
async def set_jaseb_text(client: Client, message: Message):
    global jaseb_text
    jaseb_text = get_arg(message)
    await save_jaseb_settings()
    await message.reply_text(f"Teks Jaseb diatur ke: {jaseb_text}")

@PY.UBOT("setjasebinterval", SUDO=True)
async def set_jaseb_interval(client: Client, message: Message):
    global jaseb_interval
    try:
        jaseb_interval = int(get_arg(message))
        await save_jaseb_settings()
        await message.reply_text(f"Interval Jaseb diatur ke: {jaseb_interval} detik")
    except ValueError:
        await message.reply_text("Interval harus berupa angka.")

@PY.UBOT("setjasebtarget", SUDO=True)
async def set_jaseb_target(client: Client, message: Message):
    global jaseb_target
    try:
        jaseb_target = int(get_arg(message))
        await save_jaseb_settings()
        await message.reply_text(f"Target Jaseb diatur ke: {jaseb_target}")
    except ValueError:
        await message.reply_text("ID grup harus berupa angka.")

async def jaseb_sender(client: Client):
    global jaseb_active, jaseb_text, jaseb_interval, jaseb_target
    while jaseb_active:
        if jaseb_target:
            try:
                await client.send_message(jaseb_target, jaseb_text)
            except Exception as e:
                print(f"Error sending message: {e}")
        await asyncio.sleep(jaseb_interval)

# Memuat pengaturan saat bot dijalankan
asyncio.create_task(load_jaseb_settings())
