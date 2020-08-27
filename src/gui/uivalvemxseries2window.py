# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../pyqt/valvemxseries2window.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ValveMxSeries2Window(object):
    def setupUi(self, ValveMxSeries2Window):
        ValveMxSeries2Window.setObjectName("ValveMxSeries2Window")
        ValveMxSeries2Window.resize(202, 112)
        self.groupBox_valve2x3 = QtWidgets.QGroupBox(ValveMxSeries2Window)
        self.groupBox_valve2x3.setGeometry(QtCore.QRect(10, 10, 181, 91))
        self.groupBox_valve2x3.setObjectName("groupBox_valve2x3")
        self.radioButton_from_standards = QtWidgets.QRadioButton(self.groupBox_valve2x3)
        self.radioButton_from_standards.setGeometry(QtCore.QRect(20, 30, 151, 20))
        self.radioButton_from_standards.setObjectName("radioButton_from_standards")
        self.radioButton_to_chamber = QtWidgets.QRadioButton(self.groupBox_valve2x3)
        self.radioButton_to_chamber.setGeometry(QtCore.QRect(20, 60, 151, 20))
        self.radioButton_to_chamber.setObjectName("radioButton_to_chamber")
        self.action_pump = QtWidgets.QAction(ValveMxSeries2Window)
        self.action_pump.setObjectName("action_pump")
        self.action_flows = QtWidgets.QAction(ValveMxSeries2Window)
        self.action_flows.setObjectName("action_flows")
        self.action_pressure = QtWidgets.QAction(ValveMxSeries2Window)
        self.action_pressure.setObjectName("action_pressure")
        self.action_valve2x3 = QtWidgets.QAction(ValveMxSeries2Window)
        self.action_valve2x3.setObjectName("action_valve2x3")
        self.action_electrovalves = QtWidgets.QAction(ValveMxSeries2Window)
        self.action_electrovalves.setObjectName("action_electrovalves")

        self.retranslateUi(ValveMxSeries2Window)
        QtCore.QMetaObject.connectSlotsByName(ValveMxSeries2Window)

    def retranslateUi(self, ValveMxSeries2Window):
        _translate = QtCore.QCoreApplication.translate
        ValveMxSeries2Window.setWindowTitle(_translate("ValveMxSeries2Window", "Double 3-ways valve"))
        self.groupBox_valve2x3.setTitle(_translate("ValveMxSeries2Window", "Double 3-ways Valve"))
        self.radioButton_from_standards.setText(_translate("ValveMxSeries2Window", "From Standards (P1)"))
        self.radioButton_to_chamber.setText(_translate("ValveMxSeries2Window", "To Chambers (P2)"))
        self.action_pump.setText(_translate("ValveMxSeries2Window", "Syringe pump"))
        self.action_flows.setText(_translate("ValveMxSeries2Window", "Flow controllers"))
        self.action_pressure.setText(_translate("ValveMxSeries2Window", "Pressure controller"))
        self.action_valve2x3.setText(_translate("ValveMxSeries2Window", "Double 3-ways valve"))
        self.action_electrovalves.setText(_translate("ValveMxSeries2Window", "Electro-valves"))

