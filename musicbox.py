import logging
from buttons import Buttons
from rotary import Rotary
from rfid import RFID


class MusicBox:

    def __init__(self):
        self.logger = logging.getLogger("musicbox")
        self.logger.setLevel(logging.INFO)
        log_file = logging.FileHandler("../musicbox.log")
        fmtr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_file.setFormatter(fmtr)
        log_file.setLevel(logging.INFO)
        self.logger.addHandler(log_file)
        self.rfid = RFID()
        self.buttons = Buttons()
        self.rotary = Rotary()

    def runs(self):
        self.logger.info("Starting Musicbox")

        self.RFID.watch("../mapping.yaml")
        self.Buttons.watch()
        self.Rotary.watch()


if __name__ == '__main__':
    mb = MusicBox()
    mb.run()
