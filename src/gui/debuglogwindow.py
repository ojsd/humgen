from PyQt5.QtWidgets import QDialog

from gui.uidebuglogwindow import Ui_DebuglogWindow


class DebuglogWindow(QDialog):

    def __init__(self, parent_window):
        super(DebuglogWindow, self).__init__(parent_window)

        # Set up the user interface from Designer.
        self.ui = Ui_DebuglogWindow()
        self.ui.setupUi(self)

    def get_ui(self):
        return self.ui
