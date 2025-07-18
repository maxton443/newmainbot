from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
import json
import os

ADMIN_ID = 6194108258  # 🔴 এখানেই তোমার Telegram numeric user ID বসাও

USER_FILE = "users.json"

# ইউজার ডেটা লোড
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

# ইউজার ডেটা সেভ
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# /start হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    users = load_users()

    is_new_user = user_id not in users

    if is_new_user:
        users[user_id] = {
            "name": user.full_name,
            "username": user.username,
            "joined": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_users(users)

        total_users = len(users)
        message = (
            f"✅ New User Joined\n"
            f"👤 Name: {user.full_name}\n"
            f"🆔 Username: @{user.username or 'None'}\n"
            f"📅 Join Date: {users[user_id]['joined']}\n"
            f"👥 Total Users: {total_users}"
        )

        await context.bot.send_message(chat_id=ADMIN_ID, text=message)

    await update.message.reply_text("👋 হ্যালো! আপনি বট শুরু করেছেন!")

# মেইন ফাংশন
if __name__ == "__main__":
    import asyncio
    import os
    TOKEN = "8160778255:AAFkAv4cWQ3UHUFsGVindhijYi3XPmoE40M"  # GitHub Secrets থেকে নেবে

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    asyncio.run(app.run_polling())
