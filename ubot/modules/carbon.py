from ubot import *

__MODULE__ = "carbon"
__HELP__ = f"""
<b>『 Bantuan untuk carbon 』</b>

  <b>• Perintah:</b> <code>{0}carbon [reply/text]</code>
  <b>• Penjelasan:</b> Untuk membuat text carbonara 
"""

@PY.UBOT("carbon", SUDO=True)
async def _(client, message):
    await carbon_func(client, message)
