from ubot import *


async def get_top_module(client, message):
    var = await all_var(bot.me.id, "modules")
    sorted_var = sorted(var.items(), key=lambda item: item[1], reverse=True)

    command_count = 999
    text = message.text.split()

    if len(text) == 2:
        try:
            command_count = min(max(int(text[1]), 1), 10)
        except Exception:
            pass

    total_count = sum(count for _, count in sorted_var[:command_count])

    txt = "<b>📊 ᴛᴏᴘ ᴄᴏᴍᴍᴀɴᴅ</b>\n"
    for command, count in sorted_var[:command_count]:
        txt += f"<b> ├ {command}:</b> <code>{count}</code>\n"

    txt += f"<b> ╰ ᴛᴏᴛᴀʟ ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{total_count}</code>"

    await message.reply(txt, quote=True)
