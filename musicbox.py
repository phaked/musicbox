import logging
from buttons import Buttons
from rotary import Rotary
from rfid import RFID
import RPi.GPIO as GPIO


class MusicBox:

    def __init__(self):
        self.logger = logging.getLogger("musicbox")
        self.logger.setLevel(logging.INFO)
        log_file = logging.FileHandler("../musicbox.log")
        fmtr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_file.setFormatter(fmtr)
        log_file.setLevel(logging.INFO)
        self.logger.addHandler(log_file)
        self.rfid = RFID("../mapping.yaml")
        self.buttons = Buttons()
        self.rotary = Rotary()
        mode = GPIO.getmode()

        if mode is None:
            GPIO.setmode(GPIO.BCM)
        else:
            pin_mode = gpioMode

    def runs(self):
        self.logger.info("Starting Musicbox")

        self.Rotary.watch()
        self.Buttons.watch()
        self.RFID.watch()


if __name__ == '__main__':
    mb = MusicBox()
    mb.run()
