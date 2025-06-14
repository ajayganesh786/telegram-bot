import os
import asyncio
from aiohttp import web
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes
)

# --- Bot credentials ---
BOT_TOKEN = "8032316187:AAE3J2IrFvQkI-vIgxtB2WoRadDozfx845g"
ADMIN_CHAT_ID = "1136279013"  # Replace with your real Telegram ID

# --- Bot command handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🍎 Welcome to *AV Fruits & Veggies*!\n\n"
        "You can:\n"
        "• Type /menu to see our price list 📋\n"
        "• Type /location to know our truck location 📍\n"
        "• Type /contact to get in touch 📞\n"
        "• Or *just send your order* (name, phone, items, quantity)\n\n"
        "_We’ll confirm your order shortly!_",
        parse_mode="Markdown"
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 *Today's Price List:*\n"
        "🍅 Tomato – ₹20/kg\n"
        "🧅 Onion – ₹25/kg\n"
        "🍍 Pineapple – ₹40/pc\n"
        "🍈 Papaya – ₹30/kg",
        parse_mode="Markdown"
    )

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚚 *Today's Truck Location:*\nNear Central Market, Town Square.",
        parse_mode="Markdown"
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 *Contact Us:*\nPhone: 9876543210\nTelegram: @avfruits_bot",
        parse_mode="Markdown"
    )

async def forward_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_text = update.message.text
    user = update.message.from_user
    name = user.first_name or "Unknown"
    username = f"@{user.username}" if user.username else "(no username)"

    # Format message to admin
    message = (
        f"📦 *New Order Received!*\n"
        f"👤 From: {name} {username}\n"
        f"📝 Order:\n{order_text}"
    )

    # Send to admin
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message, parse_mode="Markdown")
    await update.message.reply_text("✅ *Order received!* We will contact you soon.", parse_mode="Markdown")

# --- Background HTTP server (for Render) ---

async def handle_root(request):
    return web.Response(text="✅ Bot is running.")

async def main():
    # Start Telegram bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("location", location))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_order))

    # Start web server (keep-alive for Render)
    web_app = web.Application()
    web_app.router.add_get("/", handle_root)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8080)))
    await site.start()

    print("✅ Web server started. Starting bot polling...")
    
    # Start bot polling (non-blocking)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Run forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
