from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from ubot import *


class MSG:
    def EXPIRED_MSG_BOT(X):
        return f"""
<b>❏ Pemberitahuan</b>
<b>├ Akun :</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ Id:</b> <code>{X.me.id}</code>
<b>╰ Masa aktif telah habis</b>
"""

    def START(message):
        if message.from_user.id != USER_ID:
            msg = f"""
<b>👋 Hallo {message.from_user.first_name} !!

Dengan bot ini, anda dapat melakukan pembayaran dan pembuatan Userbot.</b>
"""
        else:
            msg = f"""
🧑‍💻 Developer <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>

✅ Gunakan dengan bijak !!!
"""
        return msg

    def TEXT_PAYMENT(harga, total, bulan):
        return f"""
<b>💬 Silahkan melakukan pembayaran terlebih dahulu</b>

<b>🎟️ Harga perbulan: 30.000</b>

<b>💳 Metode Pembayaran:</b>
 <b>├ QRIS</b>
 <b>└────•OTOMATIS PAYMENT</b>

<b>🔖 Total Harga: Rp {total}.000</b>
<b>🗓️ Total Bulan {bulan}</b> 

<b>Setelah pembayaran silahkan check tombol di bawah untuk melakukan pembayaran</b>
"""

    async def USERBOT(count):
        expired_date = await get_expired_date(ubot._ubot[int(count)].me.id)
        if expired_date is None:
            expired_date_str = "No expiration date"
        else:
            expired_date_str = expired_date.strftime('%d-%m-%Y')
        
        return f"""
<b>❏ Userbot ke</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b> ├ Akun:</b> <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a> 
<b> ├ Id:</b> <code>{ubot._ubot[int(count)].me.id}</code>
<b> ╰ Expired</b> <code>{expired_date_str}</code>
"""

    def POLICY():
        return """
<b>📜 Peraturan</b>
<b>├ Jangan melakukan spam</b>
<b>├ Jangan melakukan penipuan</b>
<b>├ Jangan melakukan penyalahgunaan userbot</b>
<b>├ Jangan melakukan penyalahgunaan bot</b>
<b>💸 Pembayaran</b>
<b>├ 1 bulan = 30.000</b>
<b>├ 3 bulan = 80.000</b>
<b>├ 6 bulan = 150.000</b>
<b>├ 1 tahun = 250.000</b>
<b>📝 Catatan</b>
<b>├ Jika anda melakukan pembayaran, anda akan mendapatkan userbot</b>
<b>├ Pembayaran ini akan di proses otomatis</b>
"""


async def sending_user(user_id):
    await bot.send_message(
        user_id,
        "💬 Silahkan buat ulang userbot anda",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔥 Buat Userbot 🔥",
                        callback_data="bahan",
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
