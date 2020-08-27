from PyQt5.QtWidgets import QRadioButton, QLineEdit
from uim.abstractuim import AbstractUim
from driver.electrovalvedriver import ElectrovalveDriver
from gui.uielectrovalvewindow import Ui_ElectrovalveWindow
from gui.uimainwindow import Ui_MainWindow


class ElectrovalveUim(AbstractUim):

    def __init__(self, valve: ElectrovalveDriver, valve_id: int, main_ui: Ui_MainWindow, electrovalve_ui: Ui_ElectrovalveWindow):
        self.main_ui = main_ui
        self.electrovalve_ui = electrovalve_ui
        self.valve_id = valve_id
        self.valve = valve

        # Connect radio buttons
        self.__get_radioButton__(valve_id, "open").clicked.connect(self.open_valve)
        self.__get_radioButton__(valve_id, "closed").clicked.connect(self.close_valve)

        self.initialize_display(valve)

    def open_valve(self):
        self.valve.open_valve()
        self.update_all_displays()
        
    def close_valve(self):
        self.valve.close_valve()
        self.update_all_displays()

    def __get_radioButton__(self, valve_id: int, open_or_closed: str) -> QRadioButton:
        radioButton = getattr(self.electrovalve_ui, "ev" + str(valve_id) + "_radioButton_" + open_or_closed)
        return radioButton

    def __get_position_lineEdit__(self, valve_id: int) -> QLineEdit:
        lineEdit = getattr(self.main_ui, "ev" + str(valve_id) + "_lineEdit_position")
        return lineEdit

    def toggle_all_widgets(self, enabled: bool):
        self.__get_position_lineEdit__(self.valve_id).setEnabled(enabled)
        self.__get_radioButton__(self.valve_id, "open").setEnabled(enabled)
        self.__get_radioButton__(self.valve_id, "closed").setEnabled(enabled)

    def update_all_displays(self):
        position = self.valve.get_position()
        self.__get_radioButton__(self.valve_id, position).setChecked(True)
        self.__get_position_lineEdit__(self.valve_id).setText(position.capitalize())
