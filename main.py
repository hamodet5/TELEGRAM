import asyncio
import random
import threading
from telethon import TelegramClient, events
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- بيانات الحساب (تأكدي أنها صحيحة) ---
API_ID = 38972492 
API_HASH = '59edb6a86e3f130732b8a0c64510cd40'
PHONE_NUMBER = '+9647844101857' 
TARGET_GROUP = 'stevenalbaghdadichat'

# --- 7 خانات للرسائل (نظام الرد) ---
MESSAGES = [
    "نورت يا غالي، الكروب مالتنا بالبايو انضم لنا خل نموله ✨",
    "هلا بيك، تعال لكروب المكالمات مالتنا، الرابط خليته بالبايو عندي 🎤",
    "ياهلا نورت، موجود رابط كروب تمويل بحسابي (بالبايو) فوت لتقصر 🚀",
    "حياك الله، ممكن تنضم لكروبنا؟ الرابط موجود بوصف حسابي 🔥",
    "كفو منك، ادخل لكروبنا الرسمي، التفاصيل واليوزر بالبايو مالي 💎",
    "منور يا طيب، سوينا تجمع جديد والروابط ببروفايلي، نورنا 🌟",
    "هلا بيك، كروب التمويل والمكالمات بالبايو مالي، انضم 🎈"
]

# خادم وهمي لإبقاء الاستضافة تعمل
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active and running!")

def run_health_check():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

async def start_bot():
    # استخدام ملف السشن المرفوع
    client = TelegramClient('Render_Session', API_ID, API_HASH)
    
    try:
        await client.start(phone=PHONE_NUMBER)
        me = await client.get_me()
        print(f"✅ تم الاتصال بنجاح بواسطة الحساب: {me.first_name}")
    except Exception as e:
        print(f"❌ فشل تسجيل الدخول: {e}")
        return

    @client.on(events.NewMessage(chats=TARGET_GROUP))
    async def handler(event):
        # تجاهل الرسائل التي نرسلها نحن
        if event.out:
            return
            
        # نظام تخطي الأخطاء (للملصقات والملفات غير المدعومة)
        try:
            # انتظار عشوائي للتمويه (15 إلى 30 ثانية)
            await asyncio.sleep(random.randint(15, 30))
            
            reply_text = random.choice(MESSAGES)
            await event.reply(reply_text)
            print(f"✅ تم الرد على رسالة من: {event.sender_id}")
            
            # استراحة أمان (دقيقة إلى دقيقتين) لمنع حظر الحساب
            await asyncio.sleep(random.randint(60, 120))
            
        except Exception as e:
            # طباعة الخطأ في السجلات والاستمرار في العمل
            print(f"⚠️ حدث خطأ بسيط وتخطاه البوت: {e}")

    print("🚀 البوت الآن يراقب المجموعة بنظام الرد التلقائي...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    # تشغيل خادم الصحة في خلفية الاستضافة
    threading.Thread(target=run_health_check, daemon=True).start()
    # تشغيل البوت
    asyncio.run(start_bot())
