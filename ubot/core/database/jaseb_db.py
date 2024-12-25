from ubot.core.database import db

async def get_jaseb_text():
    return await db.get("jaseb_text")

async def set_jaseb_text(text):
    await db.set("jaseb_text", text)

async def get_jaseb_interval():
    return await db.get("jaseb_interval")

async def set_jaseb_interval(interval):
    await db.set("jaseb_interval", interval)

async def get_jaseb_target():
    return await db.get("jaseb_target")

async def set_jaseb_target(target):
    await db.set("jaseb_target", target)
