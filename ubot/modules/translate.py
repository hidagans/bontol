from ubot import *

__MODULE__ = "translate"
__HELP__ = """
<b>『 Bantuan untuk translate 』</b>

  <b>• Perintah:</b> <code>{0}tr [reply/text]</code>
  <b>• Penjelasan:</b> untuk menerjemahkan text dengan kode negara yang diinginkan.

  <b>• Perintah:</b> <code>{0}set_lang</code>
  <b>• Penjelasan:</b> untuk mengubah bahasa.

  <b>• Perintah:</b> <code>{0}tts [reply/text]</code>
  <b>• Penjelasan:</b> untuk menerjemahkan text dengan code negara yang diinginkan serta merubahnya menjadi pesan suara.
"""


@PY.UBOT("tts", SUDO=True)
async def _(client, message):
    await tts_cmd(client, message)


@PY.UBOT("tr|tl", SUDO=True)
async def _(client, message):
    await tr_cmd(client, message)


@PY.UBOT("set_lang", SUDO=True)
async def _(client, message):
    await set_lang_cmd(client, message)


@PY.INLINE("^ubah_bahasa")
@INLINE.QUERY
async def _(client, inline_query):
    await ubah_bahasa_inline(client, inline_query)


@PY.CALLBACK("^set_bahasa")
@INLINE.DATA
async def _(client, callback_query):
    await set_bahasa_callback(client, callback_query)
