from ubot import *

__MODULE__ = "image"
__HELP__ = """
 <b>『 Bantuan untuk image 』</b>

  <b>• Perintah:</b> <code>{0}rbg [balas foto]</code>
  <b>• Penjelasan:</b> Untuk menghapus latar belakang gambar.

  <b>• Perintah:</b> <code>{0}blur [balas foto]</code>
  <b>• Penjelasan:</b> Untuk memberikan efek blur pada gambar.

  <b>• Perintah:</b> <code>{0}mirror [balas foto]</code>
  <b>• Penjelasan:</b> Untuk memberikan efek cermin pada gambar.

  <b>• Perintah:</b> <code>{0}negative [balas foto]</code>
  <b>• Penjelasan:</b> Untuk memberikan efek negatif pada gambar.
"""


@PY.UBOT("rbg", SUDO=True)
async def _(client, message):
    await rbg_cmd(client, message)


@PY.UBOT("blur", SUDO=True)
async def _(client, message):
    await blur_cmd(client, message)


@PY.UBOT("negative", SUDO=True)
async def _(client, message):
    await negative_cmd(client, message)


@PY.UBOT("miror", SUDO=True)
async def _(client, message):
    await miror_cmd(client, message)
