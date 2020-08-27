from maintenancetools import MaintenanceTools
from gui.uimaintenancetoolswindow import Ui_MaintenanceToolsWindow


class MaintenanceToolsUim:

    def __init__(self, maintenancetools: MaintenanceTools, maintenancetools_ui: Ui_MaintenanceToolsWindow):
        self.maintenancetools_ui = maintenancetools_ui
        self.maintenancetools = maintenancetools

        # Initialize syringe dimensions
        self.maintenancetools_ui.lineEdit_syringe_diameter.setText("{0:.6g}".format(self.maintenancetools.pump.get_syringe_diameter()))
        self.maintenancetools_ui.lineEdit_syringe_volume.setText("{0:.6g}".format(self.maintenancetools.pump.get_syringe_volume()))

        # Connect syringe-dimensions lineEdit
        self.maintenancetools_ui.lineEdit_syringe_volume.returnPressed.connect(self.apply_change_syringe_volume)
        self.maintenancetools_ui.lineEdit_syringe_volume.textChanged.connect(self.change_syringe_volume)
        self.maintenancetools_ui.lineEdit_syringe_diameter.returnPressed.connect(self.apply_change_syringe_diameter)
        self.maintenancetools_ui.lineEdit_syringe_diameter.textChanged.connect(self.change_syringe_diameter)

        # Connect syringe-calibration button
        self.maintenancetools_ui.button_calibrate.clicked.connect(self.calibrate_syringe)

        # Connect syringe-purge button
        self.maintenancetools_ui.button_purge.clicked.connect(self.purge_syringe)

    ####################################################################################################################
    # Syringe dimensions
    def change_syringe_volume(self):
        self.maintenancetools_ui.lineEdit_syringe_volume.setStyleSheet("color: 'orange';")

    def apply_change_syringe_volume(self):
        success = self.maintenancetools.pump.set_syringe_volume(float(self.maintenancetools_ui.lineEdit_syringe_volume.text()))
        if success:
            self.maintenancetools_ui.lineEdit_syringe_volume.setStyleSheet("color: 'green';")
        else:
            self.maintenancetools_ui.lineEdit_syringe_volume.setStyleSheet("color: 'red';")

    def change_syringe_diameter(self):
        self.maintenancetools_ui.lineEdit_syringe_diameter.setStyleSheet("color: 'orange';")

    def apply_change_syringe_diameter(self):
        success = self.maintenancetools.pump.set_syringe_diameter(float(self.maintenancetools_ui.lineEdit_syringe_diameter.text()))
        if success:
            self.maintenancetools_ui.lineEdit_syringe_diameter.setStyleSheet("color: 'green';")
        else:
            self.maintenancetools_ui.lineEdit_syringe_diameter.setStyleSheet("color: 'red';")

    ####################################################################################################################
    # Syringe calibration
    def calibrate_syringe(self):
        self.max_target_volume = self.maintenancetools.pump.calibrate_syringe()
        self.maintenancetools_ui.lineEdit_max_pumping_volume.setText("{0:.6g}".format(self.max_target_volume))

    ####################################################################################################################
    # Syringe purge
    def purge_syringe(self):
        cycles = int(self.maintenancetools_ui.lineEdit_purge_cycles.text())
        self.maintenancetools.purge_pump(cycles)