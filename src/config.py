import configparser
import utils
import threading


class Config:

    def __init__(self, filename):
        self.full_filename = "../config/" + filename
        self.config_parser = configparser.ConfigParser()
        self.file_access_lock = threading.Lock()

    def write(self, instrument, key, value):
        self.file_access_lock.acquire()
        self.config_parser.read(self.full_filename)
        self.config_parser.set(instrument, key, str(value))
        with open(self.full_filename, 'w') as configfile:
            self.config_parser.write(configfile)
        self.file_access_lock.release()

    def read(self, instrument, key):
        self.file_access_lock.acquire()
        self.config_parser.read(self.full_filename)
        value = self.config_parser.get(instrument, key)
        self.file_access_lock.release()
        value = utils.convert_to_numeric(value)
        return value
