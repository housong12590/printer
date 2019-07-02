nssm.exe install PrinterRepeater PrinterRepeater.exe
nssm.exe set PrinterRepeater AppDirectory %cd%/
nssm.exe set PrinterRepeater AppStdout %cd%/app_stdout.log
nssm.exe set PrinterRepeater AppStderr %cd%/app_stderr.log
nssm.exe start PrinterRepeater