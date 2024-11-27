from ubot import *

__MODULE__ = "openai"
__HELP__ = """
 <b>『 Bantuan untuk openai 』</b>

  <b>• Perintah:</b> <code>{0}ai</code> or <code>{0}ask</code> [query]</code>
  <b>• Penjelasan:</b> Untuk menggunakan chtgpt.

  <b>• Perintah:</b> <code>{0}dalle</code> or <code>{0}photo</code> [query]</code>
  <b>• Penjelasan:</b> Untuk membuat sebuah foto.

  <b>• Perintah:</b> <code>{0}stt [balas audio]</code>
  <b>• Penjelasan:</b> Untuk merubah pesn suara ke teks.
"""


@PY.UBOT("ai|ask", SUDO=True)
async def _(client, message):
    await ai_cmd(client, message)


@PY.UBOT("dalle|photo", SUDO=True)
async def _(client, message):
    await dalle_cmd(client, message)


@PY.UBOT("stt", SUDO=True)
async def _(client, message):
    await stt_cmd(client, message)
