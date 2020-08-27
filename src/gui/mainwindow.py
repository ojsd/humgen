from PyQt5.QtWidgets import QMainWindow

from gui.uimainwindow import Ui_MainWindow
from gui.elpresswindow import ElPressWindow
from gui.electrovalvewindow import ElectrovalveWindow
from gui.pump11elitewindow import Pump11EliteWindow
from gui.redflowmeterwindow import RedFlowMeterWindow
from gui.valvemxseries2 import ValveMxSeries2Window
from gui.maintenancetoolswindow import MaintenanceToolsWindow
from gui.temperaturewindow import TemperatureWindow
from gui.debuglogwindow import DebuglogWindow
from gui.statewindow import StateWindow

from state import State
from driver.temperaturedriver import TemperatureDriver


class MainWindow(QMainWindow):
    def __init__(self, state: State, temperature: TemperatureDriver):
        super(MainWindow, self).__init__()
        self.state = state
        self.temperature = temperature

        # Set up the user interface from Designer.
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)

        # Create the sub-windows
        self.pump_window = Pump11EliteWindow(self)
        self.electrovalve_window = ElectrovalveWindow(self)
        self.flow_window = RedFlowMeterWindow(self)
        self.pressure_window = ElPressWindow(self)
        self.valve2x3_window = ValveMxSeries2Window(self)
        self.maintenancetools_window = MaintenanceToolsWindow(self)
        self.temperature_window = TemperatureWindow(self)
        self.debuglog_window = DebuglogWindow(self)
        self.state_window = StateWindow(self)

        # Link menu buttons to sub-windows
        self.main_ui.action_pump.triggered.connect(self.__show_pump_window__)
        self.main_ui.action_electrovalves.triggered.connect(self.__show_electrovalve_window__)
        self.main_ui.action_flows.triggered.connect(self.__show_flow_window__)
        self.main_ui.action_pressure.triggered.connect(self.__show_pressure_window__)
        self.main_ui.action_valve2x3.triggered.connect(self.__show_valve2x3_window__)
        self.main_ui.action_maintenancetools.triggered.connect(self.__show_maintenancetools_window__)
        self.main_ui.action_temperature.triggered.connect(self.__show_temperature_window__)
        self.main_ui.action_debuglog.triggered.connect(self.__show_debuglog_window__)
        self.main_ui.action_state.triggered.connect(self.__show_state_window__)

    def closeEvent(self, event):
        """Actions to be performed when the MainWindow is closed by user."""
        self.state.on_exit()
        self.temperature.on_exit()

    def get_main_ui(self):
        return self.main_ui

    def get_pump_ui(self):
        return self.pump_window.get_ui()

    def get_electrovalve_ui(self):
        return self.electrovalve_window.get_ui()

    def get_flow_ui(self):
        return self.flow_window.get_ui()

    def get_pressure_ui(self):
        return self.pressure_window.get_ui()

    def get_valve2x3_ui(self):
        return self.valve2x3_window.get_ui()
    
    def get_maintenancetools_ui(self):
        return self.maintenancetools_window.get_ui()

    def get_temperature_ui(self):
        return self.temperature_window.get_ui()

    def get_debuglog_window(self):
        return self.debuglog_window.get_ui()

    def get_state_window(self):
        return self.state_window.get_ui()

    def __show_pump_window__(self):
        self.pump_window.show()

    def __show_electrovalve_window__(self):
        self.electrovalve_window.show()

    def __show_flow_window__(self):
        self.flow_window.show()

    def __show_pressure_window__(self):
        self.pressure_window.show()

    def __show_valve2x3_window__(self):
        self.valve2x3_window.show()
        
    def __show_maintenancetools_window__(self):
        self.maintenancetools_window.show()

    def __show_temperature_window__(self):
        self.temperature_window.show()

    def __show_debuglog_window__(self):
        self.debuglog_window.show()

    def __show_state_window__(self):
        self.state_window.show()
