from pyrogram import Client
from pyrogram.errors import FloodWait, ChatForwardsRestricted
from pyrogram.types import InlineQueryResultArticle, InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent
from gc import get_objects
import asyncio
import time
import os
from ubot.core.helpers.colong import progress
from ubot import ubot, Ubot, get_arg, bot


COPY_ID = {}

nyolong_jalan = False


async def download_media_copy(get, client, infomsg, message):
    global nyolong_jalan
    msg = message.reply_to_message or message
    text = get.caption or ""

    try:
        if get.photo:
            media = await client.download_media(
                get,
                progress=progress,
                progress_args=(
                    infomsg,
                    time.time(),
                    "Download Photo",
                    get.photo.file_id,
                ),
            )
            if not nyolong_jalan:
                os.remove(media)
                return
            await client.send_photo(
                message.chat.id,
                media,
                caption=text,
                reply_to_message_id=msg.id,
            )
            await infomsg.delete()
            os.remove(media)

        elif get.animation:
            media = await client.download_media(
                get,
                progress=progress,
                progress_args=(
                    infomsg,
                    time.time(),
                    "Download Animation",
                    get.animation.file_id,
                ),
            )
            if not nyolong_jalan:
                os.remove(media)
                return
            await client.send_animation(
                message.chat.id,
                animation=media,
                caption=text,
                reply_to_message_id=msg.id,
            )
            await infomsg.delete()
            os.remove(media)

        elif get.voice:
            media = await client.download_media(
                get,
                progress=progress,
                progress_args=(infomsg, time.time(), "Download Voice", get.voice.file_id),
            )
            if not nyolong_jalan:
                os.remove(media)
                return
            await client.send_voice(
                message.chat.id,
                voice=media,
                caption=text,
                reply_to_message_id=msg.id,
            )
            await infomsg.delete()
            os.remove(media)

        elif get.audio:
            media = await client.download_media(
                get,
                progress=progress,
                progress_args=(
                    infomsg,
                    time.time(),
                    "Download Audio",
                    get.audio.file_id,
                ),
            )
            thumbnail = await client.download_media(get.audio.thumbs[-1]) or None
            if not nyolong_jalan:
                os.remove(media)
                if thumbnail:
                    os.remove(thumbnail)
                return
            await client.send_audio(
                message.chat.id,
                audio=media,
                duration=get.audio.duration,
                caption=text,
                thumb=thumbnail,
                reply_to_message_id=msg.id,
            )
            await infomsg.delete()
            os.remove(media)
            if thumbnail:
                os.remove(thumbnail)

        elif get.document:
            media = await client.download_media(
                get,
                progress=progress,
                progress_args=(
                    infomsg,
                    time.time(),
                    "Download Document",
                    get.document.file_id,
                ),
            )
            if not nyolong_jalan:
                os.remove(media)
                return
            await client.send_document(
                message.chat.id,
                document=media,
                caption=text,
                reply_to_message_id=msg.id,
            )
            await infomsg.delete()
            os.remove(media)

        elif get.video:
            media = await client.download_media(
                get,
                progress=progress,
                progress_args=(
                    infomsg,
                    time.time(),
                    "Download Video",
                    get.video.file_name,
                ),
            )
            thumbnail = await client.download_media(get.video.thumbs[-1]) or None
            if not nyolong_jalan:
                os.remove(media)
                if thumbnail:
                    os.remove(thumbnail)
                return
            await client.send_video(
                message.chat.id,
                video=media,
                duration=get.video.duration,
                caption=text,
                thumb=thumbnail,
                reply_to_message_id=msg.id,
            )
            await infomsg.delete()
            os.remove(media)
            if thumbnail:
                os.remove(thumbnail)
    except Exception as e:
        await infomsg.edit(f"Gagal mengunduh dan mengirim pesan: {str(e)}")


