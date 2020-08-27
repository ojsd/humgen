import csv
import os.path
import time
from datetime import datetime
from threading import Thread

from driver.humgendriver import HumgenDriver
from driver.instrumentdriver import InstrumentDriver


class DataLogger:
    """
    Class used to periodically log the values measured by the instruments.
    The object which can be logged must have the following functions (note that this is necessarily the case for
    InstrumentDriver's children classes):
      * get_record(): a dict containing variable:value pairs
      * get_object_id(): the object's string identifyer
      * get_data_logger_header_list(): a list containing all the variables to be logged, in the desired order.
    """

    def __init__(self, filename_root, humgen: HumgenDriver):
        self.filename_root = filename_root
        self.humgen = humgen

        # List of all the instruments whose data should be logged
        self.instruments_to_log = [humgen.pump,
                                   humgen.flowA,
                                   humgen.flowB,
                                   humgen.pressure,
                                   humgen.valve1,
                                   humgen.valve2,
                                   humgen.valve2x3,
                                   humgen.picarro_code]

        # Define columns name
        self.column_names = ["datetime"]
        for instrument in self.instruments_to_log:
            self.column_names += self.__get_formatted_colnames__(instrument)

        # Create and launch write-in-log thread
        log_thread = Thread(target=self.__thread_log__)
        log_thread.daemon = True
        log_thread.start()

    def write(self):
        # Gather and sort the record in a common data list
        data_list = [datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]]
        for instrument in self.instruments_to_log:
            data_list += self.__get_instrument_variable_list__(instrument)

        # Write the data list in file
        if not self.__file_exists__():
            self.__add_header__()
        self.__write_in_file__(data_list)

    def __get_instrument_variable_list__(self, instrument: InstrumentDriver):
        instrument_record = instrument.get_record()
        instrument_data_list = []
        for variable_name in instrument.get_data_logger_header_list():
            variable_value = instrument_record[variable_name]
            variable_value = self.__format_variable__(variable_value)
            instrument_data_list.append(variable_value)
        return instrument_data_list

    def __get_file_name__(self):
        date_string = datetime.now().strftime("%Y-%m-%d")
        filename = "../log/" + date_string + "_" + self.filename_root + ".log"
        return filename

    def __file_exists__(self):
        filename = self.__get_file_name__()
        if os.path.exists(filename):
            return os.path.isfile(filename)
        else:
            return False

    def __add_header__(self):
        self.__write_in_file__(self.column_names)

    def __write_in_file__(self, data_list):
        with open(self.__get_file_name__(), 'a') as datafile:
            writer = csv.writer(datafile, delimiter='\t')
            writer.writerow(data_list)

    def __thread_log__(self):
        """
        Thread which periodically write data log to a file
        """
        while True:
            self.write()
            time.sleep(10)

    def __format_variable__(self, value, digit: int=3) -> str:
        if value is None:
            return "NA"
        elif isinstance(value, int) | isinstance(value, float):
            return str(round(value, digit))
        else:
            return value

    def __get_formatted_colnames__(self, instrument: InstrumentDriver):
        return [instrument.get_object_id() + "_" + colname for colname in instrument.get_data_logger_header_list()]
