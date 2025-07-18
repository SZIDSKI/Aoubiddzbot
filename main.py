import requests
import time
from telegram import Bot

# إعدادات API
ETHERSCAN_API_KEY = 'S97W1NKC5K14XHZJN49WJYRJCBAY6QKCN9'
TELEGRAM_BOT_TOKEN = '7873520695:AAEk04fDzqVOeIzsLTxUIMpl8c71Jj2mfpQ'
TELEGRAM_CHAT_ID = 1253755175

# عنوان محفظة كبيرة كمثال (يمكن تغييره لاحقًا)
TARGET_ADDRESS = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'  # مثال لمحفظة Vitalik Buterin

# تهيئة البوت
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# قائمة لتتبع المعاملات السابقة
seen_tx_hashes = set()

def get_transactions():
    url = f"https://api.etherscan.io/api"
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': TARGET_ADDRESS,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'desc',
        'apikey': ETHERSCAN_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] != '1':
        print("خطأ في جلب المعاملات")
        return []

    return data['result']

def send_telegram_message(text):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

def monitor():
    print("📡 بدأ المراقبة...")
    while True:
        txs = get_transactions()
        for tx in txs:
            if tx['hash'] in seen_tx_hashes:
                continue

            seen_tx_hashes.add(tx['hash'])

            eth_value = int(tx['value']) / (10 ** 18)
            if eth_value >= 100:  # معاملات بـ100 ETH أو أكثر
                message = f"🚨 معاملة حوت جديدة:\n\n" \
                          f"📦 من: {tx['from']}\n" \
                          f"🎯 إلى: {tx['to']}\n" \
                          f"💰 القيمة: {eth_value:.2f} ETH\n" \
                          f"🔗 رابط: https://etherscan.io/tx/{tx['hash']}"
                send_telegram_message(message)
                print(f"✅ تم إرسال تنبيه: {eth_value:.2f} ETH")

        time.sleep(15)  # تحقق كل 15 ثانية

if __name__ == "__main__":
    monitor()
