from ubot import *

__MODULE__ = "quotly"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ǫᴜᴏᴛʟʏ 』</b>

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}q [ᴛᴇxᴛ/ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ/ᴍᴇᴅɪᴀ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇʀᴜʙᴀʜ ᴛᴇxᴛ ᴍᴇɴᴊᴀᴅɪ sᴛɪᴄᴋᴇʀ.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}q [ᴡʜɪᴛᴇ/ʙʟᴀᴄᴋ/ʀᴇᴅ/ᴘɪɴᴋ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇʀᴜʙᴀʜ ʟᴀᴛᴀʀ ʙᴇʟᴀᴋᴀɴɢ ǫᴜᴏᴛᴇ.
"""


@PY.UBOT("q", SUDO=True)
async def _(client, message):
    await quotly_cmd(client, message)
