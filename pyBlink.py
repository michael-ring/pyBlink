import os
import sys

from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QGraphicsScene, QTableWidgetItem, \
  QAbstractItemView, QHeaderView
from PySide6.QtGui import QPixmap, QImage, QPainter, QKeyEvent, QColor

from localSyncDialog import localSyncDialog
from ui_mainwindow import Ui_MainWindow
from pathlib import Path
import json
import psutil
from remoteProjectSyncDialog import remoteProjectSyncDialog
from syncDialog import syncDialog
from imageCache import imageCache


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    screensize = self.screen().size()
    self.resize(screensize.width(), screensize.height())
    newHeightOfGraphicsView = (screensize.width() - self.ui.detailsView.width() - 4) * 2 // 3
    if newHeightOfGraphicsView > screensize.height() - 300:
      self.ui.graphicsView.setMinimumSize((screensize.height() - 300) * 3 // 2, screensize.height() - 300)
      self.ui.graphicsView.setMaximumSize((screensize.height() - 300) * 3 // 2, screensize.height() - 300)
    else:
      self.ui.graphicsView.setMinimumSize(screensize.width() - self.ui.detailsView.width() - 4,
                                          (screensize.width() - self.ui.detailsView.width() - 4) * 2 // 3)
    self.ui.actionOpen.triggered.connect(self.actionOpen)
    self.ui.actionSync.triggered.connect(self.actionSync)
    self.ui.actionRemoteOpen.triggered.connect(self.actionRemoteOpen)
    self.ui.actionDelete.triggered.connect(self.actionDelete)
    self.ui.tableWidget.currentItemChanged.connect(self.actionCurrentItemChanged)
    self.ui.tableWidget.installEventFilter(self)
    self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    self.ui.radioButton_all.setChecked(True)
    self.ui.radioButton_discarded.toggled.connect(self.radioButtonCheck)
    self.ui.radioButton_new.toggled.connect(self.radioButtonCheck)
    self.ui.radioButton_notdiscardedandnew.toggled.connect(self.radioButtonCheck)
    self.ui.radioButton_discardedbyothers.toggled.connect(self.radioButtonCheck)
    self.ui.radioButton_startrails.toggled.connect(self.radioButtonCheck)
    self.ui.radioButton_nostartrails.toggled.connect(self.radioButtonCheck)

    self.scene = QGraphicsScene()
    self.ui.graphicsView.setScene(self.scene)
    self.dateColumn = 0
    self.targetColumn = 2
    self.filterColumn = 3
    self.statusColumn = 9
    self.startrailColumn = 11

    try:
      self.config = json.load(open(Path(__file__).parent / 'config.json'))
    except:
      self.config = {}
      self.config["S3CachePath"] = "cache:cache/"
      self.config["lastUsedLocalDir"] = str(os.getcwd())
      self.config["shortNames"] = {
        "Lacerta FN1506c": "speedy",
        "Lacerta 250": "slt",
        "Askar ACL200": "vst",
        "Askar ACL200 F4": "vst"
      }

    self.imageCache = imageCache(self.windowTitle())
    self.imageCache.setTelescopeShortNames(self.config["shortNames"])
    self.imageCache.cacheUpdated.connect(self.onUpdateImageCache)

  def onUpdateImageCache(self):
    self.populateTableWidget(loadData=True)

  def populateTableWidget(self, loadData=False):
    print(f"populating tableWidget")
    if len(self.imageCache.images) != self.ui.tableWidget.rowCount():
      loadData = True
    if loadData:
      self.ui.tableWidget.clearContents()
      self.ui.tableWidget.setRowCount(len(self.imageCache.images))
      position = 0
      for index, image in self.imageCache.images.items():
        self.ui.tableWidget.setItem(position, 0, QTableWidgetItem(image['date']))
        self.ui.tableWidget.setItem(position, 1, QTableWidgetItem("{:.2f}".format(image['exposure'])))
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
        if image['statusothers'] == '✘' and image['status'] != '✘':
          for column in range(self.ui.tableWidget.columnCount()):
            self.ui.tableWidget.item(position, column).setBackground(QColor(255, 127, 127, 127))
        position += 1

    self.ui.tableWidget.setUpdatesEnabled(False)
    position = 0
    for index, image in self.imageCache.images.items():
      showItem = False
      if self.ui.radioButton_all.isChecked():
        showItem = True
      if self.ui.radioButton_new.isChecked():
        if image['status'] != '✘' and image['status'] != '✔':
          showItem = True
      if self.ui.radioButton_discarded.isChecked():
        if image['status'] == '✘':
          showItem = True
      if self.ui.radioButton_notdiscardedandnew.isChecked():
        if image['status'] != '✘':
          showItem = True
      if self.ui.radioButton_discardedbyothers.isChecked():
        if image['statusothers'] == '✘':
          showItem = True
      if self.ui.radioButton_startrails.isChecked():
        if image['startrails'] == '✔':
          showItem = True
      if self.ui.radioButton_nostartrails.isChecked():
        if image['startrails'] != '✔':
          showItem = True
      if not image['visible']:
        showItem = False
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
        imagesIndex = f'{self.ui.tableWidget.item(currentRow, self.targetColumn).text()} {self.ui.tableWidget.item(currentRow, self.filterColumn).text()} {self.ui.tableWidget.item(currentRow, self.dateColumn).text()}'
        if QKeyEvent(event).key() == Qt.Key.Key_Up:
          if self.ui.tableWidget.item(currentRow, self.statusColumn).text() != '✘':
            self.ui.tableWidget.item(currentRow, self.statusColumn).setText('✔')
            self.imageCache.images[imagesIndex]['status'] = '✔'
        if QKeyEvent(event).key() == Qt.Key.Key_Down:
          if self.ui.tableWidget.item(currentRow, self.statusColumn).text() != '✘':
            self.ui.tableWidget.item(currentRow, self.statusColumn).setText('✔')
            self.imageCache.images[imagesIndex]['status'] = '✔'
        if QKeyEvent(event).key() == Qt.Key.Key_X:
          if self.ui.tableWidget.item(currentRow, self.statusColumn).text() != '✘':
            self.ui.tableWidget.item(currentRow, self.statusColumn).setText('✘')
            self.imageCache.images[imagesIndex]['status'] = '✘'
            for column in range(self.ui.tableWidget.columnCount()):
              self.ui.tableWidget.item(currentRow, column).setBackground(QColor(255, 0, 0, 127))
          else:
            self.ui.tableWidget.item(currentRow, self.statusColumn).setText('✔')
            self.imageCache.images[imagesIndex]['status'] = '✔'
            for column in range(self.ui.tableWidget.columnCount()):
              self.ui.tableWidget.item(currentRow, column).setBackground(QColor(255, 255, 255, 255))
          return True
        if QKeyEvent(event).key() == Qt.Key.Key_T:
          if self.ui.tableWidget.item(currentRow, self.startrailColumn).text() != '✔':
            self.ui.tableWidget.item(currentRow, self.startrailColumn).setText('✔')
            self.imageCache.images[imagesIndex]['startrails'] = '✔'
          else:
            self.ui.tableWidget.item(currentRow, self.startrailColumn).setText('')
            self.imageCache.images[imagesIndex]['startrails'] = ''
          return True
    # pass the event on to the parent class
    return QMainWindow.eventFilter(self, watched, event)

  def radioButtonCheck(self):
    self.populateTableWidget()

  def actionDelete(self):
    # self.imageCache.persistStatus()
    for index, image in self.imageCache.images.copy().items():
      if image['status'] == '✘':
        self.imageCache.images[index]['visible'] = False
        if Path(image['fitspath']).exists() and Path(image['fitspath']).is_file():
          Path(image['fitspath']).unlink()
          # if Path(image['cachepath']).exists() and Path(image['cachepath']).is_file():
          #  Path(image['cachepath']).unlink()
          # self.imageCache.images.pop(index)
    self.populateTableWidget()

  def actionSync(self):
    self.imageCache.persistStatus()
    sd = syncDialog(self)
    sd.setS3CachePath(self.config['S3CachePath'])
    sd.setSpecificSyncDirectory(None)
    sd.setImageCache(self.imageCache)
    sd.open()

  def actionOpen(self):
    self.imageCache.persistStatus()
    self.workingDirectory = Path(
      QFileDialog.getExistingDirectory(self, "Select Directory", dir=str(self.config['lastUsedLocalDir'])))
    if self.workingDirectory != Path('.'):
      self.config["lastUsedLocalDir"] = str(self.workingDirectory)
      print(f"Working Directory: {self.workingDirectory}")
      lsd = localSyncDialog(self)
      lsd.setWorkingDirectory(self.workingDirectory)
      lsd.setImageCache(self.imageCache)
      lsd.setTelescopeShortNames(self.config['shortNames'])
      lsd.open()
      pass

  def actionRemoteOpen(self):
    self.imageCache.persistStatus()
    rpsd = remoteProjectSyncDialog(self)
    rpsd.setS3CachePath(self.config['S3CachePath'])
    rpsd.setImageCache(self.imageCache)
    rpsd.open()

  def closeEvent(self, event):
    self.imageCache.persistStatus()
    with open(Path(__file__).parent / 'config.json', 'w', encoding='utf-8') as file:
      json.dump(self.config, file, ensure_ascii=False, indent=2)
    event.accept()

  def actionCurrentItemChanged(self, item: QTableWidgetItem):
    if item is None:
      return
    idx = self.ui.tableWidget.item(item.row(), 2).text() + " " + self.ui.tableWidget.item(item.row(),
                                                                                          3).text() + " " + self.ui.tableWidget.item(
      item.row(), 0).text()
    self.image = QImage(self.imageCache.images[idx]['cachepath'])
    scene = QGraphicsScene(0, 0, self.ui.graphicsView.size().width(), self.ui.graphicsView.size().height())
    pixmap = QPixmap(self.image)
    pixmapitem = scene.addPixmap(pixmap)
    pixmapitem.setScale(self.ui.graphicsView.size().width() / pixmap.width())
    pixmapitem.setPos(0, 0)
    self.ui.graphicsView.setScene(scene)
    self.ui.graphicsView.setRenderHint(QPainter.RenderHint.Antialiasing)
    self.ui.graphicsView.show()

    scene = QGraphicsScene(0, 0, self.ui.detailsView.size().width(), self.ui.detailsView.size().width())
    segmentedImage = QImage(self.ui.detailsView.size().width(), self.ui.detailsView.size().width(),
                            QImage.Format.Format_RGB32)
    sourceWidth = self.ui.detailsView.size().width()
    sourceHeight = self.ui.detailsView.size().height()
    segmentWidth = self.ui.detailsView.size().width() // 3
    segmentHeight = self.ui.detailsView.size().height() // 3
    Painter = QPainter()
    Painter.begin(segmentedImage)
    Painter.drawImage(0, 0, self.image.copy(0, 0, segmentWidth, segmentHeight))
    Painter.drawImage(segmentWidth, 0,
                      self.image.copy(sourceWidth // 2 - segmentWidth // 2, 0, segmentWidth, segmentHeight))
    Painter.drawImage(2 * segmentWidth, 0, self.image.copy(sourceWidth - segmentWidth, 0, segmentWidth, segmentHeight))

    Painter.drawImage(0, segmentHeight,
                      self.image.copy(0, sourceHeight // 2 - segmentHeight // 2, segmentWidth, segmentHeight))
    Painter.drawImage(segmentWidth, segmentHeight,
                      self.image.copy(sourceWidth // 2 - segmentWidth // 2, sourceHeight // 2 - segmentHeight // 2,
                                      segmentWidth, segmentHeight))
    Painter.drawImage(2 * segmentWidth, segmentHeight,
                      self.image.copy(sourceWidth - segmentWidth, sourceHeight // 2 - segmentHeight // 2, segmentWidth,
                                      segmentHeight))

    Painter.drawImage(0, segmentHeight * 2,
                      self.image.copy(0, sourceHeight - segmentHeight, segmentWidth, segmentHeight))
    Painter.drawImage(segmentWidth, segmentHeight * 2,
                      self.image.copy(sourceWidth // 2 - segmentWidth // 2, sourceHeight - segmentHeight, segmentWidth,
                                      segmentHeight))
    Painter.drawImage(2 * segmentWidth, segmentHeight * 2,
                      self.image.copy(sourceWidth - segmentWidth, sourceHeight - segmentHeight, segmentWidth,
                                      segmentHeight))

    Painter.end()
    pixmap2 = QPixmap.fromImage(segmentedImage)
    pixmapitem2 = scene.addPixmap(pixmap2)
    pixmapitem2.setScale(1)
    pixmapitem2.setPos(0, 0)
    self.ui.detailsView.setScene(scene)
    self.ui.detailsView.setRenderHint(QPainter.RenderHint.Antialiasing)
    self.ui.detailsView.show()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
