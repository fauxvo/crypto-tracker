#!/bin/bash

# Update the current system
sudo apt-get update
sudo apt-get -y upgrade

# Install Node
wget -O - https://raw.githubusercontent.com/audstanley/NodeJs-Raspberry-Pi/master/Install-Node.sh | sudo bash

# Might have to put a catch for Node here

while true; do
    read -p "Do you want to run the python application on launch? (Y/n) " yn
    case $yn in
        [Yy]* ) printf '$-1i\ncd /home/pi/crypto-tracker/python && python3 main.py &\n.\nw\n' | sudo ex -s /etc/rc.local; break;;
        [Nn]* ) break;;
    esac
done < /dev/tty &&

while true; do
    read -p "Are you using an Adafruit SSD1306 Display driver? (Y/n) " yn
    case $yn in
        [Yy]* ) echo "dtparam=i2c_baudrate=1000000" >> sudo tee -a /boot/config.txt ; break;;
        [Nn]* ) break;;
    esac
done < /dev/tty &&

# Install Python 3
sudo apt-get install -y python3-pip python3 git python-smbus i2c-tools python3-pil python3-numpy &&

# Download the app
git clone https://github.com/fauxvo/crypto-tracker.git  &&
cd ~/crypto-tracker && npm install &&

sudo pip3 install adafruit-circuitpython-ssd1306 RPi.GPIO spidev ccxt apscheduler termcolor &&

sudo pip3 install --upgrade setuptools

cd ~
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py < /dev/tty