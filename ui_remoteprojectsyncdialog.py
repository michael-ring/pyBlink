# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'remoteProjectSyncDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QHeaderView, QLabel, QProgressBar,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_remoteProjectSyncDialog(object):
    def setupUi(self, remoteProjectSyncDialog):
        if not remoteProjectSyncDialog.objectName():
            remoteProjectSyncDialog.setObjectName(u"remoteProjectSyncDialog")
        remoteProjectSyncDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        remoteProjectSyncDialog.resize(800, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(remoteProjectSyncDialog.sizePolicy().hasHeightForWidth())
        remoteProjectSyncDialog.setSizePolicy(sizePolicy)
        remoteProjectSyncDialog.setMinimumSize(QSize(800, 500))
        remoteProjectSyncDialog.setMaximumSize(QSize(800, 500))
        remoteProjectSyncDialog.setModal(False)
        self.buttonBox = QDialogButtonBox(remoteProjectSyncDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 450, 730, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setCenterButtons(False)
        self.progressBar_overall = QProgressBar(remoteProjectSyncDialog)
        self.progressBar_overall.setObjectName(u"progressBar_overall")
        self.progressBar_overall.setGeometry(QRect(10, 25, 750, 23))
        self.progressBar_overall.setValue(24)
        self.label_overall = QLabel(remoteProjectSyncDialog)
        self.label_overall.setObjectName(u"label_overall")
        self.label_overall.setGeometry(QRect(10, 10, 750, 16))
        self.label_done = QLabel(remoteProjectSyncDialog)
        self.label_done.setObjectName(u"label_done")
        self.label_done.setGeometry(QRect(10, 423, 500, 16))
        self.treeWidget = QTreeWidget(remoteProjectSyncDialog)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(10, 50, 751, 371))
        self.treeWidget.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)

        self.retranslateUi(remoteProjectSyncDialog)
        self.buttonBox.accepted.connect(remoteProjectSyncDialog.accept)
        self.buttonBox.rejected.connect(remoteProjectSyncDialog.reject)

        QMetaObject.connectSlotsByName(remoteProjectSyncDialog)
    # setupUi

    def retranslateUi(self, remoteProjectSyncDialog):
        remoteProjectSyncDialog.setWindowTitle(QCoreApplication.translate("remoteProjectSyncDialog", u"load a remote project", None))
        self.label_overall.setText(QCoreApplication.translate("remoteProjectSyncDialog", u"Loading list of remote projects...", None))
        self.label_done.setText(QCoreApplication.translate("remoteProjectSyncDialog", u"Successfully loaded all Content", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("remoteProjectSyncDialog", u"Last Change", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("remoteProjectSyncDialog", u"Target", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("remoteProjectSyncDialog", u"Telescope", None));
    # retranslateUi

