from ubot import *


__MODULE__ = "showid"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ sʜᴏᴡɪᴅ 』</b>

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}id</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴛᴀʜᴜɪ ID ᴅᴀʀɪ ᴜsᴇʀ/ɢʀᴜᴘ/ᴄʜᴀɴɴᴇʟ.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}id [ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ/ᴍᴇᴅɪᴀ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴛᴀʜᴜɪ ID ᴅᴀʀɪ ᴜsᴇʀ/ᴍᴇᴅɪᴀ.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}getid [ᴜsᴇʀɴᴀᴍᴇ ᴜsᴇʀ/ɢʀᴜᴘ/ᴄʜᴀɴɴᴇʟ]</code>.
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴛᴀʜᴜɪ ID ᴜsᴇʀ/ɢʀᴜᴘ/ᴄʜᴀɴɴᴇʟ ᴍᴇʟᴀʟᴜɪ ᴜsᴇʀɴᴀᴍᴇ ᴅᴇɴɢᴀɴ sɪᴍʙᴏʟ @.
"""


@PY.UBOT("id", SUDO=True)
async def _(client, message):
    await id_cmd(client, message)
