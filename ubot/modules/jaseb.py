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

@PY.UBOT("setjaseb", SUDO=True)
async def set_jaseb(client: Client, message: Message):
    arg = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    if arg == "on":
        await set_jaseb_active(True, client)
        await message.reply_text("Jaseb diaktifkan.")
    elif arg == "off":
        await set_jaseb_active(False, client)
        await message.reply_text("Jaseb dinonaktifkan.")
    else:
        await message.reply_text("Gunakan perintah .setjaseb on/off")

@PY.UBOT("setjasebtext", SUDO=True)
async def set_jaseb_text_command(client: Client, message: Message):
    text = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    await set_jaseb_text(text)
    await message.reply_text(f"Teks Jaseb diatur ke: {text}")

@PY.UBOT("setjasebinterval", SUDO=True)
async def set_jaseb_interval_command(client: Client, message: Message):
    try:
        interval = int(message.text.split(maxsplit=1)[1])
        await set_jaseb_interval(interval)
        await message.reply_text(f"Interval Jaseb diatur ke: {interval} detik")
    except ValueError:
        await message.reply_text("Interval harus berupa angka.")

@PY.UBOT("setjasebtarget", SUDO=True)
async def set_jaseb_target_command(client: Client, message: Message):
    try:
        target = int(message.text.split(maxsplit=1)[1])
        await set_jaseb_target(target)
        await message.reply_text(f"Target Jaseb diatur ke: {target}")
    except ValueError:
        await message.reply_text("ID grup harus berupa angka.")

# Memuat pengaturan saat bot dijalankan
asyncio.create_task(load_jaseb_settings())
