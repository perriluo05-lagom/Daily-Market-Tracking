import subprocess
import sys
import ctypes
import os
import datetime

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    script = sys.argv[0]
    params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}" {params}', None, 1
    )
    sys.exit()

def setup_scheduler():
    task_name = "每日市场跟踪"
    python_exe = r"C:\Users\19655\AppData\Local\Programs\Python\Python312\python.exe"
    script_path = r"d:\Trae CN\program\daily_market_tracking\main.py"
    working_dir = r"d:\Trae CN\program\daily_market_tracking"
    
    print("=" * 60)
    print("正在配置每日市场跟踪任务计划")
    print("=" * 60)
    
    print(f"\n任务名称: {task_name}")
    print(f"Python路径: {python_exe}")
    print(f"脚本路径: {script_path}")
    print(f"工作目录: {working_dir}")
    
    delete_cmd = ["schtasks", "/delete", "/tn", task_name, "/f"]
    print("\n1. 删除旧任务...")
    result = subprocess.run(delete_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✅ 旧任务删除成功")
    else:
        print(f"   ⚠️ 删除旧任务失败(可能不存在): {result.stderr.strip()}")
    
    action = f'"{python_exe}" "{script_path}"'
    
    create_cmd = [
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", action,
        "/sc", "daily",
        "/st", "18:00",
        "/ru", "SYSTEM",
        "/rp", "",
        "/f",
        "/v1"
    ]
    
    print("\n2. 创建新任务(使用SYSTEM账户)...")
    result = subprocess.run(create_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✅ 任务创建成功")
    else:
        print(f"   ❌ 任务创建失败: {result.stderr.strip()}")
        return
    
    print("\n3. 设置工作目录...")
    xml_content = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>{datetime.now().isoformat()}</Date>
    <Author>Daily Market Tracking</Author>
    <Description>每日市场跟踪自动运行任务</Description>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>{datetime.now().strftime("%Y-%m-%d")}T18:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>P3D</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{python_exe}</Command>
      <Arguments>"{script_path}"</Arguments>
      <WorkingDirectory>{working_dir}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>'''
    
    import datetime
    temp_xml = os.path.join(working_dir, "task_temp.xml")
    with open(temp_xml, 'w', encoding='utf-16') as f:
        f.write(xml_content)
    
    delete_cmd = ["schtasks", "/delete", "/tn", task_name, "/f"]
    subprocess.run(delete_cmd, capture_output=True)
    
    import_cmd = ["schtasks", "/create", "/tn", task_name, "/xml", temp_xml, "/f"]
    result = subprocess.run(import_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✅ 使用XML配置任务成功")
        os.remove(temp_xml)
    else:
        print(f"   ❌ XML导入失败: {result.stderr.strip()}")
        os.remove(temp_xml)
        return
    
    print("\n4. 验证任务配置...")
    result = subprocess.run(["schtasks", "/query", "/tn", task_name, "/v"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"错误: {result.stderr}")
    
    print("\n" + "=" * 60)
    print("任务计划配置完成！")
    print("下次运行时间: 每日18:00")
    print("运行账户: SYSTEM (无论用户是否登录都会运行)")
    print("工作目录: " + working_dir)
    print("=" * 60)
    
    input("\n按任意键退出...")

if __name__ == "__main__":
    if not is_admin():
        print("正在请求管理员权限...")
        run_as_admin()
    else:
        setup_scheduler()