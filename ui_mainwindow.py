# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QColumnView, QGraphicsView, QHBoxLayout,
    QHeaderView, QMainWindow, QMenuBar, QRadioButton,
    QSizePolicy, QStatusBar, QTableWidget, QTableWidgetItem,
    QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1800, 1169)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.actionOpen.setIcon(icon)
        self.actionOpen.setMenuRole(QAction.MenuRole.NoRole)
        self.actionSync = QAction(MainWindow)
        self.actionSync.setObjectName(u"actionSync")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SyncSynchronizing))
        self.actionSync.setIcon(icon1)
        self.actionSync.setMenuRole(QAction.MenuRole.NoRole)
        self.actionZoom_Out = QAction(MainWindow)
        self.actionZoom_Out.setObjectName(u"actionZoom_Out")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ZoomOut))
        self.actionZoom_Out.setIcon(icon2)
        self.actionZoom_Out.setMenuRole(QAction.MenuRole.NoRole)
        self.actionDelete = QAction(MainWindow)
        self.actionDelete.setObjectName(u"actionDelete")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.actionDelete.setIcon(icon3)
        self.actionDelete.setMenuRole(QAction.MenuRole.NoRole)
        self.actionS3Open = QAction(MainWindow)
        self.actionS3Open.setObjectName(u"actionS3Open")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.NetworkWired))
        self.actionS3Open.setIcon(icon4)
        self.actionS3Open.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(1, 2, 1817, 1014))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.graphicsView = QGraphicsView(self.layoutWidget)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy1)
        self.graphicsView.setMinimumSize(QSize(1200, 800))
        self.graphicsView.setMaximumSize(QSize(1200, 800))
        self.graphicsView.setMouseTracking(True)

        self.horizontalLayout.addWidget(self.graphicsView)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.detailsView = QGraphicsView(self.layoutWidget)
        self.detailsView.setObjectName(u"detailsView")
        sizePolicy1.setHeightForWidth(self.detailsView.sizePolicy().hasHeightForWidth())
        self.detailsView.setSizePolicy(sizePolicy1)
        self.detailsView.setMinimumSize(QSize(600, 600))
        self.detailsView.setMaximumSize(QSize(600, 600))

        self.verticalLayout.addWidget(self.detailsView, 0, Qt.AlignmentFlag.AlignTop)

        self.tableWidget = QTableWidget(self.layoutWidget)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget, 0, Qt.AlignmentFlag.AlignBottom)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.columnView = QColumnView(self.layoutWidget)
        self.columnView.setObjectName(u"columnView")

        self.verticalLayout_2.addWidget(self.columnView)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton_all = QRadioButton(self.layoutWidget)
        self.radioButton_all.setObjectName(u"radioButton_all")

        self.horizontalLayout_3.addWidget(self.radioButton_all)

        self.radioButton_unratedbyme_2 = QRadioButton(self.layoutWidget)
        self.radioButton_unratedbyme_2.setObjectName(u"radioButton_unratedbyme_2")

        self.horizontalLayout_3.addWidget(self.radioButton_unratedbyme_2)

        self.radioButton_unratedothers = QRadioButton(self.layoutWidget)
        self.radioButton_unratedothers.setObjectName(u"radioButton_unratedothers")

        self.horizontalLayout_3.addWidget(self.radioButton_unratedothers)

        self.radioButton_startrails = QRadioButton(self.layoutWidget)
        self.radioButton_startrails.setObjectName(u"radioButton_startrails")

        self.horizontalLayout_3.addWidget(self.radioButton_startrails)

        self.radioButton_nostartrails = QRadioButton(self.layoutWidget)
        self.radioButton_nostartrails.setObjectName(u"radioButton_nostartrails")

        self.horizontalLayout_3.addWidget(self.radioButton_nostartrails)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1800, 43))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMovable(False)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionS3Open)
        self.toolBar.addAction(self.actionSync)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"pyBlink", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open from local filesystem", None))
        self.actionSync.setText(QCoreApplication.translate("MainWindow", u"Sync with S3 Share", None))
        self.actionZoom_Out.setText(QCoreApplication.translate("MainWindow", u"Zoom Out", None))
        self.actionDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.actionS3Open.setText(QCoreApplication.translate("MainWindow", u"Open from S3 Share", None))
#if QT_CONFIG(tooltip)
        self.actionS3Open.setToolTip(QCoreApplication.translate("MainWindow", u"Open from S3 Share", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_all.setText(QCoreApplication.translate("MainWindow", u"Show All", None))
        self.radioButton_unratedbyme_2.setText(QCoreApplication.translate("MainWindow", u"Not rated by me", None))
        self.radioButton_unratedothers.setText(QCoreApplication.translate("MainWindow", u"Not rated by others", None))
        self.radioButton_startrails.setText(QCoreApplication.translate("MainWindow", u"Startrails visible", None))
        self.radioButton_nostartrails.setText(QCoreApplication.translate("MainWindow", u"No Startrails visible", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

