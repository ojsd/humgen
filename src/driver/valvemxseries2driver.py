import threading
import warnings
import serial

from debuglogger import DebugLogger
from config import Config
from driver.serialdriver import SerialDriver


class ValveMxSeries2Driver(SerialDriver):
    """
    Driver for IDEX MX Series II modules through USB.
    MX II Series uses an FTDI FT232R chip to translate the UART communication into USB.
    See IDEX document #2321382G "UART/USB Communication Protocol for TitanEX/TitanEZ/TitanHP, TitanHT Driver Boards
    and MX Series II TM Modules" for detailed information about communication protocol.

    CAUTION!
    When controlling the module via I2C, RS-232, or USB, make certain the module is not set to Level Logic control. Any
    other setting (BCD, Pulse logic, etc.) is acceptable.
    Use the "F" command (see page 4 of the above-mentionned documentation for details) to change the "valve command mode"
    and restart the module (Power off then on) to apply the change.
    """

    def __init__(self, enabled: bool,
                 product: str,
                 debug_logger: DebugLogger,
                 object_id: str,
                 config: Config,
                 com_lock: threading.Lock = None):
        self.possible_valve_positions = [1, 2]
        self.error_codes = [44, 55, 66, 77, 88, 99]
        
        # Initialize logger and config
        self.debug_logger = debug_logger
        self.object_id = object_id
        self.config = config
        
        # Initialize lock used for serial communication 
        if com_lock is None:
            self.com_lock = threading.Lock()
        else:
            self.com_lock = com_lock

        super(ValveMxSeries2Driver, self).__init__(enabled,
                                                   product=product,
                                                   baudrate=19200,
                                                   parity=serial.PARITY_NONE,
                                                   stopbits=serial.STOPBITS_ONE,
                                                   bytesize=serial.EIGHTBITS,
                                                   timeout=1,
                                                   debug_logger=debug_logger,
                                                   object_id=object_id)

        # Initialize data record with void values
        self.record = {"position": -999}        

        # Launch record thread
        self._launch_thread_record_()

    def __send_command__(self, command: str, expected_data_bytes: int = 0, end_cr: bool = False) -> str:
        """
        Send a command to the instrument

        :param command: Command to be sent to the instrument
        :type command: str
        :param expected_data_bytes: Number of data bytes expected in instrument's response
        :type expected_data_bytes: int
        :param end_cr: If true, an \CR byte is expected at the end of instrument's response to command
        :type end_cr: bool
        :return: Response of the Valve to the command
        :rtype: str
        """

        # Format command
        command_r = command + "\r"  # Append \CR character
        command_byte = command_r.encode()  # Encode to byte
        self.debug_logger.debug(self.object_id, "########## COMMAND: ###############\n" + command)

        serial_connection = self.serial_connection
        self.com_lock.acquire()
        serial_connection.write(command_byte)

        if end_cr:
            expected_response_bytes = expected_data_bytes + 1
        else:
            expected_response_bytes = expected_data_bytes

        response_byte = serial_connection.read(expected_response_bytes)
        self.com_lock.release()

        if len(response_byte) != expected_response_bytes:
            # When "P" command does not require a valid position, the valve2x3 returns nothing (not even \n).
            if command[0] == "P" and len(response_byte) == 0:
                return "ERROR. Position number not valid"
            else:
                raise ValueError("Response does not have expected size", len(response_byte), expected_response_bytes)

        # Format response
        response_string = response_byte.decode()  # Convert to string
        if end_cr:
            response_string = response_string.strip('\r')  # Remove trailing \r

        self.debug_logger.debug(self.object_id,
                                "---------- RESPONSE: ----------\n"
                                + response_string + "\n"
                                + "########## END ###############")
        
        return response_string

    def set_position(self, position: int) -> bool:
        """
        Change the valve2x3 position.

        :param position: Required valve2x3 position
        :type position: int
        :return: This function checks the valve2x3 status after a position change. If the returned position matches the
        required position, return True, otherwise False.
        :rtype: bool
        """

        position_string = "%02X" % position  # String representing position hexa number in 2 digits with leading zero
        command = "P" + position_string
        self.__send_command__(command, 0, True)
        
        position_changed = self.get_position() == position
        if position_changed:
            self.debug_logger.info(self.object_id, "Position changed to #" + str(position))
        else:
            self.debug_logger.error(self.object_id, "Failed to change to position #" + str(position))
            
        return position_changed

    def set_position_to_chambers(self) -> bool:
        """
        Change the valve to the "To Chambers" position.

        :return: True if position change was successful.
        :rtype: bool
        """
        success = self.set_position(self.config.read(self.object_id, "position_to_chambers"))
        return success

    def set_position_from_standards(self) -> bool:
        """
        Change the valve to the "From Standards" position.

        :return: True if position change was successful.
        :rtype: bool
        """
        success = self.set_position(self.config.read(self.object_id, "position_from_standards"))
        return success

    def get_position(self) -> int:
        """
        Get the valve2x3's status: either the valve2x3 position (1-12) or an error code:

        * 99 – valve2x3 failure (valve2x3 can not be homed)
        * 88 – non-volatile memory error
        * 77 – valve2x3 configuration error or command mode error
        * 66 – valve2x3 positioning error
        * 55 – data integrity error
        * 44 – data CRC error

        :return: Valve status
        """
        response = self.__send_command__("S", 2, True)
        status = self.__format_hex__(response)
        if status > 12:
            self.debug_logger.error(self.object_id, "Valve returned error status: " + str(status))
        return status

    def get_position_string(self) -> str:
        """
        Get the valve2x3 position as a string. Either "to_chambers" or "from_standards".

        :rtype: str
        """
        position_int = self.get_position()
        if position_int == self.config.read(self.object_id, "position_to_chambers"):
            return "to_chambers"
        elif position_int == self.config.read(self.object_id, "position_from_standards"):
            return "from_standards"
        else:
            return "unknown _position"

    def get_command_mode(self) -> int:
        """
        Get the valve2x3 command mode. See set_command_mode() for details.
        :return: Command mode between 1 and 5.
        :rtype: int
        """
        response = self.__send_command__("D", 2, True)
        command_mode = self.__format_hex__(response)
        return command_mode

    def set_command_mode(self, command_mode: int):
        """
        Set the valve2x3 command mode:

        * 1 = Level logic
        * 2 = Single pulse logic
        * 3 = BCD logic
        * 4 = Inverted BCD logic
        * 5 = Dual pulse logic

        See IDEX document #2321500C "Driver/Controller Development Assistance Package For IDEX Health & Science MX II"
        for detailed information.

        :param command_mode: Valve command mode identifier (1 to 5)
        :type command_mode: int
        :return: Nothing.
        """
        command_mode = "%02X" % command_mode  # String representing position hexa number in 2 digits with leading zero
        command = "F" + command_mode
        self.__send_command__(command, 0, True)

    def __format_hex__(self, hexa: str) -> int:
        """
        Convert hexa string to integer.
        :param hexa: A string containing an hexadecimal-formatted integer (expl "01", "A7", etc.)
        :type hexa: str
        :return: The hexa number converted to integer.
        :rtype: int
        """
        try:
            integer = int(hexa, 16)
        except:
            raise ValueError("Input is not a valid number")
        return integer

    def __check_command_mode__(self):
        """
        Check if the valve2x3 command mode is "BCD logic". This mode is valid for all kind of Valve, whereas
        "Pulse logic" or "Dual pulse logic" are only applicable for 2-positions valves, for example.
        So mode "BCD logic" (3) is the safest and has the widest compatibility.
        If the current mode is not correct, change it to 3 and ask for hard reset in order to effectively apply the
        change, and set the current driver as inactive.
        :return: Nothing.
        """
        valve_command_mode = self.get_command_mode()
        if valve_command_mode != 3:
            self.set_command_mode(3)
            warnings.warn("The valve2x3 command mode was not 'BCD Logic', which the most reliable."
                          "The problem has been automatically corrected by a power reset of the valve2x3 is required")
            self.set_status_code(4)

    def ask_instrument_status(self):
        position = self.get_position()
        if position in self.possible_valve_positions:
            status_code = 5
        elif position in self.error_codes:
            status_code = 4
        elif position == "":
            status_code = 3
        else:
            status_code = 4
        self.set_status_code(status_code)
        return status_code

    def __update_record__(self):
        self.record["position"] = self.get_position()
        
    def _reset_record_(self):
        self.record["position"] = -999

    def get_data_logger_header_list(self):
        return ["position"]