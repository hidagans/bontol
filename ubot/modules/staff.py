from ubot import *

__MODULE__ = "staff"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ sᴛᴀғғ 』</b>

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}staff</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴛᴀʜᴜɪ ᴅᴀғᴛᴀʀ sᴇᴍᴜᴀ ᴀᴅᴍɪɴ ᴅɪᴅᴀʟᴀᴍ ɢʀᴜᴘ.
"""

@PY.UBOT("staff", SUDO=True)
async def _(client, message):
    await staff_cmd(client, message)
