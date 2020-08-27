import warnings
import threading
import traceback

from time import sleep
from abc import ABC, abstractmethod
from debuglogger import DebugLogger

class InstrumentDriver(ABC):
    """Abstract class for instrument's drivers"""

    status_codes = {1: "disabled",
                    2: "disconnected",
                    3: "no response",
                    4: "response error",
                    5: "ok"}

    def __init__(self, enabled: bool, debug_logger: DebugLogger, object_id: str):
        # Initialize logger
        self.debug_logger = debug_logger
        self.object_id = object_id
        
        # Initialize "record" dict
        if not 'record' in dir(self):
            self.record = {}
            self._reset_record_()
            
        # Initialize status code
        self.status_code = 1
        if enabled:
            self.set_status_code(2)

    def is_enabled(self) -> bool:
        return self.status_code > 1

    def set_enabled(self, enabled: bool):
        if enabled and self.is_enabled():
            warnings.warn("Instrument is already enabled")
        elif not enabled and not self.is_enabled():
            warnings.warn("Instrument is already disabled")

    def get_status_code(self) -> int:
        return self.status_code

    def set_status_code(self, status_code: int):
        self.status_code = status_code

    @abstractmethod
    def ask_instrument_status(self) -> int:
        """
        Do some tests on instruments to characterize its status, and return the corresponding status code.
        :return: Instrument status code
        :rtype: int
        """
        raise NotImplementedError("Subclasses should implement this!")

    def get_record(self):
        return self.record

    @abstractmethod
    def __update_record__(self):
        """
        Modify the "record" dict with the real values read directly from the instrument.
        :return: None
        """
        pass

    def _launch_thread_record_(self):
        if self.get_status_code() >= 4:
            thread_record = threading.Thread(target=self.__thread_record__)
            thread_record.daemon = True
            thread_record.start()

    def __thread_record__(self):
        while True:
            try:
                self.__update_record__()
            except:
                self.debug_logger.error(self.object_id, "Failed to update record.\n" + traceback.format_exc())
                self._reset_record_()
            sleep(1)

    def get_data_logger_header_list(self):
        return []

    def get_object_id(self):
        return self.object_id
    
    @abstractmethod
    def _reset_record_(self):
        """
        Initialize or reset all the record variables.
        """
        pass
