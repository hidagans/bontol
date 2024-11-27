from ubot import *

__MODULE__ = "AGcast"
__HELP__ = """
 Bantuan Untuk Auto Gcast

• Perintah : <code>{0}setgcast</code>
• Penjelasan : Untuk set delay auto gcast.

• Perintah : <code>{0}dgcast</code> [balas pesan/kirim pesan]
• Penjelasan : Untuk memulai mengirim gcast.

• Perintah : <code>{0}stopgcast</code>
• Penjelasan : Untuk menghentikan proses gcast yang sedang berjalan.

"""


@PY.UBOT("setgcast", SUDO=True)
async def _(client, message):
    await set_delay_cmd(client, message)


@PY.UBOT("dgcast", SUDO=True)
async def _(client, message):
    await gcast_cmd(client, message)


@PY.UBOT("stopgcast", SUDO=True)
async def _(client, message):
    await stop_autobroadcast_cmd(client, message)
