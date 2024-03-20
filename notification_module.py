# notification_module.py

import json
import csv
import logging
import pyautogui
import pyperclip
import time
import pygetwindow as gw
from log_config import setup_logging
import requests
import json
from config import WEBHOOK_URL, PHONE_NUMBER

# 配置日志
setup_logging()
# 使用专门的发送消息日志记录器
send_logger = logging.getLogger('sendLogger')

def load_send_status(filename):
    """加载发送状态文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_send_status(filename, status):
    """保存发送状态到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=4)

def update_send_status(filename, _id, status):
    """更新指定合同ID的发送状态"""
    logging.info(f"Starting update_send_status for _id: {_id}, status: {status}")

    send_status = load_send_status(filename)
    send_status[_id] = status

    logging.info(f"Updating send_status for _id: {_id} to status: {status}")

    save_send_status(filename, send_status)
    logging.info(f"Successfully updated send_status for _id: {_id} to status: {status}")

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
    records = read_performance_data(performance_data_filename)
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
            send_wechat_message('修链(北京)运营沟通群', msg)

            if record['激活奖励状态'] == '1':
                jiangli_msg = generate_award_message(record, awards_mapping)
                send_wechat_message('王爽', jiangli_msg)

            update_send_status(status_filename, contract_id, '发送成功')
            time.sleep(3)  # 添加3秒的延迟

            record['是否发送通知'] = 'Y'
            updated = True
            logging.info(f"Notification sent for contract INFO: {record['管家(serviceHousekeeper)']}, {record['合同ID(_id)']}")

    if updated:
        write_performance_data(performance_data_filename, records, list(records[0].keys()))
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
        print(f"Current change: {change}")

        change_id = change[0]
        change_time = change[1]
        technician_name = change[2]
        company_name = change[3]
        update_content = change[5]

        # 构建通知消息
        message = f"技师状态变更：\n技师姓名：{technician_name}\n公司名称：{company_name}\n更新时间：{change_time}\n更新内容：{update_content}"

        if change_id not in send_status:
            # 发送微信通知
            send_wechat_message('文件传输助手', message)
            # 更新状态记录文件
            update_send_status(status_filename, change_id, '通知成功')
            logging.info(f"Notification sent for technician status change: {change_id}")

# 配置企业微信Webhook地址和电话号码

def send_to_webhook(message):
    post_data = {
        'msgtype': "text",
        'text': {
            'content': message,
            'mentioned_mobile_list': [PHONE_NUMBER],
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
