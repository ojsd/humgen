# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../pyqt/elpresswindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ElPressWindow(object):
    def setupUi(self, ElPressWindow):
        ElPressWindow.setObjectName("ElPressWindow")
        ElPressWindow.resize(197, 127)
        self.groupBox_pressure = QtWidgets.QGroupBox(ElPressWindow)
        self.groupBox_pressure.setGeometry(QtCore.QRect(0, 10, 191, 111))
        self.groupBox_pressure.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.groupBox_pressure.setObjectName("groupBox_pressure")
        self.lineEdit_pressure = QtWidgets.QLineEdit(self.groupBox_pressure)
        self.lineEdit_pressure.setGeometry(QtCore.QRect(90, 60, 91, 28))
        self.lineEdit_pressure.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_pressure.setReadOnly(True)
        self.lineEdit_pressure.setObjectName("lineEdit_pressure")
        self.label_setpoint = QtWidgets.QLabel(self.groupBox_pressure)
        self.label_setpoint.setGeometry(QtCore.QRect(10, 40, 71, 16))
        self.label_setpoint.setObjectName("label_setpoint")
        self.label_pressure = QtWidgets.QLabel(self.groupBox_pressure)
        self.label_pressure.setGeometry(QtCore.QRect(10, 70, 71, 16))
        self.label_pressure.setObjectName("label_pressure")
        self.lineEdit_setpoint = QtWidgets.QLineEdit(self.groupBox_pressure)
        self.lineEdit_setpoint.setGeometry(QtCore.QRect(90, 30, 91, 31))
        self.lineEdit_setpoint.setReadOnly(False)
        self.lineEdit_setpoint.setObjectName("lineEdit_setpoint")
        self.action_pump = QtWidgets.QAction(ElPressWindow)
        self.action_pump.setObjectName("action_pump")
        self.action_flows = QtWidgets.QAction(ElPressWindow)
        self.action_flows.setObjectName("action_flows")
        self.action_pressure = QtWidgets.QAction(ElPressWindow)
        self.action_pressure.setObjectName("action_pressure")
        self.action_valve2x3 = QtWidgets.QAction(ElPressWindow)
        self.action_valve2x3.setObjectName("action_valve2x3")
        self.action_electrovalves = QtWidgets.QAction(ElPressWindow)
        self.action_electrovalves.setObjectName("action_electrovalves")

        self.retranslateUi(ElPressWindow)
        QtCore.QMetaObject.connectSlotsByName(ElPressWindow)

    def retranslateUi(self, ElPressWindow):
        _translate = QtCore.QCoreApplication.translate
        ElPressWindow.setWindowTitle(_translate("ElPressWindow", "Pressure"))
        self.groupBox_pressure.setTitle(_translate("ElPressWindow", "Pressure Controller"))
        self.label_setpoint.setText(_translate("ElPressWindow", "Setpoint:"))
        self.label_pressure.setText(_translate("ElPressWindow", "Pressure:"))
        self.action_pump.setText(_translate("ElPressWindow", "Syringe pump"))
        self.action_flows.setText(_translate("ElPressWindow", "Flow controllers"))
        self.action_pressure.setText(_translate("ElPressWindow", "Pressure controller"))
        self.action_valve2x3.setText(_translate("ElPressWindow", "Double 3-ways valve"))
        self.action_electrovalves.setText(_translate("ElPressWindow", "Electro-valves"))

