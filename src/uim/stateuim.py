import threading
from time import sleep
from uim.abstractuim import AbstractUim
from state import State
from gui.uimainwindow import Ui_MainWindow
from gui.uistatewindow import Ui_StateWindow


class StateUim(AbstractUim):

    def __init__(self, state: State, main_ui: Ui_MainWindow, state_ui: Ui_StateWindow):
        self.main_ui = main_ui
        self.state_ui = state_ui
        self.state = state

        # Connect state's radiobutton to function
        for state_name in self.state.get_states():
            to_state_function = self.state.get_to_state_function(state_name)
            self.__get_radio_button__(state_name).clicked.connect(to_state_function)

        # Connect "listen picarro" radioButton
        self.main_ui.state_radioButton_picarro_listen.clicked.connect(lambda: self.state.set_listen_picarro_code(True))
        self.main_ui.state_radioButton_picarro_listen.clicked.connect(lambda: self.toggle_all_widgets(False))
        self.main_ui.state_radioButton_picarro_ignore.clicked.connect(lambda: self.state.set_listen_picarro_code(False))
        self.main_ui.state_radioButton_picarro_ignore.clicked.connect(lambda: self.toggle_all_widgets(True))

        # Connect expert-mode lineEdit to color change when edited
        self.state_ui.lineEdit_isocalib_rate.textChanged.connect(lambda: self.state_ui.lineEdit_isocalib_rate.setStyleSheet("color: 'orange';"))
        self.state_ui.lineEdit_boost_factor.textChanged.connect(lambda: self.state_ui.lineEdit_boost_factor.setStyleSheet("color: 'orange';"))
        self.state_ui.lineEdit_primary_flow.textChanged.connect(lambda: self.state_ui.lineEdit_primary_flow.setStyleSheet("color: 'orange';"))
        self.state_ui.lineEdit_secondary_flow.textChanged.connect(lambda: self.state_ui.lineEdit_secondary_flow.setStyleSheet("color: 'orange';"))

        # Connect expert-mode lineEdit to "change" function when return pressed
        self.state_ui.lineEdit_isocalib_rate.returnPressed.connect(self.__change_isocalib_rate__)
        self.state_ui.lineEdit_boost_factor.returnPressed.connect(self.__change_isocalib_boost_factor__)
        self.state_ui.lineEdit_primary_flow.returnPressed.connect(self.__change_primary_flow__)
        self.state_ui.lineEdit_secondary_flow.returnPressed.connect(self.__change_secondary_flow__)

        self.initialize_display(None)

    def to_state_manual(self):
        self.state.to_state_manual()

    def to_state_air(self):
        self.state.to_state_air()

    def to_state_init_calib_step1(self):
        self.state.to_state_init_calib_step1()

    def to_state_init_calib_step2(self):
        self.state.to_state_init_calib_step2()

    def to_state_isocalib_stdA(self):
        self.state.to_state_isocalib_stdA()

    def to_state_isocalib_stdB(self):
        self.state.to_state_isocalib_stdB()

    def to_state_reset_calib(self):
        self.state.to_state_reset_calib()

    def to_state_humdep(self):
        self.state.to_state_humdep()

    def toggle_all_widgets(self, enabled: bool):
        for state_name in self.state.get_states():
            self.__get_radio_button__(state_name).setEnabled(enabled)

    def __get_radio_button__(self, state_name: str):
        radio_button = getattr(self.main_ui, "state_radioButton_" + state_name)
        return radio_button

    def __change_isocalib_rate__(self):
        self.state.set_isocalib_rate(float(self.state_ui.lineEdit_isocalib_rate.text()))
        self.state_ui.lineEdit_isocalib_rate.setStyleSheet("color: 'green';")

    def __change_isocalib_boost_factor__(self):
        self.state.set_isocalib_boost_factor(float(self.state_ui.lineEdit_boost_factor.text()))
        self.state_ui.lineEdit_boost_factor.setStyleSheet("color: 'green';")

    def __change_primary_flow__(self):
        self.state.set_primary_flow(float(self.state_ui.lineEdit_primary_flow.text()))
        self.state_ui.lineEdit_primary_flow.setStyleSheet("color: 'green';")

    def __change_secondary_flow__(self):
        self.state.set_secondary_flow(float(self.state_ui.lineEdit_secondary_flow.text()))
        self.state_ui.lineEdit_secondary_flow.setStyleSheet("color: 'green';")

    def update_all_displays(self):
        # RadioButtons: current state
        current_state = self.state.get_current_state()
        self.__get_radio_button__(current_state).setChecked(True)
        # RadioButtons: listen picarro code
        listen_picarro_code = self.state.get_listen_picarro_code()
        self.main_ui.state_radioButton_picarro_listen.setChecked(listen_picarro_code)
        self.main_ui.state_radioButton_picarro_ignore.setChecked(not listen_picarro_code)

    def initialize_display(self, instrument):
        self.update_all_displays()
        self.launch_thread_for_update_display()

        # Update expert mode values
        self.state_ui.lineEdit_isocalib_rate.setText("{0:.6g}".format(self.state.get_isocalib_rate()))
        self.state_ui.lineEdit_isocalib_rate.setStyleSheet("color: 'green';")
        self.state_ui.lineEdit_boost_factor.setText("{0:.6g}".format(self.state.get_isocalib_boost_factor()))
        self.state_ui.lineEdit_boost_factor.setStyleSheet("color: 'green';")
        self.state_ui.lineEdit_primary_flow.setText("{0:.6g}".format(self.state.get_primary_flow()))
        self.state_ui.lineEdit_primary_flow.setStyleSheet("color: 'green';")
        self.state_ui.lineEdit_secondary_flow.setText("{0:.6g}".format(self.state.get_secondary_flow()))
        self.state_ui.lineEdit_secondary_flow.setStyleSheet("color: 'green';")
