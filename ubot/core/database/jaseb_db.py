from ubot.core.database import mongodb

jaseb = mongodb["ubot"]["jaseb"]

async def get_jaseb_text():
    result = await jaseb.find_one({"_id": "jaseb_text"})
    return result["value"] if result else None

async def set_jaseb_text(text):
    await jaseb.update_one({"_id": "jaseb_text"}, {"$set": {"value": text}}, upsert=True)

async def get_jaseb_interval():
    result = await jaseb.find_one({"_id": "jaseb_interval"})
    return result["value"] if result else None

async def set_jaseb_interval(interval):
    await jaseb.update_one({"_id": "jaseb_interval"}, {"$set": {"value": interval}}, upsert=True)

async def get_jaseb_targets():
    result = await jaseb.find_one({"_id": "jaseb_targets"})
    return result["value"] if result else []

async def set_jaseb_targets(targets):
    await jaseb.update_one({"_id": "jaseb_targets"}, {"$set": {"value": targets}}, upsert=True)
