from pathlib import Path
import json
from types import SimpleNamespace

from apscheduler.schedulers.background import BackgroundScheduler
from termcolor import colored

import socket
import config
from PIL import Image, ImageFont, ImageOps, ImageDraw
import numpy
import time
from datetime import datetime

from cryptoAPIs import get_exchange_rate, update_data
from financialData import FinancialData
from mathFunctions import inverse_lerp, lerp

from pathlib import Path

import sys
sys.path.append('./drivers')

crypto_tracker_config_path = "../cryptoTrackerConfig.json"
crypto_tracker_config_file = Path(crypto_tracker_config_path)

if not crypto_tracker_config_file.is_file():
    print(
        colored(
            "You must create a config file before running the application.  Configure Crypto Tracker with `cd ~/crypto-tracker && npm run start`",
            'red'))
    sys.exit()


with open(crypto_tracker_config_path) as config_file:
    config_file = json.load(config_file, object_hook=lambda d: SimpleNamespace(**d))


def debug_output(output_text, colour=None):
    global config
    if config.DEBUG:
        if colour != None:
            print(colored(output_text, colour))
        else:
            print(output_text)


# Initial App Setup
if config.RUN_EMULATOR:
    import cv2
    image_encoding = 'RGB'
else:
    image_encoding = '1'


############################ Variable Declaration ####################################
run_on_schedule = config_file.applicationSettings.runOnSchedule
run_frequency_duration = True if run_on_schedule and config_file.applicationSettings.typeOfSchedule == 'Frequency / Duration' else False
job_completed = None
initial_run = True

debug_total_runs = 0

quit_application = False

number_of_coins = len(config_file.coins)

background_color = 'black'
foreground_color = 'white'

current_coin = 0
current_screen = -1
previous_coin = -1
previous_screen = -1
number_of_screens = 4

application_start_time = datetime.now()

financial_data_list = [FinancialData(0, 0, 0, 0, 0, 0, 0, 0) for _ in range(number_of_coins)]
is_ada_fruit = False
is_SH1106 = False
scheduler = BackgroundScheduler()

start_time = time.time()
display_time = config_file.applicationSettings.timeOnScreen
############################ End of Variable Declaration ####################################


# Check to see if coins are set
if not hasattr(config_file, 'coins') and len(config_file.coins) > 0:
    print(
        colored(
            "You must add at least one coin before running the application.  Configure Crypto Tracker with `cd ~/crypto-tracker && npm run start`",
            'red'))
    sys.exit()

if not config.RUN_EMULATOR and config_file.applicationSettings.typeOfDisplay == 'Adafruit SSD1306 - OLED Display':
    is_ada_fruit = True

    import board
    import busio
    import adafruit_ssd1306
    from digitalio import DigitalInOut, Direction, Pull
    from buttonMap import get_board_pin

    button_left = DigitalInOut(get_board_pin(config_file.applicationSettings.leftButtonPin))
    button_left.direction = Direction.INPUT
    button_left.pull = Pull.UP

    button_right = DigitalInOut(get_board_pin(config_file.applicationSettings.rightButtonPin))
    button_right.direction = Direction.INPUT
    button_right.pull = Pull.UP

    button_config = DigitalInOut(get_board_pin(config_file.applicationSettings.configButtonPin))
    button_config.direction = Direction.INPUT
    button_config.pull = Pull.UP

    # Create the I2C interface
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the SSD1306 OLED class.
    disp = adafruit_ssd1306.SSD1306_I2C(config_file.applicationSettings.displayWidth,
                                        config_file.applicationSettings.displayHeight, i2c)

    disp.fill(0)
    disp.show()

elif not config.RUN_EMULATOR and config_file.applicationSettings.typeOfDisplay == 'SH1106 - OLED Display':
    is_SH1106 = True
    background_color = 'white'
    foreground_color = 'black'

    import SH1106

    disp = SH1106.SH1106()
    disp.Init()
    disp.clear()

