from PySide6 import QtGui
from PySide6.QtWidgets import QDialog, QDialogButtonBox

from imageCache import imageCache
from ui_deletedialog import Ui_deleteDialog
from pathlib import Path
from rclone_python import rclone, utils


class deleteDialog(Ui_deleteDialog, QDialog):
  def cleanupDialog(self):
    self.progressBar_overall.setValue(0)
    self.label_current.setText("")
    self.label_done.setVisible(False)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setupUi(self)
    self.cleanupDialog()
    self.imageCache = None

  def setImageCache(self, imageCache):
    self.imageCache = imageCache

  def open(self, /):
    super().open()
    discarded_images = [image for image in self.imageCache.images.values() if image['status'] == '✘']
    total = len(discarded_images)
    if total > 0:
      first_image = discarded_images[0]
      cachepath = Path(first_image['cachepath']).relative_to(self.imageCache.getCacheDirectory())
      telescope = cachepath.parts[0]
      target = cachepath.parts[1]
      images_path = self.imageCache.dataSources[telescope]['ImagesPath']
      remote_path = f"{images_path}/{target}"
      try:
        self.label_current.setText(f"Loading List of Target Files from remote")
        QtGui.QGuiApplication.processEvents()
        QtGui.QGuiApplication.processEvents()
        file_list,_ = rclone.utils.run_rclone_cmd(f'lsf "{remote_path}"',['--max-depth 2','--files-only','--include "*fits*"'])
        file_list=file_list.split('\n')
        self.progressBar_overall.setValue(0)
      except utils.RcloneException as e:
        print(e.error_msg)
        file_list = []
    self.progressBar_overall.setMaximum(total)
    self.progressBar_overall.setValue(0)
    deleted = 0
    for image in discarded_images:
      for targetImage in file_list:
        targetImageName = Path(targetImage).name
        if Path(targetImageName).suffix == '.7z':
          targetImageName = Path(targetImage).stem

        if targetImageName == Path(image['fitspath']).name:
          self.label_current.setText(f"Deleting {Path(image['fitspath']).name}")
          print(f"Deleting {Path(image['fitspath']).name}")
          QtGui.QGuiApplication.processEvents()
          QtGui.QGuiApplication.processEvents()
          try:
            #pass
            rclone.delete(f"{images_path}/{targetImage}")
          except utils.RcloneException as e:
            print(e.error_msg)
          self.progressBar_overall.setValue(0)
      if Path(image['fitspath']).exists() and Path(image['fitspath']).is_file():
        Path(image['fitspath']).unlink()
      image['visible'] = False
      deleted += 1
      self.progressBar_overall.setValue(deleted)
    self.cleanupDialog()
    self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
    self.label_done.setVisible(True)
