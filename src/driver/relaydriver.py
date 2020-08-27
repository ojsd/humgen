import os
import time

from debuglogger import DebugLogger
from driver.instrumentdriver import InstrumentDriver
from config import Config

if os.uname()[4].startswith("arm"):  # Test if the program is running on RPi or not
    import RPi.GPIO as GPIO


class RelayDriver(InstrumentDriver):

    def __init__(self, enabled: bool, debug_logger: DebugLogger, object_id: str, config: Config):
        super(RelayDriver, self).__init__(enabled, debug_logger, object_id)

        # If the program is not running on RPi, automatically disable the driver
        if not os.uname()[4].startswith("arm"):
            self.set_status_code(1)
            self.debug_logger.info(object_id, "Deactivated: run only on RPi!")
            return
        else:
            self.set_status_code(self.ask_instrument_status())

        # Set a current mode
        GPIO.setmode(GPIO.BCM)

        # Remove the warnings
        GPIO.setwarnings(False)

        # Do the mapping between the object ID and the RPi pin number
        self.pin = int(config.read(object_id, "gpio_port"))

        # Define the ON/OFF value
        self.output_powered = GPIO.LOW
        self.output_unpowered = GPIO.HIGH

        # Set GPIO port as output
        GPIO.setup(self.pin, GPIO.OUT)

        # Launch record thread
        self._launch_thread_record_()

    def power_output(self):
        """ON => Close the relay => power the output"""
        # If relay is already powered => do nothing
        if self.get_position() == "powered":
            return True

        # Power output
        GPIO.output(self.pin, self.output_powered)

        # Check if valve was correctly open
        time.sleep(0.1)
        success = (GPIO.input(self.pin) == self.output_powered)
        if success:
            self.debug_logger.info(self.object_id, "Relay's output powered")
        else:
            self.debug_logger.error(self.object_id, "Failed to power relay")
        return success

    def unpower_output(self):
        """OFF => Open the relay => unpower the output"""
        # If relay is already unpowered => do nothing
        if self.get_position() == "unpowered":
            return True
        
        # Close valve
        GPIO.output(self.pin, self.output_unpowered)

        # Check if valve was correctly closed
        time.sleep(0.1)
        success = (GPIO.input(self.pin) == self.output_unpowered)
        if success:
            self.debug_logger.info(self.object_id, "Relay's output unpowered")
        else:
            self.debug_logger.error(self.object_id, "Failed to unpower relay")
        return success

    def get_position(self):
        """Get the status (powered or unpowered) of the relay."""
        if GPIO.input(self.pin) == self.output_unpowered:
            status = "unpowered"
        elif GPIO.input(self.pin) == self.output_powered:
            status = "powered"
        else:
            raise ValueError
        return status

    def ask_instrument_status(self):
        """Ask the status (disabled, or disconnected, or error, etc.) of the instrument."""
        status = 5
        return status

    def __update_record__(self):
        self.record["position"] = self.get_position()

    def _reset_record_(self):
        self.record["position"] = -999

    def get_data_logger_header_list(self):
        return ["position"]
