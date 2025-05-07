import os
import subprocess
import sys

def get_git_status():
    """获取 Git 状态"""
    try:
        # 切换到项目目录
        os.chdir('C:/cygwin64/home/frank/pyautogui')
        
        # 获取 Git 状态
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        print("Git 状态:")
        print(result.stdout)
        
        # 获取修改的文件列表
        result = subprocess.run(['git', 'diff', '--name-status'], capture_output=True, text=True)
        print("\n修改的文件列表:")
        print(result.stdout)
        
        # 获取未跟踪的文件列表
        result = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], capture_output=True, text=True)
        print("\n未跟踪的文件列表:")
        print(result.stdout)
        
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    get_git_status()
