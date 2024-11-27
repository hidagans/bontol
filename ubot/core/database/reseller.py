from ubot.core.database import mongodb

resell = mongodb["ubot"]["babu"]


async def get_seles():
    seles = await resell.find_one({"babu": "babu"})
    if not seles:
        return []
    return seles["reseller"]


async def get_malihku():
    malih_data = await resell.find_one({"status": "malih"})
    if not malih_data:
        return []
    return malih_data["malihku"]


async def add_seles(user_id):
    reseller = await get_seles()
    reseller.append(user_id)
    await resell.update_one(
        {"babu": "babu"}, {"$set": {"reseller": reseller}}, upsert=True
    )
    return True

async def add_malihku(user_id):
    malihnya = await get_malihku()
    malihnya.append(user_id)
    await resell.update_one(
        {"status": "malih"}, {"$set": {"malihku": malihnya}}, upsert=True
    )
    return True


async def remove_seles(user_id):
    reseller = await get_seles()
    reseller.remove(user_id)
    await resell.update_one(
        {"babu": "babu"}, {"$set": {"reseller": reseller}}, upsert=True
    )
    return True

async def buang_malih(user_id):
    malihnya = await get_seles()
    malihnya.remove(user_id)
    await resell.update_one(
        {"status": "malihku"}, {"$set": {"malihku": malihnya}}, upsert=True
    )
    return True
