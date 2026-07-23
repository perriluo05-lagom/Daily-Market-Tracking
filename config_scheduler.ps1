#Requires -RunAsAdministrator

<#
.SYNOPSIS
配置每日市场跟踪任务计划

.DESCRIPTION
创建Windows任务计划，每天18:00自动运行市场跟踪程序
#>

$taskName = "DailyMarketTracking"
$batchPath = "d:\Trae CN\program\daily_market_tracking\run_daily.bat"
$workingDir = "d:\Trae CN\program\daily_market_tracking"
$userDomain = $env:USERDOMAIN
$userName = $env:USERNAME

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "配置每日市场跟踪任务计划" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "任务名称: $taskName"
Write-Host "批处理路径: $batchPath"
Write-Host "工作目录: $workingDir"
Write-Host "运行账户: $userDomain\$userName"
Write-Host ""

# 1. 删除旧任务
Write-Host "1. 删除旧任务..." -ForegroundColor Yellow
$oldTasks = @($taskName, "每日市场跟踪")
foreach ($name in $oldTasks) {
    schtasks /delete /tn $name /f 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ 删除成功: $name" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ 任务不存在或删除失败: $name" -ForegroundColor Gray
    }
}
Write-Host ""

# 2. 创建新任务
Write-Host "2. 创建新任务(每日18:00，最高权限)..." -ForegroundColor Yellow
$result = schtasks /create /tn $taskName `
    /tr "`"$batchPath`"" `
    /sc daily `
    /st 18:00 `
    /ru "$userDomain\$userName" `
    /rl highest `
    /f

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ 任务创建成功" -ForegroundColor Green
} else {
    Write-Host "   ❌ 任务创建失败" -ForegroundColor Red
    Write-Host "   错误信息: $result" -ForegroundColor Red
    Write-Host ""
    Write-Host "请手动打开任务计划程序创建任务:" -ForegroundColor Yellow
    Write-Host "1. 搜索 '任务计划程序' 并打开" -ForegroundColor Gray
    Write-Host "2. 点击 '创建基本任务'" -ForegroundColor Gray
    Write-Host "3. 名称: DailyMarketTracking" -ForegroundColor Gray
    Write-Host "4. 触发器: 每天 18:00" -ForegroundColor Gray
    Write-Host "5. 操作: 启动程序" -ForegroundColor Gray
    Write-Host "6. 程序或脚本: $batchPath" -ForegroundColor Gray
    Write-Host "7. 勾选 '不管用户是否登录都要运行'" -ForegroundColor Gray
    Write-Host "8. 勾选 '使用最高权限运行'" -ForegroundColor Gray
    Read-Host "按回车退出"
    exit 1
}
Write-Host ""

# 3. 设置任务属性(无论用户是否登录都运行)
Write-Host "3. 设置任务属性(无论用户是否登录都运行)..." -ForegroundColor Yellow
schtasks /change /tn $taskName /it false /f
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ 属性设置成功" -ForegroundColor Green
} else {
    Write-Host "   ❌ 属性设置失败" -ForegroundColor Red
}
Write-Host ""

# 4. 验证任务配置
Write-Host "4. 验证任务配置..." -ForegroundColor Yellow
schtasks /query /tn $taskName /v
Write-Host ""

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "任务计划配置完成！" -ForegroundColor Green
Write-Host "下次运行时间: 每日18:00" -ForegroundColor Gray
Write-Host "运行程序: run_daily.bat" -ForegroundColor Gray
Write-Host "运行账户: $userDomain\$userName" -ForegroundColor Gray
Write-Host "工作目录: $workingDir" -ForegroundColor Gray
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "按回车退出"