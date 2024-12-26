import asyncio
import sys
from atexit import register
from pyrogram import idle
from pyrogram.errors import RPCError
from ubot import *
from ubot.core.plugins.pyn import monitor_invoices  # Pastikan import monitor_invoices

async def loader_user(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=90)
    except RPCError:
        await remove_ubot(user_id)
        await rm_all(user_id)
        await rem_expired_date(user_id)
        for X in await get_chat(user_id):
            await remove_chat(user_id, X)
        print(f"✅ {user_id} 𝗕𝗘𝗥𝗛𝗔𝗦𝗜𝗟 𝗗𝗜𝗛𝗔𝗣𝗨𝗦")
    except Exception as e:
        print(f"❌ Error occurred: {e}")

async def main():
    tasks = [
        asyncio.create_task(loader_user(int(_ubot["name"]), _ubot))
        for _ubot in await get_userbots()
    ]
    await asyncio.gather(*tasks)
    
    await bot.start()
    await asyncio.gather(loadPlugins(), installPeer(), expiredUserbots(), idle())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(monitor_invoices())
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    except Exception:
        err = traceback.format_exc()
        logging.info(err)
    finally:
        loop.stop()
        logging.info("------------------------ Stopped Services ------------------------")
#    with ThreadPoolExecutor() as pool:
#        loop.set_default_executor(pool)
