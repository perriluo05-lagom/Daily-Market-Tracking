@echo off
cd /d "d:\Trae CN\program\daily_market_tracking"
set NO_PROXY=*
echo Task started at %date% %time% >> run_daily.log
"C:\Users\19655\AppData\Local\Programs\Python\Python312\python.exe" "main.py" >> run_daily.log 2>&1
echo Task finished at %date% %time% >> run_daily.log