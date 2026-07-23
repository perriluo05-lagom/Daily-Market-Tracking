@echo off
echo ================================================
echo 配置每日市场跟踪任务计划
echo ================================================
echo.

if not "%1"=="admin" (
    echo 正在请求管理员权限...
    powershell -Command "Start-Process cmd -ArgumentList '/c %0 admin' -Verb RunAs"
    exit /b
)

echo 1. 删除旧任务...
schtasks /delete /tn "每日市场跟踪" /f
echo.

echo 2. 创建新任务(使用SYSTEM账户，无论是否登录都运行)...
schtasks /create /tn "每日市场跟踪" ^
    /tr "\"C:\Users\19655\AppData\Local\Programs\Python\Python312\python.exe\" \"d:\Trae CN\program\daily_market_tracking\main.py\"" ^
    /sc daily ^
    /st 18:00 ^
    /ru SYSTEM ^
    /f

if %errorlevel% equ 0 (
    echo    成功！
) else (
    echo    失败！错误码: %errorlevel%
    pause
    exit /b
)

echo.
echo 3. 验证任务配置...
schtasks /query /tn "每日市场跟踪" /v
echo.

echo ================================================
echo 任务计划配置完成！
echo 下次运行时间: 每日18:00
echo 运行账户: SYSTEM (无论用户是否登录都会运行)
echo ================================================
pause