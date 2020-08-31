import logging
from buttons import Buttons
from rotary import Rotary
from rfid import RFID
from time import sleep
from util import KillMe
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
        self.rotary = Rotary()
        self.rfid = RFID("../mapping.yaml")
        self.buttons = Buttons()
        self.kill = KillMe()

    def run(self):
        self.logger.info("Starting Musicbox")

        self.rotary.watch()
        self.buttons.watch()
        self.rfid.watch()
        while not self.kill.kill_me:
            sleep(1)
        self.rotary.kill = True
        self.buttons.kill = True
        self.rfid.kill = True

if __name__ == '__main__':
    mb = MusicBox()
    mb.run()
