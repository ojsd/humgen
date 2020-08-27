import threading
from time import sleep

from debuglogger import DebugLogger
from config import Config
from driver.relaydriver import RelayDriver
from driver.temp18b20driver import TempDS18B20Driver


class TemperatureDriver:
    """
    Driver controling the temperature (read temperature sensor and toggle heating)
    """

    def __init__(self,
                 switch: RelayDriver,
                 sensor: TempDS18B20Driver,
                 debug_logger: DebugLogger,
                 object_id: str,
                 config: Config):
        # Initialize logger
        self.debug_logger = debug_logger
        self.object_id = object_id
        self.config = config

        # Initialize intruments' driver
        self.switch = switch
        self.sensor = sensor
        
        # Initialize setpoint, hysteresis and refresh period
        self.setpoint = self.config.read(self.object_id, "setpoint")
        self.hysteresis = self.config.read(self.object_id, "hysteresis")
        self.refresh_period = self.config.read(self.object_id, "refresh_period_sec")

        if self.get_status_code() > 4:
            a = threading.Thread(None, self.__temp_ctrl_thread__)
            a.daemon = True
            a.start()
    
    def set_setpoint(self, setpoint: float):
        self.setpoint = setpoint
        self.config.write(self.object_id, "setpoint", setpoint)
        
    def get_setpoint(self) -> float:
        self.setpoint = float(self.config.read(self.object_id, "setpoint"))
        return self.setpoint

    def set_hysteresis(self, hysteresis: float):
        self.hysteresis = hysteresis
        self.config.write(self.object_id, "hysteresis", hysteresis)

    def get_hysteresis(self) -> float:
        self.hysteresis = float(self.config.read(self.object_id, "hysteresis"))
        return self.hysteresis

    def set_refresh_period(self, refresh_period) -> int:
        self.refresh_period = refresh_period
        self.config.write(self.object_id, "refresh_period_sec", refresh_period)

    def get_refresh_period(self) -> int:
        self.refresh_period = int(self.config.read(self.object_id, "refresh_period_sec"))
        return self.refresh_period

    def get_temperature(self) -> float:
        return self.sensor.get_record()["temperature"]

    def __control_temperature__(self):
        measured = self.get_temperature()
        if measured > self.setpoint + self.hysteresis:
            self.switch.unpower_output()
        elif measured < self.setpoint - self.hysteresis:
            self.switch.power_output()

    def __temp_ctrl_thread__(self):
        while True:
            self.__control_temperature__()
            sleep(self.config.read(self.object_id, "refresh_period_sec"))
            
    def get_status_code(self):
        return min(self.switch.get_status_code(), self.sensor.get_status_code())

    def on_exit(self):
        """Actions to be performed when the Python program exits."""
        self.switch.unpower_output()