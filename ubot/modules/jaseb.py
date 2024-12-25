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
  <b> Penjelasan:</b> Untuk menambahkan target grup atau channel Jaseb.

  <b> Perintah:</b> <code>{0}infojaseb</code>
  <b> Penjelasan:</b> Untuk menampilkan informasi pengaturan Jaseb saat ini.

  <b> Perintah:</b> <code>{0}rmjasebtarget (ID grup)</code>
  <b> Penjelasan:</b> Untuk menghapus target Jaseb yang disimpan.
"""

@PY.UBOT("setjaseb", SUDO=True)
async def set_jaseb(client: Client, message: Message):
    user_id = message.from_user.id
    arg = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    if arg == "on":
        await set_jaseb_active(user_id, True, client)
        await message.reply_text("Jaseb diaktifkan.")
    elif arg == "off":
        await set_jaseb_active(user_id, False, client)
        await message.reply_text("Jaseb dinonaktifkan.")
    else:
        await message.reply_text("Gunakan perintah .setjaseb on/off")

@PY.UBOT("setjasebtext", SUDO=True)
async def set_jaseb_text_command(client: Client, message: Message):
    user_id = message.from_user.id
    text = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    await set_jaseb_text(user_id, text)
    await message.reply_text(f"Teks Jaseb diatur ke: {text}")

@PY.UBOT("setjasebinterval", SUDO=True)
async def set_jaseb_interval_command(client: Client, message: Message):
    user_id = message.from_user.id
    try:
        interval = int(message.text.split(maxsplit=1)[1])
        await set_jaseb_interval(user_id, interval)
        await message.reply_text(f"Interval Jaseb diatur ke: {interval} detik")
    except ValueError:
        await message.reply_text("Interval harus berupa angka.")

@PY.UBOT("setjasebtarget", SUDO=True)
async def set_jaseb_target_command(client: Client, message: Message):
    user_id = message.from_user.id
    try:
        target = int(message.text.split(maxsplit=1)[1])
        await add_jaseb_target(user_id, target)
        await message.reply_text(f"Target Jaseb ditambahkan: {target}")
    except ValueError:
        await message.reply_text("ID grup harus berupa angka.")

@PY.UBOT("infojaseb", SUDO=True)
async def info_jaseb_command(client: Client, message: Message):
    user_id = message.from_user.id
    jaseb_status, jaseb_text, jaseb_interval, jaseb_targets = await load_jaseb_settings(user_id)

    # Periksa apakah jaseb_targets adalah iterable
   print(f"jaseb_targets: {jaseb_targets} (type: {type(jaseb_targets)})")
    if isinstance(jaseb_targets, (list, set, tuple)):
        targets_str = ', '.join(str(target) for target in jaseb_targets)
    else:
        targets_str = 'Tidak diatur'

    info = (
        f"Jaseb Info:\n"
        f"Status: {jaseb_status}\n"
        f"Text: {jaseb_text}\n"
        f"Interval: {jaseb_interval} detik\n"
        f"Targets: {targets_str}"
    )
    await message.reply_text(info)


@PY.UBOT("rmjasebtarget", SUDO=True)
async def remove_jaseb_target_command(client: Client, message: Message):
    user_id = message.from_user.id
    try:
        target = int(message.text.split(maxsplit=1)[1])
        await remove_jaseb_target(user_id, target)
        await message.reply_text(f"Target Jaseb dihapus: {target}")
    except ValueError:
        await message.reply_text("ID grup harus berupa angka.")
