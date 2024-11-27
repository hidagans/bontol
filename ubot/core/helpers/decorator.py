import asyncio
import logging
from pyrogram.enums import ChatType
from pyrogram.errors import RPCError, FloodWait, PersistentTimestampOutdated
from ubot import OWNER_ID, bot, ubot

logging.basicConfig(level=logging.DEBUG)

async def install_my_peer(client):
    users = []
    groups = []
    limit = 100  # Jumlah dialog yang diambil per permintaan

    try:
        # Ambil dialog dengan limit menggunakan async for loop
        async for dialog in client.get_dialogs(limit=limit):
            # Pastikan dialog.chat tidak None
            if dialog.chat:
                if dialog.chat.type == "private":
                    users.append(dialog.chat.id)
                elif dialog.chat.type in ("group", "supergroup"):
                    try:
                        # Coba akses pesan grup
                        await client.get_messages(dialog.chat.id, limit=1)  # Coba akses pesan pertama
                        groups.append(dialog.chat.id)
                    except Exception as e:
                        # Cek jika ini adalah kesalahan terkait akses
                        if 'CHANNEL_PRIVATE' in str(e):
                            logging.warning(f"Cannot access group {dialog.chat.id} (CHANNEL_PRIVATE): {e}")
                        else:
                            logging.error(f"Error accessing group {dialog.chat.id}: {e}")

        # Menyimpan data peer
        client._get_my_peer[client.me.id] = {"pm": users, "gc": groups}
        logging.info(f"Successfully installed peers for {client.me.id}")

    except Exception as e:
        logging.error(f"Failed to install peers for {client.me.id}: {e}")

# Fungsi utama untuk mengeksekusi tugas
async def installPeer():
    tasks = [install_my_peer(client) for client in ubot._ubot]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Logging hasil
    for result in results:
        if isinstance(result, Exception):
            logging.error(f"An error occurred: {result}")

    await bot.send_message(OWNER_ID, "✅ Berhasil Menginstall Data Pengguna")


async def safe_invoke(client, query, retries=3):
    for attempt in range(retries):
        try:
            return await client.invoke(query)
        except FloodWait as e:
            logging.warning(f"Rate limit exceeded. Waiting for {e.x} seconds...")
            await asyncio.sleep(e.x)
        except RPCError as e:
            logging.error(f"RPC error: {e}. Retrying...")
            await asyncio.sleep(1)
        except OSError as e:
            logging.error(f"OS error: {e}. Retrying...")
            await asyncio.sleep(1)
        except PersistentTimestampOutdated as e:
            logging.error(f"Persistent timestamp outdated. Waiting for 60 seconds...")
            await asyncio.sleep(60)
        except Exception as e:
            logging.error(f"Unexpected error: {e}. Retrying...")
            await asyncio.sleep(1)
    raise RuntimeError("All retry attempts failed.")
