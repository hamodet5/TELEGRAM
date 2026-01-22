import asyncio
import random
import threading
import sys
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient, events
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- بيانات الحساب ---
API_ID = 38972492 
API_HASH = '59edb6a86e3f130732b8a0c64510cd40'
PHONE_NUMBER = '+9647844101857' 
TARGET_GROUP = 'stevenalbaghdadichat'

# --- ✍️ نص الرسالة الجديد ---
TEXT_BASE = "قـنـاتـي بـالـبـايـو اريـد استـرزق منـهـا بـس اريد منـك طـلـب انـضـمام لا اكـثر وشـكـرا"

EMOJIS = ["✨", "💎", "🌟", "👑", "🧿", "💫", "🎯", "🌹", "❤️", "📍", "✅", "🎈", "🙏", "🌸"]
DECORATIONS = ["-", "—", "•", "~", "★", "☆", "«", "»"]

# قائمة ذاكرة لحفظ الأشخاص الذين تم الرد عليهم
replied_users = set()

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Stable - Text Only Mode")

def run_health_check():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

def generate_dynamic_message():
    """توليد رسالة بزخرفة وإيموجيات متغيرة لكسر نمط النظام"""
    selected_emojis = "".join(random.sample(EMOJIS, random.randint(4, 6)))
    dec = random.choice(DECORATIONS)
    return f"{dec} {TEXT_BASE} {selected_emojis} {dec}"

def is_sleep_time():
    """توقيت العراق (GMT+3) - استراحة من 12 ظهراً لـ 1 ظهراً"""
    baghdad_time = datetime.now(timezone.utc) + timedelta(hours=3)
    return baghdad_time.hour == 12

async def start_bot():
    # تأكدي من وجود ملف Render_Session.session في GitHub
    client = TelegramClient('Render_Session', API_ID, API_HASH)
    
    while True:
        try:
            await client.start(phone=PHONE_NUMBER)
            print("✅ البوت يعمل بنظام الرسالة النصية (الرد لمرة واحدة)...")

            @client.on(events.NewMessage(chats=TARGET_GROUP))
            async def handler(event):
                global replied_users
                # تجاهل رسائل البوت ووقت النوم
                if event.out or is_sleep_time(): 
                    return
                
                user_id = event.sender_id
                
                # فحص إذا كان المستخدم مسجلاً مسبقاً في القائمة
                if user_id in replied_users:
                    return

                try:
                    # انتظار عشوائي لتبدو الحركة طبيعية (15-30 ثانية)
                    await asyncio.sleep(random.randint(15, 30))
                    
                    # إرسال الرد النصي
                    await event.reply(generate_dynamic_message())
                    
                    # إضافة الشخص للقائمة لكي لا يتم الرد عليه مجدداً
                    replied_users.add(user_id)
                    print(f"✅ تم الرد على {user_id} بنجاح.")
                    
                    # استراحة بين الردود لحماية الحساب (2-3 دقائق)
                    await asyncio.sleep(random.randint(120, 180))
                    
                except Exception as e:
                    print(f"⚠️ خطأ أثناء الرد: {e}")

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
