import asyncio
import random
import threading
import requests
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient, events
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- الإعدادات الأساسية ---
API_ID = 38972492 
API_HASH = '59edb6a86e3f130732b8a0c64510cd40'
PHONE_NUMBER = '+9647844101857' 
TARGET_GROUP = 'stevenalbaghdadichat'

BOT_TOKEN = '7394386222:AAHMuvrYSYwKplbyiAQXbfDbifbfEdztk_k'
MY_ID = '5803355350'

TEXT_BASE = "قـنـاتـي بـالـبـايـو اريـد استـرزق منـهـا بـس اريد منـك طـلـب انـضـمام لا اكـثر وشـكـرا"
EMOJIS = ["✨", "💎", "🌟", "👑", "🧿", "💫", "🎯", "🌹", "❤️", "✅", "🙏"]

# قائمة المستخدمين الذين تم الرد عليهم
replied_users = set()

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hyper-Active Group Mode Active")

def run_health_check():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

def send_notification(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": MY_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except: pass

async def start_bot():
    # اسم جلسة جديد لضمان تحديث الاتصال
    client = TelegramClient('High_Speed_Session', API_ID, API_HASH)
    
    try:
        await client.start(phone=PHONE_NUMBER)
        send_notification("⚡ **تم تشغيل وضع السرعة القصوى!**\nالمجموعة مستهدفة والردود تعمل...")

        # استخدام عامل تصفية (Sequential) لتقليل الضغط على المعالج
        @client.on(events.NewMessage(chats=TARGET_GROUP))
        async def handler(event):
            global replied_users
            
            # تجاهل الرسائل الصادرة من حسابك
            if event.out: return

            user_id = event.sender_id

            # 1. نظام "التخطي الذكي": الرد فقط على رسالة واحدة من كل 20 رسالة لتقليل الضغط
            if random.random() > 0.05: # يقلل معالجة الرسائل بنسبة 95%
                return

            # 2. فحص إذا تم الرد عليه مسبقاً
            if user_id in replied_users:
                return

            try:
                # رد سريع مع انتظار عشوائي بسيط جداً
                await asyncio.sleep(random.randint(5, 10))
                await event.reply(f"{random.choice(EMOJIS)} {TEXT_BASE} {random.choice(EMOJIS)}")
                
                replied_users.add(user_id)
                
                # جلب الاسم وإرسال إشعار
                sender = await event.get_sender()
                name = getattr(sender, 'first_name', 'User')
                send_notification(f"✅ **رد جديد في المجموعة:**\n👤 {name}\n🆔 {user_id}")
                
                # استراحة إجبارية للبوت ليتنفس (دقيقة كاملة) بعد كل رد ناجح
                await asyncio.sleep(60)

            except Exception as e:
                print(f"Error: {e}")

        await client.run_until_disconnected()
        
    except Exception as e:
        send_notification(f"❌ توقف البوت: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    asyncio.run(start_bot())
