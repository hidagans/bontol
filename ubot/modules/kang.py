from ubot import *

__MODULE__ = "kang"
__HELP__ = """
 <b>『 Bantuan untuk kang 』</b>

  <b>• Perintah:</b> <code>{0}kang [balas ke stiker]</code>
  <b>• Penjelasan:</b> Untuk membuat costum stiker pack.
"""


#@PY.BOT("kang")
#async def _(client, message):
    #await kang_cmd_bot(client, message)


@PY.UBOT("kang", SUDO=True)
async def _(client, message):
    await kang(client, message)
