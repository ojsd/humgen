from uim.abstractuim import AbstractUim
from driver.valvemxseries2driver import ValveMxSeries2Driver
from gui.uimainwindow import Ui_MainWindow
from gui.uivalvemxseries2window import Ui_ValveMxSeries2Window


class ValveMxSeries2Uim(AbstractUim):

    def __init__(self, valve: ValveMxSeries2Driver, main_ui: Ui_MainWindow, valve2x3_ui: Ui_ValveMxSeries2Window):
        self.main_ui = main_ui
        self.valve2x3_ui = valve2x3_ui
        self.valve = valve

        # Connect radio buttons
        self.valve2x3_ui.radioButton_from_standards.clicked.connect(self.set_position_from_standards)
        self.valve2x3_ui.radioButton_to_chamber.clicked.connect(self.set_position_to_chambers)

        self.initialize_display(self.valve)

    def set_position_from_standards(self):
        self.valve.set_position_from_standards()

    def set_position_to_chambers(self):
        self.valve.set_position_to_chambers()

    def toggle_all_widgets(self, enabled: bool):
        self.valve2x3_ui.radioButton_from_standards.setEnabled(enabled)
        self.valve2x3_ui.radioButton_to_chamber.setEnabled(enabled)
        self.main_ui.valve2x3_lineEdit_position.setEnabled(enabled)

    def update_all_displays(self):
        # Read default position
        if self.valve.get_position_string() == "from_standards":
            self.valve2x3_ui.radioButton_from_standards.setChecked(True)
            self.main_ui.valve2x3_lineEdit_position.setText("From standards")
        elif self.valve.get_position_string() == "to_chambers":
            self.valve2x3_ui.radioButton_to_chamber.setChecked(True)
            self.main_ui.valve2x3_lineEdit_position.setText("To chambers")
        else:
            self.toggle_all_widgets(False)
