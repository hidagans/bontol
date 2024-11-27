from ubot import *

__MODULE__ = "copy"
__HELP__ = """
 <b>『 Bantuan untuk copy 』</b>

  <b>• Perintah:</b> <code>{0}copy [link]</code>
  <b>• Penjelasan:</b> Untuk mengambil pesan melalui link telegram.
  
  <b>• Perintah:</b> <code>{0}copy_semua idgrup ke idtujuan</code>
  <b>• Penjelasan:</b> Untuk mengambil semua pesan di target dan mengirim ke tujuan contoh penggunaan .copy_semua -1002075041230 ke -1002223073528.

  <b>• Perintah:</b> <code>{0}cancelcopy [link]</code>
  <b>• Penjelasan:</b> Untuk cancel copy yang berjalan.
  """


@PY.BOT("copy")
async def _(client, message):
    await copy_bot_msg(client, message)


@PY.UBOT("copy", SUDO=True)
async def _(client, message):
    await copy_ubot_msg(client, message)

@PY.UBOT("copy_semua")
async def _(client, message):
  await copy_semua(client, message)

@PY.UBOT("copy_batch")
async def _(client, message):
  await copy_batch(client, message)

@PY.UBOT("cancelcopy", SUDO=True)
async def _(client, message):
    await cancel_nyolong(client, message)

@PY.INLINE("^get_msg")
@INLINE.QUERY
async def _(client, inline_query):
    await copy_inline_msg(client, inline_query)


@PY.CALLBACK("^copymsg")
@INLINE.DATA
async def _(client, callback_query):
    await copy_callback_msg(client, callback_query)
