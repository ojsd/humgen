from uim.abstractuim import AbstractUim
from driver.relaydriver import RelayDriver
from gui.uimainwindow import Ui_MainWindow


class PressurePumpUim(AbstractUim):

    def __init__(self, relay: RelayDriver, ui: Ui_MainWindow):
        self.main_ui = ui
        self.relay = relay

        self.initialize_display(self.relay)
        
    def update_all_displays(self):
        self.main_ui.ppswitch_lineEdit_position.setText(self.relay.get_position().capitalize())

    def toggle_all_widgets(self, enabled: bool):
        self.main_ui.ppswitch_lineEdit_position.setEnabled(enabled)
