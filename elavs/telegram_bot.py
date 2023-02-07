import util
import json
import logging
import configparser
import firebase_admin

from firebase_admin import db
from firebase_admin import credentials

from dateutil.parser import parse

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from chats import Chat

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

global cred, default_app, ref, firebase_token, firebase_db_uri, firebase_collection_ref
global telegram_token, telegram_user, reply_markup, last_status, mychat_id
global firebase_collection_chats, chat_ref, all_chats

async def check_status(context: ContextTypes.DEFAULT_TYPE):

    global last_status, mychat_id
    logging.debug("Status checking begin ...")
    event = util.get_last_event(ref)
    if event.status != last_status:
        logging.info("last_status chanbed from " + last_status + " to " + event.status)
        last_status = event.status

        for key, val in all_chats.items():
            chat = json.loads(val, object_hook=lambda d: Chat(**d))
            await context.bot.send_message(chat_id=chat.chat_id, text = util.create_last_event_message(ref))
    else:
        logging.info("last_status doesn\'t chanbed")
    logging.debug("Status checking end.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, 
        text="Я телеграм бот, якій розкаже тобі, чи є зараз електрика на трансформаторі 2182!")
    await context.bot.send_message(chat_id=update.effective_chat.id, text = util.get_last_events(ref, 1))
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):

    match update.message.text:
        case "Остання подія":
            await context.bot.send_message(chat_id=update.effective_chat.id, text = util.create_last_event_message(ref))

        case "Підписатись":
            if util.check_chat_it_at_db(chat_ref, update.effective_chat.id):
                await context.bot.send_message(chat_id=update.effective_chat.id, 
                    text = "Ви вже підписані та будете отримувати повідомлення при зміні стану живлення!")
            else:
                logging.debug("effective_chat: %s", update.effective_chat)
                util.save_chat_id(chat_ref, 
                                  update.effective_chat.id, update.effective_chat.first_name + " " + update.effective_chat.last_name)
                await context.bot.send_message(chat_id=update.effective_chat.id, 
                                               text = "Ви зареєстровані, тепер ми спробуємо надсилати вам повідомлення автоматично!")
                global all_chats
                all_chats = util.get_all_chats(chat_ref)

        case "Статистика":
            await context.bot.send_message(chat_id=update.effective_chat.id, text = util.min_statistic(ref))


def menu_setup():

    keyboard = [
        [
            KeyboardButton("Остання подія"),
            KeyboardButton("Підписатись")
        ],
        [ KeyboardButton("Статистика") ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    return reply_markup


if __name__ == '__main__':

    logging.debug("__main__ begin...")
    config = configparser.RawConfigParser()
    config.read('resources/telegrambot.properties')

    firebase_token = config.get('firebase', 'token')
    firebase_db_uri = config.get('firebase', 'db_uri')
    firebase_collection_ref = config.get('firebase', 'collection_ref')
    firebase_collection_chats = config.get('firebase', 'collection_chats')

    cred = credentials.Certificate(firebase_token)
    default_app = firebase_admin.initialize_app(cred, {
            'databaseURL':firebase_db_uri
            })
    ref = db.reference(firebase_collection_ref)

    logging.info(firebase_collection_chats)
    chat_ref = db.reference(firebase_collection_chats)
    all_chats = util.get_all_chats(chat_ref)
    logging.info(chat_ref)

    telegram_token = config.get('telegram', 'token')
    mychat_id = config.get('telegram', 'mychat_id')
    application = ApplicationBuilder().token(telegram_token).build()
    
    reply_markup = menu_setup()
    row = util.get_last_event(ref)
    last_status = row.status
    logging.debug("last status: " + last_status)

    job_minute = application.job_queue.run_repeating(check_status, interval=300, first=10)        

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    button_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), button_reaction)
    application.add_handler(button_handler)
    
    application.run_polling()