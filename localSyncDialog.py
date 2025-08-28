import psutil
from PySide6 import QtGui
from PySide6.QtWidgets import QDialog, QDialogButtonBox
from PySide6.QtCore import Signal


from ui_localsyncdialog import Ui_localSyncDialog
import json
from pathlib import Path
from astropy.io import fits
from imageCache import imageCache
import random


class localSyncDialog(Ui_localSyncDialog, QDialog):
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

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setupUi(self)
    self.cleanupDialog()
    self.workingDirectory = None
    self.imageCache = None
    self.telescopeShortNames = {}

  def setWorkingDirectory(self, workingDirectory):
    self.workingDirectory = workingDirectory

  def setImageCache(self, imageCache):
    self.imageCache = imageCache

  def setTelescopeShortNames(self, telescopeShortNames):
    self.telescopeShortNames = telescopeShortNames

  def listener(self, mydict):
    self.progressBar_overall.setValue(mydict['progress'] * 100)
    if 'tasks' in mydict:
      if len(mydict['tasks']) > 0:
        self.progressBar_file1.setValue(mydict['tasks'][0]['progress'] * 100)
        self.label_file1.setText(Path(mydict['tasks'][0]['name']).name)
    if len(mydict['tasks']) > 1:
      self.progressBar_file2.setValue(mydict['tasks'][1]['progress'] * 100)
      self.label_file2.setText(Path(mydict['tasks'][1]['name']).name)
    if len(mydict['tasks']) > 2:
      self.progressBar_file3.setValue(mydict['tasks'][2]['progress'] * 100)
      self.label_file3.setText(Path(mydict['tasks'][2]['name']).name)
    if len(mydict['tasks']) > 3:
      self.progressBar_file4.setValue(mydict['tasks'][3]['progress'] * 100)
      self.label_file4.setText(Path(mydict['tasks'][3]['name']).name)
    QtGui.QGuiApplication.processEvents()

  def onProgressUpdate(self,value):
    self.progressBar_overall.setValue(value)
    QtGui.QGuiApplication.processEvents()

  def onFileProgressUpdate(self,filename,slot,value):
    if slot == 0:
      self.label_file1.setText(filename)
      self.progressBar_file1.setValue(value)
    if slot == 1:
      self.label_file2.setText(filename)
      self.progressBar_file2.setValue(value)
    if slot == 2:
      self.label_file3.setText(filename)
      self.progressBar_file3.setValue(value)
    if slot == 3:
      self.label_file4.setText(filename)
      self.progressBar_file4.setValue(value)
    QtGui.QGuiApplication.processEvents()

  def open(self, /):
    super().open()
    filesCount = len(list(self.workingDirectory.rglob("*.fits")))
    self.progressBar_overall.setMaximum(filesCount)

    self.imageCache.progressUpdate.connect(self.onProgressUpdate)
    self.imageCache.fileProgressUpdate.connect(self.onFileProgressUpdate)
    self.imageCache.populateCacheFromFitsDirectory(self.workingDirectory)
    print(f"Found {len(self.imageCache.images)} images")
    if len(self.imageCache.images) > 0:
      statusFileDirectory=Path(self.imageCache.images[next(iter(self.imageCache.images))]['cachepath'].parent)
      for statusfile in Path(statusFileDirectory).glob("status-*.json"):
        if statusfile.name == f"status-{psutil.Process().username()}.json":
          print(f"Loading own status from {statusfile}")
          statusImages = json.load(open(statusfile))
          for index in statusImages:
            if index in self.imageCache.images:
              self.imageCache.images[index]['status'] = statusImages[index]['status']
              self.imageCache.images[index]['startrails'] = statusImages[index]['startrails']
        else:
          print(f"Loading other status from {statusfile}")
          statusImages = json.load(open(statusfile))
          for index in statusImages:
            if index in self.imageCache.images:
              if self.imageCache.images[index]['statusothers'] == "":
                self.imageCache.images[index]['statusothers'] = statusImages[index]['status']
              elif statusImages[index]['status'] == '✘':
                self.imageCache.images[index]['statusothers'] = '✘'
              elif statusImages[index]['status'] == '✔' and self.imageCache.images[index]['statusothers'] != '✘':
                self.imageCache.images[index]['statusothers'] = statusImages[index]['status']

              if statusImages[index]['status'] == '✔':
                self.imageCache.images[index]['startrails'] = '✔'

    self.cleanupDialog()
    self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
    self.label_done.setVisible(True)
