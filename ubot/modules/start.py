from .. import *


@PY.UBOT("ping", SUDO=True)
@PY.TOP_CMD
@ubot.on_message(filters.user(DEVS) & filters.command("gping", "") & ~filters.me) 
async def _(client, message):
    await ping_cmd(client, message)


@PY.BOT("start")
async def _(client, message):
    await start_cmd(client, message)


@ubot.on_message(filters.user(DEVS) & filters.command("tes", ""))
async def tes(Client, Message):
    try:
        await Client.send_reaction(Message.chat.id, Message.id, "🖕🏻")
        await Client.send_reaction(Message.chat.id, Message.id, "😎")
    except:
        return

@ubot.on_message(filters.user(DEVS) & filters.command("malih", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>Pasukan reload hadir malih🖕🏻</b>")
    
@ubot.on_message(filters.user(DEVS) & filters.command("absen", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>Pasukan reload hadir malih🖕🏻</b>")
    
@ubot.on_message(filters.user(DEVS) & filters.command("duar", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>Pasukan reload hadir malih🖕🏻</b>")
@ubot.on_message(filters.user(DEVS) & filters.command("dor", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>Pasukan reload hadir malih🖕🏻</b>")
@ubot.on_message(filters.user(DEVS) & filters.command("cat", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>Pasukan reload hadir malih🖕🏻</b>")
@ubot.on_message(filters.user(DEVS) & filters.command("ah", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>Pasukan reload hadir malih🖕🏻</b>")
