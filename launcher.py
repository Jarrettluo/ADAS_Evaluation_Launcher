# encoding: utf-8
"""
@version: 1.0
@author: 
@file: launcher
@time: 2020/4/22 14:49
"""

import time, sys, os
"""
以下引用是由于使用PyInstaller进行软件打包时出现bug。
参考链接：https://bbs.csdn.net/topics/392428917
"""
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5 import QtCore, Qt
from PyQt5.QtCore import QThread, pyqtSignal # 引入多线程工具
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap, QImage, QCursor, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAction, QLabel, QStatusBar, QDialog, QFileDialog


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
        loadUi("launcher_sources/launcher.ui", self)
        self.child = ChildWindow()
        self.authorize = AuthorizeWindow()
        self.init_ui()
        self.service()
        self.function_software()
        self.copy_right()

    def init_ui(self):
        self.resize(700,420)
        self.setMinimumSize(QtCore.QSize(700, 420))
        self.setMaximumSize(QtCore.QSize(700, 420))
        self.setWindowTitle('智能驾驶数据评估   北京####科技有限公司')
        self.setWindowIcon(QIcon('launcher_sources/launch.png'))
        self.setFixedSize(700, 420)

        icon = QIcon('launcher_sources/service_icon.png')
        self._iconSize = QtCore.QSize(38,38)

        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(self._iconSize)
        self.pushButton.setText('') # 按钮显示文本为空

        #self.label_11.adjustSize()
        #self.label_12.setWordWrap(True)
        #self.label_12.setAlignment(QtCore.Qt.AlignTop)

        self.pushButton_2.setIcon(QIcon('launcher_sources/restart_icon.png'))
        self.pushButton_2.setText('')  # 按钮显示文本为空
        self.pushButton_2.setIconSize(self._iconSize)

        self.pushButton_4.setIcon(QIcon(QPixmap('launcher_sources/close_icon.png')))
        self.pushButton_4.setText('')  # 按钮显示文本为空
        self.pushButton_4.setIconSize(self._iconSize)

        self.pushButton_3.setIcon(QIcon(QPixmap('launcher_sources/setting_icon.png')))
        self.pushButton_3.setText('')  # 按钮显示文本为空
        self.pushButton_3.setIconSize(self._iconSize)

        self.pushButton_7.setIcon(QIcon(QPixmap('launcher_sources/report_icon.png')))
        self.pushButton_7.setText('')  # 按钮显示文本为空
        self.pushButton_7.setIconSize(self._iconSize)

        self.pushButton_6.setIcon(QIcon(QPixmap('launcher_sources/direction_icon.png')))
        self.pushButton_6.setText('')  # 按钮显示文本为空
        self.pushButton_6.setIconSize(self._iconSize)

        self.pushButton_5.setIcon(QIcon(QPixmap('launcher_sources/uninstall_icon.png')))
        self.pushButton_5.setText('')  # 按钮显示文本为空
        self.pushButton_5.setIconSize(self._iconSize)


        self.pushButton_8.setIcon(QIcon(QPixmap('launcher_sources/more_icon.png')))
        self.pushButton_8.setText('')  # 按钮显示文本为空
        self.pushButton_8.setIconSize(self._iconSize)

        self.pushButton_10.setIcon(QIcon(QPixmap('launcher_sources/copyright_icon.png')))
        self.pushButton_10.setText('')  # 按钮显示文本为空
        self.pushButton_10.setIconSize(self._iconSize)

        self.pushButton_9.setIcon(QIcon(QPixmap('launcher_sources/authorization_icon.png')))
        self.pushButton_9.setText('')  # 按钮显示文本为空
        self.pushButton_9.setIconSize(self._iconSize)

        self.pushButton_11.setIcon(QIcon(QPixmap('launcher_sources/more_icon.png')))
        self.pushButton_11.setText('')  # 按钮显示文本为空
        self.pushButton_11.setIconSize(self._iconSize)


        check_result = self.authorize.check_license_state()
        if check_result == False:
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.statusbar.showMessage("软件未激活，请激活", 2000)
        else:
            self.statusbar.showMessage("软件已授权", 2000)
            self.pushButton_11.setEnabled(True)
            self.pushButton_8.setEnabled(True)
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)

    def service(self):
        self.pushButton.clicked.connect(self.open_service)
        self.pushButton_2.clicked.connect(self.restart_service)
        self.pushButton_4.clicked.connect(self.kill_service)

    def function_software(self):
        self.pushButton_3.clicked.connect(self.open_setting)
        self.pushButton_7.clicked.connect(self.read_reports)
        self.pushButton_6.clicked.connect(self.read_direction)
        self.pushButton_5.clicked.connect(self.uninstall)
        self.pushButton_8.clicked.connect(self.more_service)

    def copy_right(self):
        self.pushButton_10.clicked.connect(self.child.OPEN)
        self.pushButton_9.clicked.connect(self.authorize.OPEN)
        self.pushButton_11.clicked.connect(self.more_service)

    def open_service(self):
        self.pushButton.setEnabled(False)
        self.statusbar.showMessage("服务启动成功", 2000)
        self.thread = Example()
        self.thread.signal.connect(self.callMain)
        self.thread.start()  # 启动线程

    def callMain(self):
        try:
            os.startfile('Flask_server.exe')
        except Exception as e:
            self.statusbar.showMessage(str(e), 1000)


    def restart_service(self):
        self.thread = Example()
        self.thread.signal.connect(self.callrestart)
        self.thread.start()  # 启动线程

    def callrestart(self):
        try:
            self.kill_service()
        except Exception as e:
            self.statusbar.showMessage(str(e), 1000)
        self.callMain()


    def kill_service(self):
        try:
            os.system('taskkill /f /t /im Flask_server.exe')
        except Exception as e:
            self.statusbar.showMessage(str(e), 1000)
        else:
            self.pushButton.setEnabled(True)
            self.statusbar.showMessage("服务已关闭", 2000)

    def open_setting(self):
        try:
            os.startfile('setup.exe')
        except Exception as e:
            self.statusbar.showMessage(str(e), 1000)



    def read_reports(self):
        # 教程 https://www.cnblogs.com/keithtt/p/7709445.html
        self.statusbar.showMessage("打开报告", 1000)
        self.thread = Example()
        self.thread.signal.connect(self.open_reports)
        self.thread.start()  # 启动线程

    def open_reports(self):
        try:
            print(PROJECT_PATH)
            os.startfile(PROJECT_PATH + '\\ADAS_Chart')
        except Exception as e:
            self.statusbar.showMessage(str(e), 1000)


    def read_direction(self):
        try:
            os.startfile(PROJECT_PATH + '\\docs\\ADAS_Evaluation_Docs.docx')
        except Exception as e:
            self.statusbar.showMessage(str(e), 1000)
        pass



    def uninstall(self):
        os.system("uninst.exe")  # 打开卸载程序
        result = os.system('taskkill /f /t /im ADAS_Evaluation_Launcher.exe')     # 关闭启动器
        pass


    def more_service(self):
        self.statusbar.showMessage("显示更多信息，待开发", 1000)
        pass


