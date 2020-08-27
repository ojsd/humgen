from PyQt5.QtWidgets import QDialog

from gui.uistatewindow import Ui_StateWindow


class StateWindow(QDialog):

    def __init__(self, parent_window):
        super(StateWindow, self).__init__(parent_window)

        # Set up the user interface from Designer.
        self.ui = Ui_StateWindow()
        self.ui.setupUi(self)

    def get_ui(self):
        return self.ui
