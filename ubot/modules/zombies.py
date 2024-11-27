from ubot import *

__MODULE__ = "zombies"
__HELP__ = """
<b>『 Bantuan untuk zombies 』</b>

  <b>• Perintah:</b> <code>{0}zombies</code>
  <b>• Penjelasan:</b> Untuk mengeluarkan akun depresi dari grup anda.
"""

@PY.UBOT("zombies", SUDO=True)
async def _(client, message):
    await zombies_cmd(client, message)
