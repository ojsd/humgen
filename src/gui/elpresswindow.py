from PyQt5.QtWidgets import QDialog

from gui.uielpresswindow import Ui_ElPressWindow


class ElPressWindow(QDialog):

    def __init__(self, parent_window):
        super(ElPressWindow, self).__init__(parent_window)

        # Set up the user interface from Designer.
        self.ui = Ui_ElPressWindow()
        self.ui.setupUi(self)

    def get_ui(self):
        return self.ui
