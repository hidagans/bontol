from ubot import *

__MODULE__ = "profile"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴘʀᴏꜰɪʟᴇ 』</b>

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}adminlist</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ sᴛᴀᴛᴜs ᴀᴅᴍɪɴ ɢʀᴜᴘ ᴀɴᴅᴀ.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}setbio [ǫᴜᴇʀʏ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ʙɪᴏ Aɴᴅᴀ.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}setname [ǫᴜᴇʀʏ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ɴᴀᴍᴀ ᴀɴᴅᴀ.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}setpp [ʙᴀʟᴀs ᴍᴇᴅɪᴀ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ: ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ Fᴏᴛᴏ Aᴋᴜɴ Aɴᴅᴀ.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}block [ʙᴀʟᴀs ᴘᴇɴɢɢᴜɴᴀ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ʙʟᴏᴋɪʀ ᴘᴇɴɢɢᴜɴᴀ.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}unblock [ǫᴜᴇʀʏ]</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ʙᴜᴋᴀ ʙʟᴏᴋɪʀ ᴘᴇɴɢɢᴜɴᴀ.
"""


@PY.UBOT("setbio", SUDO=True)
async def _(client, message):
    await set_bio(client, message)


@PY.UBOT("setname", SUDO=True)
async def _(client, message):
    await setname(client, message)


@PY.UBOT("block", SUDO=True)
async def _(client, message):
    await block_user_func(client, message)


@PY.UBOT("unblock", SUDO=True)
async def _(client, message):
    await unblock_user_func(client, message)


@PY.UBOT("setpp", SUDO=True)
async def _(client, message):
    await set_pfp(client, message)

@PY.UBOT("adminlist", SUDO=True)
async def _(client, message):
    await list_admin(client, message)
