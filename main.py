import asyncio
import random
import threading
import sys
import requests
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient, events
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- بيانات الحساب (المستخدم) ---
API_ID = 38972492 
API_HASH = '59edb6a86e3f130732b8a0c64510cd40'
PHONE_NUMBER = '+9647844101857' 
TARGET_GROUP = 'stevenalbaghdadichat'

# --- بيانات بوت الإشعارات ---
BOT_TOKEN = '7394386222:AAHMuvrYSYwKplbyiAQXbfDbifbfEdztk_k'
MY_ID = '5803355350'

# --- إعدادات الرسالة ---
TEXT_BASE = "قـنـاتـي بـالـبـايـو اريـد استـرزق منـهـا بـس اريد منـك طـلـب انـضـمام لا اكـثر وشـكـرا"
EMOJIS = ["✨", "💎", "🌟", "👑", "🧿", "💫", "🎯", "🌹", "❤️", "📍", "✅", "🙏"]
DECORATIONS = ["-", "—", "•", "~", "★", "☆"]

# قائمة الذاكرة
replied_users = set()

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Stable - Notification Mode Active")

def run_health_check():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

def send_notification(user_name, user_id):
    """إرسال إشعار لبوت التليجرام الخاص بكِ"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        text = (f"✅ تم الرد على شخص جديد:\n\n"
                f"👤 الاسم: {user_name}\n"
                f"🆔 الآيدي: {user_id}\n"
                f"🔗 الرابط: [اضغط هنا](tg://user?id={user_id})")
        payload = {"chat_id": MY_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(url, json=payload)
    except Exception as e:
        print(f"⚠️ خطأ في إرسال الإشعار: {e}")

def generate_dynamic_message():
    selected_emojis = "".join(random.sample(EMOJIS, random.randint(4, 6)))
    dec = random.choice(DECORATIONS)
    return f"{dec} {TEXT_BASE} {selected_emojis} {dec}"

def is_sleep_time():
    """توقيت العراق (GMT+3) - استراحة من 12 ظهراً لـ 1 ظهراً"""
    baghdad_time = datetime.now(timezone.utc) + timedelta(hours=3)
    return baghdad_time.hour == 12

async def start_bot():
    client = TelegramClient('Render_Session', API_ID, API_HASH)
    
    while True:
        try:
            await client.start(phone=PHONE_NUMBER)
            print("✅ البوت يعمل.. سيتم إرسال الإشعارات إليكِ فوراً.")

            @client.on(events.NewMessage(chats=TARGET_GROUP))
            async def handler(event):
                global replied_users
                if event.out or is_sleep_time(): return
                
                user_id = event.sender_id
                
                if user_id in replied_users:
                    return

                try:
                    # جلب بيانات الشخص
                    sender = await event.get_sender()
                    user_name = getattr(sender, 'first_name', 'مستخدم بدون اسم')

                    # انتظار عشوائي
                    await asyncio.sleep(random.randint(15, 30))
                    
                    # إرسال الرد
                    await event.reply(generate_dynamic_message())
                    
                    # إضافة الشخص للقائمة
                    replied_users.add(user_id)
                    
                    # إرسال إشعار لبوتك الخاص
                    send_notification(user_name, user_id)
                    
                    print(f"✅ تم الرد على {user_name} وإشعار البوت.")
                    
                    # استراحة 2-3 دقائق
                    await asyncio.sleep(random.randint(120, 180))
                    
                except Exception as e:
                    print(f"⚠️ خطأ: {e}")

            await client.run_until_disconnected()
        except Exception as e:
            print(f"❌ خطأ اتصال: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass

