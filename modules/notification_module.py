# notification_module.py
import csv
import logging
import pyautogui
import pyperclip
import time
import pygetwindow as gw
from modules.log_config import setup_logging
import requests
from modules.config import WEBHOOK_URL, PHONE_NUMBER
from modules.file_utils import load_send_status, update_send_status, read_performance_data_from_csv, write_performance_data_to_csv
from datetime import datetime

# 配置日志
setup_logging()
# 使用专门的发送消息日志记录器
send_logger = logging.getLogger('sendLogger')

def send_wechat_message(user, message):
    """模拟发送微信消息给指定的用户（测试模式）"""
    logging.info(f"Preparing to open WeChat PC application to send message to {user}...")
    # Check if WeChat window is already open
    wechat_window = gw.getWindowsWithTitle('微信')[0] if gw.getWindowsWithTitle('微信') else None

    if not wechat_window or not wechat_window.isActive:
        logging.info(f"Opening WeChat PC application to send message to {user}...")
        # 模拟打开微信PC应用的步骤
        pyautogui.hotkey('ctrl', 'alt', 'w')
        time.sleep(1)

    send_logger.info(f"Sending message to {user}: {message}")
    # 模拟查找用户的步骤
    pyautogui.hotkey('ctrl', 'f')
    pyperclip.copy(user)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    # 模拟发送消息的步骤
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(1)

    logging.info("Messages have been 'sent'.")
    
def generate_award_message(record, awards_mapping):
    service_housekeeper = record["管家(serviceHousekeeper)"]
    contract_number = record["合同编号(contractdocNum)"]
    award_messages = []
    for award in record["奖励名称"].split(', '):
        if award in awards_mapping:
            award_info = awards_mapping[award]
            award_messages.append(f'达成{award}奖励条件，获得签约奖励{award_info}元[红包][红包][红包]')
    return f'{service_housekeeper}签约合同{contract_number}\n\n' + '\n'.join(award_messages)

def notify_awards(performance_data_filename, status_filename):
    """通知奖励并更新性能数据文件，同时跟踪发送状态"""
    records = read_performance_data_from_csv(performance_data_filename)
    send_status = load_send_status(status_filename)
    updated = False

    awards_mapping = {
        '开门红': '88',
        '接好运': '188',
        '达标奖': '400',
        '优秀奖': '800',
        '精英奖': '1200'
    }

    for record in records:
        contract_id = record['合同ID(_id)']
        if record['是否发送通知'] == 'N' and send_status.get(contract_id) != '发送成功':
            next_msg = '，恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩[庆祝][庆祝][庆祝]' if '无' in record["下一级奖项所需金额差"] else f'，{record["下一级奖项所需金额差"]}'
            msg = f'''开工大吉[爆竹][爆竹][爆竹]
恭喜{record["管家(serviceHousekeeper)"]}签约合同{record["合同编号(contractdocNum)"]}并完成线上收款[烟花][烟花][烟花]

本单为本月平台累计签约第{record["活动期内第几个合同"]}单，个人累计签约第{record["管家累计单数"]}单，累计签约金额{record["管家累计金额"]}元{next_msg}'''
            
            # send_wechat_message('修链(北京)运营沟通群', msg)

            if record['激活奖励状态'] == '1':
                jiangli_msg = generate_award_message(record, awards_mapping)
                # send_wechat_message('王爽', jiangli_msg)

            update_send_status(status_filename, contract_id, '发送成功')
            time.sleep(3)  # 添加3秒的延迟

            record['是否发送通知'] = 'Y'
            updated = True
            logging.info(f"Notification sent for contract INFO: {record['管家(serviceHousekeeper)']}, {record['合同ID(_id)']}")

    if updated:
        write_performance_data_to_csv(performance_data_filename, records, list(records[0].keys()))
        logging.info("PerformanceData.csv updated with notification status.")

def notify_technician_status_changes(status_changes, status_filename):
    """
    通知技师的状态变更信息，并更新状态记录文件。

    :param status_changes: 状态变更数组
    :param status_filename: 状态记录文件的路径
    """
    # 加载状态记录文件
    send_status = load_send_status(status_filename)

    for change in status_changes:
        change_id = change[0]
        change_time = change[1]
        technician_name = change[2]
        company_name = change[3]
        update_content = change[5]
        
        parsed_time = datetime.strptime(change_time, "%Y-%m-%dT%H:%M:%S.%f%z")
        simplified_time = parsed_time.strftime("%Y-%m-%d %H:%M")      

        # message = f"技师状态变更：\n技师姓名：{technician_name}\n公司名称：{company_name}\n更新时间：{change_time}\n更新内容：{update_content}"
        message = f"您好，公司的管家：{technician_name}，在{simplified_time} {update_content} 了。"

        if change_id not in send_status:
            
            logging.info(f"Sending message to {company_name}: {message}")           
            # send_wechat_message(company_name, message)
            # send_wechat_message('王爽', message)
            # send_to_webhook(message)
            update_send_status(status_filename, change_id, '通知成功')
            
            logging.info(f"Notification sent for technician status change: {change_id}")

def send_to_webhook(message):
    post_data = {
        'msgtype': "text",
        'text': {
            'content': message,
            # 'mentioned_mobile_list': [PHONE_NUMBER],
        },
    }
  
    try:
        # 发送POST请求
        response = requests.post(WEBHOOK_URL, json=post_data)
        response.raise_for_status() # 如果响应状态码不是200，则引发异常
        logging.info(f"sendToWebhook: Response status: {response.status_code}")
        logging.info(f"sendToWebhook: Response headers: {response.headers}")
        logging.info(f"sendToWebhook: Response data: {response.json()}")
    except requests.exceptions.RequestException as e:
        logging.error(f"sendToWebhook: 发送到Webhook时发生错误: {e}")
