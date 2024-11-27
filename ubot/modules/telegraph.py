from ubot import *

__MODULE__ = "telegraph"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴛᴇʟᴇɢʀᴀᴘʜ 』</b>

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}tg [ʀᴇᴘʟʏ ᴍᴇᴅɪᴀ/ᴛᴇxᴛ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴘʟᴏᴀᴅ ᴍᴇᴅɪᴀ/ᴛᴇxᴛ ᴋᴇ ᴛᴇʟᴇɢʀᴀᴘʜ.
"""


@PY.UBOT("tg", SUDO=True)
async def _(client, message):
    await tg_cmd(client, message)
