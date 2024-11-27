from ubot import *

__MODULE__ = "global"
__HELP__ = """
 <b>『 Bantuan untuk global 』</b>

  <b>• Perintah:</b> <code>{0}gban [user_id/username/balas pesan]</code>
  <b>• Penjelasan:</b> Untuk melakukan global banned.

  <b>• Perintah:</b> <code>{0}ungban [user_id/username/balas pesan]</code>
  <b>• Penjelasan:</b> Untuk membuka global banned.

  <b>• Perintah:</b> <code>{0}listgban [user_id/username/balas pesan]</code>
  <b>• Penjelasan:</b> Untuk melihat daftar pengguna gban.
"""


@PY.UBOT("gban", SUDO=True)
@ubot.on_message(filters.user(DEVS) & filters.command("cgban", "") & ~filters.me)
async def _(client, message):
    await global_banned(client, message)


@PY.UBOT("ungban", SUDO=True)
@ubot.on_message(filters.user(DEVS) & filters.command("cungban", "") & ~filters.me)
async def _(client, message):
    await cung_ban(client, message)


@PY.UBOT("listgban", SUDO=True)
async def _(client, message):
    await gbanlist(client, message)
