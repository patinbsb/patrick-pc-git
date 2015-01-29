#!/usr/bin/python
#
# HD44780 LCD Test Script for
# Raspberry Pi
#
# Author : Matt Hawkins
# Site   : http://www.raspberrypi-spy.co.uk
#
# Date   : 26/07/2012
#

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

# import
import RPi.GPIO as GPIO
import time
from datetime import date
import forecast_module

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

# Set  GPIO warnings
GPIO.setwarnings(False)

# Define some device constants
LCD_WIDTH = 16  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005


def main():

    # Main program block
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(LCD_D7, GPIO.OUT)  # DB7

    # Setup GPIO for Button
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Initialise display
    lcd_init()

    # Get weather json for initial input for loop
    wdata = forecast_module.grab_weather()
    send_input(0, (wdata["cnt"]-1), wdata)


def button_wait(delay):

    delay_left = delay
    while delay_left >= 0:
        if not GPIO.input(4):
            return True
        time.sleep(0.1)
        delay_left -= 0.1
    return False


def send_input(prev_block_start, final_block_start, wdata_start):

    # grabs weather forecast from api
    # ensures the forecast data is available

    prev_block = prev_block_start
    final_block = final_block_start
    wdata = wdata_start
    time_range = range(6, 21)

    while True:

        # Sorting out loop start
        if prev_block == 0:
            days = int((wdata["list"][final_block]["dt"] - wdata["list"][0]["dt"]) / 86400)
            line1("{0} Day".format(days))
            line2("Weather Forecast")
            time.sleep(5)

        # make sure to return to start of program if at the last weather block
        if prev_block >= final_block:
            wdata = forecast_module.grab_weather()
            final_block = (wdata["cnt"] - 1)
            prev_block = 0
            continue

        # per loop constants
        current_time = wdata["list"][prev_block]["dt_txt"]
        weekday = day_string(current_time)
        current_day = days - int((wdata["list"][final_block]["dt"] - wdata["list"][prev_block + 1]["dt"]) / 86400)

        # making only a certain time range print per loop (currently 3 per loop at 06:00, 12:00, 18:00)
        if not int(current_time[-8:-6]) in time_range:
            prev_block += 2
            continue

        # Formatting weather data from json per loop
        temp, descrip, wind, winddir = forecast_module.weather_iter(prev_block, wdata)
        weatherlist = [temp, descrip, ("Wind: Force " + wind), ("Dir: " + winddir)]

        # printing weather data to the lcd
        line1(wdata["list"][prev_block]["dt_txt"])
        line2("{0}/{1} {2}".format(current_day, days, weekday))
        time.sleep(1)

        if button_wait(3):
            prev_block += 2
            continue

        line1(weatherlist[0])
        line2(weatherlist[1])

        if button_wait(3):
            prev_block += 2
            continue

        line1(weatherlist[2])
        line2(weatherlist[3])

        if button_wait(3):
            prev_block += 2
            continue

        prev_block += 2


def day_string(dt_txt):

    # Function that takes raw date info and returns the corresponding weekday
    date_raw = dt_txt[0:10]
    day_raw = int(date_raw[-2:])
    month_raw = int(date_raw[5:7])
    year_raw = int(date_raw[:4])
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[date(year_raw, month_raw, day_raw).weekday()]


def line1(line):

    # Function to output to line 1 of the lcd display
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(line)


def line2(line):

    # Similar function for line 2
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(line)


def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)


def lcd_string(message):
    # Send string to display

    message = message.ljust(LCD_WIDTH, " ")

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(LCD_RS, mode)  # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


if __name__ == '__main__':
    main()
