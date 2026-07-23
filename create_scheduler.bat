@echo off
schtasks /create /tn "每日市场跟踪" /tr "\"C:\Users\19655\AppData\Local\Programs\Python\Python312\python.exe\" \"d:\Trae CN\program\daily_market_tracking\main.py\"" /sc daily /st 18:00 /f
if %errorlevel% equ 0 (
    echo 任务创建成功！
    schtasks /query /tn "每日市场跟踪"
) else (
    echo 任务创建失败！错误码: %errorlevel%
)
pause