# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'deleteDialog.ui'
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

class Ui_deleteDialog(object):
    def setupUi(self, deleteDialog):
        if not deleteDialog.objectName():
            deleteDialog.setObjectName(u"deleteDialog")
        deleteDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        deleteDialog.resize(800, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(deleteDialog.sizePolicy().hasHeightForWidth())
        deleteDialog.setSizePolicy(sizePolicy)
        deleteDialog.setMinimumSize(QSize(800, 200))
        deleteDialog.setMaximumSize(QSize(800, 200))
        deleteDialog.setModal(False)
        self.buttonBox = QDialogButtonBox(deleteDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 140, 730, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setCenterButtons(False)
        self.progressBar_overall = QProgressBar(deleteDialog)
        self.progressBar_overall.setObjectName(u"progressBar_overall")
        self.progressBar_overall.setGeometry(QRect(10, 25, 750, 23))
        self.progressBar_overall.setValue(0)
        self.label_overall = QLabel(deleteDialog)
        self.label_overall.setObjectName(u"label_overall")
        self.label_overall.setGeometry(QRect(10, 10, 750, 16))
        self.label_current = QLabel(deleteDialog)
        self.label_current.setObjectName(u"label_current")
        self.label_current.setGeometry(QRect(10, 60, 750, 16))
        self.label_done = QLabel(deleteDialog)
        self.label_done.setObjectName(u"label_done")
        self.label_done.setGeometry(QRect(10, 100, 500, 16))

        self.retranslateUi(deleteDialog)
        self.buttonBox.accepted.connect(deleteDialog.accept)
        self.buttonBox.rejected.connect(deleteDialog.reject)

        QMetaObject.connectSlotsByName(deleteDialog)
    # setupUi

    def retranslateUi(self, deleteDialog):
        deleteDialog.setWindowTitle(QCoreApplication.translate("deleteDialog", u"Delete Discarded Images", None))
        self.label_overall.setText(QCoreApplication.translate("deleteDialog", u"Deleting discarded images...", None))
        self.label_current.setText("")
        self.label_done.setText(QCoreApplication.translate("deleteDialog", u"Successfully deleted discarded images", None))
    # retranslateUi

