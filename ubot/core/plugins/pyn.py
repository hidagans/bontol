import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone
from xendit import Xendit
from ubot import *

CONFIRM_PAYMENT = []

xendit_api_key = "xnd_development_1o8Vi1YRZewXs5tmDHFt760Ifoj7g9GQy8XJCNaRQyq9jkTNWcq3OlwUl2pi7"
xendit = Xendit(api_key=xendit_api_key)

# Fungsi untuk membuat invoice
async def create_invoice(amount, user_id, payer_email):
    invoice = xendit.Invoice.create(
        amount=amount,
        description=f"Payment for user {user_id}",
        external_id=f"user_{user_id}",
        payer_email=payer_email
    )
    return invoice.invoice_url, invoice.id

# Fungsi untuk memeriksa status invoice
async def check_invoice_status(invoice_id):
    invoice = xendit.Invoice.get(invoice_id)
    return invoice.status

# Fungsi untuk menangani pembayaran sukses
async def success_payment(user_id, bulan):
    now = datetime.now(timezone("Asia/Jakarta"))
    expired = now + relativedelta(months=bulan)
    await add_prem(user_id)
    await set_expired_date(user_id, expired)
    await bot.send_message(
        user_id,
        f"""
<b>✅ Pembayaran berhasil!</b>
<b>💬 Anda sekarang adalah pengguna premium.</b>
<b>🗓️ Masa aktif: Hingga {expired.strftime('%d-%m-%Y')}</b>
        """
    )

# Fungsi untuk menangani pembayaran gagal
async def failed_payment(user_id):
    await bot.send_message(
        user_id,
        """
<b>❌ Pembayaran gagal atau kadaluarsa.</b>
<b>💬 Silakan coba lagi.</b>
        """

# Fungsi untuk menangani callback tambah/kurang bulan
async def tambah_or_kurang(client, callback_query):
    data = callback_query.data.split()
    if len(data) < 2:
        await callback_query.answer("Data callback tidak lengkap.")
        return

    BULAN = int(data[1])
    HARGA = 30  # Harga per bulan dalam ribuan
    QUERY = data[0]
    try:
        if QUERY == "kurang":
            if BULAN > 1:
                BULAN -= 1
        elif QUERY == "tambah":
            if BULAN < 12:
                BULAN += 1
        TOTAL_HARGA = HARGA * BULAN
        buttons = plus_minus(BULAN, callback_query.from_user.id)
        await callback_query.message.edit_text(
            TEXT_PAYMENT(HARGA, TOTAL_HARGA, BULAN),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception as e:
        print(f"Error in tambah_or_kurang: {e}")

async def confirm_callback(client, callback_query):
    data = callback_query.data.split()
    if len(data) < 2:
        await callback_query.answer("Data callback tidak lengkap.")
        return

    user_id = int(callback_query.from_user.id)
    get = await bot.get_users(user_id)
    try:
        # Meminta email dari pengguna
        await bot.send_message(user_id, "Silakan masukkan email Anda untuk melanjutkan pembayaran.")
        email_message = await bot.listen(user_id)
        payer_email = email_message.text

        # Mendapatkan jumlah bulan dari callback data
        bulan = int(data[1])
        amount = 30 * bulan * 1000  # Menghitung jumlah pembayaran

        # Membuat invoice
        invoice_url, invoice_id = await create_invoice(amount, user_id, payer_email)

        # Tambahkan data ke CONFIRM_PAYMENT
        CONFIRM_PAYMENT.append((user_id, (invoice_id, bulan)))

        # Kirim pesan dengan tombol Cek Invoice
        buttons = [
            [InlineKeyboardButton("✅ Cek Invoice ✅", callback_data=f"check_invoice {invoice_id}")],
            [InlineKeyboardButton("❌ Batalkan", callback_data=f"home {user_id}")],
        ]
        await callback_query.message.delete()
        await bot.send_message(
            user_id,
            f"<b>💬 Silakan lakukan pembayaran terlebih dahulu di bawah ini:\n{invoice_url}</b>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except asyncio.TimeoutError:
        # Bersihkan data dari CONFIRM_PAYMENT jika timeout
        CONFIRM_PAYMENT = [entry for entry in CONFIRM_PAYMENT if entry[0] != user_id]
        await bot.send_message(user_id, "❌ Pembatalan otomatis karena tidak ada respons.")
    except Exception as e:
        print(f"Error in confirm_callback: {e}")
        await bot.send_message(user_id, "❌ Terjadi kesalahan saat membuat invoice.")

async def check_invoice_callback(client, callback_query):
    data = callback_query.data.split()
    if len(data) < 2:
        await callback_query.answer("Data callback tidak lengkap.")
        return

    invoice_id = data[1]
    user_id = None  # Inisialisasi user_id

    # Cari user_id yang sesuai dengan invoice_id
    for uid, invoice_data in CONFIRM_PAYMENT:
        if invoice_data[0] == invoice_id:
            user_id = uid
            bulan = invoice_data[1]
            break

    if user_id is None:
        await callback_query.answer("❌ Data invoice tidak ditemukan.", show_alert=True)
        return

    try:
        status = await check_invoice_status(invoice_id)
        if status == "PAID":
            await callback_query.answer("✅ Pembayaran berhasil!", show_alert=True)
            CONFIRM_PAYMENT.remove((user_id, (invoice_id, bulan)))
            await success_payment(user_id, bulan)
        elif status in ["PENDING", "UNPAID"]:
            await callback_query.answer("❌ Pembayaran belum diterima.", show_alert=True)
        elif status == "EXPIRED":
            await callback_query.answer("❌ Invoice telah kedaluwarsa.", show_alert=True)
            CONFIRM_PAYMENT.remove((user_id, (invoice_id, bulan)))
        elif status == "FAILED":
            await callback_query.answer("❌ Pembayaran gagal.", show_alert=True)
            CONFIRM_PAYMENT.remove((user_id, (invoice_id, bulan)))
    except Exception as e:
        print(f"Error in check_invoice_callback: {e}")
        await callback_query.answer("❌ Terjadi kesalahan saat memeriksa invoice.")

# Fungsi untuk membuat tombol plus/minus
def plus_minus(query, user_id):
    button = [
        [
            InlineKeyboardButton("-1 Bulan", callback_data=f"kurang {query}"),
            InlineKeyboardButton("+1 Bulan", callback_data=f"tambah {query}"),
        ],
        [InlineKeyboardButton("✅ Konfirmasi ✅", callback_data=f"confirm {query}"),],
        [InlineKeyboardButton("❌ Batalkan ❌", callback_data=f"home {user_id}"),],
    ]
    return button

def TEXT_PAYMENT(harga, total, bulan):
    return f"""
<b>💬 Silakan melakukan pembayaran terlebih dahulu</b>

<b>🎟️ Harga per bulan: Rp {harga:,}</b>

<b>💳 Metode Pembayaran:</b>
<b>├ QRIS</b>
<b>└────•OTOMATIS PAYMENT</b>

<b>🔖 Total Harga: Rp {total:,}</b>
<b>🗓️ Total Bulan: {bulan}</b>

<b>Setelah pembayaran, klik tombol di bawah untuk konfirmasi.</b>
"""
