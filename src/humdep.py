import threading
import os
import csv
import datetime
from time import sleep

from debuglogger import DebugLogger
from config import Config
from driver.humgendriver import HumgenDriver


class HumDep:

    def __init__(self, humgen: HumgenDriver, config: Config, debug_logger: DebugLogger, object_id: str):
        self.humgen = humgen
        self.config = config
        self.debug_logger = debug_logger
        self.object_id = object_id
        self.calib_ongoing = False
        self.calib_should_be_stopped = True

    def launch(self):
        if not self.calib_ongoing:
            self.calib_should_be_stopped = False
            thread_record = threading.Thread(target=self.__thread_humdep__)
            thread_record.daemon = True
            thread_record.start()
        else:
            self.debug_logger.warning(self.object_id, "Humidity calibration is already ongoing. Please stop it first.")

    def stop(self):
        if not self.calib_should_be_stopped:
            self.debug_logger.info(self.object_id, "Stopping humidity calibration...")
            self.calib_should_be_stopped = True

    def __thread_humdep__(self):
        self.debug_logger.info(self.object_id, "Starting humidity calibration...")
                
        # Get the sequence list
        sequence_list = self.__get_sequence_list__()
        if sequence_list is None:
            self.debug_logger.error(self.object_id, "No sequence available.")
            return
        self.calib_ongoing = True
        
        # Iterate over each sequence's element
        for element in sequence_list:
            if self.calib_should_be_stopped:
                    break
            
            self.debug_logger.info(self.object_id, "[" + str(element["order"]) + "/" + str(len(sequence_list)) + "] "
                                   + " Std" + element["standard"] + ": "
                                   + str(element["primary_flow_sccm"]) + "sccm, "
                                   + str(element["std_rate_ul_min"]) + "ul/min "
                                   + "for " + str(element["duration_minute"]) + " minutes.")
            # Select flow path according to requested standard
            if element["standard"] == "A":
                self.humgen.set_stdA_flow_path(element["primary_flow_sccm"], element["secondary_flow_sccm"])
            elif element["standard"] == "B":
                self.humgen.set_stdB_flow_path(element["primary_flow_sccm"], element["secondary_flow_sccm"])
            else:
                self.debug_logger.error(self.object_id, "Standard [" + element["standard"] + "] not recognized.")
                continue

            # Set infusion rate and infuse
            self.humgen.pump.set_infusion_rate(element["std_rate_ul_min"])
            self.humgen.pump.infuse()

            # Wait the requested duration, while checking if stop order has been given
            now = datetime.datetime.now()
            end_of_element = now + datetime.timedelta(minutes=float(element["duration_minute"]))
            while (datetime.datetime.now() < end_of_element):
                if self.calib_should_be_stopped:
                    break
                else:
                    sleep(1)
        self.calib_ongoing = False

    def __get_sequence_list__(self):
        """
        Read the tab-separated file containing the sequence elements.
        :return: List of dict
        """
        filename = "../config/" + self.config.read(self.object_id, "sequence_filename")
        if not os.path.exists(filename):
            self.debug_logger.error(self.object_id, "Sequence file [" + filename + "] not found.")
            return None

        with open(filename, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter='\t')
            row_number = 0
            colnames = []
            sequence_list = []
            expected_colnames = ["standard", "primary_flow_sccm", "secondary_flow_sccm", "std_rate_ul_min", "duration_minute"]
            for row in filereader:
                # First row contains column names
                if row_number == 0:
                    colnames = row
                    if sorted(expected_colnames) != sorted(colnames):
                        self.debug_logger.error(self.object_id, "Expected column names not found.")
                        return None
                # Create a dict for each row, and append it to main sequence_list
                else:
                    row_dict = {"order": row_number}
                    variable_number = 0
                    for value in row:
                        if colnames[variable_number] != "standard":
                            try:
                                value = float(value)
                            except ValueError:
                                self.debug_logger.error(self.object_id, "Row #" + str(row_number) +
                                                        ", column [" + colnames[variable_number] +
                                                        "]: value [" + value + "] not convertible to float.")
                                return None
                        row_dict[colnames[variable_number]] = value
                        variable_number += 1
                    sequence_list.append(row_dict)
                row_number += 1

        return sequence_list
