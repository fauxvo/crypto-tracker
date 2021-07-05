# Crypto Tracker

This project is a modified version of [aCallum's SafePi project](https://github.com/aCallum/SafePi) and first and foremost, I want to give them a huge shoutout for the inspiration and work put forward to create this.

Crypto Tracker takes the [SafePi](https://github.com/aCallum/SafePi) project even further and creates support for other crypto currencies, currently supporting **BTC**, **ETH**, **DOGE** and of course, **SAFEMOON**!!

Additional features include:

- Support for multiple wallets per coin
- A Javascript configuration panel which makes setting up of coins / wallets and configuration settings much easier
- Support for multiple types of displays including [Adafruit's SSD1306 OLED](https://www.adafruit.com/product/3531), [SH1106 OLED Displays](https://www.waveshare.com/wiki/1.3inch_OLED_HAT) and [SSD1105 OLED Displays](https://thepihut.com/collections/raspberry-pi-screens/products/128x32-2-23inch-oled-display-hat-for-raspberry-pi) (_currently untested)_
- The ability to schedule when the application is being run either between a specific set of times (09:00 -> 17:00) or a schedule for a particular duration (20 minutes at the start of every hour)
- The ability to toggle through your tracked coins using Next / Prev buttons (currently only the Adafruit SSD1306 Display is supported)
- Support for rotating the screen

### Prerequisites:

This project was built to support three main display drivers. I've done my best to automatically include the necessary drivers on install but you might have to do extra configuration if the display you'd like to use is not currently listed.

1. Almost any RaspberryPi (with GPIO support):
   - https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-zero-wh-with-pre-soldered-header
2. A SPI/I2C GPIO display:
   - https://www.adafruit.com/product/3531
3. SD Card 8GB or higher -- image it with Raspberry Pi OS Lite
4. Power Cable & Charger/Battery Bank

### Build the Device:

1. Burn the OS in SD Card with Raspberry Pi Imager
   - https://www.raspberrypi.org/software/
2. Connect the display to Pi GPIO Pins
3. Plug in Power
4. Install OS (Raspberry Pi OS Lite)
5. Enable SPI & I2C in Raspi Config
   - sudo raspi-config
   - select Localization Options > Timezone (needed for scheduling functionality)
   - select Interface Options > SPI > Yes (Only needed for SSH1105 Displays)
   - select Interface Options > I2C > Yes
6. Reboot the Pi
   - sudo reboot now

### Security

The crypto tracker application does not perform any operations or manipulations on any of the coins or wallets that you share with the application. The only information made available is your wallet addresses which get queried to obtain the necessary balances. The 3rd party API keys also do no permit any operations of your coins and do not have any effect on manipulating your assets. The information provided is freely available, this application only returns the extremely small subsections of the blockchain which you are requesting. Like everything with cryptocurrency, you should not share your crypto balances with anyone and no information you provide ever leaves your raspberry pi device.

### How it Works

The crypto tracker app simply uses 3rd party apis to get total coin values for the wallet addresses you provide. These values are then compared against the Tether stablecoin (USDT) to determine the approximate value of the total number of coins within the wallets provided. If the user selects a currency other than USD, the [Currency Converter API](https://free.currencyconverterapi.com/free-api-key) is used to convert that USD amount into the appropriate other currency.

The app then cycles through all of the coins provided and repeats the process. In addition to simply getting the latest values of the wallets from the blockchain APIs, the previous wallet balances are also stored in the system. The balance screen simply displays the change from the previous balances to the current balance.

In the case of coins with reflections like Safemoon, the application is not calculating reflections per say, just displaying the different between two balances which when using an exchange like Pancake Swap, will most likely show a new balance that is higher than the last time it was queried and you will see the growth your wallet has made.

### 3rd Party API Keys:

In order to get the latest information used by the crypto tracker application, use of 3rd party APIs are required. Before running the installation & configuration sections, it would be handy to have these API keys and wallet addresses already available so that you can just copy and paste the information into the configuration application

- [Currency Converter API](https://free.currencyconverterapi.com/free-api-key)
  - Used for converting coins to different currencies
- [BSC Scan API](https://bscscan.com/register)
  - Necessary for obtaining token counts for **SAFEMOON**
- [Etherscan.io API](https://etherscan.io/register)

  - Necessary for obtaining token counts for **ETH**

- If you do not plan on tracking **ETH** or **SAFEMOON**, you do not need to get API keys for these services.

### Software & Install:

1. Log in to your Raspberry PI
2. Execute the installation script in order to get the correct packages and repos

   `wget -q -O - https://raw.githubusercontent.com/fauxvo/crypto-tracker/master/installDependencies.sh | bash`

3. Follow the necessary prompts and reboot the PI
4. Setup the necessary configuration file by executing

   `cd ~/crypto-tracker && npm run start`

5. Add the coins & wallets that you'd like the application to track
6. Add in the necessary crypto tracker settings required to configure the application
7. Save the configuration and restart the PI

You can always re-run the javascript configuration application if you'd like to make any changes to your application's settings. As well, you can also edit the raw output file from that application which is located at `~/crypto-tracker/cryptoTrackerConfig.json`

Depending on if you wanted the application to run automatically or not on device startup, when executing the application, the necessary APIs are called and the application should be displaying information correctly on your display.

To run the application manually enter
`cd ~/crypto-tracker/python && sudo python3 main.py`

If you'd like to run the application manually in the background, enter
`cd ~/crypto-tracker/python && sudo python3 main.py &`

### Current Issues

Since this is my first time extending a python application, it's inevitable that there are a few minor bugs which are currently outstanding

1. I did my best to provide support for multiple screens and Raspberry Pi devices (Zero & Pi 4), other hardware hasn't been tested but should work.
2. The application runs relatively smoothly but does crash on occasion (my guess is either hitting Raspi memory / temperature limits or API limits). Simply restarting the device or re-running the application should resolve this. If you have any ideas as to what is causing that, please provide a PR!

### Future Improvements

1. Support for other crypto currencies (requests and/or PRs are welcomed!), especially coins being supported by the upcoming Safemoon wallet!
2. Using other blockchain scanning APIs which do not require API keys
3. Add button support for the SH1106 display
4. Add thread support
