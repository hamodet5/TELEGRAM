import asyncio
import random
import threading
import requests
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient, events
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- بيانات الحساب ---
API_ID = 38972492 
API_HASH = '59edb6a86e3f130732b8a0c64510cd40'
PHONE_NUMBER = '+9647844101857' 
TARGET_GROUP = 'stevenalbaghdadichat'

# --- بيانات بوت الإشعارات ---
BOT_TOKEN = '7394386222:AAHMuvrYSYwKplbyiAQXbfDbifbfEdztk_k'
MY_ID = '5803355350'

# --- ✍️ العودة للرسالة القديمة ---
TEXT_BASE = "مـقـاطـعي بـالـبـايـو للجادين واليـدفـعـون تعـال وتـاكد قـبـل لا تـدفـع"

EMOJIS = ["✨", "🔥", "🚀", "💎", "🌟", "👑", "🧿", "💫", "🎯", "🎭", "🎮", "🌹", "❤️", "🎧", "🎬"]
DECORATIONS = ["-", "—", "•", "~", "★", "☆"]

replied_users = set()

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running with Old Message")

def run_health_check():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

def send_notification(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": MY_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except: pass

def generate_dynamic_message():
    selected_emojis = "".join(random.sample(EMOJIS, random.randint(3, 5)))
    dec = random.choice(DECORATIONS)
    return f"{dec} {TEXT_BASE} {selected_emojis} {dec}"

async def start_bot():
    # استخدام اسم جلسة مستقر
    client = TelegramClient('High_Speed_Session_V2', API_ID, API_HASH)
    
    try:
        await client.start(phone=PHONE_NUMBER)
        send_notification("✅ **تمت العودة للرسالة القديمة!**\nالبوت يراقب المجموعة الآن...")

        @client.on(events.NewMessage(chats=TARGET_GROUP))
        async def handler(event):
            global replied_users
            if event.out: return

            user_id = event.sender_id

            # نظام الاحتمالات لتقليل الضغط في المجموعات السريعة
            if random.random() > 0.10: # معالجة 10% فقط من الرسائل لتجنب الحظر
                return

            if user_id in replied_users:
                return

            try:
                # انتظار عشوائي بسيط
                await asyncio.sleep(random.randint(7, 15))
                
                # الرد بالرسالة القديمة
                await event.reply(generate_dynamic_message())
                
                replied_users.add(user_id)
                
                # إشعار البوت
                sender = await event.get_sender()
                name = getattr(sender, 'first_name', 'User')
                send_notification(f"✅ **تم الرد بالرسالة القديمة:**\n👤 {name}\n🆔 {user_id}")
                
                # استراحة دقيقة لضمان عدم حظر الحساب
                await asyncio.sleep(60)

            except Exception as e:
                print(f"Error: {e}")

        await client.run_until_disconnected()
        
    except Exception as e:
        send_notification(f"❌ خطأ: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    asyncio.run(start_bot())
