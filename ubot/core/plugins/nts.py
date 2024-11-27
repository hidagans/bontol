from gc import get_objects
from io import BytesIO

from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

from ubot import *


async def addnote_cmd(client, message):
    note_name = get_arg(message)
    reply = message.reply_to_message

    if reply and note_name:
        try:
            if await get_note(client.me.id, note_name):
                return await message.reply(f"Catatan {note_name} sudah ada.")

            copy = await client.copy_message(client.me.id, message.chat.id, reply.id)
            await save_note(client.me.id, note_name, copy.id)
            await copy.reply("👆🏻 Pesan di atas ini jangan dihapus atau catatan akan hilang.")
            await message.reply("Catatan berhasil disimpan.")
        except Exception as error:
            await message.reply(f"Terjadi kesalahan: {error}")
    else:
        await message.reply("Balas pesan dan berikan nama untuk menyimpan catatan.")

async def get_cmd(client, message):
    note_name = get_arg(message)
    
    if not note_name:
        return await message.reply("Apa yang Anda cari?")

    try:
        note = await get_note(client.me.id, note_name)
        if not note:
            return await message.reply(f"Catatan {note_name} tidak ditemukan.")

        note_id = await client.get_messages(client.me.id, note)
        if note_id.text and "~>" in note_id.text:
            try:
                x = await client.get_inline_bot_results(bot.me.username, f"get_notes {id(message)}")
                msg = message.reply_to_message or message
                await client.send_inline_bot_result(
                    message.chat.id,
                    x.query_id,
                    x.results[0].id,
                    reply_to_message_id=msg.id
                )
            except Exception as error:
                await message.reply(f"Terjadi kesalahan: {error}")
        else:
            msg = message.reply_to_message or message
            await client.copy_message(
                message.chat.id,
                client.me.id,
                note,
                reply_to_message_id=msg.id
            )
    except Exception as error:
        await message.reply(f"Terjadi kesalahan: {error}")


async def get_notes_button(client, inline_query):
    _id = int(inline_query.query.split()[1])
    m = next((obj for obj in get_objects() if id(obj) == _id), None)
    
    if m:
        note_id = await get_note(m._client.me.id, m.text.split()[1])
        note_message = await m._client.get_messages(m._client.me.id, note_id)
        buttons, text_button = await notes_create_button(note_message.text)
        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                InlineQueryResultArticle(
                    title="Get Notes!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(text_button),
                )
            ],
        )
    else:
        await client.answer_inline_query(inline_query.id, results=[], cache_time=0)



async def delnote_cmd(client, message):
    note_name = get_arg(message)
    
    if not note_name:
        return await message.reply("Apa yang ingin Anda hapus?")

    try:
        note = await get_note(client.me.id, note_name)
        if not note:
            return await message.reply(f"Catatan {note_name} tidak ditemukan.")

        await rm_note(client.me.id, note_name)
        await message.reply(f"Berhasil menghapus catatan {note_name}.")
        await client.delete_messages(client.me.id, [int(note), int(note) + 1])
    except Exception as error:
        await message.reply(f"Terjadi kesalahan: {error}")



async def notes_cmd(client, message):
    try:
        msg = f"• Catatan {client.me.first_name} {client.me.last_name or ''}\n\n"
        notes_list = await all_notes(client.me.id)

        if notes_list == "None":
            msg += "Tidak ada catatan."
        else:
            msg += "\n".join(f"• {note}" for note in notes_list)

        if len(msg) > 4096:
            with BytesIO(str.encode(msg)) as out_file:
                out_file.name = "notes.txt"
                await message.reply_document(document=out_file)
        else:
            await message.reply(msg)
    except Exception as error:
        await message.reply(f"Terjadi kesalahan: {error}")

