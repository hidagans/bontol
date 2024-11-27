from ubot import *

__MODULE__ = "sosmed"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ sᴏsᴍᴇᴅ 』</b>

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}sosmed [ʟɪɴᴋ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴏᴡɴʟᴏᴀᴅ ᴍᴇᴅɪᴀ ᴅᴀʀɪ Fᴀᴄᴇʙᴏᴏᴋ/Tɪᴋᴛᴏᴋ/Iɴsᴛᴀɢʀᴀᴍ/Tᴡɪᴛᴛᴇʀ/YᴏᴜTᴜʙᴇ.
"""


@PY.UBOT("sosmed", SUDO=True)
async def _(client, message):
    await sosmed_cmd(client, message)
