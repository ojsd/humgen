import datetime
import collections
import threading


class DebugLogger:
    
    def __init__(self, filename: str):
        # Define level's order
        self.levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
        
        self.filename = filename
        self.debug_released_event = threading.Event()

        # Define FIFO list containing the last log events
        self.fifo_log_deque = collections.deque(list(), 200)
        
        # Define the minimum message's level required to display a message
        # of a given object_id.
        self.min_print_level = {"PUMP": "INFO",
                                "FLOW_A": "INFO",
                                "FLOW_B": "INFO",
                                "VALVE2x3": "INFO",
                                "E_VALVE1": "INFO",
                                "E_VALVE2": "INFO",
                                "P_CODE": "INFO",
                                "PRESSURE": "INFO",
                                "STATE": "INFO",
                                "HUMDEP": "INFO",
                                "HUMGEN": "INFO",
                                "T_SWITCH": "INFO",
                                "T_SENSOR": "INFO",
                                "P_SWITCH": "INFO"}
        self.min_file_level = {"PUMP": "INFO",
                               "FLOW_A": "INFO",
                               "FLOW_B": "INFO",
                               "VALVE2x3": "INFO",
                               "E_VALVE1": "INFO",
                               "E_VALVE2": "INFO",
                               "PRESSURE": "INFO",
                               "P_CODE": "INFO",
                               "STATE": "INFO",
                               "HUMDEP": "INFO",
                               "HUMGEN": "INFO",
                               "T_SWITCH": "INFO",
                               "T_SENSOR": "INFO",
                               "P_SWITCH": "INFO"}
    
    def debug(self, object_id, message):
        self.__write_in_log__("DEBUG", object_id, message)
    
    def info(self, object_id, message):
        self.__write_in_log__("INFO", object_id, message)
    
    def warning(self, object_id, message):
        self.__write_in_log__("WARNING", object_id, message)
    
    def error(self, object_id, message):
        self.__write_in_log__("ERROR", object_id, message)
    
    def critical(self, object_id, message):
        self.__write_in_log__("CRITICAL", object_id, message)
    
    def __write_in_log__(self, level, object_id, message):
        # Format object_id and level so that it has exactly 8 character
        # (Useful for multiline message indentation)
        object_id_formatted = '{:<8}'.format(object_id[:8])
        level_formatted = '{:<8}'.format(level[:8])
        
        # Format date of message
        datetime_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        log_line_header = "[" + datetime_string + "]" + level_formatted + " " + object_id_formatted + " "
        
        # Shift the second and following lines of the multilines messages
        # so the text is correctly indented
        message = message.replace('\n', '\n'.ljust(len(log_line_header) + 1))
        
        log_line = log_line_header + message

        # Check that the object_id is listed in min_print_level and min_file_level
        if object_id not in self.min_print_level:
            raise ValueError("Minimal logger print level not defined for " + object_id)
        if object_id not in self.min_file_level:
            raise ValueError("Minimal logger file level not defined for " + object_id)

        # Write log_line in standart output
        if self.levels[level] >= self.levels[self.min_print_level[object_id]]:
            print(log_line)

        # Write log_line in log file
        if self.levels[level] >= self.levels[self.min_file_level[object_id]]:
            # Define log file name
            date_string = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = "../log/" + date_string + "_" + self.filename + ".log"
            with open(filename, 'a') as out:
                out.write(log_line + '\n')

        if self.levels[level] > self.levels["DEBUG"]:
            # Add log to FIFO log list
            log_dict = {"datetime": datetime_string,
                        "level": level,
                        "object": object_id,
                        "message": message}
            self.fifo_log_deque.append(log_dict)

            # Fire an event: a log element has been created        
            self.debug_released_event.set()
            self.debug_released_event.clear()

    def get_fifo_deque(self):
        return self.fifo_log_deque

    def get_debug_released_event(self) -> threading.Event:
        return self.debug_released_event