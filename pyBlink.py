import sys

from PySide6.QtCore import QObject, QSize, QEvent, Qt, QAbstractTableModel
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QGraphicsScene
from PIL import Image
from PySide6.QtGui import QPixmap, QImage, QPainter, QKeyEvent
from ui_mainwindow import Ui_MainWindow
from pathlib import Path
from astropy.io import fits
from platformdirs import user_cache_dir
import cv2
from auto_stretch import apply_stretch
from rclone_python import rclone


class TableModel(QAbstractTableModel):
  def __init__(self, data):
    super().__init__()
    self._data = data

  def data(self, index, role):
    if role == Qt.DisplayRole:
      return self._data[index.row()][index.column()]

  def rowCount(self, index):
    return len(self._data)

  def columnCount(self, index):
    return len(self._data[0])


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.actionOpen.triggered.connect(self.actionOpen)
    self.ui.actionSync.triggered.connect(self.actionSync)
    self.ui.tableWidget.itemEntered.connect(self.actionTooltip)
    self.ui.tableWidget.currentItemChanged.connect(self.actionCurrentItemChanged)
    self.ui.tableWidget.installEventFilter(self)
    self.ui.radioButton_all.setChecked(True)
    self.scene = QGraphicsScene()
    self.ui.graphicsView.setScene(self.scene)
    self.images = {}
    self.cacheDirectory = Path(user_cache_dir(self.windowTitle()))
    self.cacheDirectory.mkdir(parents=True, exist_ok=True)
    self.workingDirectory = Path('.')

  def mousePressEvent(self, e):
    self.statusBar().showMessage(f"mousePressEvent {e.position()}")

  def eventFilter(self, watched, event, /):
    if watched == self.ui.tableWidget:
      if event.type() == QEvent.Type.KeyPress:
        if QKeyEvent(event).key() == Qt.Key.Key_Right:
          currentRow = self.ui.tableWidget.currentRow()
          #self.ui.droppedWidget.addItem(self.ui.listWidget.item(currentRow).text())
          #self.ui.listWidget.takeItem(currentRow)
          return True
    # pass the event on to the parent class
    return QMainWindow.eventFilter(self, watched, event)

  def listener(self, mydict):
    pass

  def actionSync(self):
    rclone.sync('uploadla:upload/speedy/_cache', self.cacheDirectory, listener=self.listener)
    pass

  def actionOpen(self):
    self.workingDirectory = Path(QFileDialog.getExistingDirectory(self, "Select Directory"))
    if self.workingDirectory != '.':
      self.ui.tableWidget.clear()
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
        image['date'] = header['DATE-LOC'].split('.')[0].replace('T', ' ')
        image['pierside'] = header['PIERSIDE']
        index = f"{image['object']} {image['filter']} {image['date']}"
        image['cachePath'] = (self.cacheDirectory / file.name).with_suffix('.jpg')
        image['detailsCachePath'] = image['cachePath'].with_stem(image['cachePath'].stem + '-aberration')
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
      #self.ui.tableWidget.setModel(self.ui.tableWidget)

  def actionCurrentItemChanged(self, item: QListWidgetItem):
    if item is None:
      return
    self.image = QImage(self.images[item.text()]['cachePath'])
    scene = QGraphicsScene(0, 0, self.ui.graphicsView.size().width(), self.ui.graphicsView.size().height())
    pixmap = QPixmap(self.image)
    pixmapitem = scene.addPixmap(pixmap)
    pixmapitem.setScale(self.ui.graphicsView.size().width() / pixmap.width())
    pixmapitem.setPos(0, 0)
    self.ui.graphicsView.setScene(scene)
    self.ui.graphicsView.setRenderHint(QPainter.Antialiasing)
    self.ui.graphicsView.show()

    detailImagePath = self.images[item.text()]['cachePath'].with_stem(
      self.images[item.text()]['cachePath'].stem + '-aberration')
    self.aberrationimage = QImage(
      self.images[item.text()]['cachePath'].with_stem(self.images[item.text()]['cachePath'].stem + '-aberration'))
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
