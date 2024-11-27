from ubot import *

__MODULE__ = "button"
__HELP__ = """
<b>『 Bantuan untuk button 』</b>

  <b>• Perintah:</b> <code>{0}button text ~> Button_text: Button_link</code>
  <b>• Penjelasan:</b> Untuk membuat tombol inline, maksimal 100 button
"""


@PY.UBOT("button")
@PY.TOP_CMD
async def _(client, message):
    await cmd_button(client, message)


@PY.INLINE("^get_button")
@INLINE.QUERY
async def _(client, inline_query):
    await inline_button(client, inline_query)
