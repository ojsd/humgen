import os
import subprocess
import time

from debuglogger import DebugLogger
from driver.instrumentdriver import InstrumentDriver
from config import Config

if os.uname()[4].startswith("arm"):  # Test if the program is running on RPi or not
    # Load modules for
    subprocess.call('modprobe w1-therm', shell=True)
    subprocess.call('modprobe w1-gpio', shell=True)


class TempDS18B20Driver(InstrumentDriver):
    """Driver for 1-Wire BS18B20 temperature sensor"""

    def __init__(self, enabled: bool, debug_logger: DebugLogger, object_id: str, config: Config):
        super(TempDS18B20Driver, self).__init__(enabled, debug_logger, object_id)

        # Initialize config
        self.config = config

        # If the program is not running on RPi, automatically disable the driver
        if not os.uname()[4].startswith("arm"):
            self.set_status_code(1)
            self.debug_logger.info(object_id, "Deactivated: run only on RPi!")
            return
        else:
            self.set_status_code(self.ask_instrument_status())

        # Initialize sensor's file, and check if it exists
        self.sensor_filename = self.__get_sensor_filename__()
        if not os.path.exists(self.sensor_filename):
            self.set_status_code(2)
        
        # Launch record thread
        self._launch_thread_record_()

    def get_temperature(self):
        """Get the temperature from the sensor."""
        lines = self.__temp_raw__()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.__temp_raw__()
            
        temp_output = lines[1].find('t=')

        if temp_output != -1:
            temp_string = lines[1].strip()[temp_output+2:]
            temp_c = float(temp_string) / 1000.0
            # temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c

    def __temp_raw__(self):
        """Get the content of the sensor's file"""
        f = open(self.sensor_filename, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def ask_instrument_status(self):
        status = 5
        return status

    def __get_sensor_filename__(self):
        filename = "/sys/bus/w1/devices/" + self.config.read(self.object_id, "sensor_id") + "/w1_slave"
        return filename

    def __update_record__(self):
        self.record["temperature"] = self.get_temperature()

    def _reset_record_(self):
        self.record["temperature"] = -999