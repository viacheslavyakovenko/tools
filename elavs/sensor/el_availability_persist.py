#!/usr/bin/python

# Start by importing the libraries we want to use

import OPi.GPIO as GPIO # This is the GPIO library we need to use the GPIO pins on the Raspberry Pi
import time # This is the time library, we need this so we can use the sleep function
import firebase_admin
import json

from firebase_admin import credentials
from firebase_admin import db
from datetime import date, datetime

class ElAvailability:
    def __init__(self, event_datetime, sensor_id, status):
        self.status = status
        self.event_datetime = event_datetime
        self.sensor_id = sensor_id


channel = 17
cred = credentials.Certificate("PLACE YOUR FIREBASE CREDENTIAL FILE LOCATION HERE")
default_app = firebase_admin.initialize_app(cred, {'databaseURL':'PLACE FIREBASE DB URI HERE'})
ref = db.reference("/electricity/availability")

def setup():
	GPIO.cleanup()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(channel, GPIO.IN)

def getStatus(signal):
    if signal:
        status = "Off"
    else:
        status =  "On"
    return status

def printlog(signal):
    status = getStatus(signal)
    print(datetime.now().isoformat() + " : 220v is " + status)

def createJson(signal):
    dto = ElAvailability(datetime.now().isoformat(), 1, getStatus(signal))
    rowJson = json.dumps(dto.__dict__)
    return rowJson

def callback(channel):
    value = GPIO.input(channel)
    print("callback called")
    printlog(value)
    dtoJson = createJson(value)
    print(dtoJson)
    ref.push().set(dtoJson)


#        print(datetime.now().isoformat() + " 220v on,  value: " + str(value))
#        row = ElAvailability(current_datetime, 1, True)
#        json = json.dumps(row.__dict__)
#        ref.push().set(json)


setup()
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=400)
GPIO.add_event_callback(channel, callback)

while True:
	# This line simply tells our script to wait 0.1 of a second, this is so the script doesnt hog all of the CPU
	time.sleep(0.5)
