import threading
from time import sleep
from PyQt5.QtWidgets import QTableWidgetItem, QCheckBox
from debuglogger import DebugLogger
from gui.uidebuglogwindow import Ui_DebuglogWindow
from gui.debuglogwindow import DebuglogWindow


class DebuglogUim:

    def __init__(self, logger: DebugLogger, debuglog_ui: Ui_DebuglogWindow, debuglog_window: DebuglogWindow):
        self.debuglog_ui = debuglog_ui
        self.logger = logger
        self.debuglog_window = debuglog_window
        self.debug_released_event = logger.get_debug_released_event()

        # Set up table columns
        self.debuglog_ui.tableWidget_log.setColumnWidth(0, 175)
        self.debuglog_ui.tableWidget_log.setColumnWidth(1, 80)
        self.debuglog_ui.tableWidget_log.setColumnWidth(2, 80)
        self.debuglog_ui.tableWidget_log.setColumnWidth(3, 400)

        # Connect instruments' checkBoxes changes and level comboBox changes to update table
        self.debuglog_ui.comboBox_level.currentTextChanged.connect(self.__update_log_table__)
        for row in range(self.debuglog_ui.verticalLayout_instruments.count()):
            widget = self.debuglog_ui.verticalLayout_instruments.itemAt(row).widget()
            if isinstance(widget, QCheckBox):
                widget.stateChanged.connect(self.__update_log_table__)

        # Create and launch the thread managing the log tableWidget updates
        a = threading.Thread(None, self.__update_thread__)
        a.daemon = True
        a.start()

    def __update_thread__(self):
        while True:
            self.debug_released_event.wait()
            self.__update_log_table__()
            sleep(0.2)

    def __update_log_table__(self):
        # Update the log table only if the QDialog carrying it is visible
        if not self.debuglog_window.isVisible():
            return

        # Get the FIFO list containing all the log events
        fifo_log_deque = self.logger.get_fifo_deque().copy()

        # Identify log elements to be removed, due to GUI filters (instruments filter and level filter)
        element_id = 0
        elements_to_delete = []
        for element in fifo_log_deque:
            if (not self.__get_checkbox__(element["object"]).isChecked())\
                    | (self.logger.levels[element["level"]] < self.logger.levels[self.debuglog_ui.comboBox_level.currentText()]):
                elements_to_delete.append(element_id)
            element_id += 1

        # Remove elements from log list
        fifo_log_deque = [i for j, i in enumerate(fifo_log_deque) if j not in elements_to_delete]

        # Add log elements to the tableWidget
        self.debuglog_ui.tableWidget_log.setRowCount(len(fifo_log_deque))
        line_number = 0
        for element in fifo_log_deque:
            self.debuglog_ui.tableWidget_log.setItem(line_number, 0, QTableWidgetItem(element["datetime"]))
            self.debuglog_ui.tableWidget_log.setItem(line_number, 1, QTableWidgetItem(element["level"]))
            self.debuglog_ui.tableWidget_log.setItem(line_number, 2, QTableWidgetItem(element["object"]))
            self.debuglog_ui.tableWidget_log.setItem(line_number, 3, QTableWidgetItem(element["message"]))
            line_number += 1
        self.debuglog_ui.tableWidget_log.viewport().update()
        # Generates a inoffensive "QBasicTimer::start: QBasicTimer can only be used with threads started with QThread" error
        self.debuglog_ui.tableWidget_log.scrollToBottom()

    def __get_checkbox__(self, object_id: str) -> QCheckBox:
        return getattr(self.debuglog_ui, "checkBox_" + object_id)
