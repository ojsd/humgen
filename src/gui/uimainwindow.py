# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../pyqt/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(719, 552)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_pump = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_pump.setGeometry(QtCore.QRect(10, 90, 241, 181))
        self.groupBox_pump.setObjectName("groupBox_pump")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_pump)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 221, 141))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_volume = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_volume.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_volume.setObjectName("gridLayout_volume")
        self.pump_label_volume_withdraw = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.pump_label_volume_withdraw.setObjectName("pump_label_volume_withdraw")
        self.gridLayout_volume.addWidget(self.pump_label_volume_withdraw, 1, 0, 1, 1)
        self.pump_label_volume_infuse = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.pump_label_volume_infuse.setObjectName("pump_label_volume_infuse")
        self.gridLayout_volume.addWidget(self.pump_label_volume_infuse, 0, 0, 1, 1)
        self.pump_lineEdit_volume_withdraw = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.pump_lineEdit_volume_withdraw.setReadOnly(True)
        self.pump_lineEdit_volume_withdraw.setObjectName("pump_lineEdit_volume_withdraw")
        self.gridLayout_volume.addWidget(self.pump_lineEdit_volume_withdraw, 1, 1, 1, 1)
        self.pump_lineEdit_volume_infuse = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.pump_lineEdit_volume_infuse.setReadOnly(True)
        self.pump_lineEdit_volume_infuse.setObjectName("pump_lineEdit_volume_infuse")
        self.gridLayout_volume.addWidget(self.pump_lineEdit_volume_infuse, 0, 1, 1, 1)
        self.pump_label_rate_infuse = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.pump_label_rate_infuse.setObjectName("pump_label_rate_infuse")
        self.gridLayout_volume.addWidget(self.pump_label_rate_infuse, 2, 0, 1, 1)
        self.pump_lineEdit_rate_infuse = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.pump_lineEdit_rate_infuse.setReadOnly(True)
        self.pump_lineEdit_rate_infuse.setObjectName("pump_lineEdit_rate_infuse")
        self.gridLayout_volume.addWidget(self.pump_lineEdit_rate_infuse, 2, 1, 1, 1)
        self.pump_label_rate_withdraw = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.pump_label_rate_withdraw.setObjectName("pump_label_rate_withdraw")
        self.gridLayout_volume.addWidget(self.pump_label_rate_withdraw, 3, 0, 1, 1)
        self.pump_lineEdit_rate_withdraw = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.pump_lineEdit_rate_withdraw.setReadOnly(True)
        self.pump_lineEdit_rate_withdraw.setObjectName("pump_lineEdit_rate_withdraw")
        self.gridLayout_volume.addWidget(self.pump_lineEdit_rate_withdraw, 3, 1, 1, 1)
        self.groupBox_valve2x3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_valve2x3.setGeometry(QtCore.QRect(10, 10, 241, 71))
        self.groupBox_valve2x3.setObjectName("groupBox_valve2x3")
        self.horizontalLayoutWidget_6 = QtWidgets.QWidget(self.groupBox_valve2x3)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(10, 30, 221, 31))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.valve2x3_label_position = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        self.valve2x3_label_position.setObjectName("valve2x3_label_position")
        self.horizontalLayout_3.addWidget(self.valve2x3_label_position)
        self.valve2x3_lineEdit_position = QtWidgets.QLineEdit(self.horizontalLayoutWidget_6)
        self.valve2x3_lineEdit_position.setReadOnly(True)
        self.valve2x3_lineEdit_position.setObjectName("valve2x3_lineEdit_position")
        self.horizontalLayout_3.addWidget(self.valve2x3_lineEdit_position)
        self.groupBox_flowA = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_flowA.setGeometry(QtCore.QRect(10, 280, 241, 101))
        self.groupBox_flowA.setObjectName("groupBox_flowA")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox_flowA)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 221, 64))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_flowA = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_flowA.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_flowA.setObjectName("gridLayout_flowA")
        self.flowA_label_flow = QtWidgets.QLabel(self.gridLayoutWidget)
        self.flowA_label_flow.setObjectName("flowA_label_flow")
        self.gridLayout_flowA.addWidget(self.flowA_label_flow, 0, 0, 1, 1)
        self.flowA_lineEdit_flow = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.flowA_lineEdit_flow.setReadOnly(True)
        self.flowA_lineEdit_flow.setObjectName("flowA_lineEdit_flow")
        self.gridLayout_flowA.addWidget(self.flowA_lineEdit_flow, 0, 1, 1, 1)
        self.flowA_lineEdit_control_function = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.flowA_lineEdit_control_function.setReadOnly(True)
        self.flowA_lineEdit_control_function.setObjectName("flowA_lineEdit_control_function")
        self.gridLayout_flowA.addWidget(self.flowA_lineEdit_control_function, 1, 1, 1, 1)
        self.flowA_label_control_function = QtWidgets.QLabel(self.gridLayoutWidget)
        self.flowA_label_control_function.setObjectName("flowA_label_control_function")
        self.gridLayout_flowA.addWidget(self.flowA_label_control_function, 1, 0, 1, 1)
        self.groupBox_flowB = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_flowB.setGeometry(QtCore.QRect(10, 390, 241, 101))
        self.groupBox_flowB.setObjectName("groupBox_flowB")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_flowB)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 30, 221, 61))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_flowB = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_flowB.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_flowB.setObjectName("gridLayout_flowB")
        self.flowB_label_flow = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.flowB_label_flow.setObjectName("flowB_label_flow")
        self.gridLayout_flowB.addWidget(self.flowB_label_flow, 0, 0, 1, 1)
        self.flowB_lineEdit_flow = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.flowB_lineEdit_flow.setReadOnly(True)
        self.flowB_lineEdit_flow.setObjectName("flowB_lineEdit_flow")
        self.gridLayout_flowB.addWidget(self.flowB_lineEdit_flow, 0, 1, 1, 1)
        self.flowB_label_control_function = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.flowB_label_control_function.setObjectName("flowB_label_control_function")
        self.gridLayout_flowB.addWidget(self.flowB_label_control_function, 1, 0, 1, 1)
        self.flowB_lineEdit_control_function = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.flowB_lineEdit_control_function.setReadOnly(True)
        self.flowB_lineEdit_control_function.setObjectName("flowB_lineEdit_control_function")
        self.gridLayout_flowB.addWidget(self.flowB_lineEdit_control_function, 1, 1, 1, 1)
        self.groupBox_pressure = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_pressure.setGeometry(QtCore.QRect(270, 10, 241, 71))
        self.groupBox_pressure.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.groupBox_pressure.setObjectName("groupBox_pressure")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox_pressure)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 221, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pressure_label_pressure = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.pressure_label_pressure.setObjectName("pressure_label_pressure")
        self.horizontalLayout.addWidget(self.pressure_label_pressure)
        self.pressure_lineEdit_pressure = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.pressure_lineEdit_pressure.setMinimumSize(QtCore.QSize(0, 28))
        self.pressure_lineEdit_pressure.setReadOnly(True)
        self.pressure_lineEdit_pressure.setObjectName("pressure_lineEdit_pressure")
        self.horizontalLayout.addWidget(self.pressure_lineEdit_pressure)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(270, 90, 241, 151))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_electrovalve1 = QtWidgets.QGroupBox(self.verticalLayoutWidget_2)
        self.groupBox_electrovalve1.setObjectName("groupBox_electrovalve1")
        self.horizontalLayoutWidget_7 = QtWidgets.QWidget(self.groupBox_electrovalve1)
        self.horizontalLayoutWidget_7.setGeometry(QtCore.QRect(10, 30, 221, 31))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ev1_label_position = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        self.ev1_label_position.setObjectName("ev1_label_position")
        self.horizontalLayout_4.addWidget(self.ev1_label_position)
        self.ev1_lineEdit_position = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        self.ev1_lineEdit_position.setReadOnly(True)
        self.ev1_lineEdit_position.setObjectName("ev1_lineEdit_position")
        self.horizontalLayout_4.addWidget(self.ev1_lineEdit_position)
        self.verticalLayout_2.addWidget(self.groupBox_electrovalve1)
        self.groupBox_electrovalve2 = QtWidgets.QGroupBox(self.verticalLayoutWidget_2)
        self.groupBox_electrovalve2.setObjectName("groupBox_electrovalve2")
        self.horizontalLayoutWidget_8 = QtWidgets.QWidget(self.groupBox_electrovalve2)
        self.horizontalLayoutWidget_8.setGeometry(QtCore.QRect(10, 30, 221, 31))
        self.horizontalLayoutWidget_8.setObjectName("horizontalLayoutWidget_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_8)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ev2_label_position = QtWidgets.QLabel(self.horizontalLayoutWidget_8)
        self.ev2_label_position.setObjectName("ev2_label_position")
        self.horizontalLayout_5.addWidget(self.ev2_label_position)
        self.ev2_lineEdit_position = QtWidgets.QLineEdit(self.horizontalLayoutWidget_8)
        self.ev2_lineEdit_position.setReadOnly(True)
        self.ev2_lineEdit_position.setObjectName("ev2_lineEdit_position")
        self.horizontalLayout_5.addWidget(self.ev2_lineEdit_position)
        self.verticalLayout_2.addWidget(self.groupBox_electrovalve2)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(530, 170, 181, 291))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 30, 161, 252))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_state = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_state.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_state.setObjectName("verticalLayout_state")
        self.state_radioButton_manual = QtWidgets.QRadioButton(self.verticalLayoutWidget_5)
        self.state_radioButton_manual.setObjectName("state_radioButton_manual")
        self.verticalLayout_state.addWidget(self.state_radioButton_manual)
        self.state_radioButton_air = QtWidgets.QRadioButton(self.verticalLayoutWidget_5)
        self.state_radioButton_air.setObjectName("state_radioButton_air")
        self.verticalLayout_state.addWidget(self.state_radioButton_air)
        self.state_radioButton_init_calib_step1 = QtWidgets.QRadioButton(self.verticalLayoutWidget_5)
        self.state_radioButton_init_calib_step1.setObjectName("state_radioButton_init_calib_step1")
        self.verticalLayout_state.addWidget(self.state_radioButton_init_calib_step1)
        self.state_radioButton_init_calib_step2 = QtWidgets.QRadioButton(self.verticalLayoutWidget_5)
        self.state_radioButton_init_calib_step2.setObjectName("state_radioButton_init_calib_step2")
        self.verticalLayout_state.addWidget(self.state_radioButton_init_calib_step2)
        self.state_radioButton_isocalib_stdA = QtWidgets.QRadioButton(self.verticalLayoutWidget_5)
        self.state_radioButton_isocalib_stdA.setObjectName("state_radioButton_isocalib_stdA")
        self.verticalLayout_state.addWidget(self.state_radioButton_isocalib_stdA)
        self.state_radioButton_isocalib_stdB = QtWidgets.QRadioButton(self.verticalLayoutWidget_5)
        self.state_radioButton_isocalib_stdB.setObjectName("state_radioButton_isocalib_stdB")
        self.verticalLayout_state.addWidget(self.state_radioButton_isocalib_stdB)
        self.state_radioButton_reset_calib = QtWidgets.QRadioButton(self.verticalLayoutWidget_5)
        self.state_radioButton_reset_calib.setObjectName("state_radioButton_reset_calib")
        self.verticalLayout_state.addWidget(self.state_radioButton_reset_calib)
        self.state_radioButton_humdep = QtWidgets.QRadioButton(self.verticalLayoutWidget_5)
        self.state_radioButton_humdep.setObjectName("state_radioButton_humdep")
        self.verticalLayout_state.addWidget(self.state_radioButton_humdep)
        self.groupBox_picarro_code = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_picarro_code.setGeometry(QtCore.QRect(530, 10, 181, 71))
        self.groupBox_picarro_code.setObjectName("groupBox_picarro_code")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_picarro_code)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 30, 161, 31))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_picarro = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_picarro.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_picarro.setObjectName("horizontalLayout_picarro")
        self.picarro_label_code = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.picarro_label_code.setObjectName("picarro_label_code")
        self.horizontalLayout_picarro.addWidget(self.picarro_label_code)
        self.picarro_lineEdit_code = QtWidgets.QLineEdit(self.horizontalLayoutWidget_4)
        self.picarro_lineEdit_code.setReadOnly(True)
        self.picarro_lineEdit_code.setObjectName("picarro_lineEdit_code")
        self.horizontalLayout_picarro.addWidget(self.picarro_lineEdit_code)
        self.groupBox_listen_picarro_code = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_listen_picarro_code.setGeometry(QtCore.QRect(530, 90, 181, 71))
        self.groupBox_listen_picarro_code.setObjectName("groupBox_listen_picarro_code")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.groupBox_listen_picarro_code)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(10, 30, 160, 31))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.state_radioButton_picarro_listen = QtWidgets.QRadioButton(self.horizontalLayoutWidget_5)
        self.state_radioButton_picarro_listen.setObjectName("state_radioButton_picarro_listen")
        self.horizontalLayout_2.addWidget(self.state_radioButton_picarro_listen)
        self.state_radioButton_picarro_ignore = QtWidgets.QRadioButton(self.horizontalLayoutWidget_5)
        self.state_radioButton_picarro_ignore.setObjectName("state_radioButton_picarro_ignore")
        self.horizontalLayout_2.addWidget(self.state_radioButton_picarro_ignore)
        self.groupBox_temperature = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_temperature.setGeometry(QtCore.QRect(270, 250, 241, 141))
        self.groupBox_temperature.setObjectName("groupBox_temperature")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_temperature)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 30, 221, 101))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.temperature_label_measure = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.temperature_label_measure.setObjectName("temperature_label_measure")
        self.gridLayout.addWidget(self.temperature_label_measure, 1, 0, 1, 1)
        self.temperature_label_setpoint = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.temperature_label_setpoint.setObjectName("temperature_label_setpoint")
        self.gridLayout.addWidget(self.temperature_label_setpoint, 0, 0, 1, 1)
        self.temperature_lineEdit_setpoint = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.temperature_lineEdit_setpoint.setReadOnly(True)
        self.temperature_lineEdit_setpoint.setObjectName("temperature_lineEdit_setpoint")
        self.gridLayout.addWidget(self.temperature_lineEdit_setpoint, 0, 1, 1, 1)
        self.temperature_lineEdit_measure = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.temperature_lineEdit_measure.setReadOnly(True)
        self.temperature_lineEdit_measure.setObjectName("temperature_lineEdit_measure")
        self.gridLayout.addWidget(self.temperature_lineEdit_measure, 1, 1, 1, 1)
        self.tempswitch_label_position = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.tempswitch_label_position.setObjectName("tempswitch_label_position")
        self.gridLayout.addWidget(self.tempswitch_label_position, 2, 0, 1, 1)
        self.tempswitch_lineEdit_position = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.tempswitch_lineEdit_position.setReadOnly(True)
        self.tempswitch_lineEdit_position.setObjectName("tempswitch_lineEdit_position")
        self.gridLayout.addWidget(self.tempswitch_lineEdit_position, 2, 1, 1, 1)
        self.groupBox_pressure_pump_switch = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_pressure_pump_switch.setGeometry(QtCore.QRect(270, 400, 241, 71))
        self.groupBox_pressure_pump_switch.setObjectName("groupBox_pressure_pump_switch")
        self.horizontalLayoutWidget_9 = QtWidgets.QWidget(self.groupBox_pressure_pump_switch)
        self.horizontalLayoutWidget_9.setGeometry(QtCore.QRect(10, 30, 221, 31))
        self.horizontalLayoutWidget_9.setObjectName("horizontalLayoutWidget_9")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_9)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.ppswitch_label_position = QtWidgets.QLabel(self.horizontalLayoutWidget_9)
        self.ppswitch_label_position.setObjectName("ppswitch_label_position")
        self.horizontalLayout_6.addWidget(self.ppswitch_label_position)
        self.ppswitch_lineEdit_position = QtWidgets.QLineEdit(self.horizontalLayoutWidget_9)
        self.ppswitch_lineEdit_position.setReadOnly(True)
        self.ppswitch_lineEdit_position.setObjectName("ppswitch_lineEdit_position")
        self.horizontalLayout_6.addWidget(self.ppswitch_lineEdit_position)
        self.groupBox_pump.raise_()
        self.groupBox_valve2x3.raise_()
        self.groupBox_flowA.raise_()
        self.groupBox_flowB.raise_()
        self.groupBox_pressure.raise_()
        self.verticalLayoutWidget_2.raise_()
        self.groupBox.raise_()
        self.groupBox_picarro_code.raise_()
        self.groupBox_listen_picarro_code.raise_()
        self.groupBox_temperature.raise_()
        self.groupBox_pressure_pump_switch.raise_()
        self.ev2_label_position.raise_()
        self.flowA_label_control_function.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 719, 26))
        self.menubar.setObjectName("menubar")
        self.menuInstrument = QtWidgets.QMenu(self.menubar)
        self.menuInstrument.setObjectName("menuInstrument")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_pump = QtWidgets.QAction(MainWindow)
        self.action_pump.setObjectName("action_pump")
        self.action_flows = QtWidgets.QAction(MainWindow)
        self.action_flows.setObjectName("action_flows")
        self.action_pressure = QtWidgets.QAction(MainWindow)
        self.action_pressure.setObjectName("action_pressure")
        self.action_valve2x3 = QtWidgets.QAction(MainWindow)
        self.action_valve2x3.setObjectName("action_valve2x3")
        self.action_electrovalves = QtWidgets.QAction(MainWindow)
        self.action_electrovalves.setObjectName("action_electrovalves")
        self.action_maintenancetools = QtWidgets.QAction(MainWindow)
        self.action_maintenancetools.setObjectName("action_maintenancetools")
        self.action_temperature = QtWidgets.QAction(MainWindow)
        self.action_temperature.setObjectName("action_temperature")
        self.action_debuglog = QtWidgets.QAction(MainWindow)
        self.action_debuglog.setObjectName("action_debuglog")
        self.action_state = QtWidgets.QAction(MainWindow)
        self.action_state.setObjectName("action_state")
        self.menuInstrument.addAction(self.action_state)
        self.menuInstrument.addAction(self.action_maintenancetools)
        self.menuInstrument.addAction(self.action_pump)
        self.menuInstrument.addAction(self.action_flows)
        self.menuInstrument.addAction(self.action_pressure)
        self.menuInstrument.addAction(self.action_valve2x3)
        self.menuInstrument.addAction(self.action_electrovalves)
        self.menuInstrument.addAction(self.action_temperature)
        self.menuInstrument.addAction(self.action_debuglog)
        self.menubar.addAction(self.menuInstrument.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pump_lineEdit_volume_infuse, self.pump_lineEdit_volume_withdraw)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Calibration - GLACCIOS"))
        self.groupBox_pump.setTitle(_translate("MainWindow", "Syringe Pump"))
        self.pump_label_volume_withdraw.setText(_translate("MainWindow", "Withdrawn (µL):"))
        self.pump_label_volume_infuse.setText(_translate("MainWindow", "Infused (µL):"))
        self.pump_label_rate_infuse.setText(_translate("MainWindow", "I Rate(µL/min):"))
        self.pump_label_rate_withdraw.setText(_translate("MainWindow", "W Rate (µL/min):"))
        self.groupBox_valve2x3.setTitle(_translate("MainWindow", "Double 3-ways Valve"))
        self.valve2x3_label_position.setText(_translate("MainWindow", "Position: "))
        self.groupBox_flowA.setTitle(_translate("MainWindow", "Flow Controller A"))
        self.flowA_label_flow.setText(_translate("MainWindow", "Flow (mln/min):"))
        self.flowA_label_control_function.setText(_translate("MainWindow", "Ctrl function: "))
        self.groupBox_flowB.setTitle(_translate("MainWindow", "Flow Controller B"))
        self.flowB_label_flow.setText(_translate("MainWindow", "Flow (mln/min):"))
        self.flowB_label_control_function.setText(_translate("MainWindow", "Ctrl function: "))
        self.groupBox_pressure.setTitle(_translate("MainWindow", "Pressure Controller"))
        self.pressure_label_pressure.setText(_translate("MainWindow", "Pressure (mbar):"))
        self.groupBox_electrovalve1.setTitle(_translate("MainWindow", "Electrovalve 1 VERT"))
        self.ev1_label_position.setText(_translate("MainWindow", "Position: "))
        self.groupBox_electrovalve2.setTitle(_translate("MainWindow", "Electrovalve 2 JAUNE"))
        self.ev2_label_position.setText(_translate("MainWindow", "Position: "))
        self.groupBox.setTitle(_translate("MainWindow", "States"))
        self.state_radioButton_manual.setText(_translate("MainWindow", "Manual"))
        self.state_radioButton_air.setText(_translate("MainWindow", "Outside Air"))
        self.state_radioButton_init_calib_step1.setText(_translate("MainWindow", "Init calib: Step 1"))
        self.state_radioButton_init_calib_step2.setText(_translate("MainWindow", "Init calib: Step 2"))
        self.state_radioButton_isocalib_stdA.setText(_translate("MainWindow", "IsoCalib: Std A"))
        self.state_radioButton_isocalib_stdB.setText(_translate("MainWindow", "IsoCalib: Std B"))
        self.state_radioButton_reset_calib.setText(_translate("MainWindow", "Reset calib"))
        self.state_radioButton_humdep.setText(_translate("MainWindow", "HumDep"))
        self.groupBox_picarro_code.setTitle(_translate("MainWindow", "Picarro code"))
        self.picarro_label_code.setText(_translate("MainWindow", "Code:"))
        self.groupBox_listen_picarro_code.setTitle(_translate("MainWindow", "Listen picarro code"))
        self.state_radioButton_picarro_listen.setText(_translate("MainWindow", "Listen"))
        self.state_radioButton_picarro_ignore.setText(_translate("MainWindow", "Ignore"))
        self.groupBox_temperature.setTitle(_translate("MainWindow", "Temperature"))
        self.temperature_label_measure.setText(_translate("MainWindow", "Measure (°C): "))
        self.temperature_label_setpoint.setText(_translate("MainWindow", "Setpoint (°C): "))
        self.tempswitch_label_position.setText(_translate("MainWindow", "Switch: "))
        self.groupBox_pressure_pump_switch.setTitle(_translate("MainWindow", "Pressure pump"))
        self.ppswitch_label_position.setText(_translate("MainWindow", "Switch: "))
        self.menuInstrument.setTitle(_translate("MainWindow", "Expert mode"))
        self.action_pump.setText(_translate("MainWindow", "Syringe pump"))
        self.action_flows.setText(_translate("MainWindow", "Flow controllers"))
        self.action_pressure.setText(_translate("MainWindow", "Pressure controller"))
        self.action_valve2x3.setText(_translate("MainWindow", "Double 3-ways valve"))
        self.action_electrovalves.setText(_translate("MainWindow", "Electro-valves"))
        self.action_maintenancetools.setText(_translate("MainWindow", "Maintenance Tools"))
        self.action_temperature.setText(_translate("MainWindow", "Temperature"))
        self.action_debuglog.setText(_translate("MainWindow", "Debug Log"))
        self.action_state.setText(_translate("MainWindow", "State"))
