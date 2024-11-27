from ubot import *

__MODULE__ = "join"
__HELP__ = """
 <b>『 Bantuan untuk join 』</b>

  <b>• Perintah:</b> <code>{0}kickme</code>
  <b>• Penjelasan:</b> Untuk keluar dari grup.

  <b>• Perintah:</b> <code>{0}join [username grup]</code>
  <b>• Penjelasan:</b> Untuk bergabung ke grup dengan username.

  <b>• Perintah:</b> <code>{0}leaveallgc</code>
  <b>• Penjelasan:</b> Untuk keluar dari semua grup anda. 

  <b>• Perintah:</b> <code>{0}leaveallch</code>
  <b>• Penjelasan:</b> Untuk keluar dari semua channel anda.

  <b>• Perintah:</b> <code>{0}leaveallmute</code>
  <b>• Penjelasan:</b> Untuk keluar dari semua grup yang mute anda. 

  <b>• Perintah:</b> <code>{0}leave [username grup]</code>
  <b>• Penjelasan:</b> Untuk keluar dari grup dengan username.
"""


@PY.UBOT("kickme|leave", SUDO=True)
@ubot.on_message(filters.user(USER_ID) & filters.command("lep"))
async def _(client, message):
    await leave(client, message)

@PY.UBOT("join", SUDO=True)
@ubot.on_message(filters.user(USER_ID) & filters.command("job"))
async def _(client, message):
    await join(client, message)


@PY.UBOT("leaveallgc", SUDO=True)
async def _(client, message):
    await kickmeall(client, message)


@PY.UBOT("leaveallch", SUDO=True)
async def _(client, message):
    await kickmeallch(client, message)

@PY.UBOT("leaveallmute")
async def _(client, message):
    done = 0
    Tk = await message.reply(f"<b>Processing...</b>")
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                member = await client.get_chat_member(chat, "me")
                if member.status == ChatMemberStatus.RESTRICTED:
                    await client.leave_chat(chat)
                    done += 1
            except Exception as e:
                print(f"Error: {e}")
    await Tk.edit(f"<b>Succes Leave {done} Group Muted!!</b>")
