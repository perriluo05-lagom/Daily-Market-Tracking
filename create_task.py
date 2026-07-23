import subprocess
import datetime
import ctypes
import sys

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

def create_scheduled_task():
    task_name = "每日市场跟踪"
    python_path = r"C:\Users\19655\AppData\Local\Programs\Python\Python312\python.exe"
    script_path = r"d:\Trae CN\program\daily_market_tracking\main.py"
    
    today = datetime.date.today()
    start_date = today.strftime("%Y/%m/%d")
    
    command = [
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", f'"{python_path}" "{script_path}"',
        "/sc", "daily",
        "/st", "18:00",
        "/sd", start_date,
        "/f"
    ]
    
    print(f"正在创建任务计划...")
    print(f"命令: {' '.join(command)}")
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("任务创建成功！")
        print("输出:", result.stdout)
        print("\n任务状态:")
        subprocess.run(["schtasks", "/query", "/tn", task_name])
        print("\n按任意键退出...")
        input()
    else:
        print("任务创建失败！")
        print("错误:", result.stderr)
        print("\n按任意键退出...")
        input()

if __name__ == "__main__":
    if not is_admin():
        print("正在请求管理员权限...")
        run_as_admin()
    else:
        create_scheduled_task()