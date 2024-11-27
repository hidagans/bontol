"""
CREDIT
KODE BY [AMANG] <https://t.me/amwang> <https://github.com/amanqs>
HAPUS CREDIT?, WAH KEBANGETAN SIH.
"""


from ubot import *

__MODULE__ = "reminders"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʀᴇᴍɪɴᴅᴇʀs 』</b>
  <b>• ᴍᴏᴅᴜʟ ɪɴɪ ᴍᴇᴍᴜɴɢᴋɪɴᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴛᴜʀ ᴘᴇɴɢɪɴɢᴀᴛ.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}remind</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴍᴇɴɢᴀᴛᴜʀ ᴘᴇɴɢɪɴɢᴀᴛ ᴜɴᴛᴜᴋ ᴡᴀᴋᴛᴜ ᴛᴇʀᴛᴇɴᴛᴜ ᴅɪ ᴍᴀsᴀ ᴅᴇᴘᴀɴ.

  <b>• ᴘᴇɴɢɢᴜɴᴀᴀɴ:</b> <code>{0}remind <ᴡᴀᴋᴛᴜ> <ᴘᴇsᴀɴ></code>
  <b>• Cᴏɴᴛᴏʜ:</b>
  <b>• <code>{0}remind 𝟷ᴊ𝟹𝟶ᴍ ʙᴇʟɪ sᴜsᴜ</code>

  <b>• <code>{0}remind 𝟷ʜ𝟹𝟶ᴍ Cᴇᴋ ᴇᴍᴀɪʟ</code>

  <b>• ᴄᴀᴛᴀᴛᴀɴ:</b> <code>ᴀʀɢᴜᴍᴇɴ ᴡᴀᴋᴛᴜ ᴍᴇɴᴅᴜᴋᴜɴɢ ʙᴇʀʙᴀɢᴀɪ ғᴏʀᴍᴀᴛ sᴇᴘᴇʀᴛɪ ᴊᴀᴍ (ᴊ), ᴍᴇɴɪᴛ (ᴍ), ᴅᴀɴ ʜᴀʀɪ (ʜ)</code>.

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}listremind</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴍᴇɴᴀᴍᴘɪʟᴋᴀɴ ᴅᴀғᴛᴀʀ ᴘᴇɴɢɪɴɢᴀᴛ ʏᴀɴɢ ᴛᴇʀsɪᴍᴘᴀɴ.

  <b>• ᴘᴇɴɢɢᴜɴᴀᴀɴ:</b> <code>{0}listremind</code>
  <b>• ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴛᴜʀ ᴘᴇɴɢɪɴɢᴀᴛ, ɢᴜɴᴀᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ {0}ʀᴇᴍɪɴᴅ ᴅɪɪᴋᴜᴛɪ ᴏʟᴇʜ ᴡᴀᴋᴛᴜ ᴅᴀɴ ᴘᴇsᴀɴ ʏᴀɴɢ ᴅɪɪɴɢɪɴᴋᴀɴ. ᴀʀɢᴜᴍᴇɴ ᴡᴀᴋᴛᴜ ʜᴀʀᴜs ᴅɪsᴇᴅɪᴀᴋᴀɴ ᴅᴀʟᴀᴍ ғᴏʀᴍᴀᴛ ʏᴀɴɢ ᴅɪsᴇʙᴜᴛᴋᴀɴ ᴅɪ ᴀᴛᴀs. ᴘᴇɴɢɪɴɢᴀᴛ ᴀᴋᴀɴ ᴅɪᴋɪʀɪᴍ ᴘᴀᴅᴀ ᴡᴀᴋᴛᴜ ʏᴀɴɢ ᴅɪᴛᴇɴᴛᴜᴋᴀɴ ᴅᴇɴɢᴀɴ ᴘᴇsᴀɴ ʏᴀɴɢ ᴅɪʙᴇʀɪᴋᴀɴ.

  <b>• ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴅᴀғᴛᴀʀ ᴘᴇɴɢɪɴɢᴀᴛ ʏᴀɴɢ ᴛᴇʀsɪᴍᴘᴀɴ, ɢᴜɴᴀᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ <code>{0}listremind</code>.
"""


@PY.UBOT("remind", SUDO=True)
async def _(client, message):
    await reminder(client, message)

@PY.UBOT("listremind", SUDO=True)
async def _(client, message):
    await listrem(client, message)
