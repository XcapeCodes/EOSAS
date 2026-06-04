@echo off

cd /d C:\Users\ojoch\EOSAS

call venv\Scripts\activate

start "EOSAS Flask Server" cmd /k "cd /d C:\Users\ojoch\EOSAS && call venv\Scripts\activate && python server.py"

timeout /t 6

start "" http://127.0.0.1:5000

pause