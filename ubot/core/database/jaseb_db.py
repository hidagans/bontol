from ubot.core.database import mongodb

async def get_jaseb_text():
    return await mongodb.get("jaseb_text")

async def set_jaseb_text(text):
    await mongodb.set("jaseb_text", text)

async def get_jaseb_interval():
    return await mongodb.get("jaseb_interval")

async def set_jaseb_interval(interval):
    await mongodb.set("jaseb_interval", interval)

async def get_jaseb_target():
    return await mongodb.get("jaseb_target")

async def set_jaseb_target(target):
    await mongodb.set("jaseb_target", target)
