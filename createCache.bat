C:
cd "%HOMEDRIVE%%HOMEPATH%\devel\pyBlink\"
call  "%HOMEDRIVE%%HOMEPATH%\devel\pyBlink\venv\Scripts\activate.bat"
set PYTHONPATH=%PYTHONPATH%;"%HOMEDRIVE%%HOMEPATH%\devel\pyBlink\"
mkdir "%HOMEDRIVE%%HOMEPATH%\devel\pyBlink\Temp" 2>NUL
python.exe  "%HOMEDRIVE%%HOMEPATH%\devel\pyBlink\createCache.py"