from ubot import *
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ubot.core.plugins.pyn import create_invoice, check_invoice_status, success_payment, failed_payment, tambah_or_kurang, confirm_callback

@PY.CALLBACK("^check_invoice")
async def check_payment_callback(client, callback_query):
    await check_invoice_callback(client, callback_query)

@PY.CALLBACK("kurang|tambah")
async def tambah_or_kurang_callback(client, callback_query):
    await tambah_or_kurang(client, callback_query)

@PY.CALLBACK("confirm")
async def confirm_payment_callback(client, callback_query):
    await confirm_callback(client, callback_query)
