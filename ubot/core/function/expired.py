import asyncio
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup
from pytz import timezone

from ubot import bot, ubot
from ubot.config import LOG_UBOT
from ubot.core.database import (get_chat, get_expired_date,
                                rem_expired_date, remove_chat, remove_ubot,
                                rm_all)
from ubot.core.helpers import MSG, Button
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

async def expired_userbot(X):
    try:
        current_time = datetime.now(timezone("Asia/Jakarta")).strftime("%d-%m-%Y")
        exp_date = await get_expired_date(X.me.id)
        
        exp = exp_date.strftime("%d-%m-%Y") if exp_date else None

        if current_time == exp:
            for chat in await get_chat(X.me.id):
                await remove_chat(X.me.id, chat)
            await rm_all(X.me.id)
            await remove_ubot(X.me.id)
            await rem_expired_date(X.me.id)
            ubot._get_my_id.remove(X.me.id)
            ubot._ubot.remove(X)
            await X.log_out()
            expired_text = MSG.EXPIRED_MSG_BOT(X)
            expired_button = Button.expired_button_bot()
            await bot.send_message(
                LOG_UBOT,
                expired_text,
                reply_markup=InlineKeyboardMarkup(expired_button),
            )
            logging.info(f"Userbot {X.me.id} has expired and logged out.")
    except Exception as e:
        logging.error(f"Error in expired_userbot: {str(e)}")

async def expiredUserbots():
    while True:
        tasks = [expired_userbot(X) for X in ubot._ubot]
        await asyncio.gather(*tasks)
        await asyncio.sleep(86400)
