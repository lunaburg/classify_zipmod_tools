import sys
import os
# 导入PySide6模块
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QToolButton,
    QLineEdit,
    QVBoxLayout,
    QFileDialog,
    QMainWindow
)

# 导入从.ui文件生成的界面类（假设生成的文件叫 ui_mainwindow.py）
from UiMainWindow import Ui_MainWindow
from ConfigDataList import ConfigDataList
from PySide6.QtCore import QRunnable, QThreadPool, QObject, Signal, Slot
import time

from BaseTask import BaseTask
import random

# 导入从.qrc文件生成的资源模块（假设生成的文件叫 resources_rc.py）
# 这个导入虽然不直接使用，但会注册资源到Qt系统中




# 创建主窗口类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 初始化UI界面
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.set_progress_bar(0)

        #toolButton 事件绑定
        # 连接按钮的点击事件到open_file_dialog函数
        self.ui.toolButton.clicked.connect(self.open_input_dir_dialog)
        self.ui.toolButton_2.clicked.connect(self.open_output_dir_dialog)
        self.ui.toolButton_3.clicked.connect(self.open_game_dir_dialog)

        self.ui.pushButton_3.clicked.connect(self.extract_button_action)
        self.ui.pushButton.clicked.connect(self.clear_text_browse_button_action)
        self.ui.pushButton_2.clicked.connect(self.button_acction)

        self.ConfigDataList = ConfigDataList()#配置信息及其他
        self.ui.textBrowser.setText('欢迎使用本工具')

         # 线程池初始化
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(4)  # 最大并发线程数

         # 任务计数器
        self.task_counter = 0
        
        # 可以在这里添加其他初始化代码
        # 例如：self.ui.pushButton.clicked.connect(...)

    def open_input_dir_dialog(self):
        # 打开文件对话框
        file_dialog = QFileDialog(self)
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",  # 对话框标题
            "",           # 初始目录（空表示默认目录）
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks  # 选项
        )
        if folder_path:
            self.ui.lineEdit.setText(folder_path)
            self.create_task("search_cards")
    
            
    def open_output_dir_dialog(self):
        # 打开文件对话框
        file_dialog = QFileDialog(self)
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",  # 对话框标题
            "",           # 初始目录（空表示默认目录）
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks  # 选项
        )
        if folder_path:
            self.ui.lineEdit_2.setText(folder_path)
            self.ConfigDataList.set_output_dir(folder_path)

    def open_game_dir_dialog(self):
        # 打开文件对话框
        file_dialog = QFileDialog(self)
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",  # 对话框标题
            "",           # 初始目录（空表示默认目录）
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks  # 选项
        )
        if folder_path:
            self.ui.lineEdit_3.setText(folder_path)
            self.ConfigDataList.set_game_dir(folder_path)
    #button_acction
    def extract_button_action(self):
        self.create_task("extract_mods")

    def create_task(self,str):
        self.task_counter += 1        
        # 创建任务实例
        task = BaseTask(self.task_counter,str,self)
        task.signals.progress.connect(self.update_progress)
        task.signals.result.connect(self.handle_result)
        task.signals.error.connect(self.handle_error)
        task.signals.progress_title.connect(self.handle_progress_title)
        task.signals.progress_msg.connect(self.handle_progress_msg)
        # 提交到线程池
        self.thread_pool.start(task)
        self.textBrowser_append(f"已提交任务:[{str}]")

    @Slot(float)
    def update_progress(self, progress):#进度条
        self.set_progress_bar(progress)

    @Slot(str)
    def handle_progress_title(self,title):
        self.set_task_title(title)

    @Slot(object)
    def handle_result(self, result):
        self.textBrowser_append(f"[结果] {result}")

    @Slot(Exception)
    def handle_error(self, error):
        self.textBrowser_append(f"[错误] {str(error)}")
    
    @Slot(str)
    def handle_progress_msg(self,msg):
        self.textBrowser_append(f"[进度] {msg}")


    def button_acction(self):
        self.set_progress_bar(40.5)
    def clear_text_browse_button_action(self):
        self.ui.textBrowser.clear()
    def textBrowser_append(self,text):
        self.ui.textBrowser.append(text)

    def set_progress_bar(self,value):
        self.ui.progressBar.setValue(value)

    def set_task_title(self,title):
        self.ui.label.setText(title)

if __name__ == "__main__":
    # 创建应用实例
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())