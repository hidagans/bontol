from ubot import *

__MODULE__ = "spam"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ sᴘᴀᴍ 』</b>

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}dspam [ᴊᴜᴍʟᴀʜ] [ᴡᴀᴋᴛᴜ ᴅᴇʟᴀʏ] [ʙᴀʟᴀs ᴘᴇsᴀɴ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴅᴇʟᴀʏ sᴘᴀᴍ.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}spam [ᴊᴜᴍʟᴀʜ] [ᴋᴀᴛᴀ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴ sᴘᴀᴍ.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}cspam</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ sᴛᴏᴘ sᴘᴀᴍ.
"""


@PY.UBOT("spam|dspam", SUDO=True)
async def _(client, message):
    if message.command[0] == "spam":
        await spam_cmd(client, message)
    if message.command[0] == "dspam":
        await dspam_cmd(client, message)


@PY.UBOT("cspam", SUDO=True)
async def _(client, message):
    await capek_dah(client, message)
