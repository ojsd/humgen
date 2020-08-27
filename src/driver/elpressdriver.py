import struct
import threading
from time import sleep

from PyExpLabSys.drivers import bronkhorst
from driver.serialdriver import SerialDriver
from serial import portNotOpenError

from debuglogger import DebugLogger
from config import Config
from driver.instrumentdriver import InstrumentDriver


class ElPressDriver(bronkhorst.Bronkhorst, InstrumentDriver):
    """
    Driver for Bronkhorst's pressure meter and controller El Press P-702CV
    For details, see the following document:
    "RS232 interface with FLOW6BUS protocol for digital multibus Mass Flow Pressure instruments
     Doc. no 9.17.027"
    """
    def __init__(self,
                 enabled: bool,
                 product: str,
                 debug_logger: DebugLogger,
                 object_id: str,
                 config: Config,
                 com_lock: threading.Lock = None):
        # Initialize logger and config
        self.debug_logger = debug_logger
        self.object_id = object_id
        self.config = config

        # Enabled / disabled
        if not enabled:
            self.set_status_code(1)
            return
        else:
            self.set_status_code(2)

        # Lock for serial communication thread
        if com_lock is None:
            self.com_lock = threading.Lock()
        else:
            self.com_lock = com_lock

        # Open serial connection
        port = SerialDriver.get_port(product)
        try:
            super(ElPressDriver, self).__init__(port, 1000)
        except IOError:
            self.set_status_code(2)
            return
        else:
            self.set_status_code(self.ask_instrument_status())

        self.set_control_mode()

        # Read setpoint from config and apply it
        setpoint_mbar = self.config.read(self.object_id, "setpoint_mbar")
        self.set_setpoint_pressure(setpoint_mbar)
        
        # Initialize data record with void values
        self.record = {}
        self._reset_record_()

        # Launch record thread
        self._launch_thread_record_()

    def comm(self, command):
        """ Send commands to device and receive reply """
        self.com_lock.acquire()
        self.ser.write(command.encode('ascii'))
        sleep(0.1)
        return_string = self.ser.read(self.ser.inWaiting())
        self.com_lock.release()
        return_string = return_string.decode()
        return return_string
    
    def set_setpoint_pressure(self, setpoint_mbar):
        """ Set the desired pressure setpoint, in mbar."""
        setpoint_mbar = float(setpoint_mbar)
        setpoint_hex = hex(struct.unpack('<I', struct.pack('<f', setpoint_mbar))[0])[2:]
        set_setpoint = ':0880012143' + setpoint_hex + '\r\n'  # Set setpoint
        response = self.comm(set_setpoint)
        response_check = response[5:].strip()
        if response_check == '000007':
            success = True
            self.debug_logger.info(self.object_id, "Setpoint: " + str(setpoint_mbar) + "mbar.")
            self.config.write(self.object_id, "setpoint_mbar", setpoint_mbar)
        else:
            success = False
            self.debug_logger.warning(self.object_id, "Failed to apply setpoint.")
        return success

    def ask_instrument_status(self):
        status = 5
        # TODO: get real status from instrument (see to_state_manual 9.17.027 §3.6 p17)
        return status

    def __update_record__(self):
        self.record["pressure"] = self.read_flow()
        
    def _reset_record_(self):
        self.record["pressure"] = -999

    def get_data_logger_header_list(self):
        return ["pressure"]