elif not config.RUN_EMULATOR and config_file.applicationSettings.typeOfDisplay == 'SSD1305 - OLED Display':
    import SPI
    import SSD1305
    # Raspberry Pi pin configuration:
    RST = None     # on the PiOLED this pin isnt used
    # Note the following are only used with SPI:
    DC = 24
    SPI_PORT = 0
    SPI_DEVICE = 0

    # 128x32 display with hardware SPI:
    disp = SSD1305.SSD1305_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
    # Initialize library.
    disp.begin()
    # Clear display.
    disp.clear()
    disp.display()


def toggleCurrentCoin(increment=True):
    global current_coin
    global previous_coin
    global current_screen

    increment_value = 1

    if not increment:
        increment_value = -1

    current_coin += increment_value
    if current_coin > len(config_file.coins) - 1:
        current_coin = 0

    if current_coin < 0:
        current_coin = len(config_file.coins) - 1

    current_screen = 0


def screen_mapper(screen):
    switcher = {
        -1: 'Initialization Screen',
        -2: 'Total Wallet Balance Screen',
        0: 'Coin Loading Screen',
        1: 'Coin Balance Screen',
        2: 'Coin Price Screen',
        3: 'Coin Difference Screen'
    }

    return switcher.get(screen, lambda: 'Invalid Screen')


def run_application():
    global run_on_schedule
    global run_frequency_duration
    global quit_application
    global job_completed
    global initial_run

    debug_output('***************** run_application *****************')
    debug_output('quit_application: ' + str(quit_application))
    debug_output('job_completed: ' + str(job_completed))
    debug_output('run_frequency_duration: ' + str(run_frequency_duration))
    debug_output('initial_run: ' + str(initial_run))
    debug_output('***************** /run_application *****************\n')

    if job_completed == None:
        job_completed = False

    if quit_application:
        debug_output('Im quit_application - False', 'red')
        return False

    if not run_on_schedule:
        debug_output('Im run_on_schedule - False', 'green')
        return True

    if not run_frequency_duration:
        if not job_completed:
            debug_output('Im Start Time / End Time - True', 'green')
            return True
        else:
            debug_output('Im Start Time / End Time - False', 'red')
            return False

    if run_frequency_duration:
        if not job_completed:
            debug_output('Im Frequency / Duration - True', 'green')
            return True
        else:
            debug_output('Im Frequency / Duration - False', 'red')
            return False

    debug_output('Im Default - False', 'red')
    return False


