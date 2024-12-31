import logging
import sqlite3
import schedule
import time
import threading
from modules.notification_module import send_wechat_message_with_tasks, send_wecom_message_with_tasks, update_task_status
from modules.log_config import setup_logging

setup_logging()  # 设置日志

task_lock = threading.Lock()
is_task_running = False  # 标志位，表示任务是否正在运行

def execute_task(task):
    global is_task_running
    with task_lock:  # 确保在执行任务时获得锁
        is_task_running = True  # 设置任务正在运行
        logging.info(f"Executing task ID: {task['id']} of type: {task['task_type']}")  # 记录任务执行
        try:
            if task['task_type'] == 'send_wechat_message':
                send_wechat_message_with_tasks(task)
            elif task['task_type'] == 'send_wecom_message':
                send_wecom_message_with_tasks(task)
            update_task_status(task['id'], 'completed')
            logging.info(f"Task ID: {task['id']} completed successfully.")  # 记录任务完成
        except Exception as e:
            logging.error(f"Error executing task ID: {task['id']}: {e}")  # 记录错误
        finally:
            is_task_running = False  # 任务完成，重置标志位

def check_tasks():
    global is_task_running
    logging.info("Checking for pending tasks...")  # 记录检查任务的开始
    if not is_task_running:  # 只有在没有任务运行时才检查任务
        conn = sqlite3.connect('tasks.db')
        conn.row_factory = sqlite3.Row  # 设置行工厂为 Row，以便返回字典
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE status='pending'")
        tasks = cursor.fetchall()
        for task in tasks:
            execute_task(task)
        conn.close()
    logging.info("Task check completed.")  # 记录检查任务的结束

def start():
    from modules.config import TASK_CHECK_INTERVAL
    schedule.every(TASK_CHECK_INTERVAL).seconds.do(check_tasks)  # 使用配置的间隔时间检查任务
    logging.info("Task scheduler started.")  # 记录启动

    while True:
        schedule.run_pending()
        time.sleep(1)