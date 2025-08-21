 #!/bin/sh
 ./.venv/bin/pyside6-uic -g python mainWindow.ui >ui_mainwindow.py
 ./.venv/bin/pyside6-uic -g python syncDialog.ui >ui_syncdialog.py
  ./.venv/bin/pyside6-uic -g python localSyncDialog.ui >ui_localsyncdialog.py