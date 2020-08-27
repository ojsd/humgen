from PyQt5.QtWidgets import QDialog

from gui.uimaintenancetoolswindow import Ui_MaintenanceToolsWindow


class MaintenanceToolsWindow(QDialog):

    def __init__(self, parent_window):
        super(MaintenanceToolsWindow, self).__init__(parent_window)

        # Set up the user interface from Designer.
        self.ui = Ui_MaintenanceToolsWindow()
        self.ui.setupUi(self)

    def get_ui(self):
        return self.ui
