import importlib
import random
from datetime import datetime, timedelta

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

from ubot import *


async def login_cmd(client, message):
    info = await message.reply("<b>Tunggu Sebentar...</b>", quote=True)
    if len(message.command) < 3:
        return await info.edit(
            f"<code>{message.text}</code> <b>Hari - string Pyrogram</b>"
        )
    try:
        expire_days = int(message.command[1])
        session_string = message.command[2]
        ub = Ubot(
            name=f"ubot_{random.randrange(999999)}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
        )
        await ub.start()
        for mod in loadModule():
            importlib.reload(importlib.import_module(f"ubot.modules.{mod}"))
        now = datetime.now(timezone("Asia/Jakarta"))
        expire_date = now + timedelta(days=expire_days)
        await set_expired_date(ub.me.id, expire_date)
        await add_ubot(
            user_id=int(ub.me.id),
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
        )
        buttons = [
            [
                InlineKeyboardButton(
                    "Cek Kadaluarsa",
                    callback_data=f"cek_masa_aktif {ub.me.id}",
                )
            ],
        ]
        await bot.send_message(
            LOG_UBOT,
            f"""
<b>❏ Userbot Diaktifkan</b>
<b> ├ Akun:</b> <a href=tg://user?id={ub.me.id}>{ub.me.first_name} {ub.me.last_name or ''}</a> 
<b> ╰ ID:</b> <code>{ub.me.id}</code>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )
        await info.edit(
            f"<b>✅ Berhasil Login Di Akun: <a href='tg://user?id={ub.me.id}'>{ub.me.first_name} {ub.me.last_name or ''}</a></b>"
        )
    except Exception as error:
        await info.edit(f"<code>{error}</code>")



async def restart_cmd(client, message):
    msg = await message.reply("<b>Processing...</b>", quote=True)
    
    # Check if the user is authorized
    if message.from_user.id not in ubot._get_my_id:
        return await msg.edit(
            f"<b>Anda bukan pengguna @{bot.me.username}!</b>"
        )
    
    # Debug: Print current bots
    print(f"Current bots: {ubot._ubot}")
    
    # Loop through the bots
    for X in ubot._ubot:
        print(f"Checking bot ID: {X.me.id}")
        if message.from_user.id == X.me.id:
            # Retrieve userbots from database
            userbots = await get_userbots()
            print(f"Retrieved userbots: {userbots}")
            
            for _ubot_ in userbots:
                # Safe access to dictionary keys
                user_id = _ubot_.get("name")
                if user_id and X.me.id == int(user_id):
                    try:
                        # Remove the bot instance from ubot._ubot
                        ubot._ubot.remove(X)
                        
                        # Create and start a new bot instance
                        UB = Ubot(
                            name=_ubot_.get("name"),
                            api_id=_ubot_.get("api_id"),
                            api_hash=_ubot_.get("api_hash"),
                            session_string=_ubot_.get("session_string"),
                        )
                        await UB.start()
                        
                        # Reload modules
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"ubot.modules.{mod}")
                            )
                        
                        return await msg.edit(
                            f"<b>✅ Berhasil Di Restart {UB.me.first_name} {UB.me.last_name or ''} | {UB.me.id}.</b>"
                        )
                    except Exception as error:
                        return await msg.edit(f"<b>{error}</b>")
    
    await msg.edit("<b>Bot tidak ditemukan.</b>")







"""
    for X in ubot._ubot:
        if message.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        UB = Ubot(**_ubot_)
                        UB.in_memory=False
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"ubot.modules.{mod}")
                            )
                        return await msg.edit(
                            f"<b>✅ Berhasil Di Restart {UB.me.first_name} {UB.me.last_name or ''} | {UB.me.id}</b>"
                        )
                    except Exception as error:
                        return await msg.edit(f"<b>{error}</b>")
"""
