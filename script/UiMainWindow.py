# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mo.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QStatusBar, QTextBrowser, QToolButton, QWidget)
import QtResource

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(794, 603)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"   QWidget#centralwidget {\n"
"         border-image:url(:/drawable/res/white_pixel.png);\n"
"     }")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(390, 0, 401, 401))
        self.frame.setStyleSheet(u"background-color: rgba(213, 228, 250, 120);\n"
"border-radius: 15px;\n"
"\n"
"border-width: 3px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);\n"
"\n"
"")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(-1, 409, 791, 171))
        self.frame_2.setStyleSheet(u"background-color: rgba(248, 207, 217, 150);\n"
"border-radius: 15px;\n"
"\n"
"border-width: 3px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);\n"
"\n"
"")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(10, 70, 341, 91))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.toolButton_2 = QToolButton(self.frame_3)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setGeometry(QRect(300, 50, 24, 31))
        self.toolButton_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;\n"
"\n"
"border-width: 1px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);")
        self.toolButton = QToolButton(self.frame_3)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(300, 11, 24, 31))
        self.toolButton.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;\n"
"\n"
"border-width: 1px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);")
        self.lineEdit_2 = QLineEdit(self.frame_3)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(100, 50, 191, 31))
        self.lineEdit_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;\n"
"\n"
"border-width: 1px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);")
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit = QLineEdit(self.frame_3)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(100, 10, 191, 31))
        self.lineEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;\n"
"\n"
"border-width: 1px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);")
        self.lineEdit.setReadOnly(True)
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 10, 81, 31))
        font = QFont()
        font.setFamilies([u":/font/res/font/\u5b57\u9b42\u65e0\u5916\u6da6\u9ed1\u4f53.ttf"])
        font.setPointSize(11)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"font-family:url(:/font/res/font/\u5b57\u9b42\u65e0\u5916\u6da6\u9ed1\u4f53.ttf);\n"
"border-radius: 0px;\n"
"\n"
"border-width: 0px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 50, 81, 31))
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"font-family:url(:/font/res/font/\u5b57\u9b42\u65e0\u5916\u6da6\u9ed1\u4f53.ttf);\n"
"border-radius: 0px;\n"
"\n"
"border-width: 0px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setGeometry(QRect(360, 10, 421, 151))
        self.frame_6.setStyleSheet(u"background-color: rgba(255, 255, 255,150);\n"
"border-radius: 15px;\n"
"\n"
"border-width: 3px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_5 = QFrame(self.frame_6)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setGeometry(QRect(10, 90, 401, 51))
        self.frame_5.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 15px;\n"
"\n"
"border-width: 3px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.progressBar = QProgressBar(self.frame_5)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(170, 10, 221, 31))
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"    text-align: center;          /* \u6587\u672c\u5bf9\u9f50 */\n"
"    font-family: \"Segoe UI\";     /* \u5b57\u4f53\u8bbe\u7f6e */\n"
"    font-size: 15px;             /* \u5b57\u53f7 */\n"
"    color: rgb(255, 255, 255);              /* \u6587\u672c\u989c\u8272 */\n"
"\n"
"    /* \u80cc\u666f\u6837\u5f0f */\n"
"    background-color: rgb(147, 147, 147);   /* \u80cc\u666f\u989c\u8272 */\n"
"    border: 2px solid rgb(227, 205, 204);   /* \u8fb9\u6846 */\n"
"    border-radius: 12px;         /* \u5706\u89d2\u534a\u5f84 */\n"
"    padding: 1px;                /* \u5185\u8fb9\u8ddd */\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    /* \u8fdb\u5ea6\u5757\u6837\u5f0f */\n"
"    background-color: #4CAF50;   /* \u4e3b\u8fdb\u5ea6\u989c\u8272 */\n"
"    border-radius: 8px;         /* \u5706\u89d2\u9700\u6bd4\u603b\u5706\u89d2\u5c0f */\n"
"    border: 1px solid #388E3C;   /* \u8fb9\u6846\u589e\u5f3a\u7acb\u4f53\u611f */\n"
"\n"
"    /* \u6e10\u53d8\u6548\u679c */\n"
"    background:qlineargradient(sprea"
                        "d:pad, x1:0, y1:0.489, x2:1, y2:0.482955, stop:0 rgba(0, 192, 211, 255), stop:1 rgba(236, 185, 255, 255));\n"
"}\n"
"")
        self.progressBar.setValue(24)
        self.label = QLabel(self.frame_5)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 151, 31))
        self.label.setFont(font)
        self.label.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 0px;\n"
"\n"
"border-width: 0px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);\n"
"font-family:url(:/font/res/font/\u5b57\u9b42\u65e0\u5916\u6da6\u9ed1\u4f53.ttf);\n"
"")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_8 = QFrame(self.frame_6)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setGeometry(QRect(10, 10, 401, 61))
        self.frame_8.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 15px;\n"
