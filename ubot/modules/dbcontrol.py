from ubot import *


@PY.BOT("prem", FILTERS.GROUP)
@PY.UBOT("prem")
async def _(client, message):
    await prem_user(client, message)

@PY.BOT("trial", FILTERS.GROUP)
@PY.UBOT("trial")
async def _(client, message):
    await trial_user(client, message)

@PY.BOT("priv", FILTERS.GROUP)
@PY.UBOT("priv")
async def _(client, message):
    await bot_priv(client, message)

@PY.BOT("malihku", FILTERS.GROUP)
@PY.UBOT("malihku")
async def _(client, message):
    await add_malih(client, message)

@PY.BOT("cekmalih", FILTERS.SUDO)
@PY.UBOT("cekmalih")
async def _(client, message):
    await cek_malih(client, message)

@PY.BOT("hapusmalih", FILTERS.SUDO)
@PY.UBOT("hapusmalih")
async def _(client, message):
    await hapus_malih(client, message)

@PY.BOT("delprem", FILTERS.GROUP)
@PY.UBOT("delprem")
async def _(client, message):
    await unprem_user(client, message)


@PY.BOT("getprem", FILTERS.SUDO)
@PY.UBOT("getprem")
async def _(cliebt, message):
    await get_prem_user(client, message)


@PY.BOT("seles", FILTERS.SUDO)
@PY.UBOT("seles")
async def _(client, message):
    await seles_user(client, message)


@PY.BOT("delseles", FILTERS.SUDO)
@PY.UBOT("delseles")
async def _(client, message):
    await unseles_user(client, message)


@PY.BOT("getseles", FILTERS.SUDO)
@PY.UBOT("getseles")
async def _(client, message):
    await get_seles_user(client, message)


@PY.BOT("setexp")
@PY.UBOT("setexp")
async def _(client, message):
    await expired_add(client, message)


@PY.BOT("cek", FILTERS.GROUP)
@PY.UBOT("cek")
async def _(client, message):
    await expired_cek(client, message)


@PY.BOT("delexp", FILTERS.SUDO)
@PY.UBOT("delexp")
async def _(client, message):
    await un_expired(client, message)


@PY.CALLBACK("restart")
async def _(client, callback_query):
    await cb_restart(client, callback_query)


@PY.CALLBACK("gitpull")
async def _(client, callback_query):
    await cb_gitpull(client, callback_query)


@PY.BOT("bcast", FILTERS.SUDO)
async def _(client, message):
    await bacotan(client, message)
