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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QGraphicsView,
    QHBoxLayout, QHeaderView, QMainWindow, QMenuBar,
    QRadioButton, QSizePolicy, QStatusBar, QTableWidget,
    QTableWidgetItem, QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1206, 946)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
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
        self.actionDelete = QAction(MainWindow)
        self.actionDelete.setObjectName(u"actionDelete")
        self.actionDelete.setEnabled(True)
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.actionDelete.setIcon(icon2)
        self.actionDelete.setMenuRole(QAction.MenuRole.NoRole)
        self.actionRemoteOpen = QAction(MainWindow)
        self.actionRemoteOpen.setObjectName(u"actionRemoteOpen")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.NetworkWired))
        self.actionRemoteOpen.setIcon(icon3)
        self.actionRemoteOpen.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setAutoFillBackground(False)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalImagesLayout = QHBoxLayout()
        self.horizontalImagesLayout.setObjectName(u"horizontalImagesLayout")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMouseTracking(True)

        self.horizontalImagesLayout.addWidget(self.graphicsView)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.detailsView = QGraphicsView(self.centralwidget)
        self.detailsView.setObjectName(u"detailsView")
        self.detailsView.setMinimumSize(QSize(600, 600))
        self.detailsView.setMaximumSize(QSize(600, 600))

        self.verticalLayout.addWidget(self.detailsView, 0, Qt.AlignmentFlag.AlignTop)


        self.horizontalImagesLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalImagesLayout)

        self.horizontaTableslLayout = QHBoxLayout()
        self.horizontaTableslLayout.setObjectName(u"horizontaTableslLayout")
        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 12):
            self.tableWidget.setColumnCount(12)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, __qtablewidgetitem11)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(12)
        self.tableWidget.verticalHeader().setVisible(False)

        self.horizontaTableslLayout.addWidget(self.tableWidget)

        self.overviewTableWidget = QTableWidget(self.centralwidget)
        if (self.overviewTableWidget.columnCount() < 2):
            self.overviewTableWidget.setColumnCount(2)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.overviewTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.overviewTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem13)
        self.overviewTableWidget.setObjectName(u"overviewTableWidget")
        self.overviewTableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.horizontaTableslLayout.addWidget(self.overviewTableWidget)


        self.verticalLayout_2.addLayout(self.horizontaTableslLayout)

        self.horizontalRadioButtonsLayout = QHBoxLayout()
        self.horizontalRadioButtonsLayout.setObjectName(u"horizontalRadioButtonsLayout")
        self.radioButton_all = QRadioButton(self.centralwidget)
        self.radioButton_all.setObjectName(u"radioButton_all")

        self.horizontalRadioButtonsLayout.addWidget(self.radioButton_all)

        self.radioButton_notdiscardedandnew = QRadioButton(self.centralwidget)
        self.radioButton_notdiscardedandnew.setObjectName(u"radioButton_notdiscardedandnew")

        self.horizontalRadioButtonsLayout.addWidget(self.radioButton_notdiscardedandnew)

        self.radioButton_new = QRadioButton(self.centralwidget)
        self.radioButton_new.setObjectName(u"radioButton_new")

        self.horizontalRadioButtonsLayout.addWidget(self.radioButton_new)

        self.radioButton_discarded = QRadioButton(self.centralwidget)
        self.radioButton_discarded.setObjectName(u"radioButton_discarded")

        self.horizontalRadioButtonsLayout.addWidget(self.radioButton_discarded)

        self.radioButton_discardedbyothers = QRadioButton(self.centralwidget)
        self.radioButton_discardedbyothers.setObjectName(u"radioButton_discardedbyothers")

        self.horizontalRadioButtonsLayout.addWidget(self.radioButton_discardedbyothers)

        self.radioButton_startrails = QRadioButton(self.centralwidget)
        self.radioButton_startrails.setObjectName(u"radioButton_startrails")

        self.horizontalRadioButtonsLayout.addWidget(self.radioButton_startrails)

        self.radioButton_nostartrails = QRadioButton(self.centralwidget)
        self.radioButton_nostartrails.setObjectName(u"radioButton_nostartrails")

        self.horizontalRadioButtonsLayout.addWidget(self.radioButton_nostartrails)


        self.verticalLayout_2.addLayout(self.horizontalRadioButtonsLayout)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1206, 39))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMovable(False)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionSync)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionRemoteOpen)
        self.toolBar.addAction(self.actionDelete)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"pyBlink", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open from local filesystem", None))
        self.actionSync.setText(QCoreApplication.translate("MainWindow", u"Sync with remote Cache", None))
        self.actionDelete.setText(QCoreApplication.translate("MainWindow", u"Delete discarded Subs", None))
        self.actionRemoteOpen.setText(QCoreApplication.translate("MainWindow", u"Open from remote Cache", None))
#if QT_CONFIG(tooltip)
        self.actionRemoteOpen.setToolTip(QCoreApplication.translate("MainWindow", u"Open from remote Cache", None))
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Date", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Duration", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Target", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Filter", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"RotatorAngle", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"PierSide", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Mean", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"FWHM", None));
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Stars", None));
        ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem10 = self.tableWidget.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Status Others", None));
        ___qtablewidgetitem11 = self.tableWidget.horizontalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Startrails", None));
        ___qtablewidgetitem12 = self.overviewTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Key", None));
        ___qtablewidgetitem13 = self.overviewTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Value", None));
        self.radioButton_all.setText(QCoreApplication.translate("MainWindow", u"Show All Subs", None))
        self.radioButton_notdiscardedandnew.setText(QCoreApplication.translate("MainWindow", u"Show not Discarded and New Subs", None))
        self.radioButton_new.setText(QCoreApplication.translate("MainWindow", u"Show New Subs", None))
        self.radioButton_discarded.setText(QCoreApplication.translate("MainWindow", u"Show Discarded Subs", None))
        self.radioButton_discardedbyothers.setText(QCoreApplication.translate("MainWindow", u"Show Discarded by Others Subs", None))
        self.radioButton_startrails.setText(QCoreApplication.translate("MainWindow", u"Subs with Startrails", None))
        self.radioButton_nostartrails.setText(QCoreApplication.translate("MainWindow", u"Subs without Startrails", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