"\n"
"border-width: 3px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);\n"
"\n"
"")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.pushButton_3 = QPushButton(self.frame_8)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(10, 10, 81, 41))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.pushButton_3.setFont(font1)
        self.pushButton_3.setStyleSheet(u"QPushButton {\n"
"   	background-color: rgb(255, 255, 255);\n"
"	border-radius: 15px;\n"
"	border-width: 3px;\n"
"	border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"	border-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(227, 236, 237);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(248, 208, 217);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    opacity: 0.5;\n"
"}")
        self.pushButton_4 = QPushButton(self.frame_8)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(110, 10, 81, 41))
        self.pushButton_4.setFont(font1)
        self.pushButton_4.setStyleSheet(u"QPushButton {\n"
"   	background-color: rgb(255, 255, 255);\n"
"	border-radius: 15px;\n"
"	border-width: 3px;\n"
"	border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"	border-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(227, 236, 237);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(248, 208, 217);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    opacity: 0.5;\n"
"}")
        self.pushButton_5 = QPushButton(self.frame_8)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(210, 10, 81, 41))
        self.pushButton_5.setFont(font1)
        self.pushButton_5.setStyleSheet(u"QPushButton {\n"
"   	background-color: rgb(255, 255, 255);\n"
"	border-radius: 15px;\n"
"	border-width: 3px;\n"
"	border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"	border-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(227, 236, 237);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(248, 208, 217);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    opacity: 0.5;\n"
"}")
        self.pushButton_6 = QPushButton(self.frame_8)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(310, 10, 81, 41))
        self.pushButton_6.setFont(font1)
        self.pushButton_6.setStyleSheet(u"QPushButton {\n"
"   	background-color: rgb(255, 255, 255);\n"
"	border-radius: 15px;\n"
"	border-width: 3px;\n"
"	border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"	border-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(227, 236, 237);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(248, 208, 217);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    opacity: 0.5;\n"
"}")
        self.frame_7 = QFrame(self.frame_2)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setGeometry(QRect(10, 10, 341, 51))
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.lineEdit_3 = QLineEdit(self.frame_7)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(100, 10, 191, 31))
        self.lineEdit_3.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;\n"
"\n"
"border-width: 1px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);")
        self.lineEdit_3.setReadOnly(True)
        self.toolButton_3 = QToolButton(self.frame_7)
        self.toolButton_3.setObjectName(u"toolButton_3")
        self.toolButton_3.setGeometry(QRect(300, 10, 24, 31))
        self.toolButton_3.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;\n"
"\n"
"border-width: 1px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);")
        self.label_2 = QLabel(self.frame_7)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 81, 31))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"font-family:url(:/font/res/font/\u5b57\u9b42\u65e0\u5916\u6da6\u9ed1\u4f53.ttf);\n"
"border-radius: 0px;\n"
"\n"
"border-width: 0px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(-1, -1, 381, 401))
        self.frame_4.setStyleSheet(u"background-color:rgba(255, 255, 255, 0);\n"
"border-radius: 10px;\n"
"\n"
"\n"
"border-image:url(:/drawable/res/text_browser_border.png);\n"
"\n"
"")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.textBrowser = QTextBrowser(self.frame_4)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(50, 30, 271, 341))
        self.textBrowser.setStyleSheet(u"background-color:rgba(255, 255, 255, 0);\n"
"border-radius: 10px;\n"
"\n"
"border-width: 3px;\n"
"border-style: solid;  /* \u53ef\u9009\u503c\uff1asolid/dotted/dashed/double\u7b49 */\n"
"border-color: rgb(0, 0, 0);\n"
"\n"
"border-image: url(:/drawable/res/text_browser.png);\n"
"padding-left: 15px;\n"
"padding-top: 15px;\n"
"padding-right: 25px;\n"
"padding-bottom: 15px;\n"
"font-family:url(:/font/res/font/minecraft_standard.otf);")
        self.pushButton = QPushButton(self.frame_4)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(330, 80, 21, 21))
        self.pushButton.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: rgba(0, 0, 0, 100);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgba(255, 255, 255, 155);\n"
"}")
        self.pushButton_2 = QPushButton(self.frame_4)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(330, 100, 21, 24))
        self.pushButton_2.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: rgba(0, 0, 0, 100);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgba(255, 255, 255, 155);\n"
"}")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u76ee\u5f55", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u76ee\u5f55", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u65e0\u4efb\u52a1", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u53d6", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u6682\u505c", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u6574\u7406", None))
        self.toolButton_3.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6e38\u620f\u8def\u5f84", None))
        self.pushButton.setText("")
        self.pushButton_2.setText("")
    # retranslateUi

