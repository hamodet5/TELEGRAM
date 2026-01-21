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

# --- المكونات المتغيرة ---
TEXT_BASE = "مـقـاطـعي بـالـبـايـو للجادين واليـدفـعـون تعـال وتـاكد قـبـل لا تـدفـع"
EMOJIS = [
    "✨", "🎤", "🔥", "🚀", "💎", "🌟", "🎈", "📣", "✅", "👑", "🎵", "💬", 
    "🦁", "⚡", "🌈", "🏆", "🎊", "🧿", "🎁", "💫", "🎯", "🎭", "🎮", 
    "🦾", "🌹", "❤️", "🎧", "🎬", "📍", "🔋", "⚠️", "🌀", "💠", "🔱"
]
DECORATIONS = ["-", "—", "•", "~", "_", "★", "☆", "¤", "«", "»"]

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Stable - Anti-Ban Mode")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_health_check():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

def generate_dynamic_message():
    """توليد رسالة بإيموجيات كثيرة ومتغيرة"""
    selected_emojis = "".join(random.sample(EMOJIS, random.randint(4, 6)))
    dec = random.choice(DECORATIONS)
    return f"{dec} {TEXT_BASE} {selected_emojis} {dec}"

def is_sleep_time():
    """التحقق بتوقيت العراق (GMT+3)"""
    # تحويل وقت السيرفر إلى توقيت العراق
    baghdad_time = datetime.now(timezone.utc) + timedelta(hours=3)
    # يتوقف البوت إذا كانت الساعة 12 ظهراً بتوقيت بغداد
    return baghdad_time.hour == 12

async def start_bot():
    while True:
        client = TelegramClient('New_Session_V2', API_ID, API_HASH, 
                                connection_retries=None, 
                                retry_delay=5)
        try:
            await client.start(phone=PHONE_NUMBER)
            print("✅ Connected! System Monitoring...")

            message_count = 0
            target_batch_size = random.randint(7, 15)

            @client.on(events.NewMessage(chats=TARGET_GROUP))
            async def handler(event):
                nonlocal message_count, target_batch_size
                if event.out: return

                # فحص وقت النوم (12 ظهراً - 1 ظهراً بتوقيت العراق)
                if is_sleep_time():
                    return

                if message_count < target_batch_size:
                    try:
                        await asyncio.sleep(random.randint(15, 30))
                        await event.reply(generate_dynamic_message())
                        message_count += 1
                        print(f"✅ Sent ({message_count}/{target_batch_size})")

                        # استراحة 2-3 دقائق بين الرسائل
                        await asyncio.sleep(random.randint(120, 180))
                        
                    except Exception as e:
                        print(f"⚠️ Error: {e}")
                else:
                    # استراحة 5 دقائق بعد انتهاء الدفعة
                    await asyncio.sleep(300)
                    message_count = 0
                    target_batch_size = random.randint(7, 15)

            await client.run_until_disconnected()
        except Exception as e:
            print(f"❌ Restarting: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
