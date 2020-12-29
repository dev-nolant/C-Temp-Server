@echo off

if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)

@echo off
pushd %~dp0
python loc_server.py
popd
pause