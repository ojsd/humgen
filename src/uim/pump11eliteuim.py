import threading
import time

import utils
from driver.pump11elitedriver import Pump11EliteDriver
from gui.uimainwindow import Ui_MainWindow
from gui.uipump11elitewindow import Ui_Pump11EliteWindow


class Pump11EliteUim:

    def __init__(self, pump: Pump11EliteDriver, main_ui: Ui_MainWindow, pump_ui: Ui_Pump11EliteWindow):
        # Input parameters as object variables
        self.main_ui = main_ui
        self.pump_ui = pump_ui
        self.pump = pump

        if self.pump.get_status_code() < 5:
            self.disable_all()
            return

        # Get max/min infusion rate
        infusion_rate_limits = self.pump.get_infusion_rate_limits()
        self.infusion_rate_limits_min = infusion_rate_limits[0]
        self.infusion_rate_limits_max = infusion_rate_limits[1]

        self.read_all()
        
        # Connect rate lineEdit
        self.pump_ui.lineEdit_rate_infuse.returnPressed.connect(self.apply_change_infusion_rate)
        self.pump_ui.lineEdit_rate_infuse.textChanged.connect(self.change_infusion_rate)
        self.pump_ui.lineEdit_rate_withdraw.returnPressed.connect(self.apply_change_withdraw_rate)
        self.pump_ui.lineEdit_rate_withdraw.textChanged.connect(self.change_withdraw_rate)

        # Connect target lineEdit
        self.pump_ui.lineEdit_volume_target.returnPressed.connect(self.apply_change_target_volume)
        self.pump_ui.lineEdit_volume_target.textChanged.connect(self.change_target_volume)

        # Connect read-all button
        self.pump_ui.button_read_all.clicked.connect(self.read_all)

        # Connect pump movement buttons
        self.pump_ui.button_infuse.clicked.connect(self.infuse_gui)
        self.pump_ui.button_stop.clicked.connect(self.stop_gui)
        self.pump_ui.button_withdraw.clicked.connect(self.withdraw_gui)
        
        self.pump_ui.button_run.clicked.connect(self.pump.run)
        self.pump_ui.button_reverse.clicked.connect(self.pump.reverse)

        # Connect clear buttons
        self.pump_ui.button_clear_volume_infuse.clicked.connect(self.clear_infused_volume)
        self.pump_ui.button_clear_volume_withdraw.clicked.connect(self.clear_withdrawn_volume)
        self.pump_ui.button_clear_volume_target.clicked.connect(self.clear_target_volume)

        # Connect read volume buttons
        self.pump_ui.button_read_volume_infuse.clicked.connect(self.update_infused_volume)
        self.pump_ui.button_read_volume_withdraw.clicked.connect(self.update_withdrawn_volume)

        # Connect reset-to-start button
        self.pump_ui.button_reset_to_start.clicked.connect(self.reset_to_start)

        # Thread to update infused and withdrawn volumes
        a = threading.Thread(None, self.setup_thread)
        a.daemon = True
        a.start()

    def read_all(self):
        self.pump_ui.lineEdit_rate_infuse.setText("{0:.6g}".format(self.pump.get_infusion_rate()))
        self.pump_ui.lineEdit_rate_withdraw.setText("{0:.6g}".format(self.pump.get_withdraw_rate()))
        self.pump_ui.lineEdit_volume_withdraw.setText("{0:.6g}".format(self.pump.get_withdrawn_volume()))
        self.pump_ui.lineEdit_volume_infuse.setText("{0:.6g}".format(self.pump.get_infused_volume()))

    def reset_to_start(self):
        self.pump.reset_to_start()

    def stop_gui(self):
        self.pump.stop()
        self.update_infused_volume()
        self.update_withdrawn_volume()            

    def disable_all(self):
        utils.disable_all_widgets(self.pump_ui.layoutWidget.parent())
        utils.disable_all_widgets(self.main_ui.groupBox_pump)

    ####################################################################################################################
    # Infuse
    def infuse_gui(self):
        self.pump.infuse()

    def change_infusion_rate(self):
        self.pump_ui.lineEdit_rate_infuse.setStyleSheet("color: 'orange';")

    def apply_change_infusion_rate(self):
        self.pump_ui.lineEdit_rate_infuse.setStyleSheet("color: 'red';")
        new_rate = utils.fit_in_range(value=float(self.pump_ui.lineEdit_rate_infuse.text()),
                                      min_max_range=self.pump.get_infusion_rate_limits())

        success = self.pump.set_infusion_rate(new_rate)
        if success:
            self.pump_ui.lineEdit_rate_infuse.setText("{0:.6g}".format(new_rate))
            self.main_ui.pump_lineEdit_rate_infuse.setText("{0:.6g}".format(new_rate))
            self.pump_ui.lineEdit_rate_infuse.setStyleSheet("color: 'green';")

    def update_infused_volume(self):
        try:
            volume_infused = self.pump.get_infused_volume()
        except ValueError:
            volume_infused = 00000000
        self.volume_infused = volume_infused
        self.pump_ui.lineEdit_volume_infuse.setText("{0:.6g}".format(self.volume_infused))

    def clear_infused_volume(self):
        self.pump.clear_infused_volume()
        self.volume_infused = self.pump.get_infused_volume()
        self.pump_ui.lineEdit_volume_infuse.setText("{0:.6g}".format(self.volume_infused))

    ####################################################################################################################
    # Withdraw
    def withdraw_gui(self):
        self.pump.withdraw()

    def change_withdraw_rate(self):
        self.pump_ui.lineEdit_rate_withdraw.setStyleSheet("color: 'orange';")

    def apply_change_withdraw_rate(self):
        self.pump_ui.lineEdit_rate_withdraw.setStyleSheet("color: 'red';")
        new_rate = utils.fit_in_range(value=float(self.pump_ui.lineEdit_rate_withdraw.text()),
                                      min_max_range=self.pump.get_withdraw_rate_limits())

        success = self.pump.set_withdraw_rate(new_rate)
        if success:
            self.pump_ui.lineEdit_rate_withdraw.setText("{0:.6g}".format(new_rate))
            self.main_ui.pump_lineEdit_rate_withdraw.setText("{0:.6g}".format(new_rate))
            self.pump_ui.lineEdit_rate_withdraw.setStyleSheet("color: 'green';")

    def update_withdrawn_volume(self):
        try:
            volume_withdrawn = self.pump.get_withdrawn_volume()
        except ValueError:
            volume_withdrawn = 00000000
        self.volume_withdrawn = volume_withdrawn
        self.pump_ui.lineEdit_volume_withdraw.setText("{0:.6g}".format(self.volume_withdrawn))

    def clear_withdrawn_volume(self):
        self.pump.clear_withdrawn_volume()
        self.volume_withdrawn = self.pump.get_withdrawn_volume()
        self.pump_ui.lineEdit_volume_withdraw.setText("{0:.6g}".format(self.volume_withdrawn))

    ####################################################################################################################
    # Target volume
    def change_target_volume(self):
        self.pump_ui.lineEdit_volume_target.setStyleSheet("color: 'orange';")

    def apply_change_target_volume(self):
        new_volume = float(self.pump_ui.lineEdit_volume_target.text())
        success = self.pump.set_target_volume(new_volume)
        if success:
            self.pump_ui.lineEdit_volume_target.setStyleSheet("color: 'green';")
        else:
            self.pump_ui.lineEdit_volume_target.setStyleSheet("color: 'red';")

    def clear_target_volume(self):
        self.pump.clear_target_volume()
        self.pump_ui.lineEdit_volume_target.setText(
            "{0:.6g}".format(self.pump.get_target_volume()))
        self.pump_ui.lineEdit_volume_target.setStyleSheet("color: 'green';")

    ####################################################################################################################
    # Threads
    def setup_thread(self):
        while True:
            if self.pump.is_moving:
                self.pump_ui.lineEdit_volume_infuse.setText("{0:.6g}".format(self.pump.get_infused_volume_from_record()))
                self.pump_ui.lineEdit_volume_withdraw.setText("{0:.6g}".format(self.pump.get_withdrawn_volume_from_record()))
                self.main_ui.pump_lineEdit_volume_infuse.setText("{0:.6g}".format(self.pump.get_infused_volume_from_record()))
                self.main_ui.pump_lineEdit_volume_withdraw.setText("{0:.6g}".format(self.pump.get_withdrawn_volume_from_record()))
            target_volume = self.pump.get_target_volume()
            self.pump_ui.lineEdit_volume_target.setText("{0:.6g}".format(target_volume))
            self.main_ui.pump_lineEdit_rate_infuse.setText("{0:.6g}".format(self.pump.get_record()["irate"]))
            self.main_ui.pump_lineEdit_rate_withdraw.setText("{0:.6g}".format(self.pump.get_record()["wrate"]))
            time.sleep(0.5)
