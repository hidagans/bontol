import asyncio
from ubot import *
import logging

async def kok_anjeng(client, message):
    Tm = await message.edit("`Processing...`")
    if len(message.command) < 2:
        return await Tm.edit("Prefix harus berupa trigger.")
    
    try:
        ub_prefix = [
            "" if prefix.lower() == "none" else prefix
            for prefix in message.command[1:]
        ]
        client.set_prefix(client.me.id, ub_prefix)
        await set_pref(client.me.id, ub_prefix)
        parsed_prefix = " ".join(ub_prefix)
        await Tm.edit(f"✅ Prefix diatur ke: {parsed_prefix}")
    except Exception as error:
        logging.error(f"Error setting prefix: {error}")
        await Tm.edit(f"Terjadi kesalahan: {error}")
        
async def change_emot(client, message):
    try:
        msg = await message.reply("Processing...", quote=True)

        if not client.me.is_premium:
            return await msg.edit(
                "<b>Untuk menggunakan perintah ini akun anda harus premium terlebih dahulu</b>"
            )

        if len(message.command) < 3:
            return await msg.edit("<b>Perintah berupa query dan value</b>")

        query_mapping = {
            "pong": "EMOJI_PING_PONG",
            "uptime": "EMOJI_UPTIME",
            "mention": "EMOJI_MENTION",
            "proses": "EMOJI_PROSES",
            "done": "EMOJI_DONE",
            "filed": "EMOJI_FILED"
        }
        command, mapping, value = message.command[:3]

        if mapping.lower() in query_mapping:
            query_var = query_mapping[mapping.lower()]
            emoji_id = next((
                entity.custom_emoji_id
                for entity in message.entities
                if entity.custom_emoji_id
            ), None)

            if emoji_id:
                await set_var(client.me.id, query_var, emoji_id)
                await msg.edit(
                    f"<b>✅ <code>{query_var}</code> Berhasil diubah ke:</b> <emoji id={emoji_id}>{value}</emoji>"
                )
            else:
                await msg.edit(
                    "<b>Emoji tidak ditemukan. Pastikan Anda menggunakan emoji kustom.</b>"
                )
        else:
            await msg.edit("<b>Mapping tidak ditemukan</b>")
    
    except Exception as error:
        logging.error(f"Error changing emoji: {error}")
        await msg.edit(f"Terjadi kesalahan: {error}")

