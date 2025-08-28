import cv2
from PIL import Image

from pathlib import Path

from PySide6 import QtCore
from auto_stretch import apply_stretch
from platformdirs import user_cache_dir
import json
import psutil
from astropy.io import fits
from PySide6.QtCore import Signal


class imageCache(QtCore.QObject):
  progressUpdate = Signal(int)
  fileProgressUpdate = Signal(str, int,int)
  cacheUpdated = Signal()

  def __init__(self, applicationName):
    super().__init__()
    self.cacheDirectory = Path(user_cache_dir(applicationName))
    self.cacheDirectory.mkdir(parents=True, exist_ok=True)
    self.images = {}
    self.telescopeShortNames = {}
    self.fileProgressSlot = 0

  def setTelescopeShortNames(self, telescopeShortNames):
    self.telescopeShortNames = telescopeShortNames

  def getCacheDirectory(self):
    return self.cacheDirectory

  def populateCacheFromFitsDirectory(self, directory):
    self.images.clear()
    imageMetaData = {}
    for file in Path(directory).rglob("ImageMetaData*.json"):
      imds = json.load(open(file))
      for imd in imds:
        imageMetaData[Path(imd['FilePath']).name] = imd
    cachePathFound = False
    cachePath = None
    doneCount = 0
    files = list(directory.rglob("*.fits"))
    for file in files:
      if 'site-packages' in str(file.parent):
        continue
      if not cachePathFound:
        print(f"Loading Fits Data from File {file} to detect cachedir")
        header = fits.getheader(file)
        telescope = header['TELESCOP']
        if telescope in self.telescopeShortNames:
          telescope = self.telescopeShortNames[telescope]
        cachePath = self.cacheDirectory / telescope / header['OBJECT']
        cachePathFound = True
      self.progressUpdate.emit(doneCount)
      if (cachePath / file.name).with_suffix('.jpg').exists():
        image = self.extractExifTags((cachePath / file.name).with_suffix('.jpg'),file)
        if image is not None:
          index = f"{image['object']} {image['filter']} {image['date']}"
          self.images[index] = image
        else:
          (cachePath / file.name).with_suffix('.jpg').unlink()
      if not (cachePath / file.name).with_suffix('.jpg').exists():
        self.addImageToCache(file)
      doneCount += 1
    self.images = dict(sorted(self.images.items()))
    self.injectStatus()
    self.cacheUpdated.emit()

  def addImageToCache(self,filename):
    self.fileProgressUpdate.emit(str(filename.name),self.fileProgressSlot,0)
    image = self.extractFitsHeaders(filename)
    self.fileProgressUpdate.emit(str(filename.name),self.fileProgressSlot,10)
    if image is not None:
      index = f"{image['object']} {image['filter']} {image['date']}"
      print(f"Creating {image['cachepath']}")
      data = fits.getdata(image['fitspath'], ext=0)
      self.fileProgressUpdate.emit(str(filename.name), self.fileProgressSlot, 20)

      if 'bayerpat' in image:
        debayered = cv2.cvtColor(data, cv2.COLOR_BayerBGGR2BGR)
        gray_image = cv2.cvtColor(debayered, cv2.COLOR_BGR2GRAY)
        normalized = gray_image
        cv2.normalize(debayered, normalized, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
      else:
        normalized = data
        cv2.normalize(data, normalized, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
      self.fileProgressUpdate.emit(str(filename.name), self.fileProgressSlot, 40)

      stretched = apply_stretch(normalized, target_bkg=0.15)
      self.fileProgressUpdate.emit(str(filename.name), self.fileProgressSlot, 60)

      im = Image.fromarray(stretched * 255)
      im = im.convert('RGB')
      im = im.resize((im.width // 2, im.height // 2))

      self.fileProgressUpdate.emit(str(filename.name), self.fileProgressSlot, 80)

      if image['pierside'] == 'East':
        im = im.rotate(180)

      exif = im.getexif()
      persistedTags = {}
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
      im.save(image['cachepath'], exif=exif, quality="web_low")
      self.images[index] = image
      self.fileProgressUpdate.emit(str(filename.name),self.fileProgressSlot,100)
      self.fileProgressSlot += 1
      if self.fileProgressSlot == 4:
        self.fileProgressSlot = 0

  def extractFitsHeaders(self,filename):
    print(f"Loading Fits Data from File: {filename}")
    header = fits.getheader(filename)

    try:
      image={}
      image['status'] = ""
      image['statusothers'] = ""
      image['startrails'] = ""
      image['adumean'] = 0
      image['detectedstars'] = 0
      image['fwhm'] = 0
      image['filter'] = header['FILTER']
      if "BAYERPAT" in header:
        image['bayerpat'] = header['BAYERPAT']
      image['object'] = header['OBJECT']
      image['telescope'] = header['TELESCOP']
      image['exposure'] = header['EXPOSURE']
      if image['telescope'] in self.telescopeShortNames:
        image['telescope'] = self.telescopeShortNames[image['telescope']]
      image['date'] = header['DATE-LOC'].split('.')[0].replace('T', ' ')
      image['pierside'] = header['PIERSIDE']
      if 'ROTATOR' in header:
        image['rotator'] = str(int(header['ROTATOR']))
      else:
        image['rotator'] = 'not found'
      image['cachepath'] = (self.cacheDirectory / image['telescope'] / image['object'] / filename.name).with_suffix(
        '.jpg')
      if not image['cachepath'].parent.exists():
        image['cachepath'].parent.mkdir(parents=True, exist_ok=True)

      image['fitspath'] = filename
      image['visible'] = True
      print(f"Fits Reading done")
      return image
    except KeyError:
      print(f"Fits Reading failed")
      return None


  def extractExifTags(self,filename,fitsFilename=None):
    im = Image.open(filename)
    image = {}
    exif = im.getexif()
    try:
      savedTags = json.loads(exif[0x9286])
      image['status'] = ""
      image['statusothers'] = ""
      image['startrails'] = ""
      image['adumean'] = 0
      image['fwhm'] = 0
      image['detectedstars'] = 0

      image['date'] = savedTags['date']
      image['object'] = savedTags['object']
      image['telescope'] = savedTags['telescope']
      image['filter'] = savedTags['filter']
      image['pierside'] = savedTags['pierside']
      image['rotator'] = savedTags['rotator']
      image['exposure'] = savedTags['exposure']
      image['cachepath'] = filename
      if fitsFilename is None:
        image['fitspath'] = Path(filename).with_suffix('.fits')
      else:
        image['fitspath'] = Path(fitsFilename)
      image['visible'] = True

      if 'adumean' in savedTags:
        image['adumean'] = savedTags['adumean']
      if 'fwhm' in savedTags:
        image['fwhm'] = savedTags['fwhm']
      if 'detectedstars' in savedTags:
        image['detectedstars'] = savedTags['detectedstars']
      return image
    except KeyError:
      print(f"Fits data in Exif Header missing/incomplete, rebuild...")
      return None

  def populateFromCachedImages(self, extraPath):
    files = list((self.cacheDirectory / extraPath).rglob("*.jpg"))
    for file in files:
      image=self.extractExifTags(file)
      if image is not None:
        index = f"{image['object']} {image['filter']} {image['date']}"
        self.images[index] = image
    self.images = dict(sorted(self.images.items()))
    self.injectStatus()
    self.cacheUpdated.emit()

  def persistStatus(self):
    if len(self.images) > 0:
      firstIndex = next(iter(self.images))
      statusfile=self.images[firstIndex]['cachepath'].parent / f'status-{psutil.Process().username()}.json'
      imagesStatus = {}
      for index, image in self.images.items():
        imagesStatus[index] = {'status': image['status'], 'statusothers': image['statusothers'],
                               'startrails': image['startrails']}

      with statusfile.open("w", encoding="UTF-8") as target:
        json.dump(imagesStatus, target, indent=2)

  def injectStatus(self):
    if len(self.images) > 0:
      firstIndex = next(iter(self.images))
      statusfile=self.images[firstIndex]['cachepath'].parent / f'status-{psutil.Process().username()}.json'
      if statusfile.exists():
        print(f"Loading status from {statusfile}")
        statusImages = json.load(open(statusfile))

        for index in statusImages:
           if index in self.images:
            self.images[index]['status'] = statusImages[index]['status']
            self.images[index]['statusothers'] = statusImages[index]['statusothers']
            self.images[index]['startrails'] = statusImages[index]['startrails']


