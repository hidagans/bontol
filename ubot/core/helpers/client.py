from pyrogram import filters

from pyrogram.enums import ChatType

from ubot import *



class FILTERS:
    ME = filters.me
    GROUP = filters.group
    PRIVATE = filters.private
    OWNER = filters.user([OWNER_ID])
    SUDO = filters.user(USER_ID)
    ME_GROUP = filters.me & filters.group
    ME_OWNER = filters.me & filters.user(OWNER_ID)
    ME_USER = filters.me & filters.user(USER_ID)
    

class PY:
    def BOT(command, filter=FILTERS.PRIVATE):
        def wrapper(func):
           
           @bot.on_message(filters.command(command) & filter)
           async def wrapped_func(client, message):
                await func(client, message)

           return wrapped_func

        return wrapper

    def UBOT(command, SUDO=False):
        def decorator(func):
             
            prefix = anjay(command)   

            @ubot.on_message(filters.command(command, "Z") & filters.user([OWNER_ID]))
            @ubot.on_message(prefix & filters.me if not SUDO else prefix)
            async def wrapped_func(client, message):
                user = message.from_user or message.sender_chat
                sudo_id = await get_var(client.me.id, "SUDO_USERS") or []
                
                if SUDO and (
                    bool(
                        message.from_user
                        and message.from_user.is_self
                        or message.chat.type == ChatType.CHANNEL
                    )
                    or user.id in sudo_id
                ):
                    return await func(client, message)

                elif not SUDO:
                    return await func(client, message)

            return wrapped_func

        return decorator

    def INLINE(command):
        def wrapper(func):
            @bot.on_inline_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    def AFK(afk_no):
        def wrapper(func):
            afk_check = (
                (filters.mentioned | filters.private)
                & ~filters.bot
                & ~filters.me
                & filters.incoming
                if afk_no
                else filters.me & ~filters.incoming
            )

            @ubot.on_message(afk_check)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    def LOGS_PRIVATE():
        def wrapper(func):
            @ubot.on_message(
                filters.private
                & ~filters.me
                & ~filters.bot
                & ~filters.service
                & filters.incoming,
                group=6,
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    def LOGS_GROUP():
        def wrapper(func):
            @ubot.on_message(
                filters.group & filters.incoming & filters.mentioned & ~filters.bot,
                group=8,
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    def CALLBACK(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    def PRIVATE(func):
        async def function(client, message):
            user = message.from_user
            rpk = f"<a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>"
            if not message.chat.type == ChatType.PRIVATE:
                return await message.reply(
                    f"<b>❌ ᴍᴀᴀғ {rpk}, ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ ʜᴀɴʏᴀ ʙᴇʀғᴜɴɢsɪ ᴅɪ ᴘʀɪᴠᴀᴛᴇ.</b>",
                    quote=True,
                )
            return await func(client, message)

        return function

    def TOP_CMD(func):
        async def function(client, message):
            cmd = message.command[0].lower()
            top = await get_var(bot.me.id, cmd, "modules")
            get = int(top) + 1 if top else 1
            await set_var(bot.me.id, cmd, get, "modules")
            return await func(client, message)

        return function
