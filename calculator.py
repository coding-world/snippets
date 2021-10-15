import RPi.GPIO as gpio
import time, board, digitalio, adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

RESET_PIN = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=RESET_PIN)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)

gpio.setmode(gpio.BCM)

matrix = [[1, 2, 3, "+"],
          [4, 5, 6, "-"],
          [7, 8, 9, "x"],
          ["*", 0, "#", "/"]]

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


def calc(operator, a, b):
    a, b = float(a), float(b)
    return str(round({
        '+': lambda: a + b,
        '-': lambda: a - b,
        'x': lambda: a * b,
        '/': lambda: a / b,
    }.get(operator)(), 8))


last = ""
current = ""
operator = ""


def show():
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), last + operator + current, font=font, fill=255)
    draw.text((0, 30), "-------------------------", font=font, fill=255)
    draw.text((0, 46), current, font=font, fill=255)
    oled.image(image)
    oled.show()


show()

try:
    while True:
        input = keypad()

        if input == "#":  # enter
            if last != "" and current != "":
                current = calc(operator, last, current)
                operator = ""
                last = ""
        elif input == "*":  # clear
            last = ""
            current = ""
            operator = ""
        elif type(input) is int:  # number
            current += str(input)
        elif operator != "" and current == "":  # switch operator
            operator = input
        elif last != "" and current != "":  # calculate and set operator
            last = calc(operator, last, current)
            operator = input
            current = ""
        elif current != "":  # set operator
            operator = input
            last = current
            current = ""

        show()
        time.sleep(0.2)

except KeyboardInterrupt:
    gpio.cleanup()
