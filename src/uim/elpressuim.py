from uim.abstractuim import AbstractUim
from driver.elpressdriver import ElPressDriver
from gui.uielpresswindow import Ui_ElPressWindow
from gui.uimainwindow import Ui_MainWindow


class ElPressUim(AbstractUim):

    def __init__(self, pressure: ElPressDriver, main_ui: Ui_MainWindow, pressure_ui: Ui_ElPressWindow):
        self.main_ui = main_ui
        self.pressure_ui = pressure_ui
        self.pressure = pressure
        self.max_flow = 1300

        # Connect pressure lineEdit
        self.pressure_ui.lineEdit_setpoint.returnPressed.connect(self.change_pressure_setpoint)

        # Initialize setpoint
        if pressure.get_status_code() >= 5:
            self.pressure_ui.lineEdit_setpoint.setText("{0:.6g}".format(self.pressure.read_setpoint()))

        self.initialize_display(self.pressure)

    def change_pressure_setpoint(self):
        flow = int(self.pressure_ui.lineEdit_setpoint.text())
        if flow <= self.max_flow:
            success = self.pressure.set_setpoint_pressure(flow)
        else:
            flow = self.max_flow
            success = self.pressure.set_setpoint_pressure(flow)
        if success:
            self.pressure_ui.lineEdit_setpoint.setStyleSheet("color: 'green';")
        else:
            self.pressure_ui.lineEdit_setpoint.setStyleSheet("color: 'red';")

    def toggle_all_widgets(self, enabled: bool):
        self.pressure_ui.lineEdit_pressure.setEnabled(enabled)
        self.pressure_ui.lineEdit_setpoint.setEnabled(enabled)
        self.main_ui.pressure_lineEdit_pressure.setEnabled(enabled)

    def update_all_displays(self):
        pressure_value = self.pressure.read_flow()
        self.pressure_ui.lineEdit_pressure.setText("{0:.6g}".format(pressure_value))
        self.main_ui.pressure_lineEdit_pressure.setText("{0:.6g}".format(pressure_value))
