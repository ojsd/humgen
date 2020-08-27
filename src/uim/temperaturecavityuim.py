from uim.abstractuim import AbstractUim
from driver.temperaturedriver import TemperatureDriver
from gui.uimainwindow import Ui_MainWindow
from gui.uitemperaturewindow import Ui_TemperatureWindow


class TemperatureUim(AbstractUim):

    def __init__(self, temperature: TemperatureDriver, main_ui: Ui_MainWindow, temperature_ui: Ui_TemperatureWindow):
        self.main_ui = main_ui
        self.temperature_ui = temperature_ui
        self.temperature = temperature

        # Connect widget changes
        self.temperature_ui.doubleSpinBox_setpoint.valueChanged.connect(self.__change_setpoint__)
        self.temperature_ui.doubleSpinBox_hysteresis.valueChanged.connect(self.__change_hysteresis__)
        self.temperature_ui.spinBox_refresh.valueChanged.connect(self.__change_refresh_period__)
        self.temperature_ui.switch_radioButton_power.clicked.connect(lambda: self.__change_switch_position__("powered"))
        self.temperature_ui.switch_radioButton_unpower.clicked.connect(lambda: self.__change_switch_position__("unpowered"))

        self.initialize_display(self.temperature)

    def __change_setpoint__(self):
        self.temperature.set_setpoint(self.temperature_ui.doubleSpinBox_setpoint.value())

    def __change_hysteresis__(self):
        self.temperature.set_hysteresis(self.temperature_ui.doubleSpinBox_hysteresis.value())

    def __change_refresh_period__(self):
        self.temperature.set_refresh_period(self.temperature_ui.spinBox_refresh.value())

    def __change_switch_position__(self, position: str):
        if position == "powered":
            self.temperature.switch.power_output()
        elif position == "unpowered":
            self.temperature.switch.unpower_output()
        else:
            raise ValueError("Position should be either 'powered' or 'unpowered'")
        
    def update_all_displays(self):
        # Get values from driver
        setpoint = self.temperature.get_setpoint()
        hysteresis = self.temperature.get_hysteresis()
        temperature = self.temperature.get_temperature()
        position = self.temperature.switch.get_position()

        # Main UI
        setpoint_str = "{0:.2g}".format(setpoint) + " +/- " + "{0:.2g}".format(hysteresis)
        self.main_ui.temperature_lineEdit_setpoint.setText(setpoint_str)
        self.main_ui.temperature_lineEdit_measure.setText("{0:.6g}".format(temperature))
        self.main_ui.tempswitch_lineEdit_position.setText(position.capitalize())

        # "Expert" UI
        self.temperature_ui.doubleSpinBox_setpoint.setValue(setpoint)
        self.temperature_ui.doubleSpinBox_hysteresis.setValue(hysteresis)
        self.temperature_ui.spinBox_refresh.setValue(self.temperature.get_refresh_period())
        self.temperature_ui.lineEdit_measure.setText("{0:.6g}".format(temperature))
        if position == "powered":
            self.temperature_ui.switch_radioButton_power.setChecked(True)
        elif position == "unpowered":
            self.temperature_ui.switch_radioButton_unpower.setChecked(True)
        else:
            raise ValueError("Position should be either 'powered' or 'unpowered'")

    def toggle_all_widgets(self, enabled: bool):
        self.main_ui.temperature_lineEdit_setpoint.setEnabled(enabled)
        self.main_ui.temperature_lineEdit_measure.setEnabled(enabled)
        self.main_ui.tempswitch_lineEdit_position.setEnabled(enabled)
        self.temperature_ui.doubleSpinBox_setpoint.setEnabled(enabled)
        self.temperature_ui.doubleSpinBox_hysteresis.setEnabled(enabled)
        self.temperature_ui.spinBox_refresh.setEnabled(enabled)
        self.temperature_ui.lineEdit_measure.setEnabled(enabled)
        self.temperature_ui.switch_radioButton_power.setEnabled(enabled)
        self.temperature_ui.switch_radioButton_unpower.setEnabled(enabled)
