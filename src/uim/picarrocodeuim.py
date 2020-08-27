from uim.abstractuim import AbstractUim
from driver.alzarddriver import AlzardDriver
from gui.uimainwindow import Ui_MainWindow


class PicarroCodeUim(AbstractUim):

    def __init__(self, picarro_code: AlzardDriver, main_ui: Ui_MainWindow):
        self.main_ui = main_ui
        self.picarro_code = picarro_code

        self.initialize_display(picarro_code)

    def toggle_all_widgets(self, enabled: bool):
        self.main_ui.picarro_lineEdit_code.setEnabled(enabled)

    def update_all_displays(self):
        self.main_ui.picarro_lineEdit_code.setText(self.picarro_code.read_code())
