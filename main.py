import asyncio
import random
import threading
import sys
from datetime import datetime
from telethon import TelegramClient, events
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- بيانات الحساب ---
API_ID = 38972492 
API_HASH = '59edb6a86e3f130732b8a0c64510cd40'
PHONE_NUMBER = '+9647844101857' 
TARGET_GROUP = 'stevenalbaghdadichat'

# --- المكونات المتغيرة (تم توسيع الإيموجيات) ---
TEXT_BASE = "كـروب مـكـالمات جـمـاعيه بـالبـايـو نـضـمـو"
EMOJIS = [
    "✨", "🎤", "🔥", "🚀", "💎", "🌟", "🎈", "📣", "✅", "👑", "🎵", "💬", 
    "🦁", "⚡", "🌈", "🏆", "🎊", "🧿", "🎁", "🔥", "💫", "🎯", "🎭", "🎮", 
    "🦾", "🌹", "❤️", "🔥", "🎧", "🎬", "📍", "🔋", "⚠️", "🌀", "💠", "🔱"
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
    # اختيار 4 إلى 6 إيموجيات عشوائية
    selected_emojis = "".join(random.sample(EMOJIS, random.randint(4, 6)))
    dec = random.choice(DECORATIONS)
    return f"{dec} {TEXT_BASE} {selected_emojis} {dec}"

def is_sleep_time():
    """التحقق مما إذا كان الوقت الحالي بين 12 ظهراً و 1 ظهراً"""
    now = datetime.now().hour
    # يتوقف البوت إذا كانت الساعة 12 (من 12:00 إلى 12:59)
    return now == 12

async def start_bot():
    while True:
        client = TelegramClient('Render_Session', API_ID, API_HASH, 
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

                # التحقق من وقت الاستراحة الكبرى (من 12 لـ 1)
                if is_sleep_time():
                    print("💤 Sleep Mode Active (12 PM - 1 PM). Skipping...")
                    return

                if message_count < target_batch_size:
                    try:
                        # انتظار عشوائي بسيط قبل الرد
                        await asyncio.sleep(random.randint(15, 30))
                        
                        await event.reply(generate_dynamic_message())
                        message_count += 1
                        print(f"✅ Sent ({message_count}/{target_batch_size})")

                        # استراحة بين الرسائل (دقيقتين إلى 3 دقائق كما طلبتِ)
                        pause_time = random.randint(120, 180)
                        await asyncio.sleep(pause_time)
                        
                    except Exception as e:
                        print(f"⚠️ Error: {e}")
                else:
                    # استراحة بين الدفعات (5 دقائق)
                    print(f"💤 Batch complete. Waiting for next round...")
                    await asyncio.sleep(300)
                    message_count = 0
                    target_batch_size = random.randint(7, 15)

            await client.run_until_disconnected()
        except Exception as e:
            print(f"❌ Restarting due to: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        sys.exit()
