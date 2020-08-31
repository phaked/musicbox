import logging
import yaml
import RPi.GPIO as GPIO
from util import KillMe, exec_mpc_func
from time import sleep
from mfrc522 import MFRC522
from mpd import MPDClient

class RFID:

    def __init__(self, map_path):
        self.reader = MFRC522()
        self.logger = logging.getLogger("musicbox")
        self.kill = False

        with open(map_path) as file:
            self.playlist_map = yaml.full_load(file)
            self.logger.info("Loading RFID playlist mapping")
            
        self.mpc = MPDClient()
        self.last_card_id = 0

    def _convert_uid(self, uid):
        id = 0
        for i in range(len(uid)):
            id = id*256+uid[i]
        return id 

    def watch(self):
        self.logger.info("Starting RFID.")

        while not self.kill:
            status , _ = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
            if status == self.reader.MI_OK:
                status, uid = self.reader.MFRC522_Anticoll()
            if status == self.reader.MI_OK:
                id = self._convert_uid(uid)
            else:
                id = 0

            if id != self.last_card_id:
                self.logger.info(f"Card with id={id} read.")
                exec_mpc_func(self.mpc, self.mpc.stop)
                exec_mpc_func(self.mpc, self.mpc.clear)
                if id != 0:
                    if id in self.playlist_map:
                        playlist = self.playlist_map[id]
                        self.logger.info(f"Play {playlist}")
                        exec_mpc_func(self.mpc, self.mpc.load, playlist)
                        exec_mpc_func(self.mpc, self.mpc.play)
                    else:
                        self.logger.info(f"RFID with uid {id} is not mapped to a playlist.")
            self.last_card_id = id
            self.reader.MFRC522_Request(self.reader.PICC_HALT)
            sleep(1)
        GPIO.cleanup()
        self.logger.info("Exiting RFID.")
        return

