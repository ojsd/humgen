# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../pyqt/pump11elitewindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Pump11EliteWindow(object):
    def setupUi(self, Pump11EliteWindow):
        Pump11EliteWindow.setObjectName("Pump11EliteWindow")
        Pump11EliteWindow.resize(392, 362)
        self.layoutWidget = QtWidgets.QWidget(Pump11EliteWindow)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 355, 104))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_volume = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_volume.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_volume.setObjectName("gridLayout_volume")
        self.button_read_volume_infuse = QtWidgets.QToolButton(self.layoutWidget)
        self.button_read_volume_infuse.setObjectName("button_read_volume_infuse")
        self.gridLayout_volume.addWidget(self.button_read_volume_infuse, 1, 3, 1, 1)
        self.button_clear_volume_infuse = QtWidgets.QToolButton(self.layoutWidget)
        self.button_clear_volume_infuse.setObjectName("button_clear_volume_infuse")
        self.gridLayout_volume.addWidget(self.button_clear_volume_infuse, 1, 4, 1, 1)
        self.button_clear_volume_target = QtWidgets.QToolButton(self.layoutWidget)
        self.button_clear_volume_target.setObjectName("button_clear_volume_target")
        self.gridLayout_volume.addWidget(self.button_clear_volume_target, 0, 4, 1, 1)
        self.button_read_volume_withdraw = QtWidgets.QToolButton(self.layoutWidget)
        self.button_read_volume_withdraw.setObjectName("button_read_volume_withdraw")
        self.gridLayout_volume.addWidget(self.button_read_volume_withdraw, 2, 3, 1, 1)
        self.button_clear_volume_withdraw = QtWidgets.QToolButton(self.layoutWidget)
        self.button_clear_volume_withdraw.setObjectName("button_clear_volume_withdraw")
        self.gridLayout_volume.addWidget(self.button_clear_volume_withdraw, 2, 4, 1, 1)
        self.label_volume_target = QtWidgets.QLabel(self.layoutWidget)
        self.label_volume_target.setObjectName("label_volume_target")
        self.gridLayout_volume.addWidget(self.label_volume_target, 0, 0, 1, 1)
        self.lineEdit_volume_target = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_volume_target.setReadOnly(False)
        self.lineEdit_volume_target.setObjectName("lineEdit_volume_target")
        self.gridLayout_volume.addWidget(self.lineEdit_volume_target, 0, 1, 1, 1)
        self.label_volume_infuse = QtWidgets.QLabel(self.layoutWidget)
        self.label_volume_infuse.setObjectName("label_volume_infuse")
        self.gridLayout_volume.addWidget(self.label_volume_infuse, 1, 0, 1, 1)
        self.lineEdit_volume_infuse = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_volume_infuse.setReadOnly(True)
        self.lineEdit_volume_infuse.setObjectName("lineEdit_volume_infuse")
        self.gridLayout_volume.addWidget(self.lineEdit_volume_infuse, 1, 1, 1, 1)
        self.label_volume_withdrawn = QtWidgets.QLabel(self.layoutWidget)
        self.label_volume_withdrawn.setObjectName("label_volume_withdrawn")
        self.gridLayout_volume.addWidget(self.label_volume_withdrawn, 2, 0, 1, 1)
        self.lineEdit_volume_withdraw = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_volume_withdraw.setReadOnly(True)
        self.lineEdit_volume_withdraw.setObjectName("lineEdit_volume_withdraw")
        self.gridLayout_volume.addWidget(self.lineEdit_volume_withdraw, 2, 1, 1, 1)
        self.button_read_all = QtWidgets.QToolButton(Pump11EliteWindow)
        self.button_read_all.setGeometry(QtCore.QRect(240, 260, 101, 30))
        self.button_read_all.setObjectName("button_read_all")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(Pump11EliteWindow)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 260, 211, 84))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_rate = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_rate.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_rate.setObjectName("gridLayout_rate")
        self.lineEdit_rate_infuse = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_rate_infuse.setReadOnly(False)
        self.lineEdit_rate_infuse.setObjectName("lineEdit_rate_infuse")
        self.gridLayout_rate.addWidget(self.lineEdit_rate_infuse, 0, 1, 1, 1)
        self.label_rate_withdraw = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_rate_withdraw.setObjectName("label_rate_withdraw")
        self.gridLayout_rate.addWidget(self.label_rate_withdraw, 1, 0, 1, 1)
        self.lineEdit_rate_withdraw = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_rate_withdraw.setReadOnly(False)
        self.lineEdit_rate_withdraw.setObjectName("lineEdit_rate_withdraw")
        self.gridLayout_rate.addWidget(self.lineEdit_rate_withdraw, 1, 1, 1, 1)
        self.label_rate_infuse = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_rate_infuse.setObjectName("label_rate_infuse")
        self.gridLayout_rate.addWidget(self.label_rate_infuse, 0, 0, 1, 1)
        self.gridLayoutWidget_4 = QtWidgets.QWidget(Pump11EliteWindow)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(20, 140, 324, 104))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_move = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_move.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_move.setObjectName("gridLayout_move")
        self.button_infuse = QtWidgets.QToolButton(self.gridLayoutWidget_4)
        self.button_infuse.setObjectName("button_infuse")
        self.gridLayout_move.addWidget(self.button_infuse, 1, 0, 1, 1)
        self.button_run = QtWidgets.QToolButton(self.gridLayoutWidget_4)
        self.button_run.setEnabled(True)
        self.button_run.setObjectName("button_run")
        self.gridLayout_move.addWidget(self.button_run, 0, 1, 1, 1)
        self.button_stop = QtWidgets.QToolButton(self.gridLayoutWidget_4)
        self.button_stop.setEnabled(True)
        self.button_stop.setObjectName("button_stop")
        self.gridLayout_move.addWidget(self.button_stop, 1, 1, 1, 1)
        self.button_withdraw = QtWidgets.QToolButton(self.gridLayoutWidget_4)
        self.button_withdraw.setObjectName("button_withdraw")
        self.gridLayout_move.addWidget(self.button_withdraw, 1, 2, 1, 1)
        self.button_reverse = QtWidgets.QToolButton(self.gridLayoutWidget_4)
        self.button_reverse.setEnabled(True)
        self.button_reverse.setObjectName("button_reverse")
        self.gridLayout_move.addWidget(self.button_reverse, 2, 1, 1, 1)
        self.button_reset_to_start = QtWidgets.QToolButton(self.gridLayoutWidget_4)
        self.button_reset_to_start.setObjectName("button_reset_to_start")
        self.gridLayout_move.addWidget(self.button_reset_to_start, 0, 2, 1, 1)

        self.retranslateUi(Pump11EliteWindow)
        QtCore.QMetaObject.connectSlotsByName(Pump11EliteWindow)

    def retranslateUi(self, Pump11EliteWindow):
        _translate = QtCore.QCoreApplication.translate
        Pump11EliteWindow.setWindowTitle(_translate("Pump11EliteWindow", "Pump 11 Elite"))
        self.button_read_volume_infuse.setText(_translate("Pump11EliteWindow", "Read"))
        self.button_clear_volume_infuse.setText(_translate("Pump11EliteWindow", "Clear"))
        self.button_clear_volume_target.setText(_translate("Pump11EliteWindow", "Clear"))
        self.button_read_volume_withdraw.setText(_translate("Pump11EliteWindow", "Read"))
        self.button_clear_volume_withdraw.setText(_translate("Pump11EliteWindow", "Clear"))
        self.label_volume_target.setText(_translate("Pump11EliteWindow", "Target volume (µL):"))
        self.label_volume_infuse.setText(_translate("Pump11EliteWindow", "Infused (µL):"))
        self.label_volume_withdrawn.setText(_translate("Pump11EliteWindow", "Withdrawn (µL):"))
        self.button_read_all.setText(_translate("Pump11EliteWindow", "Read All"))
        self.label_rate_withdraw.setText(_translate("Pump11EliteWindow", "W Rate (µL/min):"))
        self.label_rate_infuse.setText(_translate("Pump11EliteWindow", "I Rate(µL/min):"))
        self.button_infuse.setText(_translate("Pump11EliteWindow", "Infuse"))
        self.button_run.setText(_translate("Pump11EliteWindow", "Run"))
        self.button_stop.setText(_translate("Pump11EliteWindow", "Stop"))
        self.button_withdraw.setText(_translate("Pump11EliteWindow", "Withdraw"))
        self.button_reverse.setText(_translate("Pump11EliteWindow", "Reverse"))
        self.button_reset_to_start.setText(_translate("Pump11EliteWindow", "Reset to start position"))

