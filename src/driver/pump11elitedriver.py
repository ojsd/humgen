import re
import threading
import time
from datetime import datetime, timedelta

import serial

from debuglogger import DebugLogger
from driver.serialdriver import SerialDriver
from config import Config


class Pump11EliteDriver(SerialDriver):
    """
    Driver for syringe pump "Pump 11 Pico Plus Elite - Harvard Apparatus"
    For details, see the following document:
    "Pump 11 Elite & Pump 11 Pico Plus Elite
     User's manual
     Publication 5420-002 Rev 1.0
     § External Pump Control, page 50"
    """

    def __init__(self,
                 enabled: bool,
                 product: str,
                 debug_logger: DebugLogger,
                 object_id: str,
                 config: Config,
                 com_lock: threading.Lock = None):
        # Set some global variables
        self.prompt_value = [":", "<", ">", "*", "T*"]
        self.prompt_pattern = "(:|<|>|T\*|\*)"
        self.volume_units = {"ml": 3, "ul": 6, "nl": 9, "pl": 12, "fl": 15}
        self.default_volume_unit = config.read(object_id, "default_volume_unit")
        self.time_units = {"msec": 0.001, "sec": 1, "min": 60, "hr": 3600}
        self.default_time_unit = config.read(object_id, "default_time_unit")
        
        # Initialize "status" variables
        self.is_moving = False
        self.stalled = False
        self.direction = ''
        
        # Initialize debug_logger and config
        self.debug_logger = debug_logger
        self.object_id = object_id
        self.config = config

        # Initialize data record with void values
        self._reset_record_()

        # Enabled / disabled
        if not enabled:
            self.set_status_code(1)
            return
        else:
            self.set_status_code(2)
        
        # Initialize serial connection
        super(Pump11EliteDriver, self).__init__(enabled,
                                                product=product,
                                                baudrate=115200,
                                                parity=serial.PARITY_NONE,
                                                stopbits=serial.STOPBITS_ONE,
                                                bytesize=serial.EIGHTBITS,
                                                timeout=0.1,
                                                debug_logger=debug_logger,
                                                object_id=object_id)
        
        # Initialize lock used for serial communication
        if com_lock is None:
            self.com_lock = threading.RLock()
        else:
            self.com_lock = com_lock

        # Exit if pump is not connected
        if self.get_status_code() < 5:
            return

        # Initialize rate limits
        self.infusion_rate_limits = self.__get_rate_limits__("i")
        self.withdraw_rate_limits = self.__get_rate_limits__("w")

        # Initialize maximum pumping volume
        self.max_pumping_volume = self.__convert_volume_unit__(volume_in=config.read(object_id, "max_pumping_volume_ul"),
                                                               unit_in="ul",
                                                               unit_out=self.default_volume_unit)

        # Initialize variables for volume tracking
        self._is_calibrating = False

        # Initialize data record with real values
        self.__update_status__()
        if self.record["direction"] == "W":
            self.record.update({"irate": self.get_infusion_rate(),
                                "ivolume": self.get_infused_volume()})
        elif self.record["direction"] == "I":
            self.record.update({"wrate": self.get_withdraw_rate(),
                                "wvolume": self.get_withdrawn_volume()})

        # Launch status thread
        a = threading.Thread(target=self.__thread_status__)
        a.daemon = True
        a.start()

    def __send_command__(self, command: str):                        
        # Send command        
        self.debug_logger.debug(self.object_id, "########## COMMAND: ###############\n" + command)
        command_byte = (command + "\r").encode()

        attempt = 0
        success = False
        response_timeout = 3  # Number of seconds to wait response's prompt pattern

        while attempt <= 3 and not success:
            attempt += 1
            self.com_lock.acquire()
            self.serial_connection.write(command_byte)

            # Read instrument's response to command: read bytes until prompt pattern is received.
            break_anyway = datetime.now() + timedelta(seconds=response_timeout)
            while datetime.now() < break_anyway:
                response = self.serial_connection.read(1000)
                if re.search(self.prompt_pattern, response.decode()):
                    success = True
                    break
            self.com_lock.release()

        if success:
            self.debug_logger.debug(self.object_id,
                                    "---------- RESPONSE: ----------\n"
                                    + response.decode() + "\n"
                                    + "########## END ###############")
            return response.decode()
        else:
            self.debug_logger.error(self.object_id,
                                    "Command [" + command + "] did not respond a valid message, even after 3 attempts.")
            return False

    def set_infusion_rate(self, rate: float):
        self.debug_logger.info(self.object_id, "Set infusion rate: " + str(rate) +
                               self.default_volume_unit + "/" + self.default_time_unit)
        return self.__set_rate__(rate, "i")

    def get_infusion_rate(self):
        return self.__get_rate__("i")

    def get_infusion_rate_from_record(self):
        return self.record["irate"]

    def get_infusion_rate_limits(self):
        return self.infusion_rate_limits

    def infuse(self):
        # Todo OJ: Check response
        if not self._is_calibrating:
            self.set_target_volume(self.target_volume_I)
        self.debug_logger.info(self.object_id, "Sending 'infuse' order")
        response = self.__send_command__("irun")
        self.__update_status__()
        return response

    def run(self):
        self.debug_logger.info(self.object_id, "Sending 'run' order")
        response = self.__send_command__("run")
        self.__update_status__()
        return response

    def reverse(self):
        self.debug_logger.info(self.object_id, "Sending 'reverse run' order")
        response = self.__send_command__("rrun")
        self.__update_status__()
        return response

    def set_withdraw_rate(self, rate: float):
        self.debug_logger.info(self.object_id, "Set withdraw rate: "
                               + str(rate) + self.default_volume_unit + "/" + self.default_time_unit)
        return self.__set_rate__(rate, "w")

    def get_withdraw_rate(self):
        return self.__get_rate__("w")

    def get_withdraw_rate_from_record(self):
        return self.record["wrate"]

    def get_withdraw_rate_limits(self):
        return self.withdraw_rate_limits

    def withdraw(self):
        if not self._is_calibrating:
            self.set_target_volume(self.target_volume_W)
        self.debug_logger.info(self.object_id, "Sending 'withdraw' order")
        response = self.__send_command__("wrun")
        self.__update_status__()
        return response

    def __set_rate__(self, rate: float, pumping_way: str):
        if pumping_way not in ["i", "w"]:
            raise ValueError("Invalid type")

        # Check that to-be-set rate is within acceptable range
        rate_limits = self.__get_rate_limits__(pumping_way)
        if not rate_limits[0] <= rate <= rate_limits[1]:
            raise ValueError("Rate value out of range")

        response = self.__send_command__(pumping_way + "rate " + str(rate)
                                         + " " + self.default_volume_unit + "/" + self.default_time_unit)
        return response

    def __get_rate__(self, pumping_way: str):
        if pumping_way not in ["i", "w"]:
            raise ValueError("Invalid type")
        response = self.__send_command__(pumping_way + "rate")
        message = self.__split_response__(response)["message"]
        rate = self.__decode_rate_string__(message)
        return rate

    def __get_rate_limits__(self, pumping_way: str):
        # Check input paramters
        if pumping_way not in ["i", "w"]:
            error_log = "Pumping way not valid: " + pumping_way
            self.debug_logger.critical(self.object_id, error_log)
            raise ValueError(error_log)
        
        # Get message
        response = self.__send_command__(pumping_way + "rate lim")
        message = self.__split_response__(response)["message"]

        if ("Unknown command" in message) | ("Command" in message):
            self.debug_logger.error(self.object_id, "Device responded: 'Unknown command'")
            return 0, 0

        # Split message to get min and max strings
        min_max = message.split(" to ")

        # Convert min and max string to float
        rate_min = self.__decode_rate_string__(min_max[0])
        rate_max = self.__decode_rate_string__(min_max[1])

        return rate_min, rate_max

    def __decode_rate_string__(self, rate_str: str):
        rate_str = rate_str.split(" ")
        rate_value = float(rate_str[0])
        rate_unit = rate_str[1]
        rate = self.__convert_rate_unit__(rate_in=rate_value,
                                          rate_unit_in=rate_unit,
                                          volume_unit_out=self.default_volume_unit,
                                          time_unit_out=self.default_time_unit)
        return rate

    def __decode_volume_string__(self, volume_str: str, volume_unit_out: str):
        volume_str = volume_str.split(" ")        
        try:
            volume_value_in = float(volume_str[0])
        except:
            volume = -999
        else:
            volume_unit_in = volume_str[1]
            volume = self.__convert_volume_unit__(volume_in=volume_value_in,
                                                  unit_in=volume_unit_in,
                                                  unit_out=volume_unit_out)
        return volume

    def stop(self):
        response = self.__send_command__("stp")
        self.__update_status__()
        return response

    def set_syringe_volume(self, volume: float) -> bool:
        success = self.__set_volume__(volume, "s")
        return success

    def get_syringe_volume(self) -> float:
        return self.__get_volume__("s")

    def set_target_volume(self, volume: float) -> bool:
        return self.__set_volume__(volume, "t")

    def get_target_volume(self) -> float:
        return self.__get_volume__("t")

    def clear_target_volume(self) -> bool:
        return self.__clear_volume__("t")

    def get_infused_volume(self) -> float:
        return self.__get_volume__("i")

    def get_infused_volume_from_record(self) -> float:
        return self.record["ivolume"]

    def clear_infused_volume(self) -> bool:
        return self.__clear_volume__("i")

    def get_withdrawn_volume(self) -> float:
        return self.__get_volume__("w")

    def get_withdrawn_volume_from_record(self) -> float:
        return self.record["wvolume"]

    def clear_withdrawn_volume(self) -> bool:
        return self.__clear_volume__("w")

    def set_syringe_diameter(self, diameter: float):
        self.__send_command__("diameter " + str(diameter))

        # Get diameter from instrument to check if it has correctly been set
        success = self.get_syringe_diameter() == diameter
        return success

    def get_syringe_diameter(self) -> float:
        response = self.__send_command__("diameter")
        message = self.__split_response__(response)["message"]
        if message is None:
            raise ValueError("There is no 'message' part in response")
        diameter_str = message.split(" ")
        diameter = float(diameter_str[0])
        return diameter

    def ask_instrument_status(self):
        return 5

    def reset_to_start(self):
        # Go to bumper
        self.set_withdraw_rate(max(self.withdraw_rate_limits))
        self.withdraw()
        while True:
            if self.stalled:
                break
            time.sleep(0.4)

        # Go to 2.5%
        self.set_infusion_rate(max(self.infusion_rate_limits))
        self.infuse()
        self.set_target_volume(self.max_pumping_volume * 0.025)
        while self.is_moving:
            self.debug_logger.debug(self.object_id, "Moving to 2.5%")

    def calibrate_syringe(self):
        """
        Determine the syringe volume which is really usable.
        The pump's bumpers might be placed so that it is not possible to pump the full content of the syringe.
        Moreover, for safety reasons, we use only the middle 95% of the possible course.
        """
        self.debug_logger.info(self.object_id, "Pump calibration: Starting sequence")
        
        # ---- Infusing at full speed, until bumper is reached ----
        self.stop()
        self._is_calibrating = True
        
        self.set_infusion_rate(max(self.infusion_rate_limits))
        self.clear_target_volume()
        self.infuse()
        self.debug_logger.info(self.object_id, "Pump calibration: Infusing until bumper is reached")
        
        while True:
            if not self.stalled:
                self.debug_logger.debug(self.object_id, "Pump calibration: Infusing...")
            else:
                self.debug_logger.info(self.object_id, "Pump calibration: Pump stalled")
                break
            time.sleep(0.5)
        self.stop()
        
        # ---- Withdrawing at full speed, until bumper is reached ----
        self.clear_withdrawn_volume()  # Maximum pumping volume will be measured at this step
        self.set_withdraw_rate(max(self.withdraw_rate_limits))
        self.withdraw()
        self.debug_logger.info(self.object_id, "Pump calibration: Withdrawing until bumper is reached")

        while True:
            if not self.stalled:
                self.debug_logger.debug(self.object_id, "Pump calibration: Withdrawing...")
            else:
                self.debug_logger.info(self.object_id, "Pump calibration: Pump stalled")
                break
            time.sleep(0.5)
        self.stop()

        max_pumping_volume = self.get_withdrawn_volume()
        
        # ---- Go to withdraw-bumper - 2.5% ----
        self.clear_infused_volume()
        self.set_target_volume(max_pumping_volume*0.025)
        self.infuse()
        while self.is_moving:
            self.debug_logger.debug(self.object_id, "Pump calibration: Moving to 2.5%")

        max_pumping_volume *= 0.95  # Keep only 95% of the measured volume

        # Write max_pumping_volume to config file
        self.config.write(self.object_id, "max_pumping_volume_ul",
                          self.__convert_volume_unit__(max_pumping_volume, self.default_volume_unit, "ul"))
 
        self.max_pumping_volume = max_pumping_volume
        self.clear_target_volume()
        self.clear_withdrawn_volume()
        self.clear_infused_volume()
        self.force_status()
        self._is_calibrating = False

        return max_pumping_volume

    def __split_response__(self, response: str) -> dict:
        """
        Split the response in two:

        * "message" contains the response's message without line return characters
        * "prompt" contains the prompt character(s) ending a response.

        :param response: Text of the full reponse.
        :return: Dictionnary containing message and prompt.
        """
        # Find the "message" part of the response
        try:
            message = re.search("\n(.*?)\r", response).group(1)
        except AttributeError:
            # No message found
            message = None

        # Find the "prompt" part of the response
        try:
            prompt = re.search("[\S\s]*\n[0-9]{0,2}"+self.prompt_pattern, response).group(1)
        except AttributeError:
            # No message found
            prompt = None

        return {"message": message, "prompt": prompt}

    def __convert_volume_unit__(self, volume_in: float, unit_in: str, unit_out: str) -> float:
        """
        Convert a volume given in [unit_in] to [unit_out]
        :param volume_in: Input volume value
        :type volume_in: float
        :param unit_in: Input volume unit ("ml", "ul", "nl", etc.)
        :type unit_in: str
        :param unit_out: Output volume unit ("ml", "ul", "nl", etc.)
        :type unit_out: str
        :return: Input volume converted to the requested unit.
        """
        if unit_in == unit_out:
            return volume_in
        else:
            conversion_factor = 10 ** - (self.volume_units[unit_in] - self.volume_units[unit_out])
            volume_out = volume_in * conversion_factor
            return volume_out

    def __convert_time_unit__(self, time_in: float, unit_in: str, unit_out: str) -> float:
        if unit_in == unit_out:
            return time_in
        else:
            conversion_factor = self.time_units[unit_in] / self.time_units[unit_out]
            volume_out = time_in * conversion_factor
            return volume_out

    def __convert_rate_unit__(self, rate_in: float, rate_unit_in: str = None, rate_unit_out: str = None,
                              volume_unit_in: str = None, volume_unit_out: str = None, time_unit_in: str = None,
                              time_unit_out: str = None):
        if rate_unit_in is not None:
            split = rate_unit_in.split("/")
            volume_unit_in = split[0]
            time_unit_in = split[1]
        if rate_unit_out is not None:
            split = rate_unit_out.split("/")
            volume_unit_out = split[0]
            time_unit_out = split[1]

        # Convert volume
        rate_out = self.__convert_volume_unit__(rate_in, volume_unit_in, volume_unit_out)
        # Convert time. /!\ Reverse unit_in and unit_out, because time is the denominator
        rate_out = self.__convert_time_unit__(rate_out, time_unit_out, time_unit_in)
        return rate_out

    def __get_volume__(self, volume_type: str) -> float:
        """
        Get the "volume_type" volume (in the requested unit).
        :param volume_type: Type of volume. Can be "i" (infuse), "w" (withdraw), "s" (syringe) or "t" (target).
        :type volume_type: str
        :return: Volume, as known by the instrument.
        :rtype: float
        """
        if volume_type not in ["i", "w", "s", "t"]:
            raise ValueError("Invalid volume type")
        response = self.__send_command__(volume_type + "volume")
        message = self.__split_response__(response)["message"]
        if message is None:
            self.debug_logger.error(self.object_id, "There is no 'message' part in response")
            return -999

        if message == "Target volume not set.":
            volume = 0
        elif message == "Target volume not set":
            volume = 0
        else:
            volume = self.__decode_volume_string__(volume_str=message,
                                                   volume_unit_out=self.default_volume_unit)
        return volume

    def __set_volume__(self, volume: float, volume_type: str):
        if volume_type not in ["s", "t"]:
            raise ValueError("Invalid volume type")
        self.__send_command__(volume_type + "volume " + str(volume) + " " + self.default_volume_unit)

        # Get volume from instrument to check if it has correctly been set
        read_volume = self.__get_volume__(volume_type)
        success = (read_volume == volume)
        if not success:
            self.debug_logger.debug(self.object_id, "Failed to set volume")
        return success

    def __clear_volume__(self, volume_type: str):
        if volume_type not in ["i", "w", "t"]:
            raise ValueError("Invalid volume type")
        self.__send_command__("c" + volume_type + "volume")
        # Get volume from instrument to check if it has correctly been cleared
        read_volume = self.__get_volume__(volume_type)
        return read_volume == 0.0

    ####################################################################################################################
    # Status
    def __update_status__(self):
        """
        Update the 3 status variables (stalled, is_moving and direction) and the "record" dict.
        See Pump manual p57 for details about STATUS message content.
        """
        # Get pump's response to STATUS command
        response = self.__send_command__("status")
        message = self.__split_response__(response)["message"]
        if message is None:
            self.debug_logger.warning(self.object_id, "Status command returned empty status")
            return None

        # Split the response in 4 fields
        status_fields = message.split(' ')
        if len(status_fields) != 4:
            error_log = "The 4 expected status fields were not found"
            self.debug_logger.error(self.object_id, error_log)
            self._reset_record_()
            return None

        # Field 0: i/w rate (from fl/sec to ul/sec)
        pump_rate = self.__convert_rate_unit__(rate_in=int(status_fields[0]),
                                               rate_unit_in="fl/sec",
                                               volume_unit_out=self.default_volume_unit,
                                               time_unit_out=self.default_time_unit)

        # Field 1: i/w time (milliseconds)
        pumped_time = self.__convert_time_unit__(time_in=int(status_fields[1]),
                                                 unit_in="msec",
                                                 unit_out=self.default_time_unit)

        # Field 2: i/w volume (fl)
        pumped_volume = self.__convert_volume_unit__(volume_in=int(status_fields[2]),
                                                     unit_in="fl",
                                                     unit_out=self.default_volume_unit)

        # Field 3: flags
        flag_field = status_fields[3]
        self.stalled = flag_field[2] == 'S'
        if flag_field[0] == 'I' or flag_field[0] == 'W':
            self.is_moving = True
        else:
            self.is_moving = False
        self.direction = str.upper(flag_field[0])

        self.debug_logger.debug(self.object_id,
                                "Stalled: " + str(self.stalled)
                                + " - Moving: " + str(self.is_moving)
                                + " - Direction: " + self.direction)

        self.record.update({"moving": self.is_moving,
                            "stalled": self.stalled,
                            "direction": self.direction})
        if self.direction == "I":
            self.record.update({"irate": pump_rate,
                                "ivolume": pumped_volume,
                                "itime": pumped_time})
        else:
            self.record.update({"wrate": pump_rate,
                                "wvolume": pumped_volume,
                                "wtime": pumped_time})
            
        # Update rate and volume for pumping way not initialized at startup
        if self.record["irate"] is None:
            irate = self.get_infusion_rate()
            ivolume = self.get_infused_volume()
            self.record.update({"irate": irate,
                                "ivolume": ivolume})
        if self.record["wrate"] is None:
            wrate = self.get_withdraw_rate()
            wvolume = self.get_withdrawn_volume()
            self.record.update({"wrate": wrate,
                                "wvolume": wvolume})

        if not self._is_calibrating:
            self.target_volume_I = self.max_pumping_volume + self.get_withdrawn_volume()
            self.target_volume_W = self.get_infused_volume()
        
        return True
    
    def force_status(self):        
        ivolume = self.get_infused_volume()
        if ivolume is not None:
            self.record.update({"ivolume": ivolume})
        wvolume = self.get_withdrawn_volume()
        if wvolume is not None:
            self.record.update({"wvolume": wvolume})
        return 0

    def __thread_status__(self):
        """
        Thread which periodically asks the status of the pump and update the 3 status variables
        """
        while True:
            state = self.__update_status__()
            #self.force_status()
            #je viens de virer ça, car normalement plus necessaire. 
            if state is None:
                continue
            time.sleep(0.5)

    def __update_record__(self):
        """Mandatory instanciation of parent's method, but for the pump, this functionnality is managed by
        the __update_status__ function."""
        pass

    def get_data_logger_header_list(self):
        return ["moving", "direction", "irate", "ivolume", "wrate", "wvolume"]
    
    def _reset_record_(self):        
        self.record = {"moving": -999,
                       "stalled": -999,
                       "direction": -999,
                       "irate": -999,
                       "ivolume": -999,
                       "itime": -999,
                       "wrate": -999,
                       "wvolume": -999,
                       "wtime": -999}

