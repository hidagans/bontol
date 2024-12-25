from ubot.core.database import mongodb

jaseb = mongodb["ubot"]["jaseb"]

async def get_jaseb_settings(user_id):
    result = await jaseb.find_one({"_id": user_id})
    if result:
        return result.get("jaseb", "off"), result.get("text", "Pesan default"), result.get("interval", 60), result.get("targets", [])
    return "off", "Pesan default", 60, []

async def set_jaseb_settings(user_id, jaseb_status, text, interval, targets):
    await jaseb.update_one(
        {"_id": user_id},
        {"$set": {"jaseb": jaseb_status, "text": text, "interval": interval, "targets": targets}},
        upsert=True
    )
