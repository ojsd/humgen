from PyQt5.QtWidgets import QDialog

from gui.uipump11elitewindow import Ui_Pump11EliteWindow


class Pump11EliteWindow(QDialog):

    def __init__(self, parent_window):
        super(Pump11EliteWindow, self).__init__(parent_window)

        # Set up the user interface from Designer.
        self.ui = Ui_Pump11EliteWindow()
        self.ui.setupUi(self)

    def get_ui(self):
        return self.ui
