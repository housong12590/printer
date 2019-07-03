TIMEOUT /T 3

rmdir /s/q dist

rmdir /s/q build

del printer_repeater.spec

pyinstaller -F -n printer_repeater -y WinService.py --upx-dir upx394a

copy printer_repeater.cfg dist

copy start.bat dist

copy stop.bat dist

del printer_repeater.spec

