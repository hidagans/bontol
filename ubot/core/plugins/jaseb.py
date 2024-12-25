import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from ubot import ubot, get_arg

# Inisialisasi variabel global
jaseb_active = False
jaseb_text = "Pesan default"
jaseb_interval = 60  # Interval waktu dalam detik
jaseb_target = None

@PY.UBOT("setjaseb")
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

@PY.UBOY("setjasebtext")
async def set_jaseb_text(client: Client, message: Message):
    global jaseb_text
    jaseb_text = get_arg(message)
    await message.reply_text(f"Teks Jaseb diatur ke: {jaseb_text}")

@PY.UBOT("setjasebinterval")
async def set_jaseb_interval(client: Client, message: Message):
    global jaseb_interval
    try:
        jaseb_interval = int(get_arg(message))
        await message.reply_text(f"Interval Jaseb diatur ke: {jaseb_interval} detik")
    except ValueError:
        await message.reply_text("Interval harus berupa angka.")

@PY.UBOT("setjasebtarget")
async def set_jaseb_target(client: Client, message: Message):
    global jaseb_target
    jaseb_target = get_arg(message)
    await message.reply_text(f"Target Jaseb diatur ke: {jaseb_target}")

async def jaseb_sender(client, message):
    global jaseb_active, jaseb_text, jaseb_interval, jaseb_target
    while jaseb_active:
        if jaseb_target:
            try:
                await client.send_message(jaseb_target, jaseb_text)
            except Exception as e:
                print(f"Error sending message: {e}")
        await asyncio.sleep(jaseb_interval)
