from ubot.core.database import mongodb

jaseb = mongodb["ubot"]["jaseb"]

async def get_jaseb_text():
    return await jaseb.get("jaseb_text")

async def set_jaseb_text(text):
    await jaseb.set("jaseb_text", text)

async def get_jaseb_interval():
    return await jaseb.get("jaseb_interval")

async def set_jaseb_interval(interval):
    await jaseb.set("jaseb_interval", interval)

async def get_jaseb_target():
    return await jaseb.get("jaseb_target")

async def set_jaseb_target(target):
    await jaseb.set("jaseb_target", target)