def crypto_tracker():
    global config_file
    global financial_data_list
    global number_of_coins
    global current_coin
    global current_screen
    global previous_coin
    global previous_screen
    global number_of_screens
    global background_color
    global foreground_color
    global application_start_time
    global start_time
    global display_time

    frame_size = (config_file.applicationSettings.displayWidth, config_file.applicationSettings.displayHeight)
    screen_y_offset = (int)((config_file.applicationSettings.displayHeight - 32) / 2)

    title_font = ImageFont.truetype("fonts/04B_03__.TTF", 8)
    splash_font = ImageFont.truetype("fonts/aAtmospheric.ttf", 12)
    splash_font_small = ImageFont.truetype("fonts/aAtmospheric.ttf", 9)
    balance_font = ImageFont.truetype("fonts/Nunito-ExtraLight.ttf", 14)
    coin_font_large = ImageFont.truetype("fonts/aAtmospheric.ttf", 14)
    currency_font = ImageFont.truetype("fonts/lilliput steps.ttf", 8)

    arrow = Image.open('images/arrow.bmp').convert(image_encoding)
    arrow = arrow.resize((8, 8), Image.ANTIALIAS)

    local_exchange = 1

    start_time = time.time()
    initializing = True
    initializing_draw = True
    time_delta = 0

    canvas = Image.new(image_encoding, (frame_size), background_color)

    while run_application():

        time_diff = time.time() - start_time

        debug_output('Top of Loop')
        debug_output('Current Coin: ' + str(current_coin))
        debug_output('Current Screen: ' + screen_mapper(current_screen))
        debug_output('Current Time on Screen: ' + str(time_diff))

        debug_output('\n')

        # Pre loading calculations
        if(time_diff) > display_time:
            start_time = time.time()

            if (current_screen == -2):
                current_screen = previous_screen
                current_coin = previous_coin
            elif (current_coin == -1):
                toggleCurrentCoin()

            else:
                current_screen += 1
                # Need to determine when to show Difference
                if current_screen > number_of_screens - 1:
                    debug_output('In Post Loading ' + config_file.coins[current_coin].name)
                    financial_data_list[current_coin] = update_data(
                        financial_data_list[current_coin],
                        config_file.coins[current_coin])
                    toggleCurrentCoin()
                    debug_output('Going to ' + config_file.coins[current_coin].name)

        # Initialization Screen
        if current_screen == -1:
            canvas = Image.new(image_encoding, (frame_size), background_color)

            draw = ImageDraw.Draw(canvas)
            draw.text((0, 11 + screen_y_offset), 'Crypto Tracker', fill=foreground_color, font=splash_font_small)
            draw.text((75, 32 - 9 + screen_y_offset), "Initializing", fill=foreground_color, font=title_font)

            if initializing and not initializing_draw:
                # Update all of the lists initially
                for _ in range(number_of_coins):
                    debug_output("Getting: " + config_file.coins[current_coin].name)
                    financial_data_list[current_coin] = update_data(
                        financial_data_list[current_coin],
                        config_file.coins[current_coin])
                    current_coin += 1

                # To ensure that we go back to the beginning of the coin stack
                current_coin = -1
                local_exchange = get_exchange_rate(config_file.applicationSettings.localCurrency,
                                                   config_file.applicationSettings.currencyConverterAPIKey)
                initializing = False

            initializing_draw = False

        # Configuration Screen
        if current_screen == -2:
            total_balance = 0
            total_current_coin = 0

            for _ in range(number_of_coins):
                total_balance = total_balance + financial_data_list[total_current_coin].current_balance
                total_current_coin += 1

            canvas = Image.new(image_encoding, (frame_size), background_color)
            draw = ImageDraw.Draw(canvas)

            draw.text(
                (0, -1 + screen_y_offset),
                "Total Balance ",
                fill=foreground_color, font=title_font)
            draw.text(
                (1, 9 + screen_y_offset),
                config_file.applicationSettings.localCurrencyChar,
                fill=foreground_color, font=coin_font_large)
            draw.text((15, 7 + screen_y_offset),
                      "{:,.2f}".format(total_balance), fill=foreground_color, font=balance_font)

        # Coin loading screen
        if current_screen == 0:
            flip = False
            screen_x_offset = numpy.sin((time.time() * 3.5))

            if screen_x_offset < 0:
                flip = True
            else:
                flip = False

            pix = (int)(lerp(5, 29, abs(screen_x_offset)))

            canvas = Image.new(image_encoding, (frame_size), background_color)
            image = Image.open(config_file.coins[current_coin].imagePath).convert(image_encoding)

            if is_SH1106:
                image = Image.open(config_file.coins[current_coin].blackImagePath).convert(image_encoding)

            if flip:
                image = ImageOps.mirror(image)

            image = image.resize((pix, 28), Image.ANTIALIAS)
            canvas.paste(image, (28 - (int)(pix * 0.5) - 12, 2 + screen_y_offset))

            draw = ImageDraw.Draw(canvas)
            draw.text(
                (32, 11 + screen_y_offset),
                config_file.coins[current_coin].name, fill=foreground_color, font=splash_font)
            draw.text((95, 32 - 9 + screen_y_offset), "Tracker", fill=foreground_color, font=title_font)

            # if (time.time() - start_time) > 8:
            #     start_time = time.time()
            #     current_screen += 1

        # Coin Balance Screen
        if current_screen == 1:
            if not config_file.applicationSettings.showBalanceScreen:
                start_time = start_time - display_time

            canvas = Image.new(image_encoding, (frame_size), background_color)
            draw = ImageDraw.Draw(canvas)

            draw.text(
                (0, -1 + screen_y_offset),
                config_file.coins[current_coin].name + " Balance (" + config_file.coins[current_coin].symbol + ")",
                fill=foreground_color, font=title_font)
            draw.text(
                (1, 9 + screen_y_offset),
                config_file.coins[current_coin].name[0],
                fill=foreground_color, font=coin_font_large)
            draw.text((15, 7 + screen_y_offset),
                      "{:,.2f}".format(
                          lerp(
                              financial_data_list[current_coin].previous_balance,
                              financial_data_list[current_coin].current_balance, time_delta)),
                      fill=foreground_color, font=balance_font)

            draw.text(
                (0, 32 - 8 + screen_y_offset),
                "=" + config_file.applicationSettings.localCurrencyChar, fill=foreground_color, font=currency_font)
            draw.text(
                (12, 32 - 6 + screen_y_offset),
                "{:,.2f} @ {}{:,.9f}".format(
                    (
                        lerp(
                            financial_data_list[current_coin].previous_balance,
                            financial_data_list[current_coin].current_balance, time_delta) *
                        lerp(
                            financial_data_list[current_coin].previous_rate, financial_data_list[current_coin].current_rate,
                            time_delta)) * local_exchange, config_file.coins[current_coin].name[0],
                    lerp(
                        financial_data_list[current_coin].previous_rate, financial_data_list[current_coin].current_rate,
                        time_delta) * local_exchange),
                fill=foreground_color, font=title_font)

        # Coin Price Screen
        if current_screen == 2:
            if not config_file.applicationSettings.showPriceScreen:
                start_time = start_time - display_time

            canvas = Image.new(image_encoding, (frame_size), background_color)
            draw = ImageDraw.Draw(canvas)
            draw.text(
                (0, -1 + screen_y_offset),
                config_file.coins[current_coin].name + " Price (USDT)", fill=foreground_color, font=title_font)
            draw.text((1, 10 + screen_y_offset), "$", fill=foreground_color, font=coin_font_large)
            draw.text(
                (17, 7 + screen_y_offset),
                "{:,.9f}".format(
                    lerp(
                        financial_data_list[current_coin].previous_rate, financial_data_list[current_coin].current_rate,
                        time_delta))[: 13],
                fill=foreground_color, font=balance_font)

            sign = financial_data_list[current_coin].current_rate - financial_data_list[current_coin].previous_rate

            if sign > 0:
                arrow2 = ImageOps.flip(arrow)
                canvas.paste(arrow2, (115, 12 + screen_y_offset))
            if sign < 0:
                canvas.paste(arrow, (115, 12 + screen_y_offset))

            perc24 = lerp(financial_data_list[current_coin].previous_perc,
                          financial_data_list[current_coin].current_perc, time_delta)
            include_sign = ""
            if perc24 > 0:
                include_sign = "+"

            draw.text(
                (2, 32 - 6 + screen_y_offset),
                "24h {}{:,.2f}%".format(include_sign, perc24),
                fill=foreground_color, font=title_font)

        # Difference Screen
        if current_screen == 3:
            if not config_file.applicationSettings.showBalanceScreen:
                start_time = start_time - display_time

            if not config_file.coins[current_coin].hasReflections:
                start_time = start_time - display_time  # Trigger the next screen
            else:
                canvas = Image.new(image_encoding, (frame_size), background_color)
                draw = ImageDraw.Draw(canvas)
                draw.text(
                    (0, -1 + screen_y_offset),
                    config_file.coins[current_coin].name + " Balance Changes", fill=foreground_color, font=title_font)
                draw.text(
                    (1, 9 + screen_y_offset),
                    config_file.coins[current_coin].name[0],
                    fill=foreground_color, font=coin_font_large)
                draw.text((15, 7 + screen_y_offset),
                          "{:,.2f}".format(
                    lerp(
                        financial_data_list[current_coin].previous_balance_change,
                        financial_data_list[current_coin].current_balance_change, time_delta)),
                    fill=foreground_color, font=balance_font)

                draw.text(
                    (0, 32 - 8 + screen_y_offset),
                    "since " + application_start_time.strftime("%H:%M:%S"), fill=foreground_color, font=title_font)

        time_delta = inverse_lerp(0, display_time, time.time() - start_time)
        display(canvas)

    else:
        debug_output('SHUTTING DOWN')
        canvas = Image.new(image_encoding, (frame_size), background_color)
        draw = ImageDraw.Draw(canvas)
        draw.text((5, 11 + screen_y_offset), 'Shutting Down', fill=foreground_color, font=splash_font_small)
        draw.text((75, 32 - 9 + screen_y_offset), "Sleeping", fill=foreground_color, font=title_font)
        display(canvas)
        time.sleep(5)
        canvas = Image.new(image_encoding, (frame_size), background_color)
        display(canvas)


