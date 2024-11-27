from ubot import *

__MODULE__ = "purge"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴘᴜʀɢᴇ 』</b>

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}purge [ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ʙᴇʀsɪʜᴋᴀɴ (ʜᴀᴘᴜs sᴇᴍᴜᴀ ᴘᴇsᴀɴ) ᴏʙʀᴏʟᴀɴ ᴅᴀʀɪ ᴘᴇsᴀɴ ʏᴀɴɢ ᴅɪʙᴀʟᴀs ʜɪɴɢɢᴀ ʏᴀɴɢ ᴛᴇʀᴀᴋʜɪʀ.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}del [ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ʜᴀᴘᴜs ᴘᴇsᴀɴ ʏᴀɴɢ ᴅɪʙᴀʟᴀs.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}purgeme [ɴᴜᴍʙᴇʀ ᴏғ ᴍᴇssᴀɢᴇs]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ: ʜᴀᴘᴜs ᴘᴇsᴀɴ ᴀɴᴅᴀ sᴇɴᴅɪʀɪ ᴅᴇɴɢᴀɴ ᴍᴇɴᴇɴᴛᴜᴋᴀɴ ᴛᴏᴛᴀʟ ᴘᴇsᴀɴ.
"""


@PY.UBOT("del", SUDO=True)
async def _(client, message):
    await del_cmd(client, message)


@PY.UBOT("purgeme", SUDO=True)
async def _(client, message):
    await purgeme_cmd(client, message)


@PY.UBOT("purge", SUDO=True)
async def _(client, message):
    await purge_cmd(client, message)
