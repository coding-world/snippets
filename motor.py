#!/usr/bin/env python
# coding: utf8
# -*- coding: utf-8 -*-
from time import sleep
import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#Pins am Rapberry Pi
A=22
B=23
C=24
D=25
steps=int(sys.argv[1])
time = 0.001


# Pins sind Ausgänge
GPIO.setup(A,GPIO.OUT)
GPIO.setup(B,GPIO.OUT)
GPIO.setup(C,GPIO.OUT)
GPIO.setup(D,GPIO.OUT)
GPIO.output(A, False)
GPIO.output(B, False)
GPIO.output(C, False)
GPIO.output(D, False)

# Schritte 1 bis 8 definieren
def Step1():
    GPIO.output(D, True)
    sleep (time)
    GPIO.output(D, False)

def Step2():
    GPIO.output(D, True)
    GPIO.output(C, True)
    sleep (time)
    GPIO.output(D, False)
    GPIO.output(C, False)

def Step3():
    GPIO.output(C, True)
    sleep (time)
    GPIO.output(C, False)

def Step4():
    GPIO.output(B, True)
    GPIO.output(C, True)
    sleep (time)
    GPIO.output(B, False)
    GPIO.output(C, False)

def Step5():
    GPIO.output(B, True)
    sleep (time)
    GPIO.output(B, False)

def Step6():
    GPIO.output(A, True)
    GPIO.output(B, True)
    sleep (time)
    GPIO.output(A, False)
    GPIO.output(B, False)

def Step7():
    GPIO.output(A, True)
    sleep (time)
    GPIO.output(A, False)

def Step8():
    GPIO.output(D, True)
    GPIO.output(A, True)
    sleep (time)
    GPIO.output(D, False)
    GPIO.output(A, False)


# Volle Umdrehung    
for i in range (steps):    
    
    Step8()
    Step7()
    Step6()
    Step5()
    Step4()
    Step3()
    Step2()
    Step1()
    print i

if steps < 0:
 steps = 0-steps
 for i in range (steps):
  Step1()
  Step2()
  Step3()
  Step4()
  Step5()
  Step6()
  Step7()
  Step8()
  print i

GPIO.cleanup()
