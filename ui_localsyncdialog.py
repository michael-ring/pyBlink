# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'localSyncDialog.ui'
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

class Ui_localSyncDialog(object):
    def setupUi(self, localSyncDialog):
        if not localSyncDialog.objectName():
            localSyncDialog.setObjectName(u"localSyncDialog")
        localSyncDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        localSyncDialog.resize(800, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(localSyncDialog.sizePolicy().hasHeightForWidth())
        localSyncDialog.setSizePolicy(sizePolicy)
        localSyncDialog.setMinimumSize(QSize(800, 300))
        localSyncDialog.setMaximumSize(QSize(800, 300))
        localSyncDialog.setModal(False)
        self.buttonBox = QDialogButtonBox(localSyncDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 730, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setCenterButtons(False)
        self.progressBar_overall = QProgressBar(localSyncDialog)
        self.progressBar_overall.setObjectName(u"progressBar_overall")
        self.progressBar_overall.setGeometry(QRect(10, 25, 750, 23))
        self.progressBar_overall.setValue(24)
        self.progressBar_file1 = QProgressBar(localSyncDialog)
        self.progressBar_file1.setObjectName(u"progressBar_file1")
        self.progressBar_file1.setGeometry(QRect(520, 75, 240, 23))
        self.progressBar_file1.setValue(24)
        self.label_overall = QLabel(localSyncDialog)
        self.label_overall.setObjectName(u"label_overall")
        self.label_overall.setGeometry(QRect(10, 10, 750, 16))
        self.progressBar_file2 = QProgressBar(localSyncDialog)
        self.progressBar_file2.setObjectName(u"progressBar_file2")
        self.progressBar_file2.setGeometry(QRect(520, 100, 240, 23))
        self.progressBar_file2.setValue(24)
        self.progressBar_file3 = QProgressBar(localSyncDialog)
        self.progressBar_file3.setObjectName(u"progressBar_file3")
        self.progressBar_file3.setGeometry(QRect(520, 125, 240, 23))
        self.progressBar_file3.setValue(24)
        self.progressBar_file4 = QProgressBar(localSyncDialog)
        self.progressBar_file4.setObjectName(u"progressBar_file4")
        self.progressBar_file4.setGeometry(QRect(520, 150, 240, 23))
        self.progressBar_file4.setValue(24)
        self.label_file1 = QLabel(localSyncDialog)
        self.label_file1.setObjectName(u"label_file1")
        self.label_file1.setGeometry(QRect(10, 78, 500, 16))
        self.label_file2 = QLabel(localSyncDialog)
        self.label_file2.setObjectName(u"label_file2")
        self.label_file2.setGeometry(QRect(10, 103, 500, 16))
        self.label_file3 = QLabel(localSyncDialog)
        self.label_file3.setObjectName(u"label_file3")
        self.label_file3.setGeometry(QRect(10, 128, 500, 16))
        self.label_file4 = QLabel(localSyncDialog)
        self.label_file4.setObjectName(u"label_file4")
        self.label_file4.setGeometry(QRect(10, 153, 500, 16))
        self.label_done = QLabel(localSyncDialog)
        self.label_done.setObjectName(u"label_done")
        self.label_done.setGeometry(QRect(10, 203, 500, 16))

        self.retranslateUi(localSyncDialog)
        self.buttonBox.accepted.connect(localSyncDialog.accept)
        self.buttonBox.rejected.connect(localSyncDialog.reject)

        QMetaObject.connectSlotsByName(localSyncDialog)
    # setupUi

    def retranslateUi(self, localSyncDialog):
        localSyncDialog.setWindowTitle(QCoreApplication.translate("localSyncDialog", u"Sync Cache with local directories", None))
        self.label_overall.setText(QCoreApplication.translate("localSyncDialog", u"Loading Content from local Cache...", None))
        self.label_file1.setText(QCoreApplication.translate("localSyncDialog", u"TextLabel", None))
        self.label_file2.setText(QCoreApplication.translate("localSyncDialog", u"TextLabel", None))
        self.label_file3.setText(QCoreApplication.translate("localSyncDialog", u"TextLabel", None))
        self.label_file4.setText(QCoreApplication.translate("localSyncDialog", u"TextLabel", None))
        self.label_done.setText(QCoreApplication.translate("localSyncDialog", u"Successfully loaded all Content", None))
    # retranslateUi

