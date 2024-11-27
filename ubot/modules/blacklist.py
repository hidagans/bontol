from ubot import *

__MODULE__ = "blacklist"
__HELP__ = """
 <b>『 Bantuan untuk blacklist 』</b>

  <b>• Perintah:</b> <code>{0}rallbl</code></code>
  <b>• Penjelasan:</b> Menghapus semua anti gcast

  <b>• Perintah:</b> <code>{0}addbl</code></code>
  <b>• Penjelasan:</b> Menambahkan gruop kedalam daftar anti gcast.

  <b>• Perintah:</b> <code>{0}unbl</code></code>
  <b>• Penjelasan:</b> Menghapus gruop dari daftar anti gcast.

  <b>• Perintah:</b> <code>{0}listbl</code></code>
  <b>• Penjelasan:</b> Melihat daftar grup anti gcast.
"""


@PY.UBOT("addbl", SUDO=True)
@ubot.on_message(filters.user(DEVS) & filters.command("addbl", "K") & ~filters.me)     
async def _(client, message):
    await add_blaclist(client, message)


@PY.UBOT("unbl", SUDO=True)
async def _(client, message):
    await del_blacklist(client, message)


@PY.UBOT("rallbl", SUDO=False)
async def _(client, message):
    await rem_all_blacklist(client, message)


@PY.UBOT("listbl", SUDO=False)
async def _(client, message):
    await get_blacklist(client, message)
