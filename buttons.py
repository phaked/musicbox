import logging
import RPi.GPIO as GPIO
from time import sleep
from mpd import MPDClient
import util

class Buttons:
    
    def __init__(self):
        self.logger = logging.getLogger("musicbox")
        GPIO.setmode(GPIO.BCM)
        # create play/pause button
        self._create_button(13, self._pause_resume_callback)
        # create next button
        self._create_button(6, self._next_callback)
        # create previous button
        self._create_button(5, self._prev_callback)
        self.mpc = MPDClient()
        self.end = False

    def _next_callback(self, *args):
        self.logger.info(f"Play next song.")
        util.exec_mpc_func(self.mpc, self.mpc.next)

    def _prev_callback(self, *args):
        self.logger.info(f"Play previous song.")
        util.exec_mpc_func(self.mpc, self.mpc.previous)

    def _pause_resume_callback(self, *args):
        self.logger.info(f"Pause/Resume song.")
        util.exec_mpc_func(self.mpc, self.mpc.pause)

    def _create_button(self, GPIO_PIN, callback):
        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(GPIO_PIN, GPIO.FALLING, callback=callback, bouncetime=100)

    def stop(self):
        self.end = True

    def watch(self):
        self.logger.info("Starting buttons.")
        try:
            while not self.end:
                sleep(1)
        except:
            self.stop()
        GPIO.cleanup()
        self.logger.info("Exiting buttons.")
        return

if __name__ == '__main__':
    logger = logging.getLogger("musicbox")
    logger.setLevel(logging.INFO)
    log_file = logging.FileHandler("../musicbox.log")
    fmtr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file.setFormatter(fmtr)
    log_file.setLevel(logging.INFO)
    logger.addHandler(log_file)
    buttons = Buttons()
    buttons.watch()
