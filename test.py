import sys
import time
import re
import serial
import serial.tools.list_ports
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import DoorLock
import beginui
import port
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, Qt


class Find_port(QThread):
    port_change = pyqtSignal()

    def __init__(self):
        super(Find_port, self).__init__()
        self.old = list(serial.tools.list_ports.comports())

    def run(self):
        while True:
            port_list = list(serial.tools.list_ports.comports())
            if port_list != self.old:
                self.old = port_list
                self.port_change.emit()
                QThread.msleep(1000)

class recv_data(QThread):
    update_pb = pyqtSignal(int)
    port = serial.Serial()
    is_run = False
    def __init__(self):
        super(recv_data, self).__init__()

    def change_port(self, port, is_run):
        self.port = port
        self.is_run = is_run

    def run(self):
        while self.is_run:
            try:
                dat = self.port.readline()
            except:
                print('--')
                continue
            else:
                try:
                    dat = str(dat, encoding="utf-8")
                except:
                    print('---')
                    continue
                else:
                    pattern = re.compile('[\d]*')
                    dat = pattern.findall(dat)[0]
                    if len(dat) > 0:
                        dat = int(dat)
                        self.update_pb.emit(dat)
                        # print(dat)

class recv_data_2(QThread):
    re_data = pyqtSignal(str)
    port = serial.Serial()
    is_run = False
    def __init__(self):
        super(recv_data_2, self).__init__()

    def change_port(self, port, is_open):
        self.port = port
        self.is_run = is_open

    def run(self):
        while self.is_run:
            try:
                data = self.port.readline()
            except:
                # print('---')
                continue
            else:
                # print(data, len(data), type(data))
                data = str(data, encoding="utf-8")
                self.re_data.emit(data)
                # print(data)
        pass

class beginWindow(QMainWindow, beginui.Ui_Form):
    mySignal1 = pyqtSignal(str)
    mySignal2 = pyqtSignal(str)
    is_port_open = False
    def __init__(self, parent=None):
        super(beginWindow, self).__init__(parent)
        self.setupUi(self)
        self.port_find()
        self.thread3 = Find_port()
        self.thread3.port_change.connect(self.port_find)
        self.thread3.start()
        self.My_win = MyWindow()
        self.Port_win = portWindow()
        self.mySignal1.connect(self.My_win.get_port)
        self.mySignal2.connect(self.Port_win.getBeginSignal)
        self.Port_win.mySignal3.connect(self.My_win.getPortData)
        self.Port_win.mySignal3.connect(self.My_win.change_color)
        self.pushButton.clicked.connect(self.port_conn)
        self.pushButton_2.clicked.connect(self.port_plot)

    def port_find(self):
        self.comboBox.clear()
        self.comboBox_2.clear()
        list1 = []
        port_list = list(serial.tools.list_ports.comports())
        for item in port_list:
            pattern = re.compile('COM[\d]*')
            item = pattern.findall(str(item))[0]
            list1.append(item)
        list1.sort()
        self.comboBox.addItems(list1)
        self.comboBox_2.addItems(list1)

    def port_conn(self):
        self.mySignal1.emit(self.comboBox.currentText())
        if len(self.lineEdit.text()) != 0:
            self.My_win.password = self.lineEdit.text()
        if not self.is_port_open:
            self.is_port_open = True
            self.mySignal2.emit(self.comboBox_2.currentText())
            self.Port_win.checkBox.setChecked(True)
        self.My_win.show()

    def port_plot(self):
        if not self.is_port_open:
            self.is_port_open = True
            self.mySignal2.emit(self.comboBox_2.currentText())
            self.Port_win.checkBox.setChecked(True)
        self.Port_win.show()
        pass

