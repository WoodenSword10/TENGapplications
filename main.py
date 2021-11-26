import sys
import threading
import time
import re
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import DoorLock
import beginui
import port
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

class recv_data(QThread):
    update_pb = pyqtSignal(int)
    port = serial.Serial()
    def __init__(self, port, reading):
        super(recv_data, self).__init__()
        self.port = port
        self.reading = reading

    def run(self):
        while self.reading:
            try:
                dat = self.port.readline()
            except:
                continue
            else:
                try:
                    dat = str(dat, encoding="utf-8")
                except:
                    continue
                else:
                    pattern = re.compile('[\d]*')
                    dat = pattern.findall(dat)[0]
                    # print(dat)
                    if len(dat) > 0:
                        dat = int(dat)
                        self.update_pb.emit(dat)


class beginWindow(QMainWindow, beginui.Ui_Form):
    mySignal1 = pyqtSignal(str)
    port = serial.Serial()
    def __init__(self, parent=None):
        super(beginWindow, self).__init__(parent)
        self.setupUi(self)
        self.Port_win = portWindow()
        self.mySignal1.connect(self.Port_win.getBeginSignal)
        self.port_find()
        self.pushButton.clicked.connect(self.port_conn)
        self.pushButton_2.clicked.connect(self.port_plot)

    def port_find(self):
        port_list = list(serial.tools.list_ports.comports())
        for item in port_list:
            pattern = re.compile('COM[\d]*')
            item = pattern.findall(str(item))[0]
            self.comboBox.addItem(item)
            self.comboBox_2.addItem(item)

    def port_plot(self):
        self.mySignal1.emit(self.comboBox_2.currentText())
        # beginWin.hide()
        self.Port_win.show()
        pass

    def port_conn(self):
        box = QMessageBox()
        com = self.comboBox.currentText()
        try:
            self.port = serial.Serial(com, 9600)
        except:
            box.setText('<h1><center>串口连接失败！！</center></h1>')
            box.exec_()
            time.sleep(0.2)
            box.close()
        else:
            box.setText('<h1><center>串口连接成功！！</center></h1>')
            box.exec_()
            # beginWin.hide()
            time.sleep(0.2)
            box.close()
            My_win = MyWindow()
            My_win.show()
            self.Port_win.mySignal2.connect(My_win.getPortData)

class portWindow(QMainWindow, port.Ui_Dialog):
    mySignal2 = pyqtSignal(str)
    # 用来接收串口数据
    data = np.zeros(500)
    # 串口实例化，用于连接串口
    COM = serial.Serial()
    # 数据存放位置标记
    i = 0
    # 用于计算数据平均值的计数器
    j = 0
    # 用于累加前100个数据
    sum = 0
    # 用于存放平均值
    avage = 0
    # 用于第一次收到超出平均值过多的数据的标记
    k = 0
    # 用于存放K触发后的数据
    big_data = []
    # 用于存放big_data中的最大值
    max_data = 0
    def __init__(self, parent=None):
        super(portWindow, self).__init__(parent)
        self.setupUi(self)
        self.checkBox.stateChanged.connect(self.connect)

    def connect(self):
        box = QMessageBox()
        if self.checkBox.isChecked():
            if self.i == 0:
                self.i += 1
                com = self.comboBox_5.currentText()
                bote = int(self.comboBox.currentText())
                try:
                    self.COM = serial.Serial(com, bote)
                except:
                    box.setText('<h1><center>连接失败！</center></h1>')
                    box.exec_()
                    time.sleep(0.1)
                    box.close()
                else:
                    box.setText('<h1><center>连接成功！</center></h1>')
                    box.exec_()
                    time.sleep(0.1)
                    box.close()
                    self.thread = recv_data(self.COM, True)
                    self.thread.update_pb.connect(self.plot)
                    self.thread.start()
            else:
                self.thread.reading = True
                box.setText('<h1><center>已连接</center></h1>')
                box.exec_()
                time.sleep(0.1)
                box.close()
        else:
            self.thread.reading = False
            box.setText('<h1><center>连接已断开。</center></h1>')
            box.exec_()
            time.sleep(0.1)
            box.close()

    def getBeginSignal(self, connect):
        self.comboBox_5.addItem(connect)

    def plot(self, connect):
        if self.j < 50:
            self.sum += connect
            self.j += 1
            if self.j == 50:
                self.avage = self.sum / 50
                print('a' + str(self.avage))
                self.j += 1
        else:
            if self.i < 500:
                self.data[self.i] = connect
                self.i += 1
            else:
                self.data[:-1] = self.data[1:]
                self.data[499] = connect
            if connect - self.avage > 300:
                self.big_data.append(connect)
                self.k += 1
            if self.k == 150:
                self.max_data = max(self.big_data)
                if self.max_data - self.avage > 1200:
                    self.mySignal2.emit('4')
                elif self.max_data - self.avage > 1000:
                    self.mySignal2.emit('3')
                elif self.max_data - self.avage > 800:
                    self.mySignal2.emit('2')
                elif self.max_data - self.avage > 600:
                    self.mySignal2.emit('1')
                self.big_data = []
                print('b' + str(self.max_data))
                self.k = 0
        self.curve.setData(self.data)

class MyWindow(QMainWindow, DoorLock.Ui_Form):
    password = '123456'
    port = serial.Serial()
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.textBrowser.textChanged.connect(self.check_password)
        t1 = threading.Thread(target=self.recv_data)
        t1.daemon= True
        t1.start()

    def getPortData(self, connect):
        print('ok')
        if connect == '1':
            self.pushButton.setStyleSheet("background-color:#A9D0F5")
            self.textBrowser.insertPlainText('1')
            time.sleep(0.1)
            self.pushButton.setStyleSheet("background-color:none")
        elif connect == '2':
            self.pushButton_6.setStyleSheet("background-color:#A9D0F5")
            self.textBrowser.insertPlainText('4')
            time.sleep(0.1)
            self.pushButton_6.setStyleSheet("background-color:none")
        elif connect == '3':
            self.pushButton_5.setStyleSheet("background-color:#A9D0F5")
            self.textBrowser.insertPlainText('7')
            time.sleep(0.1)
            self.pushButton_5.setStyleSheet("background-color:none")
        elif connect == '4':
            self.pushButton_10.setStyleSheet("background-color:#A9D0F5")
            time.sleep(0.1)
            self.pushButton_10.setStyleSheet("background-color:none")

    def recv_data(self):
        while True:
            try:
                data = beginWin.port.readline()
            except:
                continue
            else:
                # print(data, len(data), type(data))
                data = str(data, encoding="utf-8")
                if 'a' in data or 'b' in data:
                    data = data[0]
                else:
                    data = int(data[:2]) - 48
                # print(data, type(data))
                if data == 'b':
                    self.textBrowser.insertPlainText('。')
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
        if '。' in text:
            self.textBrowser.clear()
        elif len(text) == 6:
            self.textBrowser.clear()
            if text == self.password:
                box.setText('<h1><center>密码正确</center></h1>')
                box.exec_()
            else:
                box.setText('<h1><center>密码错误！！</center></h1>')
                box.exec_()

if __name__ == '__main__':
    # m = serial.Serial('COM6', 9600)
    app = QApplication(sys.argv)
    beginWin = beginWindow()
    beginWin.show()
    # myWin = MyWindow()
    # portWin = portWindow()
    # portWin.show()
    sys.exit(app.exec_())
