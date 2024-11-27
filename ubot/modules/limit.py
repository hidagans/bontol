from ubot import *

__MODULE__ = "limit"
__HELP__ = """
 <b>『 Bantuan untuk limit 』</b>
 
  <b>• Perintah:</b> <code>{0}limit<code>
  <b>• Penjelasan:</b> Untuk mengecek batas limit akun anda.
"""


@PY.UBOT("limit", SUDO=True)
@ubot.on_message(filters.user(USER_ID) & filters.command("limit", "K") & ~filters.me)
async def _(client, message):
    await limit_cmd(client, message)
