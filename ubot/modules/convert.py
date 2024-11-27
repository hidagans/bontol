from ubot import *

__MODULE__ = "convert"
__HELP__ = """
 <b>『 Bantuan untuk convert 』</b>

  <b>• Perintah:</b> <code>{0}toanime [balas foto/sticker]</code>
  <b>• Penjelasan:</b> Merubah gambar ke anime.

  <b>• Perintah:</b> <code>{0}toimg [balas sticker/gif]</code>
  <b>• Penjelasan:</b> Merubah stiker/gif ke gambar.

  <b>• Perintah:</b> <code>{0}tosticker [balas foto]</code>
  <b>• Penjelasan:</b> Merubah foto ke sticker.

  <b>• Perintah:</b> <code>{0}togif [balas sticker]</code>
  <b>• Penjelasan:</b> Merubah sticker ke gif

  <b>• Perintah:</b> <code>{0}toaudio [balas videe]</code>
  <b>• Penjelasan:</b> Merubah vidio menjadi audia mp3.

  <b>• Perintah:</b> <code>{0}efek [efek kode - nama efek]</code>
  <b>• Efek kode:</b> <code>bengek</code> <code>robot</code> <code>jedug</code> <code>fast</code> <code>echo</code>
  <b>• Penjelasan:</b> Untuk merubah suara voice note.
  
  <b>• Perintah:</b> <code>{0}curi [balas pesan]</code>
  <b>• Penjelasan:</b> Untuk mencuri media timer, cek pesan tersimpan.
"""


@PY.UBOT("toanime", SUDO=True)
async def _(client, message):
    await convert_anime(client, message)


@PY.UBOT("toimg", SUDO=True)
async def _(client, message):
    await convert_photo(client, message)


@PY.UBOT("tosticker", SUDO=True)
async def _(client, message):
    await convert_sticker(client, message)


@PY.UBOT("togif", SUDO=True)
async def _(client, message):
    await convert_gif(client, message)


@PY.UBOT("toaudio", SUDO=True)
async def _(client, message):
    await convert_audio(client, message)


@PY.UBOT("efek", SUDO=True)
async def _(client, message):
    await convert_efek(client, message)


@PY.UBOT("curi", SUDO=True)
async def _(client, message):
    await colong_cmn(client, message)
