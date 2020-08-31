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
        self.encoder = pyky040.Encoder(CLK=6, DT=5)
        self.encoder.setup(inc_callback=self._inc, dec_callback=self._dec)
        self.kill = util.KillMe()
        self.mpc = MPDClient()

    def _inc(self, counter):
        vol = int(util.exec_mpc_func(self.mpc.status)["volume"])
        self.logger.info(f"Increasing volume to {vol+2}.")
        util.exec_mpc_func(self.mpc.setvol, vol + 2)

    def _dec(self, counter):
        vol = int(util.exec_mpc_func(self.mpc.status)["volume"])
        self.logger.info(f"Decreasing volume to {vol - 2}.")
        util.exec_mpc_func(self.mpc.setvol, vol - 2)

    def watch(self):
        self.encoder.watch()
        while not self.kill.kill_me:
            sleep(1)
        GPIO.cleanup()
        self.logger.info("Exiting rotary.")
        return
