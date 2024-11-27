from pykeyboard import InlineKeyboard
from pyrogram.errors import MessageNotModified
from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InputTextMessageContent)
import re

from ubot import *


class Button:
    def alive(get_id):
        button = [
            [
                InlineKeyboardButton(
                    text="🗑️ Tutup",
                    callback_data=f"alv_cls {int(get_id[1])} {int(get_id[2])}",
                )
            ]
        ]
        return button

    def button_add_expired(user_id):
        buttons = InlineKeyboard(row_width=3)
        keyboard = []
        for X in range(1, 13):
            keyboard.append(
                InlineKeyboardButton(
                    f"{X} Bulan",
                    callback_data=f"success {user_id} {X}",
                )
            )
        buttons.add(*keyboard)
        buttons.row(
            InlineKeyboardButton(
                "👤 Dapatkan profil 👤", callback_data=f"profil {user_id}"
            )
        )
        buttons.row(
            InlineKeyboardButton(
                "❌ Tolak pembayaran ❌", callback_data=f"failed {user_id}"
            )
        )
        return buttons

    def deak(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "⬅️ Kembali ",
                    callback_data=f"prev_ub {int(count)}",
                ),
                InlineKeyboardButton(
                    "Setujui ✅", callback_data=f"deak_akun {int(count)}"
                ),
            ],
        ]
        return button

    def expired_button_bot():
        button = [
            [
                InlineKeyboardButton(
                    text=f"{bot.me.first_name}",
                    url=f"https://t.me/{bot.me.username}",
                )
            ]
        ]
        return button

    def start(message):
        if message.from_user.id not in USER_ID:
            button = [
                [InlineKeyboardButton("🔥 Buat Userbot 🔥", callback_data="bahan")],
                [
                    InlineKeyboardButton("🛠️ Tutorial", callback_data="cb_tutor"),
                    InlineKeyboardButton("Acount status 📝", callback_data="start_profile"),
                ],
            ]
        else:
            button = [
                [InlineKeyboardButton("🔥 Buat Userbot 🔥", callback_data="bahan")],
                [
                    InlineKeyboardButton("⚙️ Updates", callback_data="gitpull"),
                    InlineKeyboardButton("Restart 🔁", callback_data="restart"),
                ],
                [
                    InlineKeyboardButton("📝 User check", callback_data="cek_ubot"),
                    InlineKeyboardButton("Hosting 💻", callback_data="host"),
                ],
            ]
        return button

    def plus_minus(query, user_id):
        button = [
            [
                InlineKeyboardButton(
                    "-1 Bulan",
                    callback_data=f"kurang {query}",
                ),
                InlineKeyboardButton(
                    "+1 Bulan",
                    callback_data=f"tambah {query}",
                ),
            ],
            [InlineKeyboardButton("✅ Konfirmasi ✅", callback_data="confirm")],
            [InlineKeyboardButton("❌ Batalkan ❌", callback_data=f"home {user_id}")],
        ]
        return button

    def userbot(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "📁 Hapus dari database 📁",
                    callback_data=f"del_ubot {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "📲 Get phone number 📲",
                    callback_data=f"get_phone {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "⏳ Cek masa aktif ⏳",
                    callback_data=f"cek_masa_aktif {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔑 Get Code Otp🔑",
                    callback_data=f"get_otp {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔐 Get Verifikasi 2L 🔐",
                    callback_data=f"get_faktor {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔥 Menyala abangku 🔥", callback_data=f"ub_deak {int(count)}"
                )
            ],
            [
                InlineKeyboardButton("⬅️", callback_data=f"prev_ub {int(count)}"),
                InlineKeyboardButton("➡️", callback_data=f"next_ub {int(count)}"),
            ],
            [
                InlineKeyboardButton("Tutup", callback_data=f"0_cls"),
            ],
        ]
        return button

    def ambil_akun(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "📁 Hapus dari database 📁",
                    callback_data=f"del_ubot {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "📲 Get phone number 📲",
                    callback_data=f"get_phone {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "⏳ Cek masa aktif ⏳",
                    callback_data=f"cek_masa_aktif {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔑 Get code Otp🔑",
                    callback_data=f"get_otp {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔐 Get code V2L 🔐",
                    callback_data=f"get_faktor {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "☠ Hapus Akun ☠", callback_data=f"ub_deak {int(count)}"
                )
            ],
            [
                InlineKeyboardButton("⬅️", callback_data=f"prev_ub {int(count)}"),
                InlineKeyboardButton("➡️", callback_data=f"next_ub {int(count)}"),
            ],
        ]
        return button


