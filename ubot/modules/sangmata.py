from ubot import *

__MODULE__ = "sangmata"
__HELP__ = """
<b>『 Bantuan untuk sangmata 』</b>

  <b>• Perintah:</b> <code>{0}sg [user_id/username/balas pesan]</code>
  <b>• Penjelasan:</b> Untuk memeriksa histori nama/username.
"""


@PY.UBOT("sg", SUDO=True)
async def _(client, message):
    await sg_cmd(client, message)
