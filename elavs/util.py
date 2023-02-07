import json
import emoji
import logging
import configparser
import firebase_admin

from firebase_admin import db
from firebase_admin import credentials
from firebase_admin.db import Reference

from dateutil.parser import parse

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from el_availability import ElAvailability
from chats import Chat


def get_last_events(ref: Reference, count: int ):

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


def get_last_event(ref: Reference):

    data = ref.order_by_key().limit_to_last(1).get()
    for key, val in data.items():
        row = json.loads(val, object_hook=lambda d: ElAvailability(**d))

    return row


def check_chat_it_at_db(ref: Reference, chat_id: int):

    logging.info("check_chat_it_at_db (%s) started...", chat_id)
    data = get_all_chats(ref)
    #TODO: It should be done in more clever way than a simple iteration
    if data is None:
        return False
    for key, val in data.items():
        chat = json.loads(val, object_hook=lambda d: Chat(**d))
        if chat.chat_id == chat_id:
            return True
        logging.info("chat_id: %s , user_name: %s", chat.chat_id, chat.user_name)
    return False


def get_all_chats(ref: Reference):

    data = ref.order_by_key().get()
    return data


def save_chat_id(ref: Reference, chat_id: int, user_name: str):

    dto = Chat(chat_id, user_name)
    rowJson = json.dumps(dto.__dict__)
    logging.info(rowJson)
    ref.push().set(rowJson)    


def create_last_event_message(ref: Reference):
    
    row = get_last_event(ref)
    event_datetime = parse(row.event_datetime)
    formated_event_datetime = event_datetime.strftime("%d-%m-%Y %H:%M")
    if row.status == 'On':
        status_symbol = emoji.emojize(':green_heart:')
    else:
        status_symbol = emoji.emojize(':broken_heart:')
    msg = status_symbol + " Станом на " + formated_event_datetime + " електрика : " + row.status
    return msg


def min_statistic(ref: Reference):

    return "Починається ... Дочекайтесь наступного релізу!"

