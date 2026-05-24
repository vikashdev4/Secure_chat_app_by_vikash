@echo off
start cmd /k python server.py
timeout /t 2
start cmd /k python gui_client.py