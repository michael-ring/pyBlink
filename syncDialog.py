from PySide6 import QtGui
from PySide6.QtWidgets import QDialog, QDialogButtonBox
from rclone_python import rclone, utils
from pathlib import Path
import psutil

from ui_syncdialog import Ui_SyncDialog
from imageCache import imageCache


class syncDialog(Ui_SyncDialog, QDialog):

  def cleanupDialog(self):
    self.progressBar_overall.setValue(0)
    self.progressBar_file1.setValue(0)
    self.progressBar_file2.setValue(0)
    self.progressBar_file3.setValue(0)
    self.progressBar_file4.setValue(0)
    self.label_file1.setText("")
    self.label_file2.setText("")
    self.label_file3.setText("")
    self.label_file4.setText("")
    self.label_done.setVisible(False)
    self.label_syncToServer.setVisible(False)
    self.label_syncFromServer.setVisible(False)
    self.label_syncStatus.setVisible(False)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setupUi(self)
    self.cleanupDialog()
    self.specificSyncDirectory = None
    self.imageCache = None

  def setImageCache(self, imageCache):
    self.imageCache = imageCache

  def setS3CachePath(self, s3CachePath):
    self.s3CachePath = s3CachePath

  def listener(self, mydict):
    self.progressBar_overall.setValue(mydict['progress'] * 100)
    if 'tasks' in mydict:
      if len(mydict['tasks']) > 0:
        self.progressBar_file1.setValue(mydict['tasks'][0]['progress'] * 100)
        self.label_file1.setText(Path(mydict['tasks'][0]['name']).name)
        #print(f"{Path(mydict['tasks'][0]['name']).name} {mydict['tasks'][0]['progress'] * 100}%")
    if len(mydict['tasks']) > 1:
      self.progressBar_file2.setValue(mydict['tasks'][1]['progress'] * 100)
      self.label_file2.setText(Path(mydict['tasks'][1]['name']).name)
      #print(f"{Path(mydict['tasks'][1]['name']).name} {mydict['tasks'][1]['progress'] * 100}%")
    if len(mydict['tasks']) > 2:
      self.progressBar_file3.setValue(mydict['tasks'][2]['progress'] * 100)
      self.label_file3.setText(Path(mydict['tasks'][2]['name']).name)
      #print(f"{Path(mydict['tasks'][2]['name']).name} {mydict['tasks'][2]['progress'] * 100}%")
    if len(mydict['tasks']) > 3:
      self.progressBar_file4.setValue(mydict['tasks'][3]['progress'] * 100)
      self.label_file4.setText(Path(mydict['tasks'][3]['name']).name)
      #print(f"{Path(mydict['tasks'][3]['name']).name} {mydict['tasks'][3]['progress'] * 100}%")
    QtGui.QGuiApplication.processEvents()
    QtGui.QGuiApplication.processEvents()

  def setSpecificSyncDirectory(self, specificSyncDirectory):
    self.specificSyncDirectory = specificSyncDirectory

  def open(self, /):
    super().open()
    syncSuccess = False
    try:
      if self.specificSyncDirectory is not None:
        self.label_syncToServer.setVisible(True)
        QtGui.QGuiApplication.processEvents()
        rclone.copy(self.imageCache.getCacheDirectory() / self.specificSyncDirectory,f'{self.s3CachePath}{self.specificSyncDirectory}', listener=self.listener, show_progress=True,
                    ignore_existing=True, args=["--transfers 4 --exclude '*.json'"])
        self.label_syncStatus.setVisible(True)
        QtGui.QGuiApplication.processEvents()
        rclone.copy(self.imageCache.getCacheDirectory() / self.specificSyncDirectory,f'{self.s3CachePath}{self.specificSyncDirectory}', listener=self.listener, show_progress=True,
                    ignore_existing=False, args=[f'--transfers 4 --include "status-{psutil.Process().username()}.json"'])
        self.label_syncFromServer.setVisible(True)
        QtGui.QGuiApplication.processEvents()
        rclone.copy(f'{self.s3CachePath}{self.specificSyncDirectory}',
                    self.imageCache.getCacheDirectory() / self.specificSyncDirectory, listener=self.listener, show_progress=True,
                    ignore_existing=True, args=["--transfers 4 --exclude '*.json'"])
        rclone.copy(f'{self.s3CachePath}{self.specificSyncDirectory}',
                    self.imageCache.getCacheDirectory() / self.specificSyncDirectory, listener=self.listener,
                    show_progress=True,
                    ignore_existing=False, args=["--transfers 4 --include '*.json'"])
      else:
        self.label_syncToServer.setVisible(True)
        QtGui.QGuiApplication.processEvents()
        rclone.copy(self.imageCache.getCacheDirectory(),self.s3CachePath, listener=self.listener, show_progress=True,
                    ignore_existing=True, args=["--transfers 4 --exclude '*.json'"])
        self.label_syncStatus.setVisible(True)
        QtGui.QGuiApplication.processEvents()
        rclone.copy(self.imageCache.getCacheDirectory(),self.s3CachePath, listener=self.listener, show_progress=True,
                    ignore_existing=False, args=[f'--transfers 4 --include "status-{psutil.Process().username()}.json"'])
        self.label_syncFromServer.setVisible(True)
        QtGui.QGuiApplication.processEvents()
        rclone.copy(self.s3CachePath, self.imageCache.getCacheDirectory(), listener=self.listener, show_progress=True,
                    ignore_existing=True, args=["--transfers 4 --exclude '*.json'"])
        rclone.copy(self.s3CachePath, self.imageCache.getCacheDirectory(), listener=self.listener, show_progress=True,
                  ignore_existing=False, args=["--transfers 4 --include '*.json'"])
      self.progressBar_overall.setValue(100)
      syncSuccess = True
    except utils.RcloneException as e:
      print(e.error_msg)
      # self.statusBar().showMessage(e.error_msg)
    self.cleanupDialog()
    self.progressBar_overall.setValue(100)
    self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
    self.label_done.setVisible(True)
    QtGui.QGuiApplication.processEvents()
    if self.specificSyncDirectory is not None and syncSuccess:
      self.imageCache.populateFromCachedImages(self.specificSyncDirectory)
      self.close()
