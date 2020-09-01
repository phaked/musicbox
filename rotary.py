# Import the module
from pyky040 import pyky040
import logging
import RPi.GPIO as GPIO
from time import sleep
from mpd import MPDClient
import util


class Rotary:

    def __init__(self):
        self.logger = logging.getLogger("musicbox")
        GPIO.setmode(GPIO.BCM)
        self.encoder = pyky040.Encoder(CLK=12, DT=16)
        self.encoder.setup(inc_callback=self._inc, dec_callback=self._dec)
        self.kill = util.KillMe()
        self.mpc = MPDClient()
        self.volume_steps = 2

    def _inc(self, counter):
        self._setvol("+")
        self.logger.info(f"Increasing volume.")


    def _dec(self, counter):
        self._setvol("-")
        self.logger.info(f"Decrasing volume.")

    def _setvol(self, inc_dec):
        vol = int(util.exec_mpc_func(self.mpc, self.mpc.status)["volume"])
        new_vol = vol
        i = 0
        while vol <= new_vol:
            if inc_dec == "-":
                new_vol = vol - self.volume_steps - i
            else:
                new_vol = vol + self.volume_steps + i

            util.exec_mpc_func(self.mpc, self.mpc.setvol, new_vol)
            i += 1
            new_vol = int(util.exec_mpc_func(self.mpc, self.mpc.status)["volume"])
        self.logger.info(f"Volume set to {new_vol}.")

    def watch(self):
        self.encoder.watch()
        while not self.kill.kill_me:
            sleep(1)
        GPIO.cleanup()
        self.logger.info("Exiting rotary.")
        return

if __name__ == '__main__':
    logger = logging.getLogger("musicbox")
    logger.setLevel(logging.INFO)
    log_file = logging.FileHandler("../musicbox.log")
    fmtr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file.setFormatter(fmtr)
    log_file.setLevel(logging.INFO)
    logger.addHandler(log_file)
    rotary = Rotary()
    rotary.watch()
