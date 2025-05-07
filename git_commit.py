import os
import subprocess
import sys

def git_commit_and_push():
    """提交并推送修改"""
    try:
        # 切换到项目目录
        os.chdir('C:/cygwin64/home/frank/pyautogui')
        
        # 添加所有修改的文件
        subprocess.run(['git', 'add', '.'], check=True)
        print("已添加所有修改的文件")
        
        # 提交修改
        commit_message = "敏感信息保护调整：只将高敏感度信息移至环境变量，保留中低敏感度信息在代码中"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print(f"已提交修改: {commit_message}")
        
        # 推送到远程仓库
        subprocess.run(['git', 'push', 'origin', 'refactor'], check=True)
        print("已推送到远程仓库")
        
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    git_commit_and_push()
