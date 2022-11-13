@echo off
@title Doctorate - Frida Hook

call env\scripts\activate.bat
echo Wait till frida-server is started.
echo Then press enter to continue... 
pause >nul
py fridahook.py