class ChildWindow(QDialog):
    def __init__(self):
        super(ChildWindow,self).__init__() # 继承父类
        loadUi("launcher_sources/child_window.ui", self)
        self.pushButton_13.clicked.connect(self.close)
        self.init_UI()
        self.resize(420,320)
        self.setMinimumSize(QtCore.QSize(420, 320))
        self.setMaximumSize(QtCore.QSize(420, 320))
        #self.setGeometry(480,380,420,320)

    def init_UI(self):
        styleFile = 'launcher_sources/dialog_style.qss'
        qssStyle = CommonHelper.readQss(styleFile)
        self.setStyleSheet(qssStyle)
        self.setWindowFlags(Qt.Qt.CustomizeWindowHint)  # 去掉标题栏的代码

        # 创建四个标签
        label_2 = QLabel(self)
        label_3 = QLabel(self)
        label_4 = QLabel(self)

        self.label.setText('版权信息')
        self.label.move(60,40)
        self.label.resize(100,28)
        label_2.setText("· 本软件由<a href = 'http://www.hirain.com/'>北京经纬恒润科技有限公司</a>开发。")
        label_2.move(60,100)
        label_2.setOpenExternalLinks(True)
        label_3.setText("· 软件图标来自<a href = 'https://www.iconfont.cn/'>阿里图标</a>。")
        label_3.move(60,130)
        label_3.setOpenExternalLinks(True)
        label_4.setText('· 版本v1.0.0，发布时间2020年5月7日。')
        label_4.move(60,160)
        self.pushButton_13.setText('确  定')
        self.pushButton_13.setGeometry(260,240,80,28)

    def OPEN(self):
        self.show()


