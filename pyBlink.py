import os
import sys

import rclone_python.utils
from PySide6 import QtGui
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QGraphicsScene, QTableWidgetItem, \
  QAbstractItemView, QHeaderView, QRadioButton, QDialog, QDialogButtonBox
from PIL import Image
from PySide6.QtGui import QPixmap, QImage, QPainter, QKeyEvent, QColor
from ui_mainwindow import Ui_MainWindow
from ui_syncdialog import Ui_SyncDialog
from ui_localsyncdialog import Ui_localSyncDialog
from pathlib import Path
from astropy.io import fits
from platformdirs import user_cache_dir
import cv2
from auto_stretch import apply_stretch
from rclone_python import rclone
import json
import psutil


def get_username():
  return psutil.Process().username()

class syncDialog(Ui_SyncDialog,QDialog):
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

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setupUi(self)
    self.cleanupDialog()

  def listener(self, mydict):
    self.progressBar_overall.setValue(mydict['progress']*100)
    if 'tasks' in mydict:
      if len(mydict['tasks']) > 0:
        self.progressBar_file1.setValue(mydict['tasks'][0]['progress']*100)
        self.label_file1.setText(Path(mydict['tasks'][0]['name']).name)
    if len(mydict['tasks']) > 1:
      self.progressBar_file2.setValue(mydict['tasks'][1]['progress'] * 100)
      self.label_file2.setText(Path(mydict['tasks'][1]['name']).name)
    if len(mydict['tasks']) > 2:
        self.progressBar_file3.setValue(mydict['tasks'][2]['progress']*100)
        self.label_file3.setText(Path(mydict['tasks'][2]['name']).name)
    if len(mydict['tasks']) > 3:
      self.progressBar_file4.setValue(mydict['tasks'][3]['progress'] * 100)
      self.label_file4.setText(Path(mydict['tasks'][3]['name']).name)
    QtGui.QGuiApplication.processEvents()

  def open(self, /):
    super().open()
    #QtGui.QGuiApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
    try:
      rclone.copy('upload:upload/_cache', window.cacheDirectory, listener=self.listener,show_progress=True,ignore_existing=True,args=["--transfers 4"])
      self.progressBar_overall.setValue(100)
      #self.statusBar().showMessage("Successfully synced cache from S3 server",5000)
    except rclone_python.utils.RcloneException as e:
      print(e.error_msg)
      #self.statusBar().showMessage(e.error_msg,5000)
    #QtGui.QGuiApplication.restoreOverrideCursor()
    self.cleanupDialog()
    self.progressBar_overall.setValue(100)
    self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

