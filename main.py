import asyncio
import random
import threading
from telethon import TelegramClient, events
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- بيانات الحساب ---
API_ID = 38972492 
API_HASH = '59edb6a86e3f130732b8a0c64510cd40'
PHONE_NUMBER = '+9647844101857' 
TARGET_GROUP = 'stevenalbaghdadichat'

# --- رسائل الرد التلقائي ---
MESSAGES = [
    "نورت يا غالي، الكروب مالتنا بالبايو انضم لنا خل نموله ✨",
    "هلا بيك، تعال لكروب المكالمات مالتنا، الرابط خليته بالبايو عندي 🎤",
    "ياهلا نورت، موجود رابط كروب تمويل بحسابي (بالبايو) فوت لتقصر 🚀",
    "حياك الله، ممكن تنضم لكروبنا؟ الرابط موجود بوصف حسابي 🔥",
    "كفو منك، ادخل لكروبنا الرسمي، التفاصيل واليوزر بالبايو مالي 💎",
    "منور يا طيب، سوينا تجمع جديد والروابط ببروفايلي، نورنا 🌟",
    "هلا بيك، كروب التمويل والمكالمات بالبايو مالي، انضم 🎈"
]

# خادم وهمي لإبقاء الاستضافة تعمل 24 ساعة
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running")

def run_health_check():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

async def start_bot():
    # سيستخدم ملف السشن المرفوع لفتح الحساب مباشرة
    client = TelegramClient('Render_Session', API_ID, API_HASH)
    await client.start(phone=PHONE_NUMBER)
    print("✅ البوت متصل ومستعد للعمل!")

    @client.on(events.NewMessage(chats=TARGET_GROUP))
    async def handler(event):
        if not event.out:
            await asyncio.sleep(random.randint(15, 30))
            try:
                reply_text = random.choice(MESSAGES)
                await event.reply(reply_text)
                print("✅ تم الرد بنجاح")
                await asyncio.sleep(random.randint(60, 120))
            except Exception as e:
                print(f"Error: {e}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    asyncio.run(start_bot())
