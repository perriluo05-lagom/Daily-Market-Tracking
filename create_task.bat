@echo off
chcp 65001 >nul

set "TASK_NAME=每日市场跟踪"
set "PYTHON_PATH=C:\Users\19655\AppData\Local\Programs\Python\Python312\python.exe"
set "SCRIPT_PATH=d:\Trae CN\program\daily_market_tracking\main.py"

for /f "tokens=1-3 delims=/ " %%a in ("%date%") do (
    set "YEAR=%%c"
    set "MONTH=%%a"
    set "DAY=%%b"
)

if /i "%MONTH:~0,1%"=="0" set "MONTH=%MONTH:~1%"
if /i "%DAY:~0,1%"=="0" set "DAY=%DAY:~1%"

set "START_DATE=%YEAR%/%MONTH%/%DAY%"

echo 正在创建任务计划...
schtasks /create ^
    /tn "%TASK_NAME%" ^
    /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" ^
    /sc daily ^
    /st 18:00 ^
    /sd %START_DATE% ^
    /ru "%USERDOMAIN%\%USERNAME%" ^
    /f

if %errorlevel% equ 0 (
    echo 任务创建成功！
    schtasks /query /tn "%TASK_NAME%"
) else (
    echo 任务创建失败！
    pause
)