class portWindow(QMainWindow, port.Ui_Dialog):
    mySignal3 = pyqtSignal(str)
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
    # 设置绘制标记
    is_painting = False
    # 设置结束记录K触发后的数据标志
    is_collect = False
    def __init__(self, parent=None):
        super(portWindow, self).__init__(parent)
        self.setupUi(self)
        self.checkBox.stateChanged.connect(self.connect)
        self.checkBox_2.stateChanged.connect(self.paint)
        self.thread = recv_data()
        self.thread.update_pb.connect(self.plot)

    def paint(self):
        if self.is_painting:
            self.is_painting = False
        else:
            self.is_painting = True

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
                    box.setWindowTitle('message')
                    box.setStandardButtons(QMessageBox.Ok)  # QMessageBox显示的按钮
                    box.button(QMessageBox.Ok).animateClick(1000)  # t时间后自动关闭(t单位为毫秒)
                    box.exec_()
                else:
                    box.setText('<h1><center>连接成功！</center></h1>')
                    box.setWindowTitle('message')
                    box.setStandardButtons(QMessageBox.Ok)  # QMessageBox显示的按钮
                    box.button(QMessageBox.Ok).animateClick(1000)  # t时间后自动关闭(t单位为毫秒)
                    box.exec_()
                    self.thread.change_port(self.COM, True)
                    self.thread.start()
            else:
                self.thread.reading = True
                box.setText('<h1><center>已连接</center></h1>')
                box.setWindowTitle('message')
                box.setStandardButtons(QMessageBox.Ok)  # QMessageBox显示的按钮
                box.button(QMessageBox.Ok).animateClick(1000)  # t时间后自动关闭(t单位为毫秒)
                box.exec_()
        else:
            self.thread.reading = False
            box.setText('<h1><center>连接已断开。</center></h1>')
            box.setWindowTitle('message')
            box.setStandardButtons(QMessageBox.Ok)  # QMessageBox显示的按钮
            box.button(QMessageBox.Ok).animateClick(1000)  # t时间后自动关闭(t单位为毫秒)
            box.exec_()
        # print('connect结束')

    def getBeginSignal(self, connect):
        print(connect)
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
            if connect - self.avage > 400:
                self.big_data.append(connect)
                self.k += 1
                self.is_collect = True
            else:
                if self.is_collect:
                    self.is_collect = False
                    self.max_data = max(self.big_data)
                    if self.max_data > 3290:
                        print('8')
                        self.mySignal3.emit('8')
                    elif self.max_data > 2800:
                        print('0')
                        self.mySignal3.emit('0')
                    elif self.max_data > 2200:
                        print('5')
                        self.mySignal3.emit('5')
                    # else:
                        # print('2')
                        # self.mySignal3.emit('2')
                    self.big_data = []
                    print('b' + str(self.max_data))
                    self.k = 0
                else:
                    pass
        if self.is_painting:
            self.curve.setData(self.data)

