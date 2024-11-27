import logging
import asyncio
import time
import dotenv
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from requests import get
from ubot import *

stop_autobroadcast = False
delay_minutes = 1

async def set_delay_cmd(client, message):
    global delay_minutes
    args = message.command[1:]

    if not args:
        return await message.edit_text("**Masukkan delay dalam menit.**")

    try:
        delay_minutes = int(args[0])
        if delay_minutes <= 0:
            raise ValueError("Delay harus lebih besar dari 0.")
    except ValueError:
        return await message.edit_text("**Format delay tidak valid. Gunakan angka positif.**")

    await message.edit_text(f"**Delay diatur ke {delay_minutes} menit.**")


async def gcast_cmd(client, message):
    if message.reply_to_message or get_arg(message):
        Man = await edit_or_reply(message, "Started global broadcast...")
    else:
        return await message.edit_text("Berikan Sebuah Pesan atau Reply")

    done = 0
    error = 0

  
    async def send_broadcast(msg, chat_id):
        nonlocal done, error
        try:
            logging.debug(f"Sending message to Chat ID: {chat_id}")
            await msg.copy(chat_id)
            done += 1
            await asyncio.sleep(60 * delay_minutes)
        except Exception as e:
            error += 1
            logging.error(f"Error sending message: {e}")
            await asyncio.sleep(60 * delay_minutes)

    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            logging.debug(f"Accessing Chat ID: {dialog.chat.id}")
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            await send_broadcast(msg, chat)

    await Man.edit_text(
        f"Berhasil Mengirim Pesan Ke {done} Grup, Gagal Mengirim Pesan Ke {error} Grup"
          )


async def stop_autobroadcast_cmd(client, message):
    global stop_autobroadcast
    stop_autobroadcast = True
    await edit_or_reply(message, "`Auto Broadcast telah dimatikan.`")

