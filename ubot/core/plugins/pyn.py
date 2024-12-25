import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone
from xendit import Xendit

CONFIRM_PAYMENT = []

xendit_api_key = "YOUR_XENDIT_API_KEY"
xendit = Xendit(api_key=xendit_api_key)

# Fungsi untuk membuat invoice
async def create_invoice(amount, user_id):
    invoice = xendit.Invoice.create(
        amount=amount * 1000,  # Konversi ke format IDR
        description=f"Payment for user {user_id}",
        external_id=f"user_{user_id}_{datetime.now().timestamp()}",
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
        for user_id, invoice_data in list(CONFIRM_PAYMENT):
            invoice_id, bulan = invoice_data
            status = await check_invoice_status(invoice_id)
            if status == "PAID":
                await success_payment(user_id, bulan)
                CONFIRM_PAYMENT.remove((user_id, invoice_data))
            elif status in ["EXPIRED", "FAILED"]:
                await failed_payment(user_id)
                CONFIRM_PAYMENT.remove((user_id, invoice_data))
        await asyncio.sleep(60)  # Cek setiap 1 menit

# Fungsi untuk menangani callback tambah/kurang bulan
async def tambah_or_kurang(client, callback_query):
    BULAN = int(callback_query.data.split()[1])
    HARGA = 30  # Harga per bulan dalam ribuan
    QUERY = callback_query.data.split()[0]
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

# Fungsi untuk memproses pembayaran
async def confirm_callback(client, callback_query):
    user_id = callback_query.from_user.id
    bulan = int(callback_query.data.split()[1])
    try:
        invoice_url, invoice_id = await create_invoice(30 * bulan, user_id)
        CONFIRM_PAYMENT.append((user_id, (invoice_id, bulan)))
        buttons = [[InlineKeyboardButton("❌ Batalkan", callback_data=f"home {user_id}")]]
        await callback_query.message.edit_text(
            f"""
<b>💬 Silahkan lakukan pembayaran melalui tautan berikut:</b>
{invoice_url}

<b>🗓️ Masa aktif: {bulan} bulan</b>
<b>🔖 Total: Rp {30 * bulan}.000</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception as e:
        print(f"Error in confirm_callback: {e}")

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