class MyWindow(QMainWindow, DoorLock.Ui_Form):
    password = '145789'
    port = serial.Serial()
    mySignal4 = pyqtSignal(str)
    mySignal5 = pyqtSignal(str)
    is_full = False
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.textBrowser.textChanged.connect(self.check_password)
        self.thread1 = recv_data_2()
        self.thread1.re_data.connect(self.recv_data)
        self.thread1.re_data.connect(self.change_color)
        self.mySignal4.connect(self.change_color)
        self.mySignal5.connect(self.send_data)

    def send_data(self, connect):
        if connect == '1':
            print('c')
            self.port.write('c'.encode())
        elif connect == '2':
            print('d')
            self.port.write('d'.encode())

    def change_color(self, connect):
        if connect == '1':
            self.pushButton.setStyleSheet("background: rgba(63, 114, 191, 0.17)")
            QApplication.processEvents()
            time.sleep(0.3)
            self.pushButton.setStyleSheet("background: none")
        elif connect == '2':
            self.pushButton_2.setStyleSheet("background: rgba(63, 114, 191, 0.17)")
            QApplication.processEvents()
            time.sleep(0.3)
            self.pushButton_2.setStyleSheet("background: none")
        elif connect == '3':
            self.pushButton_7.setStyleSheet("background: rgba(63, 114, 191, 0.17)")
            QApplication.processEvents()
            time.sleep(0.3)
            self.pushButton_7.setStyleSheet("background: none")
        elif connect == '4':
            self.pushButton_6.setStyleSheet("background: rgba(63, 114, 191, 0.17)")
            QApplication.processEvents()
            time.sleep(0.3)
            self.pushButton_6.setStyleSheet("background: none")
        if connect == '5':
            self.pushButton_3.setStyleSheet("background: rgba(63, 114, 191, 0.17)")
            QApplication.processEvents()
            time.sleep(0.3)
            self.pushButton_3.setStyleSheet("background: none")
        if connect == '6':
            self.pushButton_8.setStyleSheet("background: rgba(63, 114, 191, 0.17)")
            QApplication.processEvents()
            time.sleep(0.3)
            self.pushButton_8.setStyleSheet("background: none")
        if connect == '7':
            self.pushButton_5.setStyleSheet("background: rgba(63, 114, 191, 0.17)")
            QApplication.processEvents()
            time.sleep(0.3)
            self.pushButton_5.setStyleSheet("background: none")
        if connect == '8':
            self.pushButton_4.setStyleSheet("background: rgba(63, 114, 191, 0.17)")
            QApplication.processEvents()
            time.sleep(0.3)
            self.pushButton_4.setStyleSheet("background: none")
        if connect == '9':
            self.pushButton_9.setStyleSheet("background: rgba(63, 114, 191, 0.17)")
            QApplication.processEvents()
            time.sleep(0.3)
            self.pushButton_9.setStyleSheet("background: none")
        if connect == '0':
            self.pushButton_11.setStyleSheet("background: rgba(63, 114, 191, 0.17)")
            QApplication.processEvents()
            time.sleep(0.3)
            self.pushButton_11.setStyleSheet("background: none")
        if connect == 'b':
            self.pushButton_12.setStyleSheet("background: rgba(63, 114, 191, 0.17)")
            QApplication.processEvents()
            time.sleep(0.3)
            self.pushButton_12.setStyleSheet("background: none")
        if connect == 'a':
            self.pushButton_10.setStyleSheet("background: rgba(63, 114, 191, 0.17)")
            QApplication.processEvents()
            time.sleep(0.3)
            self.pushButton_10.setStyleSheet("background: none")

    def getPortData(self, connect):
        if not self.is_full:
            # print('ok')
            if connect == '2':
                self.textBrowser.insertPlainText('2')
            elif connect == '5':
                self.textBrowser.insertPlainText('5')
            elif connect == '8':
                self.textBrowser.insertPlainText('8')
            elif connect == '0':
                self.textBrowser.insertPlainText('0')

    def recv_data(self, data):
        if not self.is_full:
            if 'a' in data or 'b' in data:
                data = data[0]
            else:
                data = str(int(data[:2]))
            # print(data, type(data))
            self.mySignal4.emit(data)
            if data == 'b':
                self.textBrowser.insertPlainText('。')
            elif data == 'a':
                self.mySignal5.emit('2')
                pass
            elif data == '0':
                self.textBrowser.insertPlainText('0')
            elif data == '1':
                self.textBrowser.insertPlainText('1')
            elif data == '2':
                self.textBrowser.insertPlainText('2')
            elif data == '3':
                self.textBrowser.insertPlainText('3')
            elif data == '4':
                self.textBrowser.insertPlainText('4')
            elif data == '5':
                self.textBrowser.insertPlainText('5')
            elif data == '6':
                self.textBrowser.insertPlainText('6')
            elif data == '7':
                self.textBrowser.insertPlainText('7')
            elif data == '8':
                self.textBrowser.insertPlainText('8')
            elif data == '9':
                self.textBrowser.insertPlainText('9')

    def check_password(self):
        text = self.textBrowser.toPlainText()
        if '。' in text:
            self.is_full = False
            self.textBrowser.clear()
        elif len(text) == 6:
            self.is_full = True
            if text == self.password:
                self.mySignal5.emit('1')
                box = QMessageBox()
                box.setWindowTitle('massage')
                box.setText('<h1><center>The password is true !</center></h1>')
                box.setStandardButtons(QMessageBox.Ok)  # QMessageBox显示的按钮
                box.button(QMessageBox.Ok).animateClick(1000)  # t时间后自动关闭(t单位为毫秒)
                box.exec_()
            else:
                box = QMessageBox()
                box.setWindowTitle('massage')
                box.setText('<h1><center>The password is false !</center></h1>')
                box.setStandardButtons(QMessageBox.Ok)  # QMessageBox显示的按钮
                box.button(QMessageBox.Ok).animateClick(1000)  # t时间后自动关闭(t单位为毫秒)
                box.exec_()
            self.textBrowser.clear()
            self.is_full = False
        else:
            # box.exec_()
            pass

    def get_port(self, connect):
        box = QMessageBox()
        try:
            self.port = serial.Serial(connect, 9600)
            self.thread1.change_port(self.port, True)
            self.thread1.start()
        except:
            box.setText('<h1><center>连接失败！！！</center></h1>')
        else:
            box.setText('<h1><center>连接成功！！！</center></h1>')
        box.setWindowTitle('message')
        box.setStandardButtons(QMessageBox.Ok)  # QMessageBox显示的按钮
        box.button(QMessageBox.Ok).animateClick(1000)  # t时间后自动关闭(t单位为毫秒)
        box.exec_()

if __name__ == '__main__':
    # 实现不同分辨率下的电脑上的相同显示
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    beginWin = beginWindow()
    beginWin.show()
    sys.exit(app.exec_())
