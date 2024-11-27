import wget
import asyncio
import logging
import mimetypes

from ubot import *

__MODULE__ = "logs"
__HELP__ = """
<b>『 Bantuan untuk logs 』</b>

  <b>• Perintah:</b> <code>{0}logs (on/off)</code>
  <b>• Penjelasan:</b> Untuk mengaktifkan atau menonaktifkan grup logs.
"""

logging.basicConfig(level=logging.INFO)

async def send_log(client, chat_id, message, message_text, msg):
    try:
        await client.send_message(chat_id, message_text, disable_web_page_preview=True)
        await message.forward(chat_id)
    except Exception as error:
        logging.error(f"{msg} - {error}")

@PY.LOGS_PRIVATE()
async def _(client, message):
    logs = await get_var(client.me.id, "ID_LOGS")
    on_logs = await get_var(client.me.id, "ON_LOGS")

    if logs and on_logs:
        type = "Private"
        user_link = f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
        message_link = f"tg://openmessage?user_id={message.from_user.id}&message_id={message.id}"
        message_text = f"""
<b>📩 Ada pesan masuk</b>
    <b>•> Tipe pesan:</b> <code>{type}</code>
    <b>•> Link pesan:</b> [klik disini]({message_link})
    
<b>⤵️ Dibawah ini adalah pesan terusan dari: {user_link}</b>
"""
        await send_log(client, int(logs), message, message_text, "LOGS_PRIVATE")

@PY.LOGS_GROUP()
async def _(client, message):
    logs = await get_var(client.me.id, "ID_LOGS")
    on_logs = await get_var(client.me.id, "ON_LOGS")

    if logs and on_logs:
        type = "Group"
        user_link = f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
        message_link = message.link
        message_text = f"""
<b>📩 Ada pesan masuk</b>
    <b>•> Tipe pesan:</b> <code>{type}</code>
    <b>•> Link pesan:</b> [klik disini]({message_link})
    
<b>⤵️ Dibawah ini adalah pesan terusan dari: {user_link}</b>
"""
        await send_log(client, int(logs), message, message_text, "LOGS_GROUP")

@PY.UBOT("logs")
@PY.TOP_CMD
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply(
            "Harap baca menu bantuan untuk mengetahui cara penggunaanya."
        )

    query = {"on": True, "off": False, "none": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply("Opsi tidak valid, harap gunakan 'on' atau 'off'.")

    value = query[command]

    vars = await get_var(client.me.id, "ID_LOGS")

    if not vars:
        logs = await create_logs(client)
        await set_var(client.me.id, "ID_LOGS", logs)

    if command == "none" and vars:
        try:
            await client.delete_supergroup(vars)
        except Exception:
            logging.error("Error deleting supergroup")
        await set_var(client.me.id, "ID_LOGS", value)

    await set_var(client.me.id, "ON_LOGS", value)
    return await message.reply(
        f"<b>✅ <code>LOGS</code> Berhasil disetting ke:</b> <code>{value}</code>"
    )

async def create_logs(client):
    logs = await client.create_supergroup(f"Logs Ubot: {bot.me.username}")
    url = "https://telegra.ph//file/de0b0248643b4fb64c150.jpg"
    try:
        photo_path = wget.download(url)
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        return

    mime_type, _ = mimetypes.guess_type(url)
    photo_video = {"video": photo_path} if mime_type and mime_type.startswith('video') else {"photo": photo_path}

    try:
        await client.set_chat_photo(logs.id, **photo_video)
    except Exception as e:
        logging.error(f"Error setting chat photo: {e}")
    
    return logs.id
