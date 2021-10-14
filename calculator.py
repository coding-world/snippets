import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

matrix = [["1","2","3", "A"],
          ["4","5","6", "B"],
          ["7","8","9", "C"],
          ["*", "0", "#", "D"]]

column = [12, 16, 20, 21]
row = [18, 23, 24, 25]

for j in range(4):
    gpio.setup(column[j], gpio.OUT)
    gpio.output(column[j], 1)
    gpio.setup(row[j], gpio.IN, pull_up_down=gpio.PUD_UP)

def keypad():
    while True:
        for j in range(4):
            gpio.output(column[j], 0)
            for i in range(4):
                if gpio.input(row[i]) == 0:
                    char = matrix[i][j]
                    while gpio.input(row[i]) == 0:
                        pass
                    return char
            gpio.output(column[j], 1)
    return False

try:
    while True:
        print(keypad())
        time.sleep(0.2)
except KeyboardInterrupt:
    gpio.cleanup()