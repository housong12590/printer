sc stop PrinterRepeater

sc delete PrinterRepeater

TIMEOUT /T 3

rmdir /s/q dist

rmdir /s/q build

del PrinterRepeater.spec

pyinstaller -F -y --add-data "printer.cfg;." PrinterRepeater.py --upx-dir upx394a

copy printer.cfg dist

dist\PrinterRepeater.exe install

sc start PrinterRepeater