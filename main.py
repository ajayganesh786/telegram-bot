# main.py

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler, Application
)
import asyncio

# Bot token and admin chat ID
BOT_TOKEN = "8032316187:AAE3J2IrFvQkI-vIgxtB2WoRadDozfx845g"
admin_chat_id = 1136279013

# Conversation steps
ITEM, QUANTITY, NAME, PHONE = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""👋 Welcome to AV Fruits & Veggies Bot! 🍅🍍🧅

🚛 Fresh farm veggies & fruits at your doorstep.

🧾 Available Commands:
👉 /order – Place your order
👉 /price – Today's price list
👉 /location – Truck location today
👉 /contact – Call or WhatsApp us

Start now with /order""")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""📊 Today's Price List:
🍅 Tomato: ₹22/kg
🍍 Pineapple: ₹70/piece
🧅 Onion: ₹35/kg
🍈 Papaya: ₹50/kg""")

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📍 Our truck is located at Anna Nagar, near Kora Food Street.")

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 Contact us on WhatsApp: 9360409987")

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛒 What item(s) would you like to order?")
    return ITEM

async def get_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['items'] = update.message.text
    await update.message.reply_text("📦 How much quantity do you want?")
    return QUANTITY

async def get_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['quantity'] = update.message.text
    await update.message.reply_text("👤 Please enter your name:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("📱 Please enter your mobile number:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("✅ Order received! Thank you!")

    message = f"""🧾 New Order Received!
Item: {context.user_data['items']}
Quantity: {context.user_data['quantity']}
Customer Name: {context.user_data['name']}
Phone Number: {context.user_data['phone']}"""

    await context.bot.send_message(chat_id=admin_chat_id, text=message)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Order cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("order", order)],
        states={
            ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_item)],
            QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_quantity)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("location", location))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(conv_handler)

    print("✅ Bot is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()  # Keep the bot alive

# Required for Render (entry point)
if __name__ == "__main__":
    asyncio.run(main())
