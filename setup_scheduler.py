import subprocess
import sys
import ctypes

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

def create_task():
    task_name = "每日市场跟踪"
    python_exe = r"C:\Users\19655\AppData\Local\Programs\Python\Python312\python.exe"
    script_path = r"d:\Trae CN\program\daily_market_tracking\main.py"
    
    action = f'"{python_exe}" "{script_path}"'
    
    result = subprocess.run(
        ["schtasks", "/create", "/tn", task_name, "/tr", action, 
         "/sc", "daily", "/st", "18:00", "/f"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ 任务创建成功！")
        print("\n任务详情：")
        subprocess.run(["schtasks", "/query", "/tn", task_name])
    else:
        print("❌ 任务创建失败！")
        print(f"错误信息: {result.stderr}")
    
    input("\n按任意键退出...")

if __name__ == "__main__":
    if not is_admin():
        print("正在请求管理员权限...")
        run_as_admin()
    else:
        create_task()