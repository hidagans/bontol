from ubot import *
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ubot.core.plugins.pyn import create_invoice, check_invoice_status, success_payment, failed_payment, tambah_or_kurang, confirm_callback

@PY.CALLBACK("^check_payment")
async def check_payment_callback(client, callback_query):
    invoice_id = callback_query.data.split("|")[1]
    user_id = callback_query.from_user.id
    payment_status = await check_invoice_status(invoice_id)
    
    if payment_status == 'PAID':
        await success_payment(user_id, 1)  # Default 1 bulan
        await callback_query.message.edit_text("Pembayaran berhasil! Status premium telah diberikan.")
    else:
        buttons = [
            [InlineKeyboardButton("Coba Lagi", callback_data=f"check_payment|{invoice_id}")]
        ]
        await callback_query.message.edit_text(
            "Pembayaran gagal atau belum selesai. Silakan coba lagi.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@PY.CALLBACK("kurang|tambah")
async def tambah_or_kurang_callback(client, callback_query):
    await tambah_or_kurang(client, callback_query)

@PY.CALLBACK("confirm")
async def confirm_payment_callback(client, callback_query):
    await confirm_callback(client, callback_query)
