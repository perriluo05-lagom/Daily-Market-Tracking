@echo off
title Configure Daily Market Tracking Task Scheduler

if not "%1"=="admin" (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~dp0%~n0%~x0' -ArgumentList 'admin' -Verb RunAs"
    exit /b
)

echo ================================================
echo Configure Daily Market Tracking Task Scheduler
echo ================================================
echo.

echo 1. Deleting old task...
schtasks /delete /tn "DailyMarketTracking" /f
schtasks /delete /tn "每日市场跟踪" /f
echo.

echo 2. Creating new task (daily 18:00, highest privileges)...
schtasks /create /tn "DailyMarketTracking" ^
    /tr "\"d:\Trae CN\program\daily_market_tracking\run_daily.bat\"" ^
    /sc daily ^
    /st 18:00 ^
    /ru "%USERDOMAIN%\%USERNAME%" ^
    /rl highest ^
    /f

if %errorlevel% equ 0 (
    echo    Success!
) else (
    echo    Failed! Error code: %errorlevel%
    pause
    exit /b
)

echo.
echo 3. Setting task properties (run whether user is logged on or not)...
schtasks /change /tn "DailyMarketTracking" ^
    /it false ^
    /f

echo.
echo 4. Verifying task configuration...
schtasks /query /tn "DailyMarketTracking" /v
echo.

echo ================================================
echo Task Scheduler configuration completed!
echo Next run time: Daily at 18:00
echo Running program: run_daily.bat
echo Running account: %USERDOMAIN%\%USERNAME%
echo ================================================
pause