def calculate_progress(percentage: float):
    global config_file

    end_point = float(config_file.applicationSettings.displayWidth)
    return percentage * end_point


def display(canvas):
    global config_file
    global is_ada_fruit
    global is_SH1106
    global current_coin
    global previous_coin
    global current_screen
    global previous_screen
    global quit_application
    global start_time
    global display_time
    global foreground_color

    if current_screen != -1 and config_file.applicationSettings.showProgressBar:
        time_diff = time.time() - start_time
        progress_length = calculate_progress(time_diff / display_time)

        progress_line = ImageDraw.Draw(canvas)
        progress_line.line([(0, 0), (progress_length, 0)], fill=foreground_color, width=3)

    if config.RUN_EMULATOR:
        # Virtual Display
        npImage = numpy.asarray(canvas)
        frameBGR = cv2.cvtColor(npImage, cv2.COLOR_RGB2BGR)
        cv2.imshow('Crypto Tracking App', frameBGR)
        k = cv2.waitKey(16) & 0xFF
        debug_output(k)
        if k == 27 or k == 113:
            quit_application = True
        elif k == 111:
            previous_coin = current_coin
            previous_screen = current_screen
            current_screen = -2
        elif k == 2:
            toggleCurrentCoin(False)
        elif k == 3:
            toggleCurrentCoin()
    else:
        if 'button_config' in globals() and not button_config.value:
            debug_output('TOTAL WALLET')
            previous_coin = current_coin
            previous_screen = current_screen
            current_screen = -2

        if 'button_left' in globals() and not button_left.value:
            debug_output('LEFT')
            start_time = time.time()
            toggleCurrentCoin(False)

        if 'button_right' in globals() and not button_right.value:
            debug_output('RIGHT')
            start_time = time.time()
            toggleCurrentCoin()

        if config_file.applicationSettings.rotateScreen:
            canvas = canvas.rotate(180)

        # Hardware Display
        disp.image(canvas)
        if is_ada_fruit:
            disp.show()
        elif not is_SH1106:
            disp.display()

        time.sleep(1./60)


