from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from time import sleep
from config import TOKEN
from func import days2NY, engrusdict, get_aurora, getweather, logger
from game import Game
from random import randint

'''https://docs.python-telegram-bot.org/en/stable/index.html'''


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    txt = str(update.message.date.date())+' ' + \
        str(update.message.date.time())+' - ' +\
        update.message.from_user.name + ' /help (/start)'
    logger(txt, True)
    botcommand = ('/D2NY - сколько осталось до нового года',
                  '/GW - погода в Салехарде',
                  '/GAME - игра 50 спичек',
                  '/AURORA - прогноз полярных сияний',
                  '/ENG - изучение английских слов',
                  '/help - список команд')
    await update.message.reply_text('Команды бота:\n{}'.format('\n'.join(botcommand)))


async def day2NewYear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = str(update.message.date.date())+' ' + \
    str(update.message.date.time())+' - ' +\
    update.message.from_user.name + ' /D2NYT'
    logger(txt, True)
    await update.message.reply_text(f'{days2NY()}')


async def getweath(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = str(update.message.date.date())+' ' + \
    str(update.message.date.time())+' - ' +\
    update.message.from_user.name + ' /GW'
    logger(txt, True)
    await update.message.reply_text(f'{getweather()}')


async def message_processing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = str(update.message.date.date())+' ' + \
    str(update.message.date.time())+' - ' +\
    update.message.from_user.name + f' RAWTXT:{update.message.text}'
    logger(txt, True)
    """Обработка сырого текста в чате"""
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
            # ход компьютера
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
    txt = str(update.message.date.date())+' ' + \
    str(update.message.date.time())+' - ' +\
    update.message.from_user.name + ' /GAME'
    logger(txt, True)    
    """старт игры"""
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


async def getaurora(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = str(update.message.date.date())+' ' + \
    str(update.message.date.time())+' - ' +\
    update.message.from_user.name + ' /AURORA'
    logger(txt, True)
    aurora = get_aurora()
    if aurora == None:
        await update.message.reply_text('Данные не получены')
        return
    await update.message.reply_photo(aurora)


async def getruseng(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = str(update.message.date.date())+' ' + \
    str(update.message.date.time())+' - ' +\
    update.message.from_user.name + ' /ENG'
    logger(txt, True)
    await update.message.reply_text(engrusdict(), parse_mode="Markdown")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("GW", getweath))
app.add_handler(CommandHandler("AURORA", getaurora))
app.add_handler(CommandHandler("ENG", getruseng))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))
app.add_handler(CommandHandler("D2NY", day2NewYear))
app.add_handler(CommandHandler("GAME", gamestart))
app.add_handler(MessageHandler(None, message_processing))

game = Game()  # создаем игру

app.run_polling()
