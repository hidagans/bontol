from ubot.core.database import mongodb

user = mongodb["ubot"]["sudoers"]
private = mongodb["ubot"]["sudoers"]

async def get_prem():
    prem = await user.find_one({"prem": "prem"})
    if not prem:
        return []
    return prem["list"]


async def add_prem(user_id):
    list = await get_prem()
    list.append(user_id)
    await user.update_one({"prem": "prem"}, {"$set": {"list": list}}, upsert=True)
    return True


async def remove_prem(user_id):
    list = await get_prem()
    list.remove(user_id)
    await user.update_one({"prem": "prem"}, {"$set": {"list": list}}, upsert=True)
    return True

"============================================================================================="

async def private_bot(seller_id):
    await private.update_one({"private": seller_id}, {"$inc": {"batas": -1}})
    return True

async def get_priv():
    priv = await user.find_one({"status": "private"})
    if not priv:
        return []
    return priv["list"]

async def add_priv(user_id):
    list = await get_priv()
    list.append(user_id)
    await user.update_one({"status": "private"}, {"$set": {"list": list}}, upsert=True)
    return True

async def remove_priv(user_id):
    list = await get_priv()
    list.remove(user_id)
    await user.update_one({"status": "private"}, {"$set": {"list": list}}, upsert=True)
    return True
