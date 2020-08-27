import os

from debuglogger import DebugLogger
from driver.relaydriver import RelayDriver
from config import Config

if os.uname()[4].startswith("arm"):  # Test if the program is running on RPi or not
    import RPi.GPIO as GPIO


class ElectrovalveDriver(RelayDriver):

    def __init__(self, enabled: bool, debug_logger: DebugLogger, object_id: str, config: Config):
        super(ElectrovalveDriver, self).__init__(enabled, debug_logger, object_id, config)

        if not os.uname()[4].startswith("arm"):
            return

        self.normally_closed = config.read(object_id, "normally_closed") == 1
        
        # Define the open_state value
        if self.normally_closed:
            self.open_state = self.output_powered
            self.closed_state = self.output_unpowered
        else:
            self.open_state = self.output_unpowered
            self.closed_state = self.output_powered

    def open_valve(self):
        """Open the electrovalve"""
        if self.get_position() == "open":            
            return True
        
        if self.normally_closed:
            success = self.power_output()
        else:
            success = self.unpower_output()

        if success:
            self.debug_logger.info(self.object_id, "Valve opened")
        else:
            self.debug_logger.error(self.object_id, "Failed to open electrovalve")
        return success

    def close_valve(self):
        """Close the electrovalve"""
        if self.get_position() == "closed":            
            return True
            
        if self.normally_closed:            
            success = self.unpower_output()
        else:            
            success = self.power_output()

        if success:
            self.debug_logger.info(self.object_id, "Valve closed")
        else:
            self.debug_logger.error(self.object_id, "Failed to close electrovalve")
        return success

    def get_position(self):
        """Get the status (open or closed) of the electrovalve."""
        if GPIO.input(self.pin) == self.closed_state:
            status = "closed"
        elif GPIO.input(self.pin) == self.open_state:
            status = "open"
        else:
            raise ValueError
        return status
