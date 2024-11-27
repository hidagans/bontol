__MODULE__ = "vctools"
__HELP__ = """
<b>『 Bantuan untuk vctools 』</b>

  <b>• Perintah:</b> <code>{0}joinvc</code>
  <b>• Penjelasan:</b> Untuk bergabung ke voice chat group

  <b>• Perintah:</b> <code>{0}leavevc</code>
  <b>• Penjelasan:</b> Untuk meninggalkan dari voice chat group

  <b>• Perintah:</b> <code>{0}startvc</code>
  <b>• Penjelasan:</b> Untuk memulai obrolan group 

  <b>• Perintah:</b> <code>{0}stopvc</code>
  <b>• Penjelasan:</b> Untuk menghentikan obrolan group 
"""

import asyncio
from random import randint
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputPeerChannel, InputPeerChat
from pyrogram.errors import FloodWait
from ubot import *

daftar_join = []
turun_dewek = False

async def get_group_call(client, message):
    chat_peer = await client.resolve_peer(message.chat.id)

    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        try:
            if isinstance(chat_peer, InputPeerChannel):
                # Ganti client.invoke dengan safe_invoke
                full_chat = (
                    await safe_invoke(client, GetFullChannel(channel=chat_peer))
                ).full_chat
            elif isinstance(chat_peer, InputPeerChat):
                # Ganti client.invoke dengan safe_invoke
                full_chat = (
                    await safe_invoke(client, GetFullChat(chat_id=chat_peer.chat_id))
                ).full_chat

            if full_chat and full_chat.call:
                return full_chat.call
        except Exception as e:
            print(f"Error retrieving group call: {e}")

    await message.reply("**No group call Found**")
    return False

@PY.UBOT("joinvc", SUDO=True)
@ubot.on_message(filters.user(USER_ID) & filters.command("jovc"))
async def join_os(client, message):
    msg = await message.reply(f"Processing...")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    try:
        await client.group_call.start(chat_id, join_as=client.me.id)
        await asyncio.sleep(5)  # Tunggu 5 detik agar bergabung sepenuhnya
        await client.group_call.set_is_mute(True)
        await msg.edit(f"<b>Successfully joined the Voice Chat</b>")
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await join_os(client, message)  # Retry after waiting
    except Exception as e:
        await msg.edit(f"ERROR: {e}")

@PY.UBOT("leavevc", SUDO=True)
@ubot.on_message(filters.user(USER_ID) & filters.command("levc"))
async def leave_os(client, message):
    try:
        await client.group_call.stop()
        await message.reply(f"<b>Successfully left the Voice Chat</b>")
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await leave_os(client, message)  # Retry after waiting
    except Exception as e:
        await message.reply(f"ERROR: {e}")

@PY.UBOT("startvc", SUDO=True)
async def start_vctools(client, message):
    flags = " ".join(message.command[1:])
    vctitle = get_arg(message)
    chat_id = message.chat.id  # Perbaiki chat_id
    args = f"<b>Obrolan Suara Aktif</b>\n<b>Chat :</b><code>{message.chat.title}</code>"
    try:
        await client.invoke(
            CreateGroupCall(
                peer=(await client.resolve_peer(chat_id)),
                random_id=randint(10000, 999999999),
                title=vctitle if vctitle else None,
            )
        )
        await message.reply(args)
    except FloodWait as e:
        print(f"Rate limit exceeded. Waiting for {e.x} seconds...")
        await asyncio.sleep(e.x)
        await start_vctools(client, message)  # Retry after waiting
    except Exception as e:
        await message.reply(f"<b>INFO:</b> {e}")

@PY.UBOT("stopvc", SUDO=True)
async def stop_vctools(client, message):
    group_call = await get_group_call(client, message)
    if not group_call:
        return
    try:
        await client.invoke(DiscardGroupCall(call=group_call))
        await message.reply(f"<b>Obrolan Suara Diakhiri</b>\n<b>Chat :</b><code>{message.chat.title}</code>")
    except FloodWait as e:
        print(f"Rate limit exceeded. Waiting for {e.x} seconds...")
        await asyncio.sleep(e.x)
        await stop_vctools(client, message)  # Retry after waiting
    except Exception as e:
        await message.reply(f"ERROR: {e}")
