from PySide6 import QtGui
from PySide6.QtWidgets import QDialog, QTreeWidgetItem, QDialogButtonBox
from rclone_python import rclone, utils

from ui_remoteprojectsyncdialog import Ui_remoteProjectSyncDialog
from syncDialog import syncDialog


class remoteProjectSyncDialog(Ui_remoteProjectSyncDialog, QDialog):
  # Session-level cache of rclone lookups, keyed by data source name.
  # Populated on first read and reused for the rest of the app session.
  # A fresh start of the app (new process) starts with an empty cache.
  _sessionCache = {}

  @classmethod
  def clearSessionCache(cls):
    cls._sessionCache = {}

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
    self.s3ImagesPath = None

  def setS3CachePath(self, s3CachePath):
    self.s3CachePath = s3CachePath

  def setS3ImagesPath(self, s3ImagesPath):
    self.s3ImagesPath = s3ImagesPath

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
    #sd.setS3CachePath(self.s3CachePath)
    sd.setImageCache(self.imageCache)
    sd.open()

  def open(self, /):
    super().open()
    try:
      self.progressBar_overall.setValue(25)
      for dataSource,config in self.imageCache.dataSources.items():
        if config['enabled']== False:
          continue

        if dataSource in remoteProjectSyncDialog._sessionCache:
          cached = remoteProjectSyncDialog._sessionCache[dataSource]
          files = cached['files']
          latestImageDirectories = cached['latestImageDirectories']
        else:
          latestImageDirectories = {}
          try:
            files = rclone.ls(config['CachePath'], max_depth=1, dirs_only=True)
          except utils.RcloneException as e:
            print(e.error_msg)
            files = []
          try:
            imageDirectories = rclone.ls(config['ImagesPath'], max_depth=2, dirs_only=True)
          except utils.RcloneException as e:
            print(e.error_msg)
            imageDirectories = []
          for imageDirectory in imageDirectories:
            if imageDirectory['Path'].count('/') == 1:
              key=dataSource+'/'+imageDirectory['Path'].split('/')[0]
              if key not in latestImageDirectories:
                latestImageDirectories[key] = imageDirectory['Name']
              else:
                if latestImageDirectories[key] < imageDirectory['Name']:
                  latestImageDirectories[key] = imageDirectory['Name']
              pass
          remoteProjectSyncDialog._sessionCache[dataSource] = {
            'files': files,
            'latestImageDirectories': latestImageDirectories,
          }

        self.progressBar_overall.setMaximum(len(files)+25)
        telescopeItems={}
        item = QTreeWidgetItem(self.treeWidget)
        item.setText(0, dataSource)
        telescopeItems[dataSource] = item
        for fileInfo in files:
          subItem = QTreeWidgetItem(telescopeItems[dataSource])
          subItem.setText(1, fileInfo['Path'])
          key=dataSource+'/'+fileInfo['Path']
          if key in latestImageDirectories:
            subItem.setText(2, latestImageDirectories[key])
          else:
            subItem.setText(2, f'not on server')
        self.progressBar_overall.setValue(self.progressBar_overall.value()+1)
        QtGui.QGuiApplication.processEvents()
    except utils.RcloneException as e:
      print(e.error_msg)
    self.cleanupDialog()
    self.progressBar_overall.setValue(self.progressBar_overall.maximum())
    self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
    self.label_done.setVisible(True)
