# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../pyqt/statewindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StateWindow(object):
    def setupUi(self, StateWindow):
        StateWindow.setObjectName("StateWindow")
        StateWindow.resize(405, 187)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(StateWindow)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 353, 141))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_isocalib_rate = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_isocalib_rate.setObjectName("label_isocalib_rate")
        self.gridLayout.addWidget(self.label_isocalib_rate, 0, 0, 1, 1)
        self.lineEdit_primary_flow = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_primary_flow.setStyleSheet("")
        self.lineEdit_primary_flow.setFrame(True)
        self.lineEdit_primary_flow.setReadOnly(True)
        self.lineEdit_primary_flow.setObjectName("lineEdit_primary_flow")
        self.gridLayout.addWidget(self.lineEdit_primary_flow, 2, 1, 1, 1)
        self.label_secondary_flow = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_secondary_flow.setObjectName("label_secondary_flow")
        self.gridLayout.addWidget(self.label_secondary_flow, 3, 0, 1, 1)
        self.label_primary_flow = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_primary_flow.setObjectName("label_primary_flow")
        self.gridLayout.addWidget(self.label_primary_flow, 2, 0, 1, 1)
        self.label_boost_factor = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_boost_factor.setObjectName("label_boost_factor")
        self.gridLayout.addWidget(self.label_boost_factor, 1, 0, 1, 1)
        self.lineEdit_secondary_flow = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_secondary_flow.setObjectName("lineEdit_secondary_flow")
        self.gridLayout.addWidget(self.lineEdit_secondary_flow, 3, 1, 1, 1)
        self.lineEdit_boost_factor = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_boost_factor.setObjectName("lineEdit_boost_factor")
        self.gridLayout.addWidget(self.lineEdit_boost_factor, 1, 1, 1, 1)
        self.lineEdit_isocalib_rate = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_isocalib_rate.setObjectName("lineEdit_isocalib_rate")
        self.gridLayout.addWidget(self.lineEdit_isocalib_rate, 0, 1, 1, 1)
        self.action_pump = QtWidgets.QAction(StateWindow)
        self.action_pump.setObjectName("action_pump")
        self.action_flows = QtWidgets.QAction(StateWindow)
        self.action_flows.setObjectName("action_flows")
        self.action_pressure = QtWidgets.QAction(StateWindow)
        self.action_pressure.setObjectName("action_pressure")
        self.action_valve2x3 = QtWidgets.QAction(StateWindow)
        self.action_valve2x3.setObjectName("action_valve2x3")
        self.action_electrovalves = QtWidgets.QAction(StateWindow)
        self.action_electrovalves.setObjectName("action_electrovalves")

        self.retranslateUi(StateWindow)
        QtCore.QMetaObject.connectSlotsByName(StateWindow)

    def retranslateUi(self, StateWindow):
        _translate = QtCore.QCoreApplication.translate
        StateWindow.setWindowTitle(_translate("StateWindow", "State"))
        self.label_isocalib_rate.setText(_translate("StateWindow", "Isocalib rate (µL/min): "))
        self.lineEdit_primary_flow.setToolTip(_translate("StateWindow", "<html><head/><body><p>Value of the air flow used in the primary air path.</p></body></html>"))
        self.label_secondary_flow.setText(_translate("StateWindow", "Secondary flow (mln/min): "))
        self.label_primary_flow.setText(_translate("StateWindow", "Primary flow (mln/min): "))
        self.label_boost_factor.setText(_translate("StateWindow", "Isocalib rate boost factor: "))
        self.lineEdit_secondary_flow.setToolTip(_translate("StateWindow", "Value of the air flow used in the secondary air path."))
        self.lineEdit_boost_factor.setToolTip(_translate("StateWindow", "<html><head/><body><p>Multiplicative factor applied to Isocalib rate.</p><p>During state &quot;Init calib: Step 2&quot;, syringe pump infusion rate will be multiplied by this number.</p></body></html>"))
        self.lineEdit_isocalib_rate.setToolTip(_translate("StateWindow", "<html><head/><body><p>Syringe pump infusion rate used when in state &quot;IsoCalib: Std A&quot; or &quot;IsoCalib: Std B&quot;.</p></body></html>"))
        self.action_pump.setText(_translate("StateWindow", "Syringe pump"))
        self.action_flows.setText(_translate("StateWindow", "Flow controllers"))
        self.action_pressure.setText(_translate("StateWindow", "Pressure controller"))
        self.action_valve2x3.setText(_translate("StateWindow", "Double 3-ways valve"))
        self.action_electrovalves.setText(_translate("StateWindow", "Electro-valves"))

