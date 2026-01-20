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

# --- نمط الرسائل الجديد ---
MESSAGES = [
    "كـروب مـكـالمات جـمـاعيه بـالبـايـو نـضـمـو ✨",
    "نورنا بـكـروب مـكـالمات جـمـاعيه بـالبـايـو نـضـمـو 🎤",
    "تـعـال لـكـروب مـكـالمات جـمـاعيه بـالبـايـو نـضـمـو 🔥",
    "كـروب مـكـالمات جـمـاعيه بـالبـايـو نـضـمـو مـوجـود 🚀",
    "انـضـم لـكـروب مـكـالمات جـمـاعيه بـالبـايـو نـضـمـو 💎",
    "مـنور، كـروب مـكـالمات جـمـاعيه بـالبـايـو نـضـمـو 🌟",
    "كـروب مـكـالمات جـمـاعيه بـالبـايـو نـضـمـو حـيـاك 🎈"
]

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running")
    
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
        me = await client.get_me()
        print(f"✅ Connected as: {me.first_name}")
    except Exception as e:
        print(f"❌ Login Error: {e}")
        return

    @client.on(events.NewMessage(chats=TARGET_GROUP))
    async def handler(event):
        # تجاهل الرسائل الصادرة من حسابك
        if event.out:
            return
            
        try:
            # انتظار عشوائي (15 إلى 35 ثانية) لتبدو كأنها كتابة يدوية
            await asyncio.sleep(random.randint(15, 35))
            
            # اختيار رسالة بالنمط الجديد
            reply_text = random.choice(MESSAGES)
            await event.reply(reply_text)
            print(f"✅ Replied with new style to message in {TARGET_GROUP}")
            
            # استراحة أمان (دقيقة إلى دقيقتين)
            await asyncio.sleep(random.randint(60, 150))
        except Exception as e:
            print(f"⚠️ Skip error: {e}")

    print("🚀 Monitoring for new messages with New Style...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_health_check, daemon=True)
    web_thread.start()
    asyncio.run(start_bot())
