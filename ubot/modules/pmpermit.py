from gc import get_objects

from pykeyboard import InlineKeyboard
from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InlineQueryResultVideo,
                            InputTextMessageContent)

from ubot import *

FLOOD = {}
MSG_ID = {}
PM_TEXT = """
<b>🙋🏻‍♂️ Hallo {mention} ada yang bisa say bantu?

Perkenalkan saya adalah pm-security disini
silahkan tunggu majikan saya 
membalas pesan mu ini yah 
jangan spam atau anda akan terblokir otomatis 
⛔ peringatan: {warn} hati-hati</b>
"""

__MODULE__ = "pmpermit"
__HELP__ = """
<b>『 Bantuan untuk pmpermit 』</b>

   <b>• Perintah:</b> <code>{0}pmpermit (on/off)</code>
   <b>• Penjelasan:</b> Untuk mengaktifkan dan menonaktifkan pmpermit.

   <b>• Perintah:</b> <code>{0}ok or {0}setuju</code>
   <b>• Penjelasan:</b> Untuk menyetujui pengguna mengirim pesan.

   <b>• Perintah:</b> <code>{0}no or {0}tolak</code>
   <b>• Penjelasan:</b> Untuk menolak pengguna mengirim pesan.

   <b>• Perintah:</b> <code>{0}setpm (query) (value)</code>
   <b>• Penjelasan:</b> Untuk mengatur variabel teks_pmpermit limit_pmpermit.

   <b>•> Query:</b>
       •> <code>PIC</code>
       •> <code>TEXT</code>
       •> <code>LIMIT</code>
"""


@ubot.on_message(
    filters.private
    & filters.incoming
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.service,
    group=69,
)
async def _(client, message):
    user = message.from_user
    pm_on = await get_var(client.me.id, "PMPERMIT")
    if pm_on:
        if user.id in MSG_ID:
            await delete_old_message(message, MSG_ID.get(user.id, 0))
        check = await get_pm_id(client.me.id)
        if user.id not in check:
            if user.id in FLOOD:
                FLOOD[user.id] += 1
            else:
                FLOOD[user.id] = 1
            pm_limit = await get_var(client.me.id, "PM_LIMIT") or "5"
            if FLOOD[user.id] > int(pm_limit):
                del FLOOD[user.id]
                await message.reply(
                    "Sudah diingatkan jangan spam, sekarang anda diblokir."
                )
                return await client.block_user(user.id)
            pm_msg = await get_var(client.me.id, "PM_TEXT") or PM_TEXT
            if "~>" in pm_msg:
                x = await client.get_inline_bot_results(
                    bot.me.username, f"pm_pr {id(message)} {FLOOD[user.id]}"
                )
                msg = await client.send_inline_bot_result(
                    message.chat.id,
                    x.query_id,
                    x.results[0].id,
                    reply_to_message_id=message.id,
                )
                MSG_ID[user.id] = int(msg.updates[0].id)
            else:
                pm_pic = await get_var(client.me.id, "PM_PIC")
                rpk = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
                peringatan = f"{FLOOD[user.id]} / {pm_limit}"
                if pm_pic:
                    photo_video = (
                        message.reply_video
                        if pm_pic.endswith(".mp4")
                        else message.reply_photo
                    )
                    msg = await photo_video(
                        pm_pic, caption=pm_msg.format(mention=rpk, warn=peringatan)
                    )
                else:
                    msg = await message.reply(
                        pm_msg.format(mention=rpk, warn=peringatan)
                    )
                MSG_ID[user.id] = msg.id


@PY.UBOT("setpm")
async def _(client, message):
    if len(message.command) < 3:
        return await message.reply(
            "Harap baca menu bantuan untuk mengetahui cara penggunaannya."
        )
    query = {"limit": "PM_LIMIT", "text": "PM_TEXT", "pic": "PM_PIC"}
    if message.command[1].lower() not in query:
        return await message.reply("<b>❌ Query yang di masukkan tidak valid</b>")
    query_str, value_str = (
        message.text.split(None, 2)[1],
        message.text.split(None, 2)[2],
    )
    value = query[query_str]
    if value_str.lower() == "none":
        value_str = False
    await set_var(client.me.id, value, value_str)
    return await message.reply(
        f"<b>✅ <code>{value}</code> Berhasil disetting ke: <code>{value_str}</code>"
    )


