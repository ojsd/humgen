from PyQt5.QtWidgets import QDialog

from gui.uitemperaturewindow import Ui_TemperatureWindow


class TemperatureWindow(QDialog):

    def __init__(self, parent_window):
        super(TemperatureWindow, self).__init__(parent_window)

        # Set up the user interface from Designer.
        self.ui = Ui_TemperatureWindow()
        self.ui.setupUi(self)

    def get_ui(self):
        return self.ui
