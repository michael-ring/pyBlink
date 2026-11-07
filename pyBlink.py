import math
import os
import shutil
import sys
import tempfile

from PySide6.QtCore import QEvent, Qt, QProcess
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QGraphicsScene, QTableWidgetItem, \
  QAbstractItemView, QHeaderView
from PySide6.QtGui import QPixmap, QImage, QPainter, QKeyEvent, QColor

from localSyncDialog import localSyncDialog
from ui_mainwindow import Ui_MainWindow
from pathlib import Path
import json
import psutil
from astropy.io import fits
from remoteProjectSyncDialog import remoteProjectSyncDialog
from syncDialog import syncDialog
from imageCache import imageCache
from deleteDialog import deleteDialog


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    #screensize = self.screen().size() # that does not work on Windows, the pyblink windo is bigger than the screen
    screensize = self.screen().availableGeometry().size()
    #self.resize(screensize.width(), screensize.height())
    self.setGeometry(self.screen().availableGeometry())
    newHeightOfGraphicsView = (screensize.width() - self.ui.detailsView.width() - 8) * 2 // 3
    if newHeightOfGraphicsView > screensize.height() - 300:
      self.ui.graphicsView.setMinimumSize((screensize.height() - 300) * 3 // 2, screensize.height() - 300)
      self.ui.graphicsView.setMaximumSize((screensize.height() - 300) * 3 // 2, screensize.height() - 300)
    else:
      self.ui.graphicsView.setMinimumSize(screensize.width() - self.ui.detailsView.width() - 8,
                                          (screensize.width() - self.ui.detailsView.width() - 8) * 2 // 3)
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
    self.imageOneToOne = False
    self.imageFocus = None
    self.ui.graphicsView.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    self.ui.graphicsView.viewport().installEventFilter(self)
    # Disable scrollbars on the graphics view (they remain off even when scene is changed)
    self.ui.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.ui.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    # Also disable scrollbars for the details view since we set scenes there as well
    self.ui.detailsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.ui.detailsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.dateColumn = 0
    self.targetColumn = 2
    self.filterColumn = 3
    self.statusColumn = 9
    self.startrailColumn = 11

    try:
      self.config = json.load(open(Path(__file__).parent / 'config.json'))
    except:
      self.config = {}
      self.config["datasources"] = {}
      self.config["datasources"]["slt"] = {
        "name":"slt",
        "enabled":True,
        "ImagesPath":"upload:/upload",
        "CachePath":"cache:/cache"
      }
      self.config["lastUsedLocalDir"] = str(os.getcwd())

    self.imageCache = imageCache(self.windowTitle())
    self.imageCache.setDataSources(self.config["datasources"])
    self.imageCache.cacheUpdated.connect(self.onUpdateImageCache)
    remoteProjectSyncDialog.clearSessionCache()

  def onUpdateImageCache(self):
    self.populateTableWidget(loadData=True)

  def populateOverviewTableWidget(self):
    print(f"populating overviewTableWidget")
    data={}
    for index, image in self.imageCache.images.items():
      key=f"{image['filter']} ({image['exposure']}s)"
      if not key in data:
        if image['status'] == '✘':
          data[key] = 0
        else:
          data[key] = 1
      else:
        if image['status'] != '✘':
          data[key] += 1
    self.ui.overviewTableWidget.clearContents()
    self.ui.overviewTableWidget.setRowCount(len(data))
    for index, (key, value) in enumerate(data.items()):
      self.ui.overviewTableWidget.setItem(index, 0, QTableWidgetItem(key))
      self.ui.overviewTableWidget.setItem(index, 1, QTableWidgetItem(str(value)))


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
    self.populateOverviewTableWidget()

  def mousePressEvent(self, e):
    self.statusBar().showMessage(f"mousePressEvent {e.position()}")

  def eventFilter(self, watched, event, /):
    if watched == self.ui.graphicsView.viewport() and event.type() == QEvent.Type.MouseButtonPress:
      if event.button() == Qt.MouseButton.LeftButton and hasattr(self, 'image'):
        point = self.ui.graphicsView.mapToScene(event.position().toPoint())
        if 0 <= point.x() < self.image.width() and 0 <= point.y() < self.image.height():
          if self.imageOneToOne:
            self.imageOneToOne = False
          else:
            self.imageFocus = (point.x(), point.y())
            self.imageOneToOne = True
          self.renderMainImage()
          self.ui.tableWidget.setFocus(Qt.FocusReason.OtherFocusReason)
          return True
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
          self.populateOverviewTableWidget()
          return True
        if QKeyEvent(event).key() == Qt.Key.Key_T:
          if self.ui.tableWidget.item(currentRow, self.startrailColumn).text() != '✔':
            self.ui.tableWidget.item(currentRow, self.startrailColumn).setText('✔')
            self.imageCache.images[imagesIndex]['startrails'] = '✔'
          else:
            self.ui.tableWidget.item(currentRow, self.startrailColumn).setText('')
            self.imageCache.images[imagesIndex]['startrails'] = ''
          return True
        if QKeyEvent(event).key() == Qt.Key.Key_S:
          self.plateSolve(imagesIndex)
          return True
    # pass the event on to the parent class
    return QMainWindow.eventFilter(self, watched, event)

  def findAstap(self):
    candidates = [self.config.get("astapPath"), shutil.which("astap"), shutil.which("astap_cli"),
                  "/Applications/ASTAP.app/Contents/MacOS/astap",
                  "C:\\Program Files\\astap\\astap.exe"]
    for candidate in candidates:
      if candidate and Path(candidate).is_file():
        return candidate
    return None

  def plateSolve(self, imagesIndex):
    if getattr(self, "astapProcess", None) is not None:
      self.statusBar().showMessage("Plate solving already running...")
      return
    astap = self.findAstap()
    if astap is None:
      self.statusBar().showMessage("ASTAP not found, set 'astapPath' in config.json")
      return
    image = self.imageCache.images[imagesIndex]
    source = Path(image['fitspath'])
    if not source.exists():
      self.statusBar().showMessage(f"Plate solving needs the FITS file, not found: {source}")
      return
    self.solveDir = tempfile.mkdtemp(prefix="pyBlink-astap-")
    self.solveBase = str(Path(self.solveDir) / "solve")
    self.astapProcess = QProcess(self)
    self.astapProcess.finished.connect(self.onPlateSolveFinished)
    self.astapProcess.errorOccurred.connect(self.onPlateSolveFinished)
    self.statusBar().showMessage(f"Plate solving {source.name} ...")
    self.astapProcess.start(astap, ["-f", str(source), "-wcs", "-o", self.solveBase])

  def onPlateSolveFinished(self, *args):
    process = self.astapProcess
    if process is None:
      return
    self.astapProcess = None
    wcsFile = Path(self.solveBase + ".wcs")
    try:
      if not wcsFile.exists():
        self.statusBar().showMessage("Plate solving failed: no solution found")
        return
      header = fits.Header.fromfile(str(wcsFile), sep='', endcard=False, padding=False)
      ra = header['CRVAL1']
      dec = header['CRVAL2']
      if 'CROTA2' in header:
        rotation = header['CROTA2']
      else:
        rotation = math.degrees(math.atan2(-header['CD1_2'], header['CD2_2']))
      if rotation < 0:
        rotation += 180
      scale = math.hypot(header['CD1_1'], header['CD2_1']) * 3600
      raH = ra / 15
      raM = (raH - int(raH)) * 60
      decAbs = abs(dec)
      decM = (decAbs - int(decAbs)) * 60
      self.statusBar().showMessage(
        f"Solved: RA {int(raH):02d}h {int(raM):02d}m {(raM - int(raM)) * 60:04.1f}s ({ra:.4f}°)  "
        f"Dec {'-' if dec < 0 else '+'}{int(decAbs):02d}° {int(decM):02d}' {(decM - int(decM)) * 60:04.1f}\" ({dec:.4f}°)  "
        f"Rotation {rotation:.2f}°  Scale {scale:.2f}\"/px")
    except Exception as e:
      self.statusBar().showMessage(f"Plate solving failed: {e}")
    finally:
      shutil.rmtree(self.solveDir, ignore_errors=True)

  def radioButtonCheck(self):
    self.populateTableWidget()

  def updateOverviewTableWithRankings(self, image_key, table_row):
    """Calculate rankings for the selected image and update overview table."""
    if image_key not in self.imageCache.images:
      return

    current_image = self.imageCache.images[image_key]
    current_filter = current_image['filter']
    current_exposure = current_image['exposure']
    current_fwhm = current_image['fwhm']
    current_detected_stars = current_image['detectedstars']
    current_mean = current_image['adumean']
    # Collect all images with same filter and exposure
    matching_images = []
    stars_candidateCount = 0
    fwhm_candidateCount = 0
    mean_candidateCount = 0
    stars_rank = 0
    fwhm_rank = 0
    mean_rank = 0
    for img_idx, img_data in self.imageCache.images.items():
      if img_data['filter'] == current_filter and img_data['exposure'] == current_exposure:
        if img_data['status'] != '✘':  # Only consider images that are not discarded
          if img_data['detectedstars'] > 0:
              stars_candidateCount += 1
              if img_data['detectedstars'] < current_detected_stars:
                stars_rank += 1
          if img_data['fwhm'] > 0:
              fwhm_candidateCount += 1
              if img_data['fwhm'] < current_fwhm:
                fwhm_rank += 1
          if img_data['adumean'] > 0:
              mean_candidateCount += 1
              if img_data['adumean'] < current_mean:
                mean_rank += 1

    # Update overview table with rankings
    # Find the row in overview table corresponding to this filter
    filter_text = current_filter
    for row in range(self.ui.overviewTableWidget.rowCount()):
      cell = self.ui.overviewTableWidget.item(row, 1)  # #Subs column (index 1, Filter is hidden at 0)
      if cell is None:
        continue
      # Check if this row's filter matches
      filter_cell = self.ui.overviewTableWidget.item(row, 0)
      if filter_cell and filter_cell.text() == filter_text + f" ({current_exposure:.1f}s)":
        # Update ranking columns (indices 2, 3, 4)
        self.ui.overviewTableWidget.setItem(row, 2, QTableWidgetItem(f"{stars_rank}/{stars_candidateCount}"))
        self.ui.overviewTableWidget.setItem(row, 3, QTableWidgetItem(f"{mean_candidateCount-mean_rank}/{mean_candidateCount}"))
        self.ui.overviewTableWidget.setItem(row, 4, QTableWidgetItem(f"{fwhm_candidateCount-fwhm_rank}/{fwhm_candidateCount}"))
      else:
        self.ui.overviewTableWidget.setItem(row, 2, QTableWidgetItem(str("")))
        self.ui.overviewTableWidget.setItem(row, 3, QTableWidgetItem(str("")))
        self.ui.overviewTableWidget.setItem(row, 4, QTableWidgetItem(str("")))


  def actionDelete(self):
    dd = deleteDialog(self)
    dd.setImageCache(self.imageCache)
    dd.open()
    self.populateTableWidget()

  def actionSync(self):
    self.imageCache.persistStatus()
    sd = syncDialog(self)
    #sd.setS3CachePath(self.config['S3CachePath'])
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
      #lsd.setTelescopeShortNames(self.config['shortNames'])
      lsd.open()
      pass

  def actionRemoteOpen(self):
    self.imageCache.persistStatus()
    rpsd = remoteProjectSyncDialog(self)
    #rpsd.setS3CachePath(self.config['S3CachePath'])
    #rpsd.setS3ImagesPath(self.config['S3ImagesPath'])
    rpsd.setImageCache(self.imageCache)
    rpsd.open()

  def closeEvent(self, event):
    self.imageCache.persistStatus()
    with open(Path(__file__).parent / 'config.json', 'w', encoding='utf-8') as file:
      json.dump(self.config, file, ensure_ascii=False, indent=2)
    event.accept()

  def resizeEvent(self, event):
    super().resizeEvent(event)
    if hasattr(self, 'image') and not self.image.isNull():
      self.renderMainImage()

  def renderMainImage(self):
    pixmap = QPixmap.fromImage(self.image)
    if pixmap.isNull():
      return

    self.scene.clear()
    self.scene.addPixmap(pixmap)
    self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
    viewport = self.ui.graphicsView.viewport().size()
    if viewport.width() <= 0 or viewport.height() <= 0:
      return

    self.ui.graphicsView.resetTransform()
    if not self.imageOneToOne:
      scale = min(viewport.width() / pixmap.width(), viewport.height() / pixmap.height())
      self.ui.graphicsView.scale(scale, scale)

    if self.imageFocus is None:
      self.imageFocus = (pixmap.width() / 2, pixmap.height() / 2)

    if self.imageOneToOne:
      focusX, focusY = self.imageFocus
      halfWidth = viewport.width() / 2
      halfHeight = viewport.height() / 2
      if 2 * halfWidth >= pixmap.width():
        focusX = pixmap.width() / 2
      else:
        focusX = min(max(focusX, halfWidth), pixmap.width() - halfWidth)
      if 2 * halfHeight >= pixmap.height():
        focusY = pixmap.height() / 2
      else:
        focusY = min(max(focusY, halfHeight), pixmap.height() - halfHeight)
      self.imageFocus = (focusX, focusY)
      self.ui.graphicsView.centerOn(focusX, focusY)
    else:
      self.ui.graphicsView.centerOn(pixmap.width() / 2, pixmap.height() / 2)
    self.ui.graphicsView.setRenderHint(QPainter.RenderHint.Antialiasing)
    self.ui.graphicsView.show()

  def actionCurrentItemChanged(self, item: QTableWidgetItem):
    if item is None:
      return
    idx = self.ui.tableWidget.item(item.row(), 2).text() + " " + self.ui.tableWidget.item(item.row(),
                                                                                          3).text() + " " + self.ui.tableWidget.item(
      item.row(), 0).text()
    # Calculate and display rankings in overview table
    self.updateOverviewTableWithRankings(idx, item.row())

    self.image = QImage(self.imageCache.images[idx]['cachepath'])
    self.renderMainImage()

    scene = QGraphicsScene(0, 0, self.ui.detailsView.size().width(), self.ui.detailsView.size().width())
    segmentedImage = QImage(self.ui.detailsView.size().width(), self.ui.detailsView.size().width(),
                            QImage.Format.Format_RGB32)
    sourceWidth = self.image.width()
    sourceHeight = self.image.height()
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
