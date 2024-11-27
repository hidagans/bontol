from ubot import *

__MODULE__ = "font"
__HELP__ = """
 <b>『 Bantuan untuk font 』</b>

  <b>• Perintah:</b> <code>{0}font [balas pesan/berikan pesan]</code>
  <b>• Penjelasan:</b> Untuk merubah teks dengan costum font.
"""


@PY.UBOT("font", SUDO=True)
async def _(client, message):
    await font_message(client, message)


@PY.INLINE("^get_font")
@INLINE.QUERY
async def _(client, inline_query):
    await font_inline(client, inline_query)


@PY.CALLBACK("^get")
@INLINE.DATA
async def _(client, callback_query):
    await font_callback(client, callback_query)


@PY.CALLBACK("^next")
@INLINE.DATA
async def _(client, callback_query):
    await font_next(client, callback_query)


@PY.CALLBACK("^prev")
@INLINE.DATA
async def _(client, callback_query):
    await font_prev(client, callback_query)
