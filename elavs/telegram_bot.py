import util
import logging
import configparser
import firebase_admin

from firebase_admin import db
from firebase_admin import credentials
from dateutil.parser import parse
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

global cred, default_app, ref, firebase_token, firebase_db_uri, firebase_collection_ref, telegram_token, telegram_user, reply_markup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, 
        text="Я телеграм бот, якій розкаже тобі, чи є зараз електрика на трансформаторі 2182!")
    await context.bot.send_message(chat_id=update.effective_chat.id, text = util.get_last_events(ref, 1))
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def button_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):

    match update.message.text:
        case "Остання подія":
            await context.bot.send_message(chat_id=update.effective_chat.id, text = util.create_last_event_message(ref))
        case "5 останніх подій":
            await context.bot.send_message(chat_id=update.effective_chat.id, text = "Ваша Галя балувана - хоче все і відразу!")
        case "Статистика":
            # await context.bot.send_message(chat_id=update.effective_chat.id, text = "Починається ... Дочекайтесь наступного релізу!")
            await context.bot.send_message(chat_id=update.effective_chat.id, text = util.min_statistic(ref))

def menu_setup():

    keyboard = [
        [
            KeyboardButton("Остання подія"),
            KeyboardButton("5 останніх подій")
        ],
        [ KeyboardButton("Статистика") ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    return reply_markup

if __name__ == '__main__':

    config = configparser.RawConfigParser()
    config.read('resources/telegrambot.properties')

    firebase_token = config.get('firebase', 'token')
    firebase_db_uri = config.get('firebase', 'db_uri')
    firebase_collection_ref = config.get('firebase', 'collection_ref')
    cred = credentials.Certificate(firebase_token)
    default_app = firebase_admin.initialize_app(cred, {
            'databaseURL':firebase_db_uri
            })
    ref = db.reference(firebase_collection_ref)

    telegram_token = config.get('telegram', 'token')
    application = ApplicationBuilder().token(telegram_token).build()

    reply_markup = menu_setup()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    button_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), button_reaction)
    application.add_handler(button_handler)
    
    application.run_polling()