def start_crypto_tracker():
    global scheduler
    global job_completed
    global initial_run
    global debug_total_runs

    print('Starting Crypto Tracker from Schedule')

    print('Current job_completed value: ' + str(job_completed))
    print('InitialRun: ' + str(initial_run))
    job_completed = False

    debug_total_runs += 1

    debug_output('The crypto_tracker App has run ' + str(debug_total_runs) + ' times', 'yellow')

    scheduler.print_jobs()
    crypto_tracker()


def end_crypto_tracker():
    global job_completed
    debug_output('Inside end_crypto_tracker', 'green')
    if job_completed != None:
        job_completed = True
        debug_output('======================================== Job Completed ====================================', 'green')
        scheduler.print_jobs()


if run_on_schedule and run_frequency_duration:
    debug_output('Starting Frequency / Duration Job Schedules', 'green')
    scheduler.add_job(
        start_crypto_tracker, 'interval', minutes=config_file.applicationSettings.schedule.duration,
        next_run_time=datetime.now())
    scheduler.add_job(end_crypto_tracker, 'interval', minutes=config_file.applicationSettings.schedule.frequency)
    scheduler.print_jobs()
    scheduler.start()


if run_on_schedule and not run_frequency_duration:
    debug_output('Starting Start Time / End Time Job Schedules', 'green')

    # Parse the time into a format that scheduler can understand
    start_time = config_file.applicationSettings.schedule.start_time.split(':')
    end_time = config_file.applicationSettings.schedule.endTime.split(':')
    scheduler.add_job(start_crypto_tracker, 'cron', hour=start_time[0], minute=start_time[1])
    scheduler.add_job(end_crypto_tracker, 'cron', hour=end_time[0], minute=end_time[1])

    scheduler.print_jobs()
    scheduler.start()

while not quit_application:

    if not run_on_schedule:
        crypto_tracker()

if config.RUN_EMULATOR:
    # Virtual display
    cv2.destroyAllWindows()
    debug_output('destroyed nicely')
else:
    pass
