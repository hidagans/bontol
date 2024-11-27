from time import time

from ubot import *

__MODULE__ = "afk"
__HELP__ = """
<b>『 Bantuan Untuk Afk 』</b>

  <b>• Perintah:</b> <code>{0}afk</code></code>
  <b>• Penjelasan:</b> untuk mengaktifkan afk 

  <b>• Perintah:</b> <code>{0}unafk</code></code>
  <b>• Penjelasan:</b> untuk menonaktifkan afk
"""


class AwayFromKeyboard:
    def __init__(self, client, message, reason=""):
        self.client = client
        self.message = message
        self.reason = reason

    async def set_afk(self):
        db_afk = {"time": time(), "reason": self.reason}
        msg_afk = (
            f"<b>❏ Sedang afk\n ╰ alasan: {self.reason}</b>"
            if self.reason
            else "<b>❏ Sedang afk</b>"
        )
        await set_var(self.client.me.id, "AFK", db_afk)
        await self.message.reply(msg_afk, disable_web_page_preview=True)
        return await self.message.delete()

    async def get_afk(self):
        var = await get_var(self.client.me.id, "AFK")
        if var:
            afk_time = var.get("time")
            afk_reason = var.get("reason")
            afk_runtime = await get_time(time() - afk_time)
            afk_text = (
                f"<b>❏ Sedang afk\n ├ waktu: {afk_runtime}\n ╰ alasan: {afk_reason}</b>"
                if afk_reason
                else f"<b>❏ Sedang afk\n ╰ waktu: {afk_runtime}</b>"
            )
            return await self.message.reply(afk_text, disable_web_page_preview=True)

    async def unset_afk(self):
        var = await get_var(self.client.me.id, "AFK")
        if var:
            afk_time = var.get("time")
            afk_runtime = await get_time(time() - afk_time)
            afk_text = f"<b>❏ Kembali online\n ╰ afk selama: {afk_runtime}"
            await self.message.reply(afk_text)
            await self.message.delete()
            return await remove_var(self.client.me.id, "AFK")


@PY.UBOT("afk")
async def _(client, message):
    reason = get_arg(message)
    afk_handler = AwayFromKeyboard(client, message, reason)
    await afk_handler.set_afk()


@PY.AFK(True)
async def _(client, message):
    afk_handler = AwayFromKeyboard(client, message)
    await afk_handler.get_afk()


@PY.UBOT("unafk")
async def _(client, message):
    afk_handler = AwayFromKeyboard(client, message)
    return await afk_handler.unset_afk()
