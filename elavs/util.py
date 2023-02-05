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
