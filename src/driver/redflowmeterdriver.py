import threading
import sys
import traceback
from time import time, sleep


from PyExpLabSys.drivers import vogtlin
from driver.serialdriver import SerialDriver
from serial import SerialException

from debuglogger import DebugLogger
from driver.instrumentdriver import InstrumentDriver


class RedFlowMeterDriver(vogtlin.RedFlowMeter, InstrumentDriver):
    data_type_mapping = {
        'f32': 'float',
        'u32': 'long',
        'u16': 'register',
        's8': 'string'
    }

    control_function_mapping = {
        "Automatic setpoint": 0,
        "Digital setpoint": 1,
        "Analog setpoint": 2,
        "Valve control": 10,
        "0%": 20,
        "100%": 21,
        "Fully closed": 22,
        "Fully open": 23,
        "Test mode analog": 30,
        "Test mode DAC": 31
    }

    """Class managing the GSC-A9TS-DD22 flow controller (Vogtlin)"""
    def __init__(self, enabled: bool,
                 product: str,
                 debug_logger: DebugLogger,
                 object_id: str,
                 com_lock: threading.Lock = None,
                 address: int = 247):

        # Initialize logger
        self.debug_logger = debug_logger
        self.object_id = object_id

        # Enabled / disabled
        if not enabled:
            self.set_status_code(1)
            return
        else:
            self.set_status_code(2)            
        
        # Open serial connection
        self.address = address
        self.port = SerialDriver.get_port(product)
        serial_com_kwargs = {'CLOSE_PORT_AFTER_EACH_CALL': True}
        try:
            super(RedFlowMeterDriver, self).__init__(self.port, address, **serial_com_kwargs)
        except SerialException:
            self.set_status_code(2)
            return
        else:
            self.set_status_code(5)

        # Define wait_time: time to wait before to serial messages
        # At least 3.5 char (see smart_digi_com_E1_5 document p7)
        self.wait_time = 0.008 / 9600 * self.serial_com_kwargs['BAUDRATE']

        # Variables representing the last known order (used to recover from reset)
        self.last_known_setpoint = None
        self.last_known_control_function = None
        self.reseting = False



        # Initialize lock used for serial communication 
        if com_lock is None:
            self.com_lock = threading.Lock()
        else:
            self.com_lock = com_lock

        # Initialize data record with void values
        self._reset_record_()

        # Launch record thread
        self._launch_thread_record_()

    def __read_value__(self, register, data_type, number_of_registers=4):
        # Ensure wait time
        sleep(max(0, self.wait_time - (time() - self._last_call)))

        method_name = "read_" + self.data_type_mapping[data_type]
        method = getattr(self.instrument, method_name)

        value = -999
        loop = 0
        while value == -999 and loop <= 2:
            self.com_lock.acquire()
            if self.data_type_mapping[data_type] == "string":
                try:
                    value = method(register, number_of_registers)
                except:
                    self.debug_logger.warning(self.object_id, "Read error [" + method_name + "][" + str(register) + "]")
                    self.debug_logger.warning(self.object_id, traceback.format_exc())
                    sleep(3)
            else:                
                try:
                    value = method(register)
                except:
                    self.debug_logger.warning(self.object_id, "Read error [" + method_name + "][" + str(register) + "]")
                    self.debug_logger.warning(self.object_id, traceback.format_exc())
                    sleep(3)
            self.com_lock.release()
            loop += 1

        if loop > 2:
            self.debug_logger.error(self.object_id, "Repeated read error! [" + method_name + "][" + str(register) + "]")
            self.debug_logger.warning(self.object_id, "Reseting device due to repeated errors")
            self.reset_instrument()

        # Set last call time
        self._last_call = time()
        return value

    def __write_value__(self, register, data_type, value):
        # Ensure wait time
        sleep(max(0, self.wait_time - (time() - self._last_call)))

        # Determine ModBus method
        method_name = "write_" + self.data_type_mapping[data_type]
        method = getattr(self.instrument, method_name)

        # Write value
        status = "KO"
        loop = 0
        while status == "KO" and loop <= 2:
            self.com_lock.acquire()
            try:
                method(register, value)
            except:
                self.debug_logger.warning(self.object_id, "Write error [" + method_name + "]")
                self.debug_logger.warning(self.object_id, traceback.format_exc())
                status = "KO"
                sleep(3)
            else:
                status = 'OK'
            self.com_lock.release()
            loop += 1

        if loop > 2:
            self.debug_logger.error(self.object_id, "Repeated write error! [" + method_name + "]")

        # Set last call time
        self._last_call = time()

    def get_gas_flow(self):
        gas_flow = self.__read_value__(0x0000, "f32")
        self.debug_logger.debug(self.object_id, "Gas flow = " + str(gas_flow))
        return gas_flow

    def get_temperature(self):
        temperature = self.__read_value__(0x0002, "f32")
        self.debug_logger.debug(self.object_id, "Temperature = " + str(temperature))
        return temperature

    def get_setpoint_gas_flow(self):
        setpoint_gas_flow = self.__read_value__(0x0006, "f32")
        self.debug_logger.debug(self.object_id, "Setpoint gas flow = " + str(setpoint_gas_flow))
        return setpoint_gas_flow

    def set_setpoint_gas_flow(self, value):
        # TODO: Be sure about the unit!
        self.__write_value__(0x0006, "f32", value)
        self.last_known_setpoint = value
        self.debug_logger.debug(self.object_id, "Setpoint gas flow set to: " + str(value))

    def get_valve_control_signal(self):
        valve_control_signal = self.__read_value__(0x000a, "f32")
        self.debug_logger.debug(self.object_id, "Valve control signal = " + str(valve_control_signal))
        return valve_control_signal

    def set_valve_control_signal(self, value):
        self.__write_value__(0x000a, "f32", value)
        self.debug_logger.debug(self.object_id, "Valve control signal set to: " + str(value))

    def get_alarms(self):
        alarms = self.__read_value__(0x000c, "u16")
        self.debug_logger.debug(self.object_id, "Alarms = " + str(alarms))
        return alarms

    def get_hardware_errors(self):
        hardware_errors = self.__read_value__(0x000d, "u16")
        self.debug_logger.debug(self.object_id, "Hardware errors = " + str(hardware_errors))
        return hardware_errors

    def get_control_function(self):
        control_function = self.__read_value__(0x000e, "u16")
        self.debug_logger.debug(self.object_id, "Control function = " + str(control_function))
        return control_function

    def get_control_function_as_string(self) -> str:
        control_function = self.get_control_function()
        # Revert dict
        revert_mapping = dict(zip(self.control_function_mapping.values(), self.control_function_mapping.keys()))
        control_function_string = revert_mapping[control_function]
        return control_function_string

    def set_control_function(self, value):
        self.__write_value__(0x000e, "u16", value)
        self.last_known_control_function = value
        self.debug_logger.debug(self.object_id, "Control function set to: " + str(value))

    def set_control_fully_open(self):
        self.set_control_function(23)

    def set_control_fully_closed(self):
        self.set_control_function(22)

    def set_control_digital_setpoint(self):
        self.set_control_function(1)

    def get_device_address(self):
        device_address = self.__read_value__(0x0013, "u16")
        self.debug_logger.debug(self.object_id, "Device address = " + str(device_address))
        return device_address

    def set_device_address(self, value):
        self.__write_value__(0x0013, "u16", value)
        self.debug_logger.debug(self.object_id, "Device address set to: " + str(value))

    def get_serial_number(self):
        serial_number = self.__read_value__(0x001e, "u32")
        self.debug_logger.debug(self.object_id, "Serial number = " + str(serial_number))
        return serial_number

    def reset_hardware_errors(self):
        self.__write_value__(0x404f, "u16", 32768)  # Clear all hardware errors
        self.debug_logger.debug(self.object_id, "Hardware errors reset")

    def soft_reset(self):
        self.__write_value__(0x0034, "u16", 1)  # Write any value to this register to soft reset
        self.debug_logger.debug(self.object_id, "Soft reset")

    def reset_instrument(self):
        print("RESETING")
        self.reseting = True
        self.soft_reset()
        self.reset_hardware_errors()
        self.set_setpoint_gas_flow(self.last_known_setpoint)
        self.set_control_function(self.last_known_control_function)
        self.reseting = False

    def ask_instrument_status(self):
        status = 5
        # TODO: get real status from instrument
        return status

    def __update_record__(self):
        self.record.update({"flow": self.get_gas_flow(),
                            "temperature": self.get_temperature(),
                            "setpoint": self.get_setpoint_gas_flow()})
        
    def __thread_record__(self):
        while True:
            if not self.reseting:
                self.__update_record__()
            else:
                print("Reseting: __update_record__ disabled")
            sleep(0.4)

    def _reset_record_(self):
        self.record = {"flow": -999,
                       "temperature": -999,
                       "setpoint": -999}

    def get_data_logger_header_list(self):
        return ["flow", "setpoint", "temperature"]