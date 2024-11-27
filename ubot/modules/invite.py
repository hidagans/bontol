from ubot import *

__MODULE__ = "invite"
__HELP__ = """
 <b>『 Bantuan untuk invite 』</b>

  <b>• Perintah:</b> <code>{0}invite [username]</code> 
  <b>• Penjelasan:</b> Untuk mengundang anggota ke grup.

  <b>• Perintah:</b> <code>{0}inviteall [username grup- cooldown - anggota]</code>
  <b>• Penjelasan:</b> Untuk mengundang anggota ke grup anda. 

  <b>• Perintah:</b> <code>{0}cancel</code>
  <b>• Penjelasan:</b> Untuk membatalkan proses anda.
  """


@PY.UBOT("invite", SUDO=True)
async def _(client, message):
    await invite_cmd(client, message)


@PY.UBOT("inviteall", SUDO=True)
async def _(client, message):
    await inviteall_cmd(client, message)


@PY.UBOT("cancel", SUDO=True)
async def _(client, message):
    await cancel_cmd(client, message)
