import asyncio
from datetime import datetime
from gc import get_objects
from time import time
from random import randint

from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ubot import *


async def send_msg_to_owner(client, message):
    if message.from_user.id == OWNER_ID:
        return
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    "👤 Profil", callback_data=f"profil {message.from_user.id}"
                ),
                InlineKeyboardButton(
                    "Jawab 💬", callback_data=f"jawab_pesan {message.from_user.id}"
                ),
            ],
        ]
        await client.send_message(
            OWNER_ID,
            f"<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>\n\n<code>{message.text}</code>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

async def reak(client, message):
    await client.send_reaction(message.chat.id, message.id, "⚡")

async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    apa = (
        message.edit_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await apa(*args, **kwargs)

def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.id

    elif not message.from_user.is_self:
        reply_id = message.id

    return reply_id

async def ping_cmd(client: Client, message: Message):
    start = datetime.now()
    try:
        await client.invoke(Ping(ping_id=0))
    except Exception as e:
        print(f"Error during ping: {e}")
        return await message.reply("❌ <b>Ping gagal.</b>", quote=True)

    end = datetime.now()
    uptime = await get_time((time() - start_time))
    delta_ping = round((end - start).microseconds / 1000, 2)

    # Dapatkan emoji khusus atau default
    emot_pong_id = await get_var(client.me.id, "EMOJI_PING_PONG") or None
    emot_pong = f"<emoji id='{emot_pong_id}'></emoji>" if emot_pong_id else "🏓"

    emot_uptime_id = await get_var(client.me.id, "EMOJI_UPTIME") or None
    emot_uptime = f"<emoji id='{emot_uptime_id}'></emoji>" if emot_uptime_id else "⏰"

    emot_anuan_id = await get_var(client.me.id, "EMOJI_MENTION") or None
    emot_anuan = f"<emoji id='{emot_anuan_id}'></emoji>" if emot_anuan_id else "😱"

    # Animasi awal
    xx = await edit_or_reply(message, f"{emot_pong} <b>Memulai ping...</b>")
    await asyncio.sleep(1)

    if client.me.is_premium:
        _ping = f"""
<code>───⬤───────⬤───────⬤───</code>
<b><emoji id='{emot_pong_id}'></emoji> Pong:</b> <code><b><i>{delta_ping} ms</i></b></code>
<b><emoji id='{emot_uptime_id}'></emoji> Uptime:</b> <code><b><i>{uptime}</i></b></code>
<code>───⬤───────⬤───────⬤───</code>
"""
    else:
        _ping = f"""
<code>─⬤──⬤──⬤─</code>
<b>{emot_pong} Pong:</b> <code><b><i>{delta_ping} ms</i></b></code>
<b>{emot_anuan} Uptime:</b> <code><b><i>{uptime}</i></b></code>
<code>─⬤──⬤──⬤─</code>
"""

    try:
        await asyncio.gather(
            xx.delete(),  # Hapus animasi awal
            client.send_message(
                chat_id=message.chat.id,
                text=_ping,
                reply_to_message_id=message.message_id if hasattr(message, 'message_id') else None,
                disable_web_page_preview=True,
            ),
        )
    except Exception as e:
        print(f"Exception occurred: {e}")
        if hasattr(xx, 'edit'):
            await xx.edit(_ping, disable_web_page_preview=True)

async def start_cmd(client, message):
    await add_served_user(message.from_user.id)
    await send_msg_to_owner(client, message)
    if len(message.command) < 2:
        buttons = Button.start(message)
        msg = MSG.START(message)
        await message.reply(msg, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        txt = message.text.split(None, 1)[1]
        msg_id = txt.split("_", 1)[1]
        send = await message.reply("<b>Tunggu Sebentar...</b>")
        if "secretMsg" in txt:
            try:
                m = [obj for obj in get_objects() if id(obj) == int(msg_id)][0]
            except Exception as error:
                return await send.edit(f"<b>❌ Eror:</b> <code>{error}</code>")
            user_or_me = [m.reply_to_message.from_user.id, m.from_user.id]
            if message.from_user.id not in user_or_me:
                return await send.edit(
                    f"<b>Mau ngapain sayangku gk boleh loh ini<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>"
                )
            else:
                text = await client.send_message(
                    message.chat.id,
                    m.text.split(None, 1)[1],
                    protect_content=True,
                    reply_to_message_id=message.id,
                )
                await send.delete()
                await asyncio.sleep(120)
                await message.delete()
                await text.delete()
        elif "copyMsg" in txt:
            try:
                m = [obj for obj in get_objects() if id(obj) == int(msg_id)][0]
            except Exception as error:
                return await send.edit(f"<b>❌ Eror:</b> <code>{error}</code>")
            id_copy = int(m.text.split()[1].split("/")[-1])
            if "t.me/c/" in m.text.split()[1]:
                chat = int("-100" + str(m.text.split()[1].split("/")[-2]))
            else:
                chat = str(m.text.split()[1].split("/")[-2])
            try:
                get = await client.get_messages(chat, id_copy)
                await get.copy(message.chat.id, reply_to_message_id=message.id)
                await send.delete()
            except Exception as error:
                await send.edit(error)


