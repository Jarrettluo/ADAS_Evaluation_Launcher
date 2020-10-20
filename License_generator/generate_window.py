# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: generate_window
@time: 2020/5/26 13:59
"""
import os
import sys, time
"""
以下引用是由于使用PyInstaller进行软件打包时出现bug。
参考链接：https://bbs.csdn.net/topics/392428917
"""
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QDate, QDateTime, QDate, QTime, QDateTime, Qt, QStringListModel # 引入多线程工具
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap, QImage, QCursor, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAction, QLabel, QStatusBar, QDialog, QFileDialog
from active_license.get_mac_addr import hash_msg


def app_path():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        return os.path.dirname(sys.executable) # 使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__) # 没打包前的py目录

PROJECT_PATH = app_path()



class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("Generator.ui", self)
        self.resize(405,480)
        self.setMinimumSize(QtCore.QSize(415,490))
        self.setMaximumSize(QtCore.QSize(415,490))
        self.setWindowTitle('智能驾驶数据评估激活码生成器')
        self.setWindowIcon(QIcon('admin.ico'))

        self.toolButton.clicked.connect(self.msg)
        self.file_path = ''
        self.mac_addr = ''
        self.active_date = ''
        self.generate_lic()
        self.license_record = LicenseRecord()
        self.init_UI()

    def init_UI(self):
        # Mac地址掩码
        self.lineEdit.setInputMask('HH:HH:HH:HH:HH:HH;_')
        self.lineEdit.textChanged.connect(self.get_mac)
        self.dateTimeEdit.setCalendarPopup(True)
        self.now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.dateTimeEdit.setDateTime(QDateTime.fromString(self.now_time, 'yyyy-MM-dd hh:mm:ss'))
        self.dateTimeEdit.dateTimeChanged.connect(self.get_date)
        self.lineEdit_2.setText(' ')
        # listView
        items = self.license_record.get_license_history()
        # print(items)
        listModel = QStringListModel()
        listModel.setStringList(items)
        self.listView.setModel(listModel)

    def get_mac(self):
        self.mac_addr = self.lineEdit.text()
        self.generate_lic()

    def get_date(self, dateTime):
        self.active_date = dateTime.toString(Qt.ISODate)
        self.generate_lic()

    def msg(self):
        directory1 = QFileDialog.getExistingDirectory(self, "选取文件夹", "C:/")  # 起始路径
        self.lineEdit_2.setText(directory1)
        self.file_path = directory1
        # print(directory1)
        self.generate_lic()

    def generate_lic(self):
        if self.file_path and self.mac_addr:
            self.pushButton.setEnabled(True)
            self.pushButton.clicked.connect(self.save_lic)
        else:
            self.pushButton.setEnabled(False)

    def save_lic(self):
        psw = hash_msg('faw' + str(self.mac_addr))
        license_str = {}
        license_str['mac'] = self.mac_addr
        # print("******", self.active_date)
        license_str['time_str'] = self.active_date
        license_str['psw'] = psw
        s = str(license_str)
        from AEScoder import PrpCrypt
        pc = PrpCrypt('keyskeyskeyskeys')  # 初始化密钥

        s_encrypt = pc.encrypt(s)   # <class 'bytes'>
        d = pc.decrypt(s_encrypt)  # 解密
        # print(d)
        mac_str = self.mac_addr.replace(':', '')
        time_str = self.now_time.replace(' ', '_')
        time_str = time_str.replace(':', '')
        file_path = self.file_path + '/license_'+ mac_str + '_' + time_str + '.lic'
        s_encrypt = str(s_encrypt, encoding = "utf-8")   #  bytes to str
        with open(file_path, 'w', encoding='utf-8') as lic:
            lic.write(str(s_encrypt))
            lic.close()
        record_msg = self.now_time + "/" + mac_str + "/" + license_str['time_str'] + "/" + file_path
        self.license_record.write_license_record(record_msg)
        self.init_UI()  # 重置

class LicenseRecord():
    def __init__(self):
        self.path = os.getcwd()
        self.file = self.path + '/records.txt'
    def get_license_history(self):
        with open(self.file, 'r') as f:
            license_list = f.readlines()
            f.close()
        return license_list
    def write_license_record(self, lic_record):
        with open(self.file, 'a+') as f:
            f.write(lic_record + '\n')  # 加\n换行显示
            f.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())