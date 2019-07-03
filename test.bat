
del printer_test.spec
pyinstaller -F -n printer_test -y printer_test.py

copy print_test.temp dist
del printer_test.spec