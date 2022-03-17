import sys
import time
import RPi.GPIO as GPIO

delay = 0.002
pinout = [22, 23, 24, 25]

def setup():
  GPIO.setmode(GPIO.BCM)
  for pin in pinout:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)


def microstep(last_pin, pin):
  GPIO.output(pinout[pin], True)
  time.sleep(delay)
  GPIO.output(pinout[last_pin], False)
  time.sleep(delay)


def move(steps):
  if steps > 0:
    GPIO.output(pinout[3], True)
    for i in range(steps):
      for j in range(4):
        microstep((j+3)%4, j)
    GPIO.output(pinout[3], False)
  else:
    GPIO.output(pinout[0], True)
    for i in range(-steps):
      for j in range(3, -1, -1):
        print(j)
        microstep((j+1)%4, j)
    GPIO.output(pinout[0], False)


if len(sys.argv) == 2:
  setup()
  move(int(sys.argv[1]))
  GPIO.cleanup()
