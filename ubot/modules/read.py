from ubot import *

__MODULE__ = "read"
__HELP__ = """
 <b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴏᴄʀ 』</b>
  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}ocr [ʙᴀʟᴀs ᴍᴇᴅɪᴀ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴄᴀ ᴛᴇᴋs ᴅᴀʀɪ ᴍᴇᴅɪᴀ.
"""


@PY.UBOT("ocr", SUDO=True)
async def _(client, message):
    await read_cmd(client, message)
