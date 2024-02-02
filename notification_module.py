# notification_module.py

import csv
import logging
import pyautogui
import pyperclip
import time
from log_config import setup_logging

# 配置日志
setup_logging()
# 使用专门的发送消息日志记录器
send_logger = logging.getLogger('sendLogger')

def send_wechat_message(user, message):
    """模拟发送微信消息给指定的用户（测试模式）"""
    logging.info(f"[TEST MODE] Preparing to open WeChat PC application to send message to {user}...")

    # 模拟打开微信PC应用的步骤
    # pyautogui.hotkey('ctrl', 'alt', 'w')
    # time.sleep(1)

    send_logger.info(f"[TEST MODE] Sending message to {user}: {message}")
    # 模拟查找用户的步骤
    # pyautogui.hotkey('ctrl', 'f')
    # pyperclip.copy(user)
    # pyautogui.hotkey('ctrl', 'v')
    # time.sleep(1)
    # pyautogui.press('enter')
    # time.sleep(1)


    # 模拟发送消息的步骤
    # pyperclip.copy(message)
    # pyautogui.hotkey('ctrl', 'v')
    # pyautogui.press('enter')
    # time.sleep(1)

    logging.info("[TEST MODE] Messages have been 'sent' in test mode.")


def read_performance_data(filename):
    """读取性能数据文件并返回记录列表"""
    with open(filename, mode='r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_performance_data(filename, data, fieldnames):
    """写入性能数据到文件"""
    with open(filename, mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
def notify_awards(performance_data_filename):
    """通知奖励并更新性能数据文件"""
    records = read_performance_data(performance_data_filename)
    fieldnames = records[0].keys() if records else []
    updated = False

    for record in records:
        if record['激活奖励状态'] == '1' and record['是否发送通知'] == 'N':
            # 模拟发送微信消息
            send_wechat_message('文件传输助手', f"合同ID: {record['合同ID(_id)']}, 奖励已激活")
            record['是否发送通知'] = 'Y'
            updated = True
            logging.info(f"Notification sent for contract ID: {record['合同ID(_id)']}")

    if updated:
        write_performance_data(performance_data_filename, records, fieldnames)
        logging.info("PerformanceData.csv updated with notification status.")