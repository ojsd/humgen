# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../pyqt/temperaturewindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TemperatureWindow(object):
    def setupUi(self, TemperatureWindow):
        TemperatureWindow.setObjectName("TemperatureWindow")
        TemperatureWindow.resize(360, 199)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(TemperatureWindow)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 313, 141))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_setpoint = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_setpoint.setObjectName("label_setpoint")
        self.gridLayout.addWidget(self.label_setpoint, 0, 0, 1, 1)
        self.lineEdit_measure = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_measure.setStyleSheet("")
        self.lineEdit_measure.setFrame(True)
        self.lineEdit_measure.setReadOnly(True)
        self.lineEdit_measure.setObjectName("lineEdit_measure")
        self.gridLayout.addWidget(self.lineEdit_measure, 2, 1, 1, 1)
        self.label_switch_position = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_switch_position.setObjectName("label_switch_position")
        self.gridLayout.addWidget(self.label_switch_position, 3, 0, 1, 1)
        self.label_measure = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_measure.setObjectName("label_measure")
        self.gridLayout.addWidget(self.label_measure, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.switch_radioButton_power = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
        self.switch_radioButton_power.setObjectName("switch_radioButton_power")
        self.horizontalLayout_2.addWidget(self.switch_radioButton_power)
        self.switch_radioButton_unpower = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
        self.switch_radioButton_unpower.setObjectName("switch_radioButton_unpower")
        self.horizontalLayout_2.addWidget(self.switch_radioButton_unpower)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 1, 1, 1)
        self.label_refresh = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_refresh.setObjectName("label_refresh")
        self.gridLayout.addWidget(self.label_refresh, 1, 0, 1, 1)
        self.spinBox_refresh = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
        self.spinBox_refresh.setMaximum(1800)
        self.spinBox_refresh.setObjectName("spinBox_refresh")
        self.gridLayout.addWidget(self.spinBox_refresh, 1, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.doubleSpinBox_setpoint = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.doubleSpinBox_setpoint.setDecimals(1)
        self.doubleSpinBox_setpoint.setObjectName("doubleSpinBox_setpoint")
        self.horizontalLayout.addWidget(self.doubleSpinBox_setpoint)
        self.label_plus_minus = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_plus_minus.setObjectName("label_plus_minus")
        self.horizontalLayout.addWidget(self.label_plus_minus)
        self.doubleSpinBox_hysteresis = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.doubleSpinBox_hysteresis.setSingleStep(0.1)
        self.doubleSpinBox_hysteresis.setObjectName("doubleSpinBox_hysteresis")
        self.horizontalLayout.addWidget(self.doubleSpinBox_hysteresis)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.action_pump = QtWidgets.QAction(TemperatureWindow)
        self.action_pump.setObjectName("action_pump")
        self.action_flows = QtWidgets.QAction(TemperatureWindow)
        self.action_flows.setObjectName("action_flows")
        self.action_pressure = QtWidgets.QAction(TemperatureWindow)
        self.action_pressure.setObjectName("action_pressure")
        self.action_valve2x3 = QtWidgets.QAction(TemperatureWindow)
        self.action_valve2x3.setObjectName("action_valve2x3")
        self.action_electrovalves = QtWidgets.QAction(TemperatureWindow)
        self.action_electrovalves.setObjectName("action_electrovalves")

        self.retranslateUi(TemperatureWindow)
        QtCore.QMetaObject.connectSlotsByName(TemperatureWindow)

    def retranslateUi(self, TemperatureWindow):
        _translate = QtCore.QCoreApplication.translate
        TemperatureWindow.setWindowTitle(_translate("TemperatureWindow", "Temperature"))
        self.label_setpoint.setText(_translate("TemperatureWindow", "Setpoint (°C): "))
        self.label_switch_position.setText(_translate("TemperatureWindow", "Switch: "))
        self.label_measure.setText(_translate("TemperatureWindow", "Measure (°C): "))
        self.switch_radioButton_power.setText(_translate("TemperatureWindow", "Power"))
        self.switch_radioButton_unpower.setText(_translate("TemperatureWindow", "Unpower"))
        self.label_refresh.setText(_translate("TemperatureWindow", "Refresh ctrl (s)"))
        self.spinBox_refresh.setToolTip(_translate("TemperatureWindow", "<html><head/><body><p>Period at which the system will check </p><p>if measured temperature is within setpoint range.</p></body></html>"))
        self.label_plus_minus.setText(_translate("TemperatureWindow", "+/-"))
        self.doubleSpinBox_hysteresis.setToolTip(_translate("TemperatureWindow", "Hysteresis"))
        self.action_pump.setText(_translate("TemperatureWindow", "Syringe pump"))
        self.action_flows.setText(_translate("TemperatureWindow", "Flow controllers"))
        self.action_pressure.setText(_translate("TemperatureWindow", "Pressure controller"))
        self.action_valve2x3.setText(_translate("TemperatureWindow", "Double 3-ways valve"))
        self.action_electrovalves.setText(_translate("TemperatureWindow", "Electro-valves"))

