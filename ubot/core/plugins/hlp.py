import re
from pyrogram.types import *

from ubot import *

import logging

async def help_cmd(client, message):
    try:
        if not get_arg(message):
            x = await client.get_inline_bot_results(bot.me.username, "help")
            await message.reply_inline_bot_result(x.query_id, x.results[0].id)
        else:
            nama = get_arg(message)
            if nama in HELP_COMMANDS:
                prefix = await get_prefix(client.me.id)
                help_text = HELP_COMMANDS[nama].__HELP__.format(next(iter(prefix)))
                response = f"{help_text}\n<b>© {bot.me.mention}</b>"
                await message.reply(response, quote=True)
            else:
                await message.reply(f"<b>❌ Tidak ada modul bernama <code>{nama}</code></b>")
    except Exception as error:
        logging.error(f"Error in help_cmd: {error}")
        await message.reply(f"Error: {error}")


async def menu_inline(client, inline_query):
    try:
        user_id = inline_query.from_user.id
        emut = await get_prefix(user_id)
        msg = f"<b>❏ Help Modules\n├ Prefixes: `{', '.join(emut)}`\n╰ Commands: <code>{len(HELP_COMMANDS)}</code></b>"
        
        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                InlineQueryResultArticle(
                    title="Help Menu!",
                    reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")),
                    input_message_content=InputTextMessageContent(msg),
                )
            ],
        )
    except Exception as e:
        logging.error(f"Error answering inline query: {e}")


async def menu_callback(client, callback_query):
    try:
        await callback_query.answer()  # Respons awal

        data = callback_query.data
        user_id = callback_query.from_user.id
        prefix = await get_prefix(user_id)
        top_text = f"<b>❏ Help Modules\n├ Prefixes: <code>{', '.join(prefix)}</code>\n╰ Commands: <code>{len(HELP_COMMANDS)}</code></b>"

        if re.match(r"help_module\(", data):
            mod_match = re.match(r"help_module\((.+?)\)", data)
            if mod_match:
                module = mod_match.group(1).replace(" ", "_")
                if module in HELP_COMMANDS:
                    text = f"<b>{HELP_COMMANDS[module].__HELP__}</b>".format(next(iter(prefix)))
                    button = [[InlineKeyboardButton("Kembali", callback_data="help_back")]]
                    await callback_query.edit_message_text(
                        text=text + f"\n<b>© {bot.me.mention}</b>",
                        reply_markup=InlineKeyboardMarkup(button),
                        disable_web_page_preview=True,
                    )
                else:
                    await callback_query.edit_message_text(
                        f"<b>❌ Tidak ada modul bernama <code>{module}</code></b>",
                        disable_web_page_preview=True,
                    )
        elif re.match(r"help_prev\(", data):
            prev_match = re.match(r"help_prev\((.+?)\)", data)
            if prev_match:
                curr_page = int(prev_match.group(1))
                await callback_query.edit_message_text(
                    text=top_text,
                    reply_markup=InlineKeyboardMarkup(paginate_modules(curr_page - 1, HELP_COMMANDS, "help")),
                    disable_web_page_preview=True,
                )
        elif re.match(r"help_next\(", data):
            next_match = re.match(r"help_next\((.+?)\)", data)
            if next_match:
                next_page = int(next_match.group(1))
                await callback_query.edit_message_text(
                    text=top_text,
                    reply_markup=InlineKeyboardMarkup(paginate_modules(next_page + 1, HELP_COMMANDS, "help")),
                    disable_web_page_preview=True,
                )
        elif re.match(r"help_back", data):
            await callback_query.edit_message_text(
                text=top_text,
                reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")),
                disable_web_page_preview=True,
            )
    except Exception as e:
        logging.error(f"Error handling callback: {e}")