async def copy_semua(client, message):
    global nyolong_jalan
    nyolong_jalan = True

    try:
        # Ambil argumen dari pesan
        args = message.text.split()

        # Pastikan argumen benar
        if len(args) != 4 or args[2].lower() != "ke":
            await message.reply_text("Format salah! Gunakan: `.copy_semua <from_chat_id> ke <to_chat_id>`")
            return

        # Parse chat IDs
        from_chat_id = int(args[1])
        to_chat_id = int(args[3])

        # Mulai menyalin pesan
        await message.reply_text(f"Sedang menyalin pesan dari {from_chat_id} ke {to_chat_id}...")

        # Ambil semua pesan dari chat sumber
        all_messages = []
        async for msg in client.get_chat_history(from_chat_id):
            all_messages.append(msg)

        # Proses pesan dari yang paling awal
        for msg in reversed(all_messages):
            if not nyolong_jalan:
                break
            try:
                # Coba menyalin pesan tanpa mendownload media terlebih dahulu
                await msg.copy(to_chat_id)
                await asyncio.sleep(1)  # Tambahkan jeda kecil untuk menghindari pembatasan API
            except FloodWait as e:
                print(f"Terjadi FloodWait selama {e.x} detik.")
                await asyncio.sleep(e.x)
            except ChatForwardsRestricted:
                print(f"Pesan {msg.id} memiliki restriksi konten.")
                infomsg = await message.reply("<code>Processing...</code>")
                await download_media_copy(msg, client, infomsg, message)
            except Exception as e:
                print(f"Gagal menyalin pesan {msg.id}: {str(e)}")

        await message.reply_text("Proses penyalinan pesan selesai!")

    except Exception as e:
        await message.reply_text(f"Terjadi kesalahan: {str(e)}")
    finally:
        nyolong_jalan = False


async def copy_batch(client, message):
    global nyolong_jalan
    nyolong_jalan = True

    try:
        # Minta ID target dari pengguna
        await message.reply_text("Silahkan kirimkan ID target:")
        target_id_msg = await client.ask(
            chat_id=message.chat.id,
            text="Silahkan kirimkan ID target:",
            timeout=60
        )
        target_id = int(target_id_msg.text.strip())

        # Minta ID pesan awal dari pengguna
        await message.reply_text("Silahkan masukkan ID pesan awal untuk batch:")
        start_msg_id_msg = await client.ask(
            chat_id=message.chat.id,
            text="Silahkan masukkan ID pesan awal untuk batch:",
            timeout=60
        )
        start_msg_id = int(start_msg_id_msg.text.strip())

        # Minta ID pesan akhir dari pengguna
        await message.reply_text("Silahkan masukkan ID pesan akhir untuk batch:")
        end_msg_id_msg = await client.ask(
            chat_id=message.chat.id,
            text="Silahkan masukkan ID pesan akhir untuk batch:",
            timeout=60
        )
        end_msg_id = int(end_msg_id_msg.text.strip())

        # Konfirmasi dari pengguna
        confirmation_msg = await message.reply_text(
            f"Apakah Anda yakin ingin menyalin pesan dari ID {start_msg_id} hingga {end_msg_id} ke ID {target_id}? \nKetik 'yes' untuk melanjutkan atau 'no' untuk membatalkan."
        )
        
        try:
            user_response = await client.ask(
                chat_id=message.chat.id,
                text="Ketik 'yes' untuk melanjutkan atau 'no' untuk membatalkan.",
                timeout=60
            )
            
            if user_response.text.lower() == 'no':
                await message.reply_text("Proses dibatalkan.")
                nyolong_jalan = False
                return
            elif user_response.text.lower() != 'yes':
                await message.reply_text("Jawaban tidak valid. Proses dibatalkan.")
                nyolong_jalan = False
                return
        except asyncio.TimeoutError:
            await message.reply_text("Kedaluarsa! Proses dibatalkan.")
            nyolong_jalan = False
            return

        # Menyalin pesan
        await message.reply_text(f"Sedang menyalin pesan dari ID {start_msg_id} hingga {end_msg_id} ke ID {target_id}...")

        copied_count = 0
        async for msg in client.get_chat_history(taget_id):
            if not nyolong_jalan:
                break
            if msg.id < start_msg_id:
                continue
            if msg.id > end_msg_id:
                break

            try:
                await msg.copy(target_id, reply_to_message_id=msg.id)
                copied_count += 1
                await message.reply_text(f"Pesan {msg.id} disalin.")
                await asyncio.sleep(1)
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except ChatForwardsRestricted:
                infomsg = await message.reply("<code>Processing...</code>")
                await download_media_copy(msg, client, infomsg, message)
            except Exception as e:
                await message.reply_text(f"Gagal menyalin pesan {msg.id}: {str(e)}")

        await message.reply_text(f"Proses penyalinan pesan selesai! Total pesan yang disalin: {copied_count}")

    except Exception as e:
        await message.reply_text(f"Terjadi kesalahan: {str(e)}")
    finally:
        nyolong_jalan = False



