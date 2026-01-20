import asyncioimport asyncio
import random
import threading
from telethon import TelegramClient, events
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- بيانات الحساب ---
API_ID = 38972492 
API_HASH = '59edb6a86e3f130732b8a0c64510cd40'
PHONE_NUMBER = '+9647844101857' 
TARGET_GROUP = 'stevenalbaghdadichat'

MESSAGES = [
    "نورت يا غالي، الكروب مالتنا بالبايو انضم لنا خل نموله ✨",
    "هلا بيك، تعال لكروب المكالمات مالتنا، الرابط خليته بالبايو عندي 🎤",
    "ياهلا نورت، موجود رابط كروب تمويل بحسابي (بالبايو) فوت لتقصر 🚀",
    "حياك الله، ممكن تنضم لكروبنا؟ الرابط موجود بوصف حسابي 🔥",
    "كفو منك، ادخل لكروبنا الرسمي، التفاصيل واليوزر بالبايو مالي 💎",
    "منور يا طيب، سوينا تجمع جديد والروابط ببروفايلي، نورنا 🌟",
    "هلا بيك، كروب التمويل والمكالمات بالبايو مالي، انضم 🎈"
]

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running")
    
    # إضافة دعم لطلبات HEAD لحل مشكلة UptimeRobot
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_health_check():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

async def start_bot():
    client = TelegramClient('Render_Session', API_ID, API_HASH)
    try:
        await client.start(phone=PHONE_NUMBER)
        print("✅ Connected and Monitoring...")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    @client.on(events.NewMessage(chats=TARGET_GROUP))
    async def handler(event):
        if not event.out:
            try:
                await asyncio.sleep(random.randint(15, 35))
                await event.reply(random.choice(MESSAGES))
                print(f"✅ Replied to message in {TARGET_GROUP}")
                await asyncio.sleep(random.randint(60, 150))
            except:
                pass
    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    asyncio.run(start_bot())

    print("🚀 البوت الآن يراقب المجموعة بنظام الرد التلقائي...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    # تشغيل خادم الصحة في خلفية الاستضافة
    threading.Thread(target=run_health_check, daemon=True).start()
    # تشغيل البوت
    asyncio.run(start_bot())
