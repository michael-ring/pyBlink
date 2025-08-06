import os
import sys
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QGraphicsScene, QTableWidgetItem, \
  QAbstractItemView, QHeaderView
from PIL import Image
from PySide6.QtGui import QPixmap, QImage, QPainter, QKeyEvent, QColor
from ui_mainwindow import Ui_MainWindow
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

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    screensize = self.screen().size()
    self.resize(screensize.width(), screensize.height())
    self.ui.graphicsView.setMinimumSize(screensize.width()-self.ui.detailsView.width()-4,(screensize.width()-self.ui.detailsView.width()-4)*2//3)
    self.ui.actionOpen.triggered.connect(self.actionOpen)
    self.ui.actionSync.triggered.connect(self.actionSync)
    self.ui.tableWidget.itemEntered.connect(self.actionTooltip)
    self.ui.tableWidget.currentItemChanged.connect(self.actionCurrentItemChanged)
    self.ui.tableWidget.installEventFilter(self)
    self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    self.ui.radioButton_all.setChecked(True)
    self.scene = QGraphicsScene()
    self.ui.graphicsView.setScene(self.scene)
    self.images = {}
    self.cacheDirectory = Path(user_cache_dir(self.windowTitle()))
    self.cacheDirectory.mkdir(parents=True, exist_ok=True)
    try:
      self.config = json.load(open(Path(__file__).parent / 'config.json'))
    except:
      self.config = {}
      self.config["S3BucketName"] = "uploadsla"
      self.config["username"] = os.getlogin()
      self.config["lastUsedLocalDir"] = os.getcwd()
      self.config["lastUsedS3Dir"] = config["S3BucketName"] + ":/"
      self.config["shortNames"] = {}

  def mousePressEvent(self, e):
    self.statusBar().showMessage(f"mousePressEvent {e.position()}")

  def eventFilter(self, watched, event, /):
    if watched == self.ui.tableWidget:
      if event.type() == QEvent.Type.KeyPress:
        statusColumn=5
        startrailColumn=7
        currentRow = self.ui.tableWidget.currentRow()
        imagesIndex=f'{self.ui.tableWidget.item(currentRow,1).text()} {self.ui.tableWidget.item(currentRow,2).text()} {self.ui.tableWidget.item(currentRow,0).text()}'
        if QKeyEvent(event).key() == Qt.Key.Key_Up:
          if self.ui.tableWidget.item(currentRow,statusColumn).text() != '✘':
            self.ui.tableWidget.item(currentRow,statusColumn).setText('✔')
            self.images[imagesIndex]['status']='✔'
        if QKeyEvent(event).key() == Qt.Key.Key_Down:
          if self.ui.tableWidget.item(currentRow,statusColumn).text() != '✘':
            self.ui.tableWidget.item(currentRow,statusColumn).setText('✔')
            self.images[imagesIndex]['status'] = '✔'
        if QKeyEvent(event).key() == Qt.Key.Key_X:
          if self.ui.tableWidget.item(currentRow,statusColumn).text() != '✘':
            self.ui.tableWidget.item(currentRow,statusColumn).setText('✘')
            self.images[imagesIndex]['status']='✘'
            for column in range(self.ui.tableWidget.columnCount()):
              self.ui.tableWidget.item(currentRow,column).setBackground(QColor(255,0,0,127))
          else:
            self.ui.tableWidget.item(currentRow,statusColumn).setText('✔')
            self.images[imagesIndex]['status'] = '✔'
            for column in range(self.ui.tableWidget.columnCount()):
              self.ui.tableWidget.item(currentRow, column).setBackground(QColor(255, 255, 255, 255))
          return True
        if QKeyEvent(event).key() == Qt.Key.Key_T:
          if self.ui.tableWidget.item(currentRow, startrailColumn).text() != '✔':
            self.ui.tableWidget.item(currentRow, startrailColumn).setText('✔')
            self.images[imagesIndex]['startrails'] = '✔'
          else:
            self.ui.tableWidget.item(currentRow, startrailColumn).setText('')
            self.images[imagesIndex]['startrails'] = ''
          return True
    # pass the event on to the parent class
    return QMainWindow.eventFilter(self, watched, event)

  def listener(self, mydict):
    pass

  def actionSync(self):
    rclone.sync('uploadla:upload/speedy/_cache', self.cacheDirectory, listener=self.listener)
    pass

  def actionOpen(self):
    userName=get_username()
    self.workingDirectory = Path(QFileDialog.getExistingDirectory(self, "Select Directory"),dir=Path(self.config['lastUsedLocalDir']))
    if self.workingDirectory != '.':
      self.config["lastUsedLocalDir"] = self.workingDirectory
      self.images.clear()
      for file in self.workingDirectory.rglob("*.fits"):
        if 'site-packages' in str(file.parent):
          continue
        image = {}
        image['fullPath'] = file
        header = fits.getheader(image['fullPath'])
        image['filter'] = header['FILTER']
        if "BAYERPAT" in header:
          image['bayerpat'] = header['BAYERPAT']
        image['object'] = header['OBJECT']
        image['telescope'] = header['TELESCOP']
        if image['telescope'] in self.config["shortNames"]:
          image['telescope'] = self.config["shortNames"][image['telescope']]
        image['date'] = header['DATE-LOC'].split('.')[0].replace('T', ' ')
        image['pierside'] = header['PIERSIDE']
        if 'ROTATOR' in header:
          image['rotator'] = str(int(header['ROTATOR']))
        else:
          image['rotator'] = 'not found'
        image['status'] = ""
        image['statusothers'] = ""
        image['startrails'] = ""
        index = f"{image['object']} {image['filter']} {image['date']}"
        image['cachePath'] = (self.cacheDirectory / image['telescope'] / image['object'] / file.name).with_suffix('.jpg')
        image['detailsCachePath'] = image['cachePath'].with_stem(image['cachePath'].stem + '-aberration')
        if not image['cachePath'].parent.exists():
          image['cachePath'].parent.mkdir(parents=True, exist_ok=True)
        if not image['cachePath'].exists():
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
          im.save(image['cachePath'])

        if not image['detailsCachePath'].exists():
          im = Image.open(image['cachePath'])
          new_im = Image.new('RGB', (600, 600))
          im_crop = im.crop((0, 0, 200, 200))
          new_im.paste(im_crop, (0, 0))
          im_crop = im.crop((im.width / 2 - 100, 0, im.width / 2 + 100, 200))
          new_im.paste(im_crop, (200, 0))
          im_crop = im.crop((im.width - 200, 0, im.width, 200))
          new_im.paste(im_crop, (400, 0))

          im_crop = im.crop((0, im.height / 2 - 100, 200, im.height / 2 + 100))
          new_im.paste(im_crop, (0, 200))
          im_crop = im.crop((im.width / 2 - 100, im.height / 2 - 100, im.width / 2 + 100, im.height / 2 + 100))
          new_im.paste(im_crop, (200, 200))
          im_crop = im.crop((im.width - 200, im.height / 2 - 100, im.width, im.height / 2 + 100))
          new_im.paste(im_crop, (400, 200))

          im_crop = im.crop((0, im.height - 200, 200, im.height))
          new_im.paste(im_crop, (0, 400))
          im_crop = im.crop((im.width / 2 - 100, im.height - 200, im.width / 2 + 100, im.height))
          new_im.paste(im_crop, (200, 400))
          im_crop = im.crop((im.width - 200, im.height - 200, im.width, im.height))
          new_im.paste(im_crop, (400, 400))

          new_im.save(image['detailsCachePath'])
        self.images[index] = image
      self.images = dict(sorted(self.images.items()))
      if len(self.images) > 0:
        statusfile = self.images[next(iter(self.images))]['cachePath'].parent / f'status-{userName}.json'
        if statusfile.exists():
          statusImages = json.load(open(statusfile))
          for index in statusImages:
            if index in self.images:
              self.images[index]['status'] = statusImages[index]['status']
              self.images[index]['startrails'] = statusImages[index]['startrails']

      self.ui.tableWidget.clearContents()
      self.ui.tableWidget.setRowCount(len(self.images))
      position=0
      for index,image in self.images.items():
        self.ui.tableWidget.setItem(position, 0, QTableWidgetItem(image['date']))
        self.ui.tableWidget.setItem(position, 1, QTableWidgetItem(image['object']))
        self.ui.tableWidget.setItem(position, 2, QTableWidgetItem(image['filter']))
        self.ui.tableWidget.setItem(position, 3, QTableWidgetItem(image['rotator']))
        self.ui.tableWidget.setItem(position, 4, QTableWidgetItem(image['pierside']))
        self.ui.tableWidget.setItem(position, 5, QTableWidgetItem(image['status']))
        self.ui.tableWidget.setItem(position, 6, QTableWidgetItem(image['statusothers']))
        self.ui.tableWidget.setItem(position, 7, QTableWidgetItem(image['startrails']))
        if image['status'] == '✘':
          for column in range(self.ui.tableWidget.columnCount()):
            self.ui.tableWidget.item(position, column).setBackground(QColor(255, 0, 0, 127))
        position += 1

  def closeEvent(self, event):
    if len(self.images) > 0:
      userName = get_username()
      statusfile=self.images[next(iter(self.images))]['cachePath'].parent / f'status-{userName}.json'
      cleanImages=self.images.copy()
      for index,image in cleanImages.items():
        image.pop('fullPath')
        image.pop('cachePath')
        image.pop('detailsCachePath')
        image.pop('telescope')
        image.pop('object')
        image.pop('filter')
        image.pop('date')
        image.pop('pierside')
        image.pop('rotator')
        cleanImages[index]=image

      with statusfile.open("w", encoding="UTF-8") as target:
        json.dump(cleanImages, target, indent=2)
    event.accept()

  def actionCurrentItemChanged(self, item: QTableWidgetItem):
    if item is None:
      return
    idx=self.ui.tableWidget.item(item.row(), 1).text()+" "+self.ui.tableWidget.item(item.row(), 2).text()+" "+self.ui.tableWidget.item(item.row(), 0).text()
    self.image = QImage(self.images[idx]['cachePath'])
    scene = QGraphicsScene(0, 0, self.ui.graphicsView.size().width(), self.ui.graphicsView.size().height())
    pixmap = QPixmap(self.image)
    pixmapitem = scene.addPixmap(pixmap)
    pixmapitem.setScale(self.ui.graphicsView.size().width() / pixmap.width())
    pixmapitem.setPos(0, 0)
    self.ui.graphicsView.setScene(scene)
    self.ui.graphicsView.setRenderHint(QPainter.Antialiasing)
    self.ui.graphicsView.show()

    detailImagePath = self.images[idx]['cachePath'].with_stem(
      self.images[idx]['cachePath'].stem + '-aberration')
    self.aberrationimage = QImage(
      self.images[idx]['cachePath'].with_stem(self.images[idx]['cachePath'].stem + '-aberration'))
    scene = QGraphicsScene(0, 0, self.ui.detailsView.size().width(), self.ui.detailsView.size().height())
    pixmap = QPixmap(self.aberrationimage)
    pixmapitem = scene.addPixmap(pixmap)
    pixmapitem.setScale(self.ui.detailsView.size().width() / pixmap.width())
    pixmapitem.setPos(0, 0)
    self.ui.detailsView.setScene(scene)
    self.ui.detailsView.setRenderHint(QPainter.Antialiasing)
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