class AuthorizeWindow(QDialog):
    def __init__(self):
        super(AuthorizeWindow, self).__init__() # 继承父类
        loadUi("launcher_sources/authorization.ui", self)
        mySignal = pyqtSignal()
        self.resize(569, 342)
        self.setMinimumSize(QtCore.QSize(569, 342))
        self.setMaximumSize(QtCore.QSize(569, 342))

        self.active_time = ''   # 定义时间
        self.psw = ''   # 定义密码

        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.get_license)
        self.Read_license()

        self.init_UI()
        self.pushButton_3.clicked.connect(self.init_UI_2)


    def init_UI(self):
        styleFile = 'launcher_sources/dialog_style.qss'
        qssStyle = CommonHelper.readQss(styleFile)
        self.setStyleSheet(qssStyle)
        self.setWindowFlags(Qt.Qt.CustomizeWindowHint)  # 去掉标题栏的代码
        self.pushButton.setText('关  闭')

        from active_license.get_mac_addr import get_mac_address
        a = get_mac_address()
        self.label_4.setText(a)

        self.label.adjustSize()
        self.label_2.adjustSize()
        self.label_3.adjustSize()
        self.label_4.adjustSize()
        self.label_6.adjustSize()
        self.init_UI_2()

    def init_UI_2(self):
        check_state = self.check_license_state()
        if check_state == False:
            # print("*********" + str(check_state))
            self.lineEdit.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
        else:
            # print("---", check_state)
            self.lineEdit.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            # self.statusBar().showMessage('请重启后，激活软件')
            # MainWindow.init_ui()


    def check_license_state(self):
        from active_license.check_license import CheckLicense
        # check the license
        if self.active_time and self.psw:
            check_time_result = CheckLicense().check_date(self.active_time)
            check_psw_result = CheckLicense().check_psw(self.psw)
            date_time = str(self.active_time).replace('T', ' ')
            if check_psw_result:
                if check_time_result:
                    self.label_5.setText(f'已激活，授权时间截止{date_time}')
                    self.label_5.adjustSize()
                    return True
                else:
                    self.label_5.setText(f'激活码已过期，授权时间截止{date_time}')
            else:
                self.label_5.setText(f'未激活，请更换license')
        else:
            self.label_5.setText(f'未激活，请激活软件后使用')
        self.label_5.adjustSize()
        return False

    def get_license(self):
        license_file_path, _ = QFileDialog.getOpenFileName(self, "选取文件", "C:/", "All Files (*.lic);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        filename = license_file_path.split('/')[-1]
        # print(filename)
        if filename:
            with open(license_file_path, 'r') as license_file:
                x = license_file.readline()
                # print(x)

            files = self.get_license_files()
            # print(files)
            if files:
                for file in files:
                    os.remove(os.getcwd() + '/LICENSE/' + file)

            license_file_path_new = os.getcwd() + '/LICENSE/'+filename
            with open(license_file_path_new, 'w') as f:
                f.write(x)
                f.close()
            self.Read_license()
        pass

    def get_license_files(self):
        path = os.getcwd() + '/LICENSE'
        files = os.listdir(path)
        return files

    def Read_license(self):
        path = os.getcwd() + '/LICENSE'
        files = self.get_license_files()
        if files:
            filename = files[0]
            self.lineEdit.setText(filename)

            with open(path + '/' + filename, 'r', encoding='utf-8') as f:
                lic_msg = f.read()
                f.close()
            from AEScoder import PrpCrypt
            # str to bytes
            lic_msg = bytes(lic_msg, encoding="utf8")
            pc = PrpCrypt('keyskeyskeyskeys')  # 初始化密钥
            license_str = pc.decrypt(lic_msg)  # 解密
            # print(license_str)

            license_dic = eval(license_str)
            mac = license_dic['mac']
            self.active_time = license_dic['time_str']
            self.psw = license_dic['psw']
            self.textBrowser.setPlaceholderText(self.psw)

        else:
            self.lineEdit.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.lineEdit.setPlaceholderText('license.lic')
            self.textBrowser.setPlaceholderText('license.lic')

    def OPEN(self):
        self.show()

import psutil


def judgeprocess(processname):
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == processname:
            print(pid)
            return 0
            break
    else:
        print("not found")
        return 1


class Example(QThread):
    signal = pyqtSignal()    # 括号里填写信号传递的参数, 这里是无参数传递，其他参数传递方法参考：https://www.cnblogs.com/XJT2018/p/10222981.html
    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        self.signal.emit()    # 发射信号


#编写一个公共类CommomHelper,用于帮助解读qss文件
class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r',encoding = 'utf-8') as f:
            return f.read()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    styleFile = 'launcher_sources/style.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    window.setStyleSheet(qssStyle)

    window.show()
    sys.exit(app.exec_())