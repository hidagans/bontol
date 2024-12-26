import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone
from xendit import Xendit
from ubot import *

PENDING_PAYMENTS = []

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
    )

# Fungsi untuk memantau invoice
async def monitor_invoices():
    while True:
        print(f"Type of PENDING_PAYMENTS: {type(PENDING_PAYMENTS)}")
        for user_id, invoice_data in list(PENDING_PAYMENTS):
            invoice_id, bulan = invoice_data
            status = await check_invoice_status(invoice_id)
            if status == "PAID":
                await success_payment(user_id, bulan)
                PENDING_PAYMENTS.remove((user_id, invoice_data))
            elif status in ["EXPIRED", "FAILED"]:
                await failed_payment(user_id)
                PENDING_PAYMENTS.remove((user_id, invoice_data))
        await asyncio.sleep(60)  # Cek setiap 1 menit

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
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    PENDING_PAYMENTS.append((get.id, (data[1], 1)))  # Menambahkan tuple dengan bulan default 1
    try:
        button = [[InlineKeyboardButton("❌ Batalkan", callback_data=f"home {user_id}")]]
        
        # Meminta email dari pengguna
        await bot.send_message(user_id, "Silakan masukkan email Anda untuk melanjutkan pembayaran.")
        email_message = await bot.listen(user_id)
        payer_email = email_message.text
        
        # Mendapatkan jumlah bulan dari callback data
        bulan = int(data[1])
        amount = 30 * bulan * 1000  # Menghitung jumlah pembayaran
        
        # Membuat invoice
        invoice_url, invoice_id = await create_invoice(amount, user_id, payer_email)
        
        await callback_query.message.delete()
        pesan = await bot.ask(
            user_id,
            f"<b>💬 Silakan lakukan pembayaran terlebih dahulu di bawah ini\n {invoice_url}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=300,
        )
    except asyncio.TimeoutError as out:
        if get.id in PENDING_PAYMENTS:
            PENDING_PAYMENTS.remove((get.id, (data[1], 1)))
            return await bot.send_message(get.id, "Pembatalan otomatis.")

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

# Fungsi untuk menampilkan teks pembayaran
def TEXT_PAYMENT(harga, total, bulan):
    return f"""
<b>💬 Silahkan melakukan pembayaran terlebih dahulu</b>

<b>🎟️ Harga perbulan: {harga}.000</b>

<b>💳 Metode Pembayaran:</b>
<b>├ QRIS</b>
<b>└────•OTOMATIS PAYMENT</b>

<b>🔖 Total Harga: Rp {total}.000</b>
<b>🗓️ Total Bulan: {bulan}</b>

<b>Setelah pembayaran, silakan klik tombol di bawah untuk melakukan konfirmasi.</b>
"""
