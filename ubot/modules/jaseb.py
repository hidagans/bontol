import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from ubot import *

__MODULE__ = "jaseb"
__HELP__ = """
<b> Bantuan untuk Jaseb </b>

   <b> Perintah:</b> <code>{0}setjaseb (on/off)</code>
   <b> Penjelasan:</b> Untuk mengaktifkan dan menonaktifkan Jaseb.

  <b> Perintah:</b> <code>{0}setjasebtext (teks)</code>
  <b> Penjelasan:</b> Untuk mengatur teks pesan Jaseb.

  <b> Perintah:</b> <code>{0}setjasebinterval (detik)</code>
  <b> Penjelasan:</b> Untuk mengatur interval waktu pengiriman pesan Jaseb dalam detik.

  <b> Perintah:</b> <code>{0}setjasebtarget (ID grup)</code>
  <b> Penjelasan:</b> Untuk mengatur target grup atau channel Jaseb.
"""

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
    arg = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
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
    jaseb_text = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    await save_jaseb_settings()
    await message.reply_text(f"Teks Jaseb diatur ke: {jaseb_text}")

@PY.UBOT("setjasebinterval", SUDO=True)
async def set_jaseb_interval(client: Client, message: Message):
    global jaseb_interval
    try:
        jaseb_interval = int(message.text.split(maxsplit=1)[1])
        await save_jaseb_settings()
        await message.reply_text(f"Interval Jaseb diatur ke: {jaseb_interval} detik")
    except ValueError:
        await message.reply_text("Interval harus berupa angka.")

@PY.UBOT("setjasebtarget", SUDO=True)
async def set_jaseb_target(client: Client, message: Message):
    global jaseb_target
    try:
        jaseb_target = int(message.text.split(maxsplit=1)[1])
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