class localSyncDialog(Ui_localSyncDialog,QDialog):
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

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setupUi(self)
    self.cleanupDialog()

  def listener(self, mydict):
    self.progressBar_overall.setValue(mydict['progress']*100)
    if 'tasks' in mydict:
      if len(mydict['tasks']) > 0:
        self.progressBar_file1.setValue(mydict['tasks'][0]['progress']*100)
        self.label_file1.setText(Path(mydict['tasks'][0]['name']).name)
    if len(mydict['tasks']) > 1:
      self.progressBar_file2.setValue(mydict['tasks'][1]['progress'] * 100)
      self.label_file2.setText(Path(mydict['tasks'][1]['name']).name)
    if len(mydict['tasks']) > 2:
        self.progressBar_file3.setValue(mydict['tasks'][2]['progress']*100)
        self.label_file3.setText(Path(mydict['tasks'][2]['name']).name)
    if len(mydict['tasks']) > 3:
      self.progressBar_file4.setValue(mydict['tasks'][3]['progress'] * 100)
      self.label_file4.setText(Path(mydict['tasks'][3]['name']).name)
    QtGui.QGuiApplication.processEvents()

  def open(self, /):
    super().open()
    try:
      self.progressBar_overall.setValue(100)
    except rclone_python.utils.RcloneException as e:
      print(e.error_msg)
    self.cleanupDialog()
    self.progressBar_overall.setValue(100)
    self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    screensize = self.screen().size()
    self.resize(screensize.width(), screensize.height())
    newHeightOfGraphicsView = (screensize.width()-self.ui.detailsView.width()-4)*2//3
    if newHeightOfGraphicsView > screensize.height()-300:
      self.ui.graphicsView.setMinimumSize((screensize.height()-300)*3//2,screensize.height()-300)
      self.ui.graphicsView.setMaximumSize((screensize.height()-300)*3//2,screensize.height()-300)
    else:
      self.ui.graphicsView.setMinimumSize(screensize.width()-self.ui.detailsView.width()-4,(screensize.width()-self.ui.detailsView.width()-4)*2//3)
    self.ui.actionOpen.triggered.connect(self.actionOpen)
    self.ui.actionSync.triggered.connect(self.actionSync)
    self.ui.actionDelete.triggered.connect(self.actionDelete)
    self.ui.tableWidget.itemEntered.connect(self.actionTooltip)
    self.ui.tableWidget.currentItemChanged.connect(self.actionCurrentItemChanged)
    self.ui.tableWidget.installEventFilter(self)
    self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    self.ui.radioButton_all.setChecked(True)
    self.ui.radioButton_discarded.toggled.connect(self.radioButtonCheck)
    self.ui.radioButton_notdiscarded.toggled.connect(self.radioButtonCheck)
    self.ui.radioButton_startrails.toggled.connect(self.radioButtonCheck)
    self.ui.radioButton_notdiscarded.toggled.connect(self.radioButtonCheck)
    self.ui.radioButton_nostartrails.toggled.connect(self.radioButtonCheck)
    self.ui.radioButton_discardedbyothers.toggled.connect(self.radioButtonCheck)
    self.scene = QGraphicsScene()
    self.ui.graphicsView.setScene(self.scene)
    self.images = {}
    self.cacheDirectory = Path(user_cache_dir(self.windowTitle()))
    self.cacheDirectory.mkdir(parents=True, exist_ok=True)
    self.dateColumn = 0
    self.targetColumn = 2
    self.filterColumn = 3
    self.statusColumn = 9
    self.startrailColumn = 11

    try:
      self.config = json.load(open(Path(__file__).parent / 'config.json'))
    except:
      self.config = {}
      self.config["S3BucketName"] = "uploadsla"
      self.config["username"] = get_username()
      self.config["lastUsedLocalDir"] = os.getcwd()
      self.config["lastUsedS3Dir"] = config["S3BucketName"] + ":/"
      self.config["shortNames"] = {}

  def populateTableWidget(self,loadData=False):
    print(f"populating tableWidget")
    if len(self.images) != self.ui.tableWidget.rowCount():
      loadData = True
    if loadData:
      self.ui.tableWidget.clearContents()
      self.ui.tableWidget.setRowCount(len(self.images))
      position=0
      for index, image in self.images.items():
        self.ui.tableWidget.setItem(position, 0, QTableWidgetItem(image['date']))
        self.ui.tableWidget.setItem(position, 1, QTableWidgetItem(image['exposure']))
        self.ui.tableWidget.setItem(position, 2, QTableWidgetItem(image['object']))
        self.ui.tableWidget.setItem(position, 3, QTableWidgetItem(image['filter']))
        self.ui.tableWidget.setItem(position, 4, QTableWidgetItem(image['rotator']))
        self.ui.tableWidget.setItem(position, 5, QTableWidgetItem(image['pierside']))
        self.ui.tableWidget.setItem(position, 6, QTableWidgetItem("{:.2f}".format(image['adumean'])))
        self.ui.tableWidget.setItem(position, 7, QTableWidgetItem("{:.2f}".format(image['fwhm'])))
        self.ui.tableWidget.setItem(position, 8, QTableWidgetItem(str(image['detectedstars'])))
        self.ui.tableWidget.setItem(position, 9, QTableWidgetItem(image['status']))
        self.ui.tableWidget.setItem(position, 10, QTableWidgetItem(image['statusothers']))
        self.ui.tableWidget.setItem(position, 11, QTableWidgetItem(image['startrails']))
        if image['status'] == '✘':
          for column in range(self.ui.tableWidget.columnCount()):
            self.ui.tableWidget.item(position, column).setBackground(QColor(255, 0, 0, 127))
        position += 1

    self.ui.tableWidget.setUpdatesEnabled(False)
    position = 0
    for index, image in self.images.items():
      showItem=False
      if self.ui.radioButton_all.isChecked():
        showItem=True
      if self.ui.radioButton_notdiscarded.isChecked():
        if image['status'] != '✘' and image['status'] != '✔':
          showItem=True
      if self.ui.radioButton_discarded.isChecked():
        if image['status'] == '✘':
          showItem=True
      if self.ui.radioButton_discardedbyothers.isChecked():
        if image['statusothers'] == '✘':
          showItem=True
      if self.ui.radioButton_startrails.isChecked():
        if image['startrails'] == '✔':
          showItem=True
      if self.ui.radioButton_nostartrails.isChecked():
        if image['startrails'] != '✔':
          showItem=True
      if showItem:
        self.ui.tableWidget.showRow(position)
      else:
        self.ui.tableWidget.hideRow(position)
      position += 1

    self.ui.tableWidget.setUpdatesEnabled(True)


  def mousePressEvent(self, e):
    self.statusBar().showMessage(f"mousePressEvent {e.position()}")

  def eventFilter(self, watched, event, /):
    if watched == self.ui.tableWidget:
      if event.type() == QEvent.Type.KeyPress:
        currentRow = self.ui.tableWidget.currentRow()
        imagesIndex=f'{self.ui.tableWidget.item(currentRow,self.targetColumn).text()} {self.ui.tableWidget.item(currentRow,self.filterColumn).text()} {self.ui.tableWidget.item(currentRow,self.dateColumn).text()}'
        if QKeyEvent(event).key() == Qt.Key.Key_Up:
          if self.ui.tableWidget.item(currentRow,self.statusColumn).text() != '✘':
            self.ui.tableWidget.item(currentRow,self.statusColumn).setText('✔')
            self.images[imagesIndex]['status']='✔'
        if QKeyEvent(event).key() == Qt.Key.Key_Down:
          if self.ui.tableWidget.item(currentRow,self.statusColumn).text() != '✘':
            self.ui.tableWidget.item(currentRow,self.statusColumn).setText('✔')
            self.images[imagesIndex]['status'] = '✔'
        if QKeyEvent(event).key() == Qt.Key.Key_X:
          if self.ui.tableWidget.item(currentRow,self.statusColumn).text() != '✘':
            self.ui.tableWidget.item(currentRow,self.statusColumn).setText('✘')
            self.images[imagesIndex]['status']='✘'
            for column in range(self.ui.tableWidget.columnCount()):
              self.ui.tableWidget.item(currentRow,column).setBackground(QColor(255,0,0,127))
          else:
            self.ui.tableWidget.item(currentRow,self.statusColumn).setText('✔')
            self.images[imagesIndex]['status'] = '✔'
            for column in range(self.ui.tableWidget.columnCount()):
              self.ui.tableWidget.item(currentRow, column).setBackground(QColor(255, 255, 255, 255))
          return True
        if QKeyEvent(event).key() == Qt.Key.Key_T:
          if self.ui.tableWidget.item(currentRow, self.startrailColumn).text() != '✔':
            self.ui.tableWidget.item(currentRow, self.startrailColumn).setText('✔')
            self.images[imagesIndex]['startrails'] = '✔'
          else:
            self.ui.tableWidget.item(currentRow, self.startrailColumn).setText('')
            self.images[imagesIndex]['startrails'] = ''
          return True
    # pass the event on to the parent class
    return QMainWindow.eventFilter(self, watched, event)

  def radioButtonCheck(self):
    self.populateTableWidget()

  def actionDelete(self):
    for index,image in self.images.copy().items():
      if image['status'] == '✘':
        if Path(image['fullPath']).exists() and Path(image['fullPath']).is_file():
          Path(image['fullPath']).unlink()
          if Path(image['cachePath']).exists() and Path(image['cachePath']).is_file():
            Path(image['cachePath']).unlink()
          self.images.pop(index)
    self.populateTableWidget()

  def actionSync(self):
    sd = syncDialog(self)
    sd.open()

  def actionOpen(self):
    userName=get_username()
    self.workingDirectory = Path(QFileDialog.getExistingDirectory(self, "Select Directory"),dir=Path(self.config['lastUsedLocalDir']))
    if self.workingDirectory != '.':
      self.config["lastUsedLocalDir"] = self.workingDirectory
      print(f"Working Directory: {self.workingDirectory}")

      lsd = localSyncDialog(self)
      lsd.open()

      self.images.clear()
      cachePathFound=False
      cachePath=None
      imageMetaData={}
      for file in self.workingDirectory.rglob("ImageMetaData*.json"):
        imds=json.load(open(file))
        for imd in imds:
          imageMetaData[Path(imd['FilePath']).name]=imd
      QtGui.QGuiApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
      for file in self.workingDirectory.rglob("*.fits"):
        if 'site-packages' in str(file.parent):
          continue
        image = {}
        image['fullPath'] = file
        if cachePathFound == False:
          print(f"Loading Fits Data from File {file} to detect cachedir")
          header = fits.getheader(image['fullPath'])
          image['object'] = header['OBJECT']
          image['telescope'] = header['TELESCOP']
          if image['telescope'] in self.config["shortNames"]:
            image['telescope'] = self.config["shortNames"][image['telescope']]
          cachePath=self.cacheDirectory / image['telescope'] / image['object']
          cachePathFound = True
        if (cachePath / file.name).with_suffix('.jpg').exists():
          self.statusBar().showMessage(f'Loading {file.name} from cache')
          QtGui.QGuiApplication.processEvents()
          print(f'Loading Fits data from File {(cachePath / file.name).with_suffix('.jpg')}')
          im=Image.open((cachePath / file.name).with_suffix('.jpg'))
          exif=im.getexif()
          try:
            savedTags=json.loads(exif[0x9286])
            image['date']=savedTags['date']
            image['object']=savedTags['object']
            image['telescope']=savedTags['telescope']
            image['filter']=savedTags['filter']
            image['pierside']=savedTags['pierside']
            image['rotator']=savedTags['rotator']
            image['exposure']=savedTags['exposure']

            if 'adumean' in savedTags:
              image['adumean'] = savedTags['adumean']
            else:
              image['adumean'] = 0

            if 'fwhm' in savedTags:
              image['fwhm']=savedTags['fwhm']
            else:
              image['fwhm']=0

            if 'detectedstars' in savedTags:
              image['detectedstars'] = savedTags['detectedstars']
            else:
              image['detectedstars'] = 0

          except KeyError:
            print(f"Fits data in Exif Header missing/incomplete, rebuild...")
            (cachePath / file.name).with_suffix('.jpg').unlink()
        if not (cachePath / file.name).with_suffix('.jpg').exists():
          self.statusBar().showMessage(f'Loading and converting {file.name}')
          QtGui.QGuiApplication.processEvents()

          print(f"Loading Fits Data from File: {file}")
          header = fits.getheader(image['fullPath'])
          image['filter'] = header['FILTER']
          if "BAYERPAT" in header:
            image['bayerpat'] = header['BAYERPAT']
          image['object'] = header['OBJECT']
          image['telescope'] = header['TELESCOP']
          image['exposure'] = header['EXPOSURE']
          if image['telescope'] in self.config["shortNames"]:
            image['telescope'] = self.config["shortNames"][image['telescope']]
          image['date'] = header['DATE-LOC'].split('.')[0].replace('T', ' ')
          image['pierside'] = header['PIERSIDE']
          if 'ROTATOR' in header:
            image['rotator'] = str(int(header['ROTATOR']))
          else:
            image['rotator'] = 'not found'
          print(f"Fits Reading done")

          image['adumean'] = 0
          image['detectedstars'] = 0
          image['fwhm'] = 0
          if file.name in imageMetaData:
            if 'ADUMean' in imageMetaData[file.name]:
              image['adumean']=imageMetaData[file.name]['ADUMean']
            if 'DetectedStars' in imageMetaData[file.name]:
              image['detectedstars']=imageMetaData[file.name]['DetectedStars']
            if 'FWHM' in imageMetaData[file.name]:
              image['fwhm']=imageMetaData[file.name]['FWHM']

        image['status'] = ""
        image['statusothers'] = ""
        image['startrails'] = ""
        index = f"{image['object']} {image['filter']} {image['date']}"
        image['cachePath'] = (self.cacheDirectory / image['telescope'] / image['object'] / file.name).with_suffix('.jpg')
        #image['detailsCachePath'] = image['cachePath'].with_stem(image['cachePath'].stem + '-aberration')
        if not image['cachePath'].parent.exists():
          image['cachePath'].parent.mkdir(parents=True, exist_ok=True)
        if not image['cachePath'].exists():
          print(f"Creating {image['cachePath']}")
          data = fits.getdata(image['fullPath'], ext=0)
          if 'bayerpat' in image:
            debayered = cv2.cvtColor(data, cv2.COLOR_BayerBGGR2BGR)
            gray_image = cv2.cvtColor(debayered, cv2.COLOR_BGR2GRAY)
            normalized = gray_image
            cv2.normalize(debayered, normalized, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            stretched = apply_stretch(normalized, target_bkg=0.15)
          else:
            normalized = data
            cv2.normalize(data, normalized, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            stretched = apply_stretch(normalized, target_bkg=0.15)

          im = Image.fromarray(stretched * 255)
          im = im.convert('RGB')

          if image['pierside'] == 'East':
            im = im.rotate(180)

          exif = im.getexif()
          persistedTags={}
          persistedTags['date'] = image['date']
          persistedTags['object'] = image['object']
          persistedTags['telescope'] = image['telescope']
          persistedTags['filter'] = image['filter']
          persistedTags['pierside'] = image['pierside']
          persistedTags['rotator'] = image['rotator']
          persistedTags['adumean'] = image['adumean']
          persistedTags['detectedstars'] = image['detectedstars']
          persistedTags['fwhm'] = image['fwhm']
          persistedTags['exposure'] = image['exposure']
          exif[0x9286] = json.dumps(persistedTags)

          im.save(image['cachePath'], exif=exif)

        self.images[index] = image
      self.images = dict(sorted(self.images.items()))
      print(f"Found {len(self.images)} images")
      if len(self.images) > 0:
        statusfile = self.images[next(iter(self.images))]['cachePath'].parent / f'status-{userName}.json'
        if statusfile.exists():
          print(f"Loading status from {statusfile}")
          statusImages = json.load(open(statusfile))
          for index in statusImages:
            if index in self.images:
              self.images[index]['status'] = statusImages[index]['status']
              self.images[index]['startrails'] = statusImages[index]['startrails']
      self.populateTableWidget(True)
      QtGui.QGuiApplication.restoreOverrideCursor()

  def closeEvent(self, event):
    if len(self.images) > 0:
      userName = get_username()
      statusfile=self.images[next(iter(self.images))]['cachePath'].parent / f'status-{userName}.json'
      imagesStatus={}
      for index,image in self.images.items():
        imagesStatus[index]={ 'status': image['status'], 'statusothers': image['statusothers'], 'startrails': image['startrails']}

      with statusfile.open("w", encoding="UTF-8") as target:
        json.dump(imagesStatus, target, indent=2)
    event.accept()

  def actionCurrentItemChanged(self, item: QTableWidgetItem):
    if item is None:
      return
    idx=self.ui.tableWidget.item(item.row(), 2).text()+" "+self.ui.tableWidget.item(item.row(), 3).text()+" "+self.ui.tableWidget.item(item.row(), 0).text()
    self.image = QImage(self.images[idx]['cachePath'])
    scene = QGraphicsScene(0, 0, self.ui.graphicsView.size().width(), self.ui.graphicsView.size().height())
    pixmap = QPixmap(self.image)
    pixmapitem = scene.addPixmap(pixmap)
    pixmapitem.setScale(self.ui.graphicsView.size().width() / pixmap.width())
    pixmapitem.setPos(0, 0)
    self.ui.graphicsView.setScene(scene)
    self.ui.graphicsView.setRenderHint(QPainter.RenderHint.Antialiasing)
    self.ui.graphicsView.show()

    scene = QGraphicsScene(0, 0, self.ui.detailsView.size().width(), self.ui.detailsView.size().width())
    segmentedImage=QImage(self.ui.detailsView.size().width(), self.ui.detailsView.size().width(), QImage.Format.Format_RGB32)
    sourceWidth=self.ui.detailsView.size().width()
    sourceHeight=self.ui.detailsView.size().height()
    segmentWidth=self.ui.detailsView.size().width()//3
    segmentHeight=self.ui.detailsView.size().height()//3
    Painter=QPainter()
    Painter.begin(segmentedImage)
    Painter.drawImage(0, 0, self.image.copy(0,0,segmentWidth,segmentHeight))
    Painter.drawImage(segmentWidth, 0, self.image.copy(sourceWidth//2-segmentWidth//2,0,segmentWidth,segmentHeight))
    Painter.drawImage(2*segmentWidth, 0, self.image.copy(sourceWidth-segmentWidth,0,segmentWidth,segmentHeight))

    Painter.drawImage(0, segmentHeight, self.image.copy(0,sourceHeight//2-segmentHeight//2,segmentWidth,segmentHeight))
    Painter.drawImage(segmentWidth, segmentHeight, self.image.copy(sourceWidth//2-segmentWidth//2,sourceHeight//2-segmentHeight//2,segmentWidth,segmentHeight))
    Painter.drawImage(2*segmentWidth, segmentHeight, self.image.copy(sourceWidth-segmentWidth,sourceHeight//2-segmentHeight//2,segmentWidth,segmentHeight))

    Painter.drawImage(0, segmentHeight*2, self.image.copy(0,sourceHeight-segmentHeight,segmentWidth,segmentHeight))
    Painter.drawImage(segmentWidth, segmentHeight*2, self.image.copy(sourceWidth//2-segmentWidth//2,sourceHeight-segmentHeight,segmentWidth,segmentHeight))
    Painter.drawImage(2*segmentWidth, segmentHeight*2, self.image.copy(sourceWidth-segmentWidth,sourceHeight-segmentHeight,segmentWidth,segmentHeight))

    Painter.end()
    pixmap2=QPixmap.fromImage(segmentedImage)
    pixmapitem2 = scene.addPixmap(pixmap2)
    pixmapitem2.setScale(1)
    pixmapitem2.setPos(0, 0)
    self.ui.detailsView.setScene(scene)
    self.ui.detailsView.setRenderHint(QPainter.RenderHint.Antialiasing)
    self.ui.detailsView.show()

  def actionTooltip(self, item: QListWidgetItem):
    text = item.text()
    text_width = self.fontMetrics().boundingRect(text).width()
    width = self.width()
    # if text_width > width:
    item.setToolTip(text)
    # else:
    #    item.setToolTip('')

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())