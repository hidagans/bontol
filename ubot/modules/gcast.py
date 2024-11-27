from ubot import *

__MODULE__ = "gcast"
__HELP__ = """
 <b>『 Bantuan untuk gcast 』</b>

  <b>• Perintah:</b> <code>{0}ucast [balas pesan/kirim pesan]</code>
  <b>• Penjelasan:</b> Untuk mengirim pesan kesemua pengguna.

  <b>• Perintah:</b> <code>{0}gcast [balas pesan/kirim pesan]</code>
  <b>• Penjelasan:</b> Untuk mengirim pesan kesemua gruop.

  <b>• Perintah:</b> <code>{0}cgcast</code>
  <b>• Penjelasan:</b> Untuk membatalkan proses gcast.

  <b>• Perintah:</b> <code>{0}send [username/user_id - teks/reply]</code>
  <b>• Penjelasan:</b> Untuk mengirim pesan pribadi secara rahasia.

  <b>• Perintah:</b> <code>{0}spamg [balas pesan]</code>
  <b>• Penjelasan:</b> Untuk mengirim pesan gcast kesemua gruop.
  
  <b>• Untuk menggunakan button gunakan format: <code> Teks ~ button_teks:button_url</code>
"""


@PY.UBOT("gcast", SUDO=True)
@ubot.on_message(filters.user(USER_ID) & filters.command("gcast", "^") & ~filters.me)     
async def _(client, message):
    await broadcast_group_cmd(client, message)


@PY.UBOT("ucast", SUDO=True)
async def _(client, message):
    await broadcast_users_cmd(client, message)


@PY.UBOT("cgcast", SUDO=True)
async def _(client, message):
    await cancel_broadcast(client, message)

@PY.UBOT("send", SUDO=True)
async def _(client, message):
    await send_msg_cmd(client, message)


@PY.INLINE("^get_send")
@INLINE.QUERY
async def _(client, inline_query):
    await send_inline(client, inline_query)


@PY.INLINE("^gcast_button")
@INLINE.QUERY
async def _(client, inline_query):
    await gcast_inline(client, inline_query)
 

@PY.UBOT("spamg", SUDO=True)
@ubot.on_message(filters.user(USER_ID) & filters.command("spamg", "K") & ~filters.me)
async def _(client, message):
    await spam_broadcast_cmd(client, message)
