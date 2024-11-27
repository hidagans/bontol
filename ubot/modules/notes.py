from ubot import *

__MODULE__ = "notes"
__HELP__ = """
<b>『 Bantuan untuk notes 』</b>

  <b>• Perintah:</b> <code>{0}addnote</code> [note_name - reply]
  <b>• Penjelasan:</b> Untuk menyimpan catatan.

  <b>• Perintah:</b> <code>{0}get</code> [note_name]
  <b>• Penjelasan:</b> Untuk mendapatkan catatan yg di simpan.

  <b>• Perintah:</b> <code>{0}delnote</code> [note_name]
  <b>• Penjelasan:</b> Untuk menghapus catatan yg di simpan.

  <b>• Perintah:</b> <code>{0}notes</code>
  <b>• Penjelasan:</b> Untuk melihat daftar catatan yang disimpan.

  <b>note: Untuk menggunakan button, gunakan format:</b>
  <code>text ~> button_text: button_url</code>
"""


@PY.UBOT("addnote", SUDO=True)
@PY.TOP_CMD
async def _(client, message):
    await addnote_cmd(client, message)


@PY.UBOT("get", SUDO=True)
@PY.TOP_CMD
async def _(client, message):
    await get_cmd(client, message)


@PY.INLINE("^get_notes")
@INLINE.QUERY
async def _(client, inline_query):
    await get_notes_button(client, inline_query)


@PY.UBOT("delnote", SUDO=True)
@PY.TOP_CMD
async def _(client, message):
    await delnote_cmd(client, message)


@PY.UBOT("notes", SUDO=True)
@PY.TOP_CMD
async def _(client, message):
    await notes_cmd(client, message)
