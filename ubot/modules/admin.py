from ubot import *

__MODULE__ = "Admin"
__HELP__ = """
<b>『 Bantuan untuk admin 』</b>

  <b>• Perintah:</b> <code>{0}kick [user_id/username/reply user]</code>
  <b>• Penjelasan:</b> untuk menendang anggota dari grup.

  <b>• Perintah:</b> <code>{0}ban [user_id/username/reply user]</code>
  <b>• Penjelasan:</b> untuk memblokir anggota dari grup.

  <b>• Perintah:</b> <code>{0}mute [user_id/username/reply user]</code>
  <b>• Penjelasan:</b> untuk membisukan anggota dari grup.

  <b>• Perintah:</b> <code>{0}unban [user_id/username/reply user]</code>
  <b>• Penjelasan:</b> untuk membuka blokir anggota dari grup.

  <b>• Perintah:</b> <code>{0}unmute [user_id/username/reply user]</code>
  <b>• Penjelasan:</b> untuk membuka pembisuan anggota dari grup.
"""


@PY.UBOT("kick|ban|mute|unmute|unban", SUDO=True)
async def _(client, message):
    await admin_bannen(client, message)

@PY.UBOT("pin|unpin", SUDO=True)
async def _(client, message):
    await pin_message(client, message)

@PY.UBOT("promote|fullpromote", SUDO=True)
async def _(client, message):
    await promotte(client, message)

@PY.UBOT("demote", SUDO=True)
async def _(client, message):
    await demote(client, message)
    
@PY.UBOT("getlink", SUDO=True)
async def _(client, message):
    await invite_link(client, message)
