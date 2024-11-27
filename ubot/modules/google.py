from ubot import *

__MODULE__ = "google"
__HELP__ = """
 <b>『 Bantuan untuk google 』</b>

  <b>• Perintah:</b> <code>{0}google [query]</code>
  <b>• Penjelasan:</b> Untuk mencari sesuatu.
"""


@PY.UBOT("google", SUDO=True)
async def _(client, message):
    await gsearch(client, message)
