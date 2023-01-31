from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from time import sleep
from config import TOKEN
from func import calcrun, days2NY, getweather
from game import Game
from random import randint

'''https://docs.python-telegram-bot.org/en/stable/index.html'''


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    botcommand = ['/calc выражение - математический калькулятор',
                  '/D2NY - сколько осталось до нового года',
                  '/GW - погода в Салехарде',
                  '/echo -  эхо-ответ: что получил то и послал',
                  '/GAME - игра 50 спичек']

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
    if update.message.text[0] != '/':
        if game.gamestatus:
            # запущена игра
            # ход игрока
            try:
                matches = int(update.message.text)
            except:
                await update.message.reply_text('Я не понял ваш ответ. Напишите цифрой, сколько вы берете спичек.')
                return
            if not 0 < matches < 9:
                await update.message.reply_text('можно брать только от 1 до 8 спичек')
                return
            game.action_player(matches)
            if game.check_game_state():
                await update.message.reply_text('Поздравляю вас, вы выиграли')
                game.stop()
                return
            message = f'На столе {game.heap} спичек.'
            await update.message.reply_text(message)
            sleep(1)
            message = f'Я взял {game.action_cpu()} спичек\n'
            await update.message.reply_text(message)
            message = f'На столе {game.heap} спичек.'
            await update.message.reply_text(message)
            sleep(1)
            if game.check_game_state():
                message = f'Я выиграл'
                await update.message.reply_text(message)
                game.stop()
                return
            message = 'Ваш ход'
            await update.message.reply_text(message)
            return

async def gamestart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not game.gamestatus:
        game.start()
        message = game.help
        await update.message.reply_text(message)
        message = f'Игра началась.\nНа столе {game.heap} спичек\n'

        if randint(1, 100) > 50:
            message = 'Я хожу первый\n'
            message += f'Я взял {game.action_cpu()}\n'
            message += f'Осталось {game.heap}\nВаш ход'
            await update.message.reply_text(message)
        else:
            message = 'Ваш ход'
            await update.message.reply_text(message)


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("GW", getweath))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("calc", calc))
app.add_handler(CommandHandler("echo", echo))
app.add_handler(CommandHandler("D2NY", day2NewYear))
app.add_handler(CommandHandler("GAME", gamestart))

app.add_handler(MessageHandler(None, message_processing))

game = Game()


app.run_polling()
