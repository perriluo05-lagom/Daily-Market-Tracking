@echo off
chcp 65001 >nul
cd /d "d:\Trae CN\program\daily_market_tracking"
python -c "import json; f='data/subscription_status.json'; d=json.load(open(f,'r',encoding='utf-8')); d['active']=False; json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=2); print('✓ 已成功取消订阅！'); print('✓ 未来将不再收到每日市场分析报告邮件'); print(''); print('如需恢复订阅，请双击运行 resubscribe.bat')"
pause
