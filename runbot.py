from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from time import sleep
from config import TOKEN
from func import days2NY, engrusdict, get_aurora, getweather, logger
from game import Game
from random import randint

from gameXO import GameX0

'''https://docs.python-telegram-bot.org/en/stable/index.html'''


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    txt = str(update.message.date.date())+' ' + \
        str(update.message.date.time())+' - ' +\
        update.message.from_user.name + ' /help (/start)'
    logger(txt, True)
    botcommand = ('/D - сколько осталось до нового года',
                  '/W - погода в Салехарде',
                  '/A - прогноз полярных сияний',
                  '/G1 - игра 50 спичек',
                  '/G2 - игра крестики-нолики',
                  '/GR - остановка всех игр',
                  '/E - изучение английских слов',
                  '/help(/start) - список команд')
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
        if gameX0.gamestatus:
            message = gameX0.game_step(update.message.text)
            await update.message.reply_text(message,parse_mode="Markdown")
            return


async def gamestart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if gameX0.gamestatus:
        await update.message.reply_text('вы не закончили игру крестики нолики')
        return
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


async def gameX0start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if game.gamestatus:
        await update.message.reply_text('вы не закончили игру спички')
        return
    if not gameX0.gamestatus:
        msg = gameX0.gamestart()
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text('игра уже идет')


async def game_reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    game.stop()
    gameX0.gamestop()
    await update.message.reply_text('все игры остановлены')

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("W", getweath))
app.add_handler(CommandHandler("A", getaurora))
app.add_handler(CommandHandler("E", getruseng))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))
app.add_handler(CommandHandler("D", day2NewYear))
app.add_handler(CommandHandler("G1", gamestart))
app.add_handler(CommandHandler("G2", gameX0start))
app.add_handler(CommandHandler("Gr", game_reset))

app.add_handler(MessageHandler(None, message_processing))

game = Game()  # создаем игру спички
gameX0 = GameX0()  # создаем игру крестики-нолики

app.run_polling()