async def copy_bot_msg(client, message):
    if message.from_user.id not in ubot._get_my_id:
        return
    Tm = await message.reply("Tunggu Sebentar...")
    link = get_arg(message)
    if not link:
        return await Tm.edit(
            f"<b><code>{message.text}</code> [link]</b>"
        )
    if link.startswith(("https", "t.me")):
        msg_id = int(link.split("/")[-1])
        if "t.me/c/" in link:
            chat = int("-100" + str(link.split("/")[-2]))
        else:
            chat = str(link.split("/")[-2])
        try:
            get = await client.get_messages(chat, msg_id)
            await get.copy(message.chat.id)
            await Tm.delete()
        except Exception as error:
            await Tm.edit(error)
    else:
        await Tm.edit("Link tidak valid.")


async def copy_ubot_msg(client, message):
    
    
    msg = message.reply_to_message or message
    infomsg = await message.reply("<code>Processing...</code>")
    link = get_arg(message)
    if not link:
        return await infomsg.edit(
            f"<b><code>{message.text}</code> [link]</b>"
        )
        
    
    
    if link.startswith(("https", "t.me")):
        msg_id = int(link.split("/")[-1])
        
        
        
        if "t.me/c/" in link:
            chat = int("-100" + str(link.split("/")[-2]))
            try:
                get = await client.get_messages(chat, msg_id)
                try:
                    await get.copy(message.chat.id, reply_to_message_id=msg.id)
                    await infomsg.delete()
                except Exception:
                    await download_media_copy(get, client, infomsg, message)
            except Exception as e:
                await infomsg.edit(str(e))
        else:
            chat = str(link.split("/")[-2])
            try:
                get = await client.get_messages(chat, msg_id)
                await get.copy(message.chat.id, reply_to_message_id=msg.id)
                await infomsg.delete()
            except Exception:
                try:
                    text = f"get_msg {id(message)}"
                    x = await client.get_inline_bot_results(bot.me.username, text)
                    results = await client.send_inline_bot_result(
                        message.chat.id,
                        x.query_id,
                        x.results[0].id,
                        reply_to_message_id=msg.id,
                    )
                    COPY_ID[client.me.id] = int(results.updates[0].id)
                    await infomsg.delete()
                except Exception as error:
                    await infomsg.edit(f"{str(error)}")
                    
    
    else:
        await infomsg.edit("Nyolong dihentikan")


async def copy_inline_msg(client, inline_query):
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get message!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Klik Disini",
                                    callback_data=f"copymsg_{int(inline_query.query.split()[1])}",
                                )
                            ],
                        ]
                    ),
                    input_message_content=InputTextMessageContent(
                        "<b>🔒 Konten Yang Mau Diambil Bersifat Private✅</b>"
                    ),
                )
            )
        ],
    )


async def copy_callback_msg(client, callback_query):
    try:
        q = int(callback_query.data.split("_", 1)[1])
        m = [obj for obj in get_objects() if id(obj) == q][0]
        await m._client.unblock_user(bot.me.username)
        await callback_query.edit_message_text("<code>Tunggu Sebentar</code>")
        copy = await m._client.send_message(
            bot.me.username, f"/copy {m.text.split()[1]}"
        )
        msg = m.reply_to_message or m
        await asyncio.sleep(1.5)
        await copy.delete()
        async for get in m._client.search_messages(bot.me.username, limit=1):
            await m._client.copy_message(
                m.chat.id, bot.me.username, get.id, reply_to_message_id=msg.id
            )
            await m._client.delete_messages(m.chat.id, COPY_ID[m._client.me.id])
            await get.delete()
    except Exception as error:
        await callback_query.edit_message_text(f"<code>{error}</code>")

async def cancel_nyolong(client, message):
    global nyolong_jalan

    if not nyolong_jalan:
        return await message.reply_text("<b>Tidak ada penyolongan konten berlangsung.</b>")

    nyolong_jalan = False
    await message.delete()
