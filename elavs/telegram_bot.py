import json
import emoji
import logging
import configparser
import firebase_admin

from firebase_admin import db
from firebase_admin import credentials
from dateutil.parser import parse
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters


#TODO: should be moved to external module
class ElAvailability:
    def __init__(self, event_datetime, sensor_id, status):
        self.event_datetime = event_datetime
        self.sensor_id = sensor_id
        self.status = status

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

global cred, default_app, ref, firebase_token, firebase_db_uri, firebase_collection_ref, telegram_token, telegram_user

def getLastEvents( count ):

    data = ref.order_by_key().limit_to_last(count).get()
    for key, val in data.items():
        row = json.loads(val, object_hook=lambda d: ElAvailability(**d))
        event_datetime = parse(row.event_datetime)
        formated_event_datetime = event_datetime.strftime("%d-%m-%Y %H:%M")
    if row.status == 'On':
        status_symbol = emoji.emojize(':green_heart:')
    else:
        status_symbol = emoji.emojize(':broken_heart:')
    msg = status_symbol + " Станом на " + formated_event_datetime + " електрика : " + row.status
    return msg

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, 
        text="Я телеграм бот, якій розкаже тобі, чи є зараз електрика на трансформаторі 2182!")
    await context.bot.send_message(chat_id=update.effective_chat.id, text = getLastEvents(1))

    keyboard = [
        [
            KeyboardButton("Остання подія"),
            KeyboardButton("5 останніх подій")
        ],
        [ KeyboardButton("Статистика") ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def button_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):

    match update.message.text:
        case "Остання подія":
            await context.bot.send_message(chat_id=update.effective_chat.id, text = getLastEvents(1))
        case "5 останніх подій":
            await context.bot.send_message(chat_id=update.effective_chat.id, text = "Ваша Галя балувана - хоче все і відразу!")
        case "Статистика":
            await context.bot.send_message(chat_id=update.effective_chat.id, text = "Починається ... Дочекайтесь наступного релізу!")

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
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    button_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), button_reaction)
    application.add_handler(button_handler)
    
    application.run_polling()