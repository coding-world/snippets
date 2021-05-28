#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as gpio
import MFRC522
import signal

continue_reading = True

# LED Setup
rot = 18
gruen = 23
blau = 24
gpio.setmode(gpio.BCM)
gpio.setup(rot, gpio.OUT)
gpio.setup(gruen, gpio.OUT)
gpio.setup(blau, gpio.OUT)

def ledsOff():
    gpio.output(rot, gpio.LOW)
    gpio.output(gruen, gpio.LOW)
    gpio.output(blau, gpio.LOW)


def end_read(signal,frame):
    global continue_reading
    continue_reading = False
    gpio.cleanup()

signal.signal(signal.SIGINT, end_read)

MIFAREReader = MFRC522.MFRC522()

print "Lass die LEDs leuchten! Strg+c = beenden"
while continue_reading:
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        MIFAREReader.MFRC522_SelectTag(uid)
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        if status == MIFAREReader.MI_OK:
            data = MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
            if type(data) is list:
                text = "".join(chr(x) for x in data)
                print text
                if "gruen" in text:
                    ledsOff()
                    gpio.output(gruen, gpio.HIGH)
                if "rot" in text:
                    ledsOff()
                    gpio.output(rot, gpio.HIGH)
                if "blau" in text:
                    ledsOff()
                    gpio.output(blau, gpio.HIGH)
        else:
            print "Es gab ein Fehler :("