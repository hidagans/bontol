import asyncio
from datetime import datetime
from time import time
from pyrogram.errors import FloodWait, RPCError
from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ubot import (
    ubot, get_expired_date, DEVS, get_seles, get_time,
    Button, unpackInlineMessage, get_var, bot,
    start_time, get_prefix, safe_invoke
)

async def profile_command(client, message):
    dia = message.from_user.id
    my_id = [ubot_instance.me.id for ubot_instance in ubot._ubot]
    status2 = "aktif" if dia in my_id else "tidak aktif"
    
    if dia in DEVS:
        status = "<b>premium</b> <code>[Own]</code>"
    elif dia in await get_seles():
        status = "<b>premium</b> <code>[admin]</code>"
    else:
        status = "<b>premium</b> <code>[user]</code>"
    
    uptime = await get_time((time() - start_time))
    start = datetime.now()
    
    try:
        await safe_invoke(client, Ping(ping_id=0))  # Menggunakan safe_invoke untuk ping
    except Exception as e:
        print(f"Gagal melakukan ping: {e}")
        delta_ping = "Tidak diketahui"
    else:
        end = datetime.now()
        delta_ping = (end - start).microseconds / 1000
    
    exp = await get_expired_date(dia)
    habis = exp.strftime("%d.%m.%Y") if exp else "None"
    prefix = await get_prefix(dia)
    prefix_text = prefix[0] if prefix else "Tidak ada prefix"
    
    b = InlineKeyboardMarkup([[InlineKeyboardButton(text="Tutup", callback_data="0_cls")]])
    
    await message.reply_text(f"""
<b>Reload Your Bot</b>
<b>Status Ubot:</b> <code>{status2}</code>
<b>Status Pengguna:</b> <i>{status}</i>
<b>Prefixes :</b> <code>{prefix_text}</code>
<b>Tanggal Kedaluwarsa:</b> <code>{habis}</code>
<b>Uptime Ubot:</b> <code>{uptime}</code>
<b>Ping:</b> <code>{delta_ping:.2f} ms</code>
""", reply_markup=b)

async def ewdsfgj(client, callback_query):
    user_id = callback_query.from_user.id
    my_id = [ubot_instance.me.id for ubot_instance in ubot._ubot]
    
    status2 = "aktif" if user_id in my_id else "tidak aktif"
    
    if user_id in DEVS:
        status = "<b>premium</b> <code>[kepala toko]</code>"
    elif user_id in await get_seles():
        status = "<b>premium</b> <code>[kasir]</code>"
    else:
        status = "<b>premium</b> <code>[pembeli]</code>"
    
    uptime = await get_time((time() - start_time))
    start = datetime.now()
    
    try:
        await safe_invoke(client, Ping(ping_id=0))  # Menggunakan safe_invoke untuk ping
    except Exception as e:
        print(f"Gagal melakukan ping: {e}")
        delta_ping = "Tidak diketahui"
    else:
        end = datetime.now()
        delta_ping = (end - start).microseconds / 1000
    
    exp = await get_expired_date(user_id)
    habis = exp.strftime("%d.%m.%Y") if exp else "None"
    prefix = await get_prefix(user_id)
    ubotstatus = "Aktif" if exp else "Nonaktif"
    
    if ubotstatus == "Nonaktif":
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Buat Userbot", callback_data="start_pmb")],
                [InlineKeyboardButton(text="Kembali", callback_data="start0"),
                 InlineKeyboardButton(text="Tutup", callback_data="0_cls")]
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Kembali", callback_data="start0"),
                 InlineKeyboardButton(text="Tutup", callback_data="0_cls")]
            ]
        )
    
    await callback_query.edit_message_text(f"""
<b>Reload Your Bot</b>
<b>Status Ubot:</b> <code>{status2}</code>
<b>Status Pengguna:</b> <i>{status}</i>
<b>Prefixes :</b> <code>{prefix[0]}</code>
<b>Tanggal Kedaluwarsa:</b> <code>{habis}</code>
<b>Uptime Ubot:</b> <code>{uptime}</code>
<b>Ping:</b> <code>{delta_ping:.2f} ms</code>
""", reply_markup=keyboard)
