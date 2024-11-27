from ubot.core.database import mongodb

vardb = mongodb["ubot"]["variable"]

async def set_var(bot_id, var_name, value, query="var"):
    update_data = {"$set": {f"{query}.{var_name}": value}}
    await vardb.update_one({"_id": bot_id}, update_data, upsert=True)


async def get_var(bot_id, var_name, query="var"):
    result = await vardb.find_one({"_id": bot_id})
    return result.get(query, {}).get(var_name, None) if result else None


async def remove_var(bot_id, var_name, query="var"):
    remove_data = {"$unset": {f"{query}.{var_name}": ""}}
    await vardb.update_one({"_id": bot_id}, remove_data)


async def all_var(user_id, query="var"):
    result = await vardb.find_one({"_id": user_id})
    return result.get(query) if result else None


async def remove_all_var(bot_id):
    await vardb.delete_one({"_id": bot_id})


async def get_list_from_var(user_id, var_name, query="var"):
    var_data = await get_var(user_id, var_name, query)
    return [int(x) for x in str(var_data).split()] if var_data else []


async def add_to_var(user_id, var_name, value, query="var"):
    var_list = await get_list_from_var(user_id, var_name, query)
    var_list.append(value)
    await set_var(user_id, var_name, " ".join(map(str, vars_list)), query)

async def add_to_var_jaseb(user_id, var_name, value, query="var"):
    var_list = await get_list_from_var(user_id, var_name, query)
    var_list.append(value)
    await set_var(user_id, var_name, " ".join(map(str, var_list)), query)

async def remove_from_var(user_id, var_name, value, query="var"):
    var_list = await get_list_from_var(user_id, var_name, query)
    if value in var_list:
        var_list.remove(value)
        await set_var(user_id, var_name, " ".join(map(str, var_list)), query)


async def get_pm_id(user_id):
    pm_id = await get_var(user_id, "PM_PERMIT")
    return [int(x) for x in str(pm_id).split()] if pm_id else []


async def add_pm_id(me_id, user_id):
    pm_id = await get_var(me_id, "PM_PERMIT")
    if pm_id:
        user_id = f"{pm_id} {user_id}"
    await set_var(me_id, "PM_PERMIT", user_id)


async def remove_pm_id(me_id, user_id):
    pm_id = await get_var(me_id, "PM_PERMIT")
    if pm_id:
        list_id = [int(x) for x in str(pm_id).split() if x != str(user_id)]
        await set_var(me_id, "PM_PERMIT", " ".join(map(str, list_id)))

