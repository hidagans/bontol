from ubot import *

__MODULE__ = "prefix"
__HELP__ = """
 <b>『 Bantuan untuk prefix 』</b>

  <b>• Perintah:</b> <code>{0}prefix</code> [Trigger]
  <b>• Penjelasan:</b> Untung mengatur handler userbot anda.

  <b>• Perintah:</b> <code>{0}setemoji - [Query] [Emoji_prem]</code> 
  <b>• Query:</b>
         <b>•> PONG</b>
         <b>•> UPTIME</b>
         <b>•> MENTION</b>
  <b>• Penjelasan: Untuk merubah tapilan emoji pong,uptime, dan mention pada ping 
"""


@PY.UBOT("prefix", SUDO=True)
async def _(client, message):
    await kok_anjeng(client, message)


@PY.UBOT("setemoji")
@PY.TOP_CMD
async def _(client, message):
    await change_emot(client, message)
