import logging
import firebase_admin
import json
from firebase_admin import credentials
from firebase_admin import db
from datetime import date, datetime
from dateutil.parser import parse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup
from el_availability import ElAvailability

from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

global cred 
global default_app 
global ref 

cred = credentials.Certificate("/home/vaclav/prj/u-sensor-not-repo/petprj-firebase-adminsdk-m9fp4-e509ecc234.json")
default_app = firebase_admin.initialize_app(cred, {
		'databaseURL':'https://petprj-default-rtdb.firebaseio.com/'
		})

ref = db.reference("/electricity/availability/")

def getLastEvents( count ):
    data = ref.order_by_key().limit_to_last(count).get()
    print(data)
    for key, val in data.items():
        row = json.loads(val, object_hook=lambda d: ElAvailability(**d))
        event_datetime = parse(row.event_datetime)
        formated_event_datetime = event_datetime.strftime("%d-%m-%Y %H:%M")
        print(row.event_datetime, row.status)
    msg = "Станом на " + formated_event_datetime + " електрика : " + row.status
    return msg

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, 
        text="Я телеграм бот, якій розкаже тобі, чи є зараз електрика на трансформаторі 2182!")
    await context.bot.send_message(chat_id=update.effective_chat.id, text = getLastEvents(1))

    # keyboard = [
    #     [
    #         InlineKeyboardButton("Станом на зараз", callback_data="1"),
    #         InlineKeyboardButton("Останні 5 подій", callback_data="5"),
    #     ],
    #     [InlineKeyboardButton("Статистика", callback_data="stat")],
    # ]

    # reply_markup = InlineKeyboardMarkup(keyboard)

    keyboard = [
        [
            KeyboardButton("1", callback_data="1"),
            KeyboardButton("5", callback_data="5")
        ],
        [ KeyboardButton("stat") ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    match query.data:
        case "1":
            await context.bot.send_message(chat_id=update.effective_chat.id, text = getLastEvents(1))
        case "5":
            await context.bot.send_message(chat_id=update.effective_chat.id, text = "Ваша Галя балувана - хоче все і відразу!")
        case stat:
            await context.bot.send_message(chat_id=update.effective_chat.id, text = "Починається ... Дочекайтесь наступного релізу!")

if __name__ == '__main__':
    application = ApplicationBuilder().token('PLACE TELEGRAM BOT TOKEN HERE').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()
