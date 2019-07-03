TIMEOUT /T 3

rmdir /s/q dist

rmdir /s/q build

del printer_repeater.spec

pyinstaller -F -n printer_repeater -y WinService.py -i ciin_logo.ico --upx-dir upx394a

copy printer_repeater.cfg dist

copy start.bat dist

copy stop.bat dist

del printer_repeater.spec

pyinstaller -F -n print_test -y -i ciin_logo.ico printer_test.py

copy print_test.temp dist
del print_test.spec

