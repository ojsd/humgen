from PyQt5.QtWidgets import QDialog

from gui.uielectrovalvewindow import Ui_ElectrovalveWindow


class ElectrovalveWindow(QDialog):

    def __init__(self, parent_window):
        super(ElectrovalveWindow, self).__init__(parent_window)

        # Set up the user interface from Designer.
        self.ui = Ui_ElectrovalveWindow()
        self.ui.setupUi(self)

    def get_ui(self):
        return self.ui
