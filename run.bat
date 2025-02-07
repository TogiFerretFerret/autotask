@echo off
setlocal

REM Download and extract portable Python
echo Downloading portable Python...
curl -LO https://www.python.org/ftp/python/3.13.2/python-3.13.2-embed-amd64.zip
mkdir python
tar -xf python-3.13.2-embed-amd64.zip -C python

REM Add Python to PATH
set PATH=%CD%\python;%CD%\python\scripts;%PATH%
REM Install pip
echo Installing pip...
curl -LO https://bootstrap.pypa.io/get-pip.py
python\python.exe get-pip.py
del %CD%\python\none.save
ren %CD%\python\python313._pth none.save
python\python.exe -m pip install pip --upgrade
REM Install packages...
echo Installing required packages...
pip install opencv-python mss pyaudio pyautogui pyperclip google-genai pillow

REM Open two command windows to run lms.py and run-uv.py
echo Starting program...
$env:GOOGLE_API_KEY="AIzaSyCiS5-KzHJE0F82WCVLmLB06A3KkJRmT_s"
python\python.exe main.py
powershell Start-Sleep -m 500
echo All tasks completed.
endlocal
pause