class INLINE:
    def QUERY(func):
        async def wrapper(client, inline_query):
            users = ubot._get_my_id
            if inline_query.from_user.id not in users:
                await client.answer_inline_query(
                    inline_query.id,
                    cache_time=0,
                    results=[
                        (
                            InlineQueryResultArticle(
                                title=f"Anda belum order @{bot.me.username}",
                                input_message_content=InputTextMessageContent(
                                    f"Silahkan order di @{bot.me.username} biar bisa menggunakan inline ini"
                                ),
                            )
                        )
                    ],
                )
            else:
                await func(client, inline_query)

        return wrapper

    def DATA(func):
        async def wrapper(client, callback_query):
            users = ubot._get_my_id
            if callback_query.from_user.id not in users:
                await callback_query.answer(
                    f"Mangkanya order userbot @{bot.me.username} dulu baru bisa klik tombol ini",
                    True,
                )
            else:
                try:
                    await func(client, callback_query)
                except MessageNotModified:
                    await callback_query.answer("❌ ERROR")

        return wrapper


async def create_button(m):
    buttons = InlineKeyboard(row_width=1)
    keyboard = []
    msg = []
    if "~>" not in m.text.split(None, 1)[1]:
        for X in m.text.split(None, 1)[1].split():
            X_parts = X.split(":", 1)
            keyboard.append(
                InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1])
            )
            msg.append(X_parts[0])
        buttons.add(*keyboard)
        if m.reply_to_message:
            text = m.reply_to_message.text
        else:
            text = " ".join(msg)
    else:
        for X in m.text.split("~>", 1)[1].split():
            X_parts = X.split(":", 1)
            keyboard.append(
                InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1])
            )
        buttons.add(*keyboard)
        text = m.text.split("~>", 1)[0].split(None, 1)[1]

    return buttons, text

async def gcast_create_button(m):
    buttons = InlineKeyboard(row_width=2)
    keyboard = []
    split_text = m.text.split("~", 1)
    for X in split_text[1].split():
        button_data = X.split("|", 1)
        button_label = button_data[0].replace("_", " ")
        button_url = button_data[1]
        keyboard.append(InlineKeyboardButton(button_label, url=button_url))
    buttons.add(*keyboard)
    text_button = split_text[0].split(None, 1)[1]
    return buttons, text_button

async def notes_create_button(text):
    buttons = InlineKeyboard(row_width=2)
    keyboard = []
    split_text = text.split("~>", 1)
    for X in split_text[1].split():
        split_X = X.split(":", 1)
        button_text = split_X[0].replace("_", " ")
        button_url = split_X[1]
        keyboard.append(InlineKeyboardButton(button_text, url=button_url))
    buttons.add(*keyboard)
    text_button = split_text[0]
    return buttons, text_button

def extract_text_and_keyboard(input_text, row_width=2):
    keyboard = []
    try:
        input_text = input_text.strip()
        if input_text.startswith("`"):
            input_text = input_text[1:]
        if input_text.endswith("`"):
            input_text = input_text[:-1]

        text, buttons = input_text.split("~")

        button_matches = re.findall(r"\[.+\,.+\]", buttons)
        for btn_str in button_matches:
            btn_str = re.sub(r"[\[\]]", "", btn_str)
            btn_str = btn_str.split(",")
            btn_txt, btn_url = btn_str[0].strip(), btn_str[1].strip()

            if get_urls_from_text(btn_url):
                keyboard.append([btn_txt, btn_url])

        return text, keyboard
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_urls_from_text(text):
    regex = r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]
            [.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(
            \([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\
            ()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""".strip()
    return re.findall(regex, text)


def create_inline_keyboard(buttons_list, row_width=2):
    keyboard = []
    for button_text, button_url in buttons_list:
        if get_urls_from_text(button_url):
            button = InlineKeyboardButton(text=button_text, url=button_url)
        else:
            button = InlineKeyboardButton(text=button_text, callback_data=button_url)
        keyboard.append(button)

    return InlineKeyboardMarkup(build_menu(keyboard, n_cols=row_width))


def build_menu(buttons, n_cols, footer_buttons=None):
    menu = [buttons[i : i + n_cols] for i in range(0, len(buttons), n_cols)]
    if footer_buttons:
        menu.append(footer_buttons)
    return menu
  
