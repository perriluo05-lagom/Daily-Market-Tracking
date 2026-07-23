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

def get_current_user():
    try:
        import getpass
        return getpass.getuser()
    except:
        return os.environ.get('USERNAME', 'unknown')

def get_user_domain():
    return os.environ.get('USERDOMAIN', '.')

def create_task():
    task_name = "DailyMarketTracking"
    batch_path = r"d:\Trae CN\program\daily_market_tracking\run_daily.bat"
    working_dir = r"d:\Trae CN\program\daily_market_tracking"
    
    user_domain = get_user_domain()
    user_name = get_current_user()
    
    print("=" * 60)
    print("Configure Daily Market Tracking Task Scheduler")
    print("=" * 60)
    
    print(f"\nTask Name: {task_name}")
    print(f"Batch Path: {batch_path}")
    print(f"Working Directory: {working_dir}")
    print(f"Running Account: {user_domain}\\{user_name}")
    
    print("\n1. Deleting old tasks...")
    for name in [task_name, "每日市场跟踪"]:
        delete_cmd = ["schtasks", "/delete", "/tn", name, "/f"]
        result = subprocess.run(delete_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Deleted task: {name}")
        else:
            print(f"   ⚠️ Task not found or delete failed: {name}")
    
    print("\n2. Creating task (daily 18:00)...")
    create_cmd = [
        "schtasks", "/create", "/tn", task_name,
        "/tr", f'"{batch_path}"',
        "/sc", "daily",
        "/st", "18:00",
        "/ru", f"{user_domain}\\{user_name}",
        "/rl", "highest",
        "/f"
    ]
    result = subprocess.run(create_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✅ Task created successfully")
    else:
        print(f"   ❌ Task creation failed: {result.stderr.strip()}")
        return
    
    print("\n3. Setting task properties (run whether user is logged on or not)...")
    change_cmd = ["schtasks", "/change", "/tn", task_name, "/it", "false", "/f"]
    result = subprocess.run(change_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✅ Properties set successfully")
    else:
        print(f"   ❌ Property setting failed: {result.stderr.strip()}")
    
    print("\n4. Verifying task configuration...")
    result = subprocess.run(["schtasks", "/query", "/tn", task_name, "/v"], capture_output=True, text=True)
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')
        for line in lines[:25]:
            print(line)
    else:
        print(f"   ❌ Verification failed: {result.stderr.strip()}")
    
    print("\n" + "=" * 60)
    print("Task Scheduler configuration completed!")
    print(f"Next run time: Daily at 18:00")
    print(f"Running program: run_daily.bat")
    print(f"Running account: {user_domain}\\{user_name}")
    print(f"Working directory: {working_dir}")
    print("=" * 60)
    
    input("\nPress any key to exit...")

if __name__ == "__main__":
    if not is_admin():
        print("Requesting administrator privileges...")
        run_as_admin()
    else:
        create_task()