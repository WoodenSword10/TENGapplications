import sys
import threading
import time

import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from DoorLock import Ui_Form

class MyWindow(QMainWindow, Ui_Form):
    password = '123456'
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.textBrowser.textChanged.connect(self.check_password)
        t1 = threading.Thread(target=self.recv_data)
        t1.daemon= True
        t1.start()

    def recv_data(self):
        while True:
            try:
                data = m.readline()
            except:
                continue
            else:
                print(data, len(data), type(data))
                data = str(data, encoding="utf-8")
                if 'a' in data or 'b' in data:
                    data = data[0]
                else:
                    data = int(data[:2]) - 48
                # print(data, type(data))
                if data == 'b':
                    self.textBrowser.clear()
                    self.pushButton_12.setStyleSheet("background-color:#A9D0F5")
                    time.sleep(0.1)
                    self.pushButton_12.setStyleSheet("background-color:none")
                elif data == 'a':
                    self.pushButton_10.setStyleSheet("background-color:#A9D0F5")
                    time.sleep(0.1)
                    self.pushButton_10.setStyleSheet("background-color:none")
                elif data == 0:
                    self.pushButton_11.setStyleSheet("background-color:#A9D0F5")
                    self.textBrowser.insertPlainText('0')
                    time.sleep(0.1)
                    self.pushButton_11.setStyleSheet("background-color:none")
                elif data == 1:
                    self.pushButton.setStyleSheet("background-color:#A9D0F5")
                    self.textBrowser.insertPlainText('1')
                    time.sleep(0.1)
                    self.pushButton.setStyleSheet("background-color:none")
                elif data == 2:
                    self.pushButton_2.setStyleSheet("background-color:#A9D0F5")
                    self.textBrowser.insertPlainText('2')
                    time.sleep(0.1)
                    self.pushButton_2.setStyleSheet("background-color:none")
                elif data == 3:
                    self.pushButton_7.setStyleSheet("background-color:#A9D0F5")
                    self.textBrowser.insertPlainText('3')
                    time.sleep(0.1)
                    self.pushButton_7.setStyleSheet("background-color:none")
                elif data == 4:
                    self.pushButton_6.setStyleSheet("background-color:#A9D0F5")
                    self.textBrowser.insertPlainText('4')
                    time.sleep(0.1)
                    self.pushButton_6.setStyleSheet("background-color:none")
                elif data == 5:
                    self.pushButton_3.setStyleSheet("background-color:#A9D0F5")
                    self.textBrowser.insertPlainText('5')
                    time.sleep(0.1)
                    self.pushButton_3.setStyleSheet("background-color:none")
                elif data == 6:
                    self.pushButton_8.setStyleSheet("background-color:#A9D0F5")
                    self.textBrowser.insertPlainText('6')
                    time.sleep(0.1)
                    self.pushButton_8.setStyleSheet("background-color:none")
                elif data == 7:
                    self.pushButton_5.setStyleSheet("background-color:#A9D0F5")
                    self.textBrowser.insertPlainText('7')
                    time.sleep(0.1)
                    self.pushButton_5.setStyleSheet("background-color:none")
                elif data == 8:
                    self.pushButton_4.setStyleSheet("background-color:#A9D0F5")
                    self.textBrowser.insertPlainText('8')
                    time.sleep(0.1)
                    self.pushButton_4.setStyleSheet("background-color:none")
                elif data == 9:
                    self.pushButton_9.setStyleSheet("background-color:#A9D0F5")
                    self.textBrowser.insertPlainText('9')
                    time.sleep(0.1)
                    self.pushButton_9.setStyleSheet("background-color:none")

    def check_password(self):
        box = QMessageBox()
        text = self.textBrowser.toPlainText()
        if len(text) == 6:
            self.textBrowser.clear()
            if text == self.password:
                box.setText('密码正确')
                box.exec_()
            else:
                box.setText('密码错误')
                box.exec_()

if __name__ == '__main__':
    m = serial.Serial('COM3', 9600)
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
