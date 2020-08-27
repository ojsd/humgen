import os

from debuglogger import DebugLogger
from driver.instrumentdriver import InstrumentDriver
from config import Config

if os.uname()[4].startswith("arm"):  # Test if the program is running on RaspberryPi or not.
    import RPi.GPIO as GPIO


class AlzardDriver(InstrumentDriver):
    """
    Driver for the Al-Zard optocoupler isolator 24V to 5V level voltage converter board.
    This board receives 24V signal from the Picarro "valve" output and securely converts it to On/Off signal readable by
    the RaspberryPi.
    4 board's inputs are used, creating a 4-bits binary code used to transmit picarro's instructions to the RaspberryPi.
    """
    
    def __init__(self, enabled: bool, debug_logger: DebugLogger, object_id: str, config: Config):
        super(AlzardDriver, self).__init__(enabled, debug_logger, object_id)

        # Initialize input_ignore: whether to ignore picarro state changes or not
        self.input_ignored = config.read(object_id, "ignore_at_startup")

        # If the program is not running on RPi, automatically disable the Valve driver
        if not os.uname()[4].startswith("arm"):
            self.set_status_code(1)
            self.debug_logger.info(object_id, "Deactivated: run only on RPi!")
            return
        else:
            self.set_status_code(self.ask_instrument_status())
            
        # Set the current mode
        GPIO.setmode(GPIO.BCM)

        # Removing the warnings
        GPIO.setwarnings(False)

        self.pin1 = config.read(object_id, "gpio_port_1")
        self.pin2 = config.read(object_id, "gpio_port_2")
        self.pin3 = config.read(object_id, "gpio_port_3")

        GPIO.setup(self.pin1, GPIO.IN)
        GPIO.setup(self.pin2, GPIO.IN)
        GPIO.setup(self.pin3, GPIO.IN)

        # Launch record thread
        self._launch_thread_record_()

    def read_code(self) -> str:
        """Read the 3-bits binary code from Al-Zard board outputs."""
        state1 = not GPIO.input(self.pin1)
        state2 = not GPIO.input(self.pin2)
        state3 = not GPIO.input(self.pin3)
        code = str(int(state1)) + str(int(state2)) + str(int(state3))
        return code

    def ignore_input(self, ignore: bool) -> None:
        """Ignore (or not) the changes of the Picarro code"""
        self.input_ignored = ignore

    def is_input_ignored(self) -> bool:
        return self.input_ignored
    
    def ask_instrument_status(self) -> int:
        status = 5
        return status

    def __update_record__(self) -> None:
        self.record["code"] = self.read_code()
        
    def _reset_record_(self) -> None:
        self.record["code"] = "---"

    def get_data_logger_header_list(self) -> list:
        return ["code"]
