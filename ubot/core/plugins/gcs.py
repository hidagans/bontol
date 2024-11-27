import asyncio
from gc import get_objects

from pyrogram import enums
from pyrogram.enums import ChatType
from pyrogram.errors.exceptions import *

from ubot import *


def get_message(message):
    if message.reply_to_message:
        return message.reply_to_message
    elif len(message.command) > 1:
        return " ".join(message.command[1:])
    return ""


async def get_broadcast_id(client, query):
    chats = []
    chat_types = {
        "group": [ChatType.GROUP, ChatType.SUPERGROUP],
        "users": [ChatType.PRIVATE],
    }
    try:
        async for dialog in client.get_dialogs():
            if dialog.chat.type in chat_types.get(query, []):
                chats.append(dialog.chat.id)
    except ChannelPrivate:
        logging.warning("Channel is private and cannot be accessed.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    return chats



async def broadcast_group_cmd(client, message):
    emot_proses = await get_var(client.me.id, "EMOJI_PROSES") or "6113789201717660877"
    try:
        msg = await message.reply(f"<emoji id={emot_proses}>⌛</emoji> Sedang menyebarkan pesan broadcast...", quote=True)

        send = get_message(message)
        if not send:
            return await msg.edit("Tolong reply pesan atau ketik pesan")

        chats = await get_broadcast_id(client, "group")
        blacklist = await get_chat(client.me.id)

        done, failed = 0, 0
        for chat_id in chats:
            if chat_id not in blacklist and chat_id not in BLACKLIST_CHAT:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    done += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    try:
                        if message.reply_to_message:
                            await send.copy(chat_id)
                        else:
                            await client.send_message(chat_id, send)
                        done += 1
                    except Exception:
                        failed += 1
                except Exception:
                    failed += 1

        await msg.delete()
        await message.reply(f"""
        <b><emoji id=5974448685835094905>🔺</emoji> Pesan broadcast ke grup berhasil</b> 
        <b><emoji id=5021905410089550576>✅</emoji> Berhasil ke: {done} grup</b>
        <b><emoji id=5019523782004441717>❌</emoji> Gagal ke: {failed} grup</b>
        """)
    except Exception as e:
        await client.send_message(message.chat.id, "<b><emoji id=5019523782004441717>❌</emoji> Gagal mengambil detail Broadcast!!")
        logging.error(f"An error occurred: {e}")

#async def cancel_broadcast(client, message):
    #global broadcast_running

    #if not broadcast_running:
        #return await message.reply_text("<code>Tidak ada pengiriman pesan broadcast yang sedang berlangsung.</code>")

    #broadcast_running = False
    #await message.delete()

async def broadcast_users_cmd(client, message):
    msg = await message.reply("Processing...")
    blacklist = await get_chat(client.me.id)
    done = 0
    async for dialog in client.get_dialogs(limit=None):
        if dialog.chat.type == ChatType.PRIVATE:
            if message.reply_to_message:
                send = message.reply_to_message
            else:
                if len(message.command) < 2:
                    return await msg.edit(
                        "Silakan balas ke pesan atau berikan pesan.")
                else:
                    send = message.text.split(None, 1)[1]
            chat_id = dialog.chat.id
            if chat_id not in blacklist and chat_id not in DEVS:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    done += 1
                except Exception:
                    pass
 
    await msg.edit(f"**Successfully Sent Message To `{done}` Groups chat**")



async def send_msg_cmd(client, message):
    try:
        if message.reply_to_message:
            chat_id = message.text.split()[1] if len(message.command) > 1 else message.chat.id
            if message.reply_to_message.reply_markup:
                x = await client.get_inline_bot_results(client.me.username, f"get_send {id(message)}")
                await client.send_inline_bot_result(chat_id, x.query_id, x.results[0].id)
            else:
                await message.reply_to_message.copy(chat_id, protect_content=True)
            await message.reply(f"✅ Pesan berhasil dikirim ke {chat_id}")
        else:
            if len(message.command) < 3:
                return await message.reply("Ketik tujuan dan pesan yang ingin dikirim")
            chat_id, chat_text = message.text.split(None, 2)[1:]
            await client.send_message(chat_id, chat_text, protect_content=True)
            await message.reply(f"✅ Pesan berhasil dikirim ke {chat_id}")
    except Exception as t:
        logging.error(f"Failed to send message: {t}")
        await message.reply(f"{t}")


async def send_inline(client, inline_query):
    _id = int(inline_query.query.split()[1])
    m = [obj for obj in get_objects() if id(obj) == _id][0]
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get send!",
                    reply_markup=m.reply_to_message.reply_markup,
                    input_message_content=InputTextMessageContent(
                        m.reply_to_message.text
                    ),
                )
            )
        ],
    )


async def gcast_inline(client, inline_query):
    get_id = int(inline_query.query.split(None, 1)[1])
    m = [obj for obj in get_objects() if id(obj) == get_id][0]
    buttons, text = await gcast_create_button(m)
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get button!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(text),
                )
            )
        ],
    )