@PY.UBOT("pmpermit")
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply(
            "Harapa baca menu bantuan untuk mengetahui cara penggunaannya."
        )

    toggle_options = {"off": False, "on": True}
    toggle_option = message.command[1].lower()

    if toggle_option not in toggle_options:
        return await message.reply("Opsi tidak valid. Harap gunakan 'on' atau 'off'.")

    value = toggle_options[toggle_option]
    text = "ᴅɪᴀᴋᴛɪғᴋᴀɴ" if value else "Dinonaktifkan"

    await set_var(client.me.id, "PMPERMIT", value)
    await message.reply(f"<b>✅ Pmpermit berhasil {text}</b>")


@PY.INLINE("pm_pr")
async def _(client, inline_query):
    get_id = inline_query.query.split()
    m = [obj for obj in get_objects() if id(obj) == int(get_id[1])][0]
    pm_msg = await get_var(m._client.me.id, "PM_TEXT") or PM_TEXT
    pm_limit = await get_var(m._client.me.id, "PM_LIMIT") or 5
    pm_pic = await get_var(m._client.me.id, "PM_PIC")
    rpk = f"[{m.from_user.first_name} {m.from_user.last_name or ''}](tg://user?id={m.from_user.id})"
    peringatan = f"{int(get_id[2])} / {pm_limit}"
    buttons, text = await pmpermit_button(pm_msg)
    if pm_pic:
        photo_video = (
            InlineQueryResultVideo
            if pm_pic.endswith(".mp4")
            else InlineQueryResultPhoto
        )
        photo_video_url = (
            {"video_url": pm_pic, "thumb_url": pm_pic}
            if pm_pic.endswith(".mp4")
            else {"photo_url": pm_pic}
        )
        hasil = [
            photo_video(
                **photo_video_url,
                title="Dapatkan tombol!",
                caption=text.format(mention=rpk, warn=peringatan),
                reply_markup=buttons,
            )
        ]
    else:
        hasil = [
            (
                InlineQueryResultArticle(
                    title="Dapatkan tombol!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(
                        text.format(mention=rpk, warn=peringatan)
                    ),
                )
            )
        ]
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=hasil,
    )


@PY.UBOT("ok|setuju")
async def _(client, message):
    user = message.chat
    rpk = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
    var = await get_pm_id(client.me.id)
    if user.id not in var:
        await add_pm_id(client.me.id, user.id)
        return await message.reply(f"<b>✅ Baiklah, {rpk} telah diterima</b>")
    else:
        return await message.reply(f"<b>{rpk} Sudah diterima</b>")


@PY.UBOT("no|tolak")
async def _(client, message):
    user = message.chat
    rpk = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
    vars = await get_pm_id(client.me.id)
    if user.id not in vars:
        await message.reply(f"<b>🙏🏻 Maaf ⁣{rpk} anda telah diblokir</b>")
        return await client.block_user(user.id)
    else:
        await remove_pm_id(client.me.id, user.id)
        return await message.reply(
            f"<b>🙏🏻 Maaf {rpk} anda telah di tolak untuk menghubungi akun ini lagi</b>"
        )


async def pmpermit_button(m):
    buttons = InlineKeyboard(row_width=1)
    keyboard = []
    for X in m.split("~>", 1)[1].split():
        X_parts = X.split(":", 1)
        keyboard.append(
            InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1])
        )
    buttons.add(*keyboard)
    text = m.split("~>", 1)[0]

    return buttons, text


async def delete_old_message(message, msg_id):
    try:
        await message._client.delete_messages(message.chat.id, msg_id)
    except:
        pass
