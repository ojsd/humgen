from PyQt5.QtWidgets import QDialog

from gui.uiredflowmeterwindow import Ui_RedFlowMeterWindow


class RedFlowMeterWindow(QDialog):

    def __init__(self, parent_window):
        super(RedFlowMeterWindow, self).__init__(parent_window)

        # Set up the user interface from Designer.
        self.ui = Ui_RedFlowMeterWindow()
        self.ui.setupUi(self)

    def get_ui(self):
        return self.ui
