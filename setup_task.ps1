$taskName = "每日市场跟踪"
$pythonPath = "C:\Users\19655\AppData\Local\Programs\Python\Python312\python.exe"
$scriptPath = "d:\Trae CN\program\daily_market_tracking\main.py"
$workingDir = "d:\Trae CN\program\daily_market_tracking"

Write-Host "================================================"
Write-Host "配置每日市场跟踪任务计划"
Write-Host "================================================"
Write-Host ""

Write-Host "1. 删除旧任务..."
schtasks /delete /tn $taskName /f
Write-Host ""

Write-Host "2. 创建新任务..."
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$scriptPath`"" -WorkingDirectory $workingDir

$trigger = New-ScheduledTaskTrigger -Daily -At 18:00

$principal = New-ScheduledTaskPrincipal -UserId "19655" -LogonType Interactive

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

$task = New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -Settings $settings

Register-ScheduledTask -TaskName $taskName -InputObject $task -Force

Write-Host ""
Write-Host "3. 验证任务配置..."
schtasks /query /tn $taskName /v

Write-Host ""
Write-Host "================================================"
Write-Host "任务计划配置完成！"
Write-Host "下次运行时间: 每日18:00"
Write-Host "运行账户: 当前用户"
Write-Host "工作目录: $workingDir"
Write-Host "================================================"

Read-Host "按回车键退出"