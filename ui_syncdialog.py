# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'syncDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QProgressBar, QSizePolicy, QWidget)

class Ui_SyncDialog(object):
    def setupUi(self, SyncDialog):
        if not SyncDialog.objectName():
            SyncDialog.setObjectName(u"SyncDialog")
        SyncDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        SyncDialog.resize(800, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SyncDialog.sizePolicy().hasHeightForWidth())
        SyncDialog.setSizePolicy(sizePolicy)
        SyncDialog.setMinimumSize(QSize(800, 300))
        SyncDialog.setMaximumSize(QSize(800, 300))
        SyncDialog.setModal(False)
        self.buttonBox = QDialogButtonBox(SyncDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 250, 730, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setCenterButtons(False)
        self.progressBar_overall = QProgressBar(SyncDialog)
        self.progressBar_overall.setObjectName(u"progressBar_overall")
        self.progressBar_overall.setGeometry(QRect(10, 25, 750, 23))
        self.progressBar_overall.setValue(24)
        self.progressBar_file1 = QProgressBar(SyncDialog)
        self.progressBar_file1.setObjectName(u"progressBar_file1")
        self.progressBar_file1.setGeometry(QRect(520, 75, 240, 23))
        self.progressBar_file1.setValue(24)
        self.label_overall = QLabel(SyncDialog)
        self.label_overall.setObjectName(u"label_overall")
        self.label_overall.setGeometry(QRect(10, 10, 750, 16))
        self.progressBar_file2 = QProgressBar(SyncDialog)
        self.progressBar_file2.setObjectName(u"progressBar_file2")
        self.progressBar_file2.setGeometry(QRect(520, 100, 240, 23))
        self.progressBar_file2.setValue(24)
        self.progressBar_file3 = QProgressBar(SyncDialog)
        self.progressBar_file3.setObjectName(u"progressBar_file3")
        self.progressBar_file3.setGeometry(QRect(520, 125, 240, 23))
        self.progressBar_file3.setValue(24)
        self.progressBar_file4 = QProgressBar(SyncDialog)
        self.progressBar_file4.setObjectName(u"progressBar_file4")
        self.progressBar_file4.setGeometry(QRect(520, 150, 240, 23))
        self.progressBar_file4.setValue(24)
        self.label_file1 = QLabel(SyncDialog)
        self.label_file1.setObjectName(u"label_file1")
        self.label_file1.setGeometry(QRect(10, 78, 500, 16))
        self.label_file2 = QLabel(SyncDialog)
        self.label_file2.setObjectName(u"label_file2")
        self.label_file2.setGeometry(QRect(10, 103, 500, 16))
        self.label_file3 = QLabel(SyncDialog)
        self.label_file3.setObjectName(u"label_file3")
        self.label_file3.setGeometry(QRect(10, 128, 500, 16))
        self.label_file4 = QLabel(SyncDialog)
        self.label_file4.setObjectName(u"label_file4")
        self.label_file4.setGeometry(QRect(10, 153, 500, 16))
        self.label_done = QLabel(SyncDialog)
        self.label_done.setObjectName(u"label_done")
        self.label_done.setGeometry(QRect(10, 253, 500, 16))
        self.label_syncToServer = QLabel(SyncDialog)
        self.label_syncToServer.setObjectName(u"label_syncToServer")
        self.label_syncToServer.setGeometry(QRect(10, 178, 500, 16))
        self.label_syncFromServer = QLabel(SyncDialog)
        self.label_syncFromServer.setObjectName(u"label_syncFromServer")
        self.label_syncFromServer.setGeometry(QRect(10, 228, 500, 16))
        self.label_syncStatus = QLabel(SyncDialog)
        self.label_syncStatus.setObjectName(u"label_syncStatus")
        self.label_syncStatus.setGeometry(QRect(10, 203, 500, 16))

        self.retranslateUi(SyncDialog)
        self.buttonBox.accepted.connect(SyncDialog.accept)
        self.buttonBox.rejected.connect(SyncDialog.reject)

        QMetaObject.connectSlotsByName(SyncDialog)
    # setupUi

    def retranslateUi(self, SyncDialog):
        SyncDialog.setWindowTitle(QCoreApplication.translate("SyncDialog", u"Syncing Cache with Remote Server", None))
        self.label_overall.setText(QCoreApplication.translate("SyncDialog", u"Syncing local Cache with remote Cache", None))
        self.label_file1.setText(QCoreApplication.translate("SyncDialog", u"TextLabel", None))
        self.label_file2.setText(QCoreApplication.translate("SyncDialog", u"TextLabel", None))
        self.label_file3.setText(QCoreApplication.translate("SyncDialog", u"TextLabel", None))
        self.label_file4.setText(QCoreApplication.translate("SyncDialog", u"TextLabel", None))
        self.label_done.setText(QCoreApplication.translate("SyncDialog", u"Successfully updated Caches", None))
        self.label_syncToServer.setText(QCoreApplication.translate("SyncDialog", u"Sync local Cache to remote Cache", None))
        self.label_syncFromServer.setText(QCoreApplication.translate("SyncDialog", u"Sync remote Cache to local Cache", None))
        self.label_syncStatus.setText(QCoreApplication.translate("SyncDialog", u"Sync local Status to remote Cache", None))
    # retranslateUi

