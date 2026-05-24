@echo off
cd /d %~dp0

start cmd /k python server.py
timeout /t 2 >nul
start cmd /k python client.py
