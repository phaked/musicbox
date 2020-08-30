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
        self.kill = util.KillMe()
        self.mpc = MPDClient()

    def my_inc(counter):
        mpc.connect("localhost", 6600)
        vol = int(mpc.status()["volume"])
        mpc.setvol(vol + 2)
        mpc.close()
        mpc.disconnect()
        print('lauter')

    def my_dec(counter):
        mpc.connect("localhost", 6600)
        vol = int(mpc.status()["volume"])
        mpc.setvol(vol - 2)
        mpc.close()
        mpc.disconnect()
        print('leiser')

    def watch(self):
        while not self.kill.kill_me:
            sleep(1)
        GPIO.cleanup()
        self.logger.info("Exiting")
        return



# Init the encoder pins


# Or the encoder as a device (must be installed on the system beforehand!)
# my_encoder = pyky040.Encoder(device='/dev/input/event0')

# Setup the options and callbacks (see documentation)
my_encoder.setup(inc_callback=my_inc, dec_callback=my_dec)

# Launch the listener
my_encoder.watch()
