from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال على Render!")

app = ApplicationBuilder().token("7873520695:AAEk04fDzqVOeIzsLTxUIMpl8c71Jj2mfpQ").build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
