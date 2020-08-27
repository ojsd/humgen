# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../pyqt/electrovalvewindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ElectrovalveWindow(object):
    def setupUi(self, ElectrovalveWindow):
        ElectrovalveWindow.setObjectName("ElectrovalveWindow")
        ElectrovalveWindow.resize(182, 213)
        self.verticalLayoutWidget = QtWidgets.QWidget(ElectrovalveWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 161, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_electrovalve1 = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.groupBox_electrovalve1.setObjectName("groupBox_electrovalve1")
        self.ev1_radioButton_open = QtWidgets.QRadioButton(self.groupBox_electrovalve1)
        self.ev1_radioButton_open.setGeometry(QtCore.QRect(20, 30, 151, 20))
        self.ev1_radioButton_open.setObjectName("ev1_radioButton_open")
        self.ev1_radioButton_closed = QtWidgets.QRadioButton(self.groupBox_electrovalve1)
        self.ev1_radioButton_closed.setGeometry(QtCore.QRect(20, 60, 151, 20))
        self.ev1_radioButton_closed.setObjectName("ev1_radioButton_closed")
        self.verticalLayout.addWidget(self.groupBox_electrovalve1)
        self.groupBox_electrovalve2 = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.groupBox_electrovalve2.setObjectName("groupBox_electrovalve2")
        self.ev2_radioButton_open = QtWidgets.QRadioButton(self.groupBox_electrovalve2)
        self.ev2_radioButton_open.setGeometry(QtCore.QRect(20, 30, 151, 20))
        self.ev2_radioButton_open.setObjectName("ev2_radioButton_open")
        self.ev2_radioButton_closed = QtWidgets.QRadioButton(self.groupBox_electrovalve2)
        self.ev2_radioButton_closed.setGeometry(QtCore.QRect(20, 60, 151, 20))
        self.ev2_radioButton_closed.setObjectName("ev2_radioButton_closed")
        self.verticalLayout.addWidget(self.groupBox_electrovalve2)
        self.action_pump = QtWidgets.QAction(ElectrovalveWindow)
        self.action_pump.setObjectName("action_pump")
        self.action_flows = QtWidgets.QAction(ElectrovalveWindow)
        self.action_flows.setObjectName("action_flows")
        self.action_pressure = QtWidgets.QAction(ElectrovalveWindow)
        self.action_pressure.setObjectName("action_pressure")
        self.action_valve2x3 = QtWidgets.QAction(ElectrovalveWindow)
        self.action_valve2x3.setObjectName("action_valve2x3")
        self.action_electrovalves = QtWidgets.QAction(ElectrovalveWindow)
        self.action_electrovalves.setObjectName("action_electrovalves")

        self.retranslateUi(ElectrovalveWindow)
        QtCore.QMetaObject.connectSlotsByName(ElectrovalveWindow)

    def retranslateUi(self, ElectrovalveWindow):
        _translate = QtCore.QCoreApplication.translate
        ElectrovalveWindow.setWindowTitle(_translate("ElectrovalveWindow", "Electrovalves"))
        self.groupBox_electrovalve1.setTitle(_translate("ElectrovalveWindow", "Electrovalve 1 VERT"))
        self.ev1_radioButton_open.setText(_translate("ElectrovalveWindow", "Open"))
        self.ev1_radioButton_closed.setText(_translate("ElectrovalveWindow", "Closed"))
        self.groupBox_electrovalve2.setTitle(_translate("ElectrovalveWindow", "Electrovalve 2 JAUNE"))
        self.ev2_radioButton_open.setText(_translate("ElectrovalveWindow", "Open"))
        self.ev2_radioButton_closed.setText(_translate("ElectrovalveWindow", "Closed"))
        self.action_pump.setText(_translate("ElectrovalveWindow", "Syringe pump"))
        self.action_flows.setText(_translate("ElectrovalveWindow", "Flow controllers"))
        self.action_pressure.setText(_translate("ElectrovalveWindow", "Pressure controller"))
        self.action_valve2x3.setText(_translate("ElectrovalveWindow", "Double 3-ways valve"))
        self.action_electrovalves.setText(_translate("ElectrovalveWindow", "Electro-valves"))

