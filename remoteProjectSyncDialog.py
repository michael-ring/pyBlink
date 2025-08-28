from PySide6 import QtGui
from PySide6.QtWidgets import QDialog, QTreeWidgetItem, QDialogButtonBox
from rclone_python import rclone, utils

from ui_remoteprojectsyncdialog import Ui_remoteProjectSyncDialog
from syncDialog import syncDialog


class remoteProjectSyncDialog(Ui_remoteProjectSyncDialog, QDialog):
  def cleanupDialog(self):
    self.progressBar_overall.setValue(0)
    self.label_done.setVisible(False)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setupUi(self)
    self.cleanupDialog()
    self.treeWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)
    self.buttonBox.accepted.connect(self.onAccepted)
    self.buttonBox.rejected.connect(self.onRejected)
    self.imageCache = None
    self.s3CachePath = None

  def setS3CachePath(self, s3CachePath):
    self.s3CachePath = s3CachePath

  def setImageCache(self, imageCache):
    self.imageCache = imageCache

  def onAccepted(self):
    pass

  def onRejected(self):
    pass

  def onItemDoubleClicked(self, item):
    telescope = item.parent().text(0)
    target = item.text(1)
    self.close()
    sd = syncDialog(self.parent())
    sd.setSpecificSyncDirectory(specificSyncDirectory=f"{telescope}/{target}")
    sd.setS3CachePath(self.s3CachePath)
    sd.setImageCache(self.imageCache)
    sd.open()

  def open(self, /):
    super().open()
    try:
      self.progressBar_overall.setValue(25)
      files = rclone.ls(self.s3CachePath, max_depth=2, dirs_only=True)
      self.progressBar_overall.setMaximum(len(files)+25)
      telescopeItems={}
      for fileInfo in files:
        if fileInfo['Path'].count('/') == 0:
          item = QTreeWidgetItem(self.treeWidget)
          item.setText(0, fileInfo['Path'])
          telescopeItems[fileInfo['Path']] = item
        if fileInfo['Path'].count('/') == 1:
          subItem = QTreeWidgetItem(telescopeItems[fileInfo['Path'].split('/')[0]])
          subItem.setText(1, fileInfo['Path'].split('/')[1])
        self.progressBar_overall.setValue(self.progressBar_overall.value()+1)
        QtGui.QGuiApplication.processEvents()
    except utils.RcloneException as e:
      print(e.error_msg)
    self.cleanupDialog()
    self.progressBar_overall.setValue(self.progressBar_overall.maximum())
    self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
    self.label_done.setVisible(True)
