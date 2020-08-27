from uim.abstractuim import AbstractUim
from driver import redflowmeterdriver
from driver.redflowmeterdriver import RedFlowMeterDriver
from gui.uimainwindow import Ui_MainWindow


class RedFlowMeterUim(AbstractUim):

    def __init__(self, flow: RedFlowMeterDriver, channel: str, main_ui: Ui_MainWindow, flow_ui):
        self.main_ui = main_ui
        self.flow_ui = flow_ui
        self.flow = flow

        self.__setup_gui_variable_names__(channel)

        # Initialize combo box "control function"
        if self.flow.get_status_code() >= 5:
            mapping = self.flow.control_function_mapping
            sorted_items = sorted(mapping, key=mapping.get)
            self.comboBox_flow_control_function.addItems(sorted_items)
            self.comboBox_flow_control_function.setCurrentText(self.recover_key(mapping, self.flow.get_control_function()))
            self.comboBox_flow_control_function.currentTextChanged.connect(self.set_control_function)

        self.doubleSpinBox_flow_setpoint.valueChanged.connect(self.set_setpoint_gas_flow)
        self.doubleSpinBox_flow_valve_control.valueChanged.connect(self.set_valve_control)

        # Connect action button
        self.toolButton_flow_reset_hardware_error.clicked.connect(self.reset_hardware_errors)
        self.toolButton_flow_soft_reset.clicked.connect(self.soft_reset)

        self.initialize_display(self.flow)

    def recover_key(self, dicty, value):
        for a_key in dicty.keys():
            if (dicty[a_key] == value):
                return a_key

    def set_setpoint_gas_flow(self):
        self.flow.set_setpoint_gas_flow(self.doubleSpinBox_flow_setpoint.value())

    def update_setpoint_gas_flow(self) -> None:
        setpoint_gas_flow = self.flow.get_setpoint_gas_flow()
        if setpoint_gas_flow is None:
            value = -1
        else:
            value = setpoint_gas_flow
        self.doubleSpinBox_flow_setpoint.setValue(value)

    def update_flow(self) -> None:
        gas_flow = self.flow.get_record()["flow"]
        if gas_flow is None:
            text = "--"
        else:
            text = "{0:.6g}".format(gas_flow)
        self.lineEdit_flow_flow.setText(text)
        self.main_flow_lineEdit_flow.setText(text)

    def update_temperature(self) -> None:
        temperature = self.flow.get_record()["temperature"]
        if temperature is None:
            temperature_text = "--"
        else:
            temperature_text = "{0:.6g}".format(temperature)
        self.lineEdit_flow_temperature.setText(temperature_text)

    def update_alarm(self) -> None:
        alarms = self.flow.get_alarms()
        if alarms is None:
            alarms_text = "--"
        else:
            alarms_text = "{0:b}".format(alarms)
        self.lineEdit_flow_alarm.setText(alarms_text)

    def set_valve_control(self) -> None:
        self.flow.set_valve_control_signal(self.doubleSpinBox_flow_valve_control.value())

    def update_valve_control(self) -> None:
        valve_control_signal = self.flow.get_valve_control_signal()
        if valve_control_signal is None:
            value = -1
        else:
            value = valve_control_signal
        self.doubleSpinBox_flow_valve_control.setValue(value)

    def set_control_function(self) -> None:
        value = self.flow.control_function_mapping[self.comboBox_flow_control_function.currentText()]
        self.flow.set_control_function(value)

    def update_control_function(self) -> None:
        self.main_flow_lineEdit_control_function.setText(self.flow.get_control_function_as_string())

    def update_hardware_errors(self) -> None:
        hardware_errors = self.flow.get_hardware_errors()
        if hardware_errors is None:
            text = "--"
        else:
            text = "{0:b}".format(hardware_errors)
        self.lineEdit_flow_hardware_error.setText(text)

    def reset_hardware_errors(self) -> None:
        self.flow.reset_hardware_errors()

    def soft_reset(self) -> None:
        self.flow.soft_reset()

    def __setup_gui_variable_names__(self, channel: str) -> None:
        if channel == "A":
            self.comboBox_flow_control_function = self.flow_ui.flowA_comboBox_control_function
            self.doubleSpinBox_flow_valve_control = self.flow_ui.flowA_doubleSpinBox_valve_control
            self.doubleSpinBox_flow_setpoint = self.flow_ui.flowA_doubleSpinBox_setpoint
            self.lineEdit_flow_alarm = self.flow_ui.flowA_lineEdit_alarm
            self.lineEdit_flow_flow = self.flow_ui.flowA_lineEdit_flow
            self.lineEdit_flow_hardware_error = self.flow_ui.flowA_lineEdit_hardware_error
            self.lineEdit_flow_temperature = self.flow_ui.flowA_lineEdit_temperature
            self.toolButton_flow_reset_hardware_error = self.flow_ui.flowA_toolButton_reset_hardware_error
            self.toolButton_flow_soft_reset = self.flow_ui.flowA_toolButton_soft_reset
            self.main_flow_lineEdit_flow = self.main_ui.flowA_lineEdit_flow
            self.main_flow_lineEdit_control_function = self.main_ui.flowA_lineEdit_control_function
        elif channel == "B":
            self.comboBox_flow_control_function = self.flow_ui.flowB_comboBox_control_function
            self.doubleSpinBox_flow_valve_control = self.flow_ui.flowB_doubleSpinBox_valve_control
            self.doubleSpinBox_flow_setpoint = self.flow_ui.flowB_doubleSpinBox_setpoint
            self.lineEdit_flow_alarm = self.flow_ui.flowB_lineEdit_alarm
            self.lineEdit_flow_flow = self.flow_ui.flowB_lineEdit_flow
            self.lineEdit_flow_hardware_error = self.flow_ui.flowB_lineEdit_hardware_error
            self.lineEdit_flow_temperature = self.flow_ui.flowB_lineEdit_temperature
            self.toolButton_flow_reset_hardware_error = self.flow_ui.flowB_toolButton_reset_hardware_error
            self.toolButton_flow_soft_reset = self.flow_ui.flowB_toolButton_soft_reset
            self.main_flow_lineEdit_flow = self.main_ui.flowB_lineEdit_flow
            self.main_flow_lineEdit_control_function = self.main_ui.flowB_lineEdit_control_function

    def toggle_all_widgets(self, enabled: bool) -> None:
        self.comboBox_flow_control_function.setEnabled(enabled)
        self.doubleSpinBox_flow_valve_control.setEnabled(enabled)
        self.doubleSpinBox_flow_setpoint.setEnabled(enabled)
        self.lineEdit_flow_alarm.setEnabled(enabled)
        self.lineEdit_flow_flow.setEnabled(enabled)
        self.lineEdit_flow_hardware_error.setEnabled(enabled)
        self.lineEdit_flow_temperature.setEnabled(enabled)
        self.toolButton_flow_reset_hardware_error.setEnabled(enabled)
        self.toolButton_flow_soft_reset.setEnabled(enabled)
        self.main_flow_lineEdit_flow.setEnabled(enabled)
        self.main_flow_lineEdit_control_function.setEnabled(enabled)

    def update_all_displays(self) -> None:
        self.update_temperature()
        self.update_flow()
        self.update_control_function()
