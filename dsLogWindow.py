# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dsLog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dsLog(object):
    def setupUi(self, dsLog):
        dsLog.setObjectName("dsLog")
        dsLog.resize(360, 480)
        dsLog.setMinimumSize(QtCore.QSize(360, 480))
        dsLog.setMaximumSize(QtCore.QSize(360, 480))
        dsLog.setFocusPolicy(QtCore.Qt.StrongFocus)
        dsLog.setWindowTitle("DS Log Converter")
        self.inputList = QtWidgets.QListWidget(dsLog)
        self.inputList.setGeometry(QtCore.QRect(10, 50, 341, 201))
        self.inputList.setObjectName("inputList")
        self.runButton = QtWidgets.QPushButton(dsLog)
        self.runButton.setGeometry(QtCore.QRect(10, 350, 341, 121))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.runButton.setFont(font)
        self.runButton.setDefault(False)
        self.runButton.setFlat(False)
        self.runButton.setObjectName("runButton")
        self.outputList = QtWidgets.QListWidget(dsLog)
        self.outputList.setGeometry(QtCore.QRect(10, 300, 341, 31))
        self.outputList.setObjectName("outputList")
        self.addButton = QtWidgets.QPushButton(dsLog)
        self.addButton.setGeometry(QtCore.QRect(10, 10, 121, 31))
        self.addButton.setObjectName("addButton")
        self.outButton = QtWidgets.QPushButton(dsLog)
        self.outButton.setGeometry(QtCore.QRect(10, 260, 121, 31))
        self.outButton.setObjectName("outButton")

        self.retranslateUi(dsLog)
        QtCore.QMetaObject.connectSlotsByName(dsLog)

    def retranslateUi(self, dsLog):
        _translate = QtCore.QCoreApplication.translate
        self.runButton.setText(_translate("dsLog", "Process Logs"))
        self.addButton.setText(_translate("dsLog", "Add Log File"))
        self.outButton.setText(_translate("dsLog", "Set Out File"))

