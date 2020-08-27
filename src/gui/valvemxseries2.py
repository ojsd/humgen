from PyQt5.QtWidgets import QDialog

from gui.uivalvemxseries2window import Ui_ValveMxSeries2Window


class ValveMxSeries2Window(QDialog):

    def __init__(self, parent_window):
        super(ValveMxSeries2Window, self).__init__(parent_window)

        # Set up the user interface from Designer.
        self.ui = Ui_ValveMxSeries2Window()
        self.ui.setupUi(self)

    def get_ui(self):
        return self.ui
