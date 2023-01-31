from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler

from config import TOKEN
from func import calcrun, days2NY, getweather

'''https://docs.python-telegram-bot.org/en/stable/index.html'''


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    botcommand = ['/calc выражение - математический калькулятор',
                  '/D2NY - сколько осталось до нового года',
                  '/GW - погода в Салехарде',
                  '/echo -  эхо-ответ: что получил то и послал',]

    await update.message.reply_text('Команды бота:\n{}'.format('\n'.join(botcommand)))


async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(calcrun(update.message.text.split(" ")[1]))


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'{update.message.text}')


async def day2NewYear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'{days2NY()}')


async def getweath(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'{getweather()}')


async def message_processing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text[0] !='/': 
        await update.message.reply_text('Просто текст')



app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("GW", getweath))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("calc", calc))
app.add_handler(CommandHandler("echo", echo))
app.add_handler(CommandHandler("D2NY", day2NewYear))

app.add_handler(MessageHandler(None,message_processing))

app.run_polling()
