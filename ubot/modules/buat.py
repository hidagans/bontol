from ubot import *

__MODULE__ = "create"
__HELP__ = """
 <b>『 Bantuan untuk create 』</b>

  <b>• Perintah:</b> <code>{0}create gc</code>
  <b>• Penjelasan:</b> Untuk membuat gruop telegram.

  <b>• Perintah:</b> <code>{0}create ch</code>
  <b>• Penjelasan:</b> Untuk membuat channel telegram.
"""


@PY.UBOT("create", SUDO=True)
async def _(client, message):
    await buat_apaam(client, message)
