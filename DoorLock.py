# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DoorLock.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(951, 605)
        Form.setMinimumSize(QtCore.QSize(951, 605))
        Form.setMaximumSize(QtCore.QSize(951, 605))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(100, 10, 751, 61))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(290, 100, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(250, 250, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 250, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(410, 340, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(410, 430, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(250, 430, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(250, 340, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(570, 250, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(Form)
        self.pushButton_8.setGeometry(QtCore.QRect(570, 340, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(Form)
        self.pushButton_9.setGeometry(QtCore.QRect(570, 430, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(Form)
        self.pushButton_10.setGeometry(QtCore.QRect(250, 520, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(Form)
        self.pushButton_11.setGeometry(QtCore.QRect(410, 520, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_11.setFont(font)
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(Form)
        self.pushButton_12.setGeometry(QtCore.QRect(570, 520, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_12.setFont(font)
        self.pushButton_12.setObjectName("pushButton_12")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(290, 150, 341, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "智能密码锁"))
        self.label.setText(_translate("Form", "Micro/Nano Electronic Devices Research group"))
        self.label_2.setText(_translate("Form", "please enter the password:"))
        self.pushButton.setText(_translate("Form", "1"))
        self.pushButton_2.setText(_translate("Form", "2"))
        self.pushButton_3.setText(_translate("Form", "5"))
        self.pushButton_4.setText(_translate("Form", "8"))
        self.pushButton_5.setText(_translate("Form", "7"))
        self.pushButton_6.setText(_translate("Form", "4"))
        self.pushButton_7.setText(_translate("Form", "3"))
        self.pushButton_8.setText(_translate("Form", "6"))
        self.pushButton_9.setText(_translate("Form", "9"))
        self.pushButton_10.setText(_translate("Form", "close"))
        self.pushButton_11.setText(_translate("Form", "0"))
        self.pushButton_12.setText(_translate("Form", "clear"))
