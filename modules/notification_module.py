# notification_module.py
import logging
import pyautogui
import pyperclip
import time
import pygetwindow as gw
import re
from modules.log_config import setup_logging
import requests
from modules.config import *
from modules.file_utils import load_send_status, update_send_status, read_performance_data_from_csv, write_performance_data_to_csv
from datetime import datetime

# 配置日志
setup_logging()
# 使用专门的发送消息日志记录器
send_logger = logging.getLogger('sendLogger')

def send_wechat_message(user, message):
    logging.info(f"Preparing to open WeChat PC application to send message to {user}...")
    active_window = gw.getActiveWindow()
    is_active = re.match(r'^微信', active_window.title) is not None

    if not is_active:
        logging.info(f"Opening WeChat PC application to send message to {user}...")
        pyautogui.hotkey('ctrl', 'alt', 'w')
        time.sleep(1)
        
    pyautogui.hotkey('ctrl', 'f')
    pyperclip.copy(user)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(1)

    logging.info("Messages have been 'sent'.")

def send_wecom_message(user, message):
    logging.info(f"Preparing to open WeCom PC application to send message to {user}...")
    wechat_window = gw.getWindowsWithTitle('企业微信')[0] if gw.getWindowsWithTitle('企业微信') else None

    if not wechat_window or not wechat_window.isActive:
        logging.info(f"Opening WeCom PC application to send message to {user}...")
        pyautogui.hotkey('shift', 'alt', 's')
        time.sleep(1)

    pyautogui.hotkey('alt')
    time.sleep(0.1) # 可以根据需要调整延迟时间
    pyautogui.hotkey('alt')
    
    pyperclip.copy(user)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

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
            award_messages.append(f'达成{award}奖励条件，获得签约奖励{award_info}元 \U0001F9E7\U0001F9E7\U0001F9E7')
    return f'{service_housekeeper}签约合同{contract_number}\n\n' + '\n'.join(award_messages)

def preprocess_rate(rate):
    # 检查比率数据是否为空或不是有效的浮点数
    if rate.strip() and rate.replace('.', '', 1).isdigit():
        # 将比率数据转换为浮点数
        rate_float = float(rate)
        # 如果rate大于等于1，返回"100%"
        if rate_float >= 1:
            return "100%"
        else:
            # 将比率数据转换为浮点数，然后乘以100得到百分比
            return f"{int(rate_float * 100)}%"
    else:
        # 处理无效或空数据（例如，返回"N/A"或其他占位符）
        return "-"
def preprocess_amount(amount):
    # 检查金额数据是否为空或不是有效的浮点数
    if amount.strip() and amount.replace('.', '', 1).isdigit():
        # 将金额数据转换为浮点数，然后格式化为带有千位符号的整数字符串
        return f"{int(float(amount)):,d}"
    else:
        # 处理无效或空数据（例如，返回0或其他占位符）
        return "0"
    
def notify_awards_ctt1mc_beijing(performance_data_filename, status_filename):
    """通知奖励并更新性能数据文件，同时跟踪发送状态"""
    records = read_performance_data_from_csv(performance_data_filename)
    send_status = load_send_status(status_filename)
    updated = False

    awards_mapping = {
        '达标奖': '200',
        '优秀奖': '400',
        '精英奖': '1200'
    }

    # 提取最大的“管家累计金额”、“管家客单价”、“管家转化率”
    max_accumulated_amount = max(record['管家累计金额'] for record in records)
    max_average_price = max(int(float(record['平均客单价(average)'])) for record in records if record['平均客单价(average)'].strip() and record['平均客单价(average)'].replace('.', '', 1).isdigit())

    max_conversion_rate = max(record['转化率(conversion)'] for record in records)
    # 提取小于100%的有效转化率
    valid_conversion_rates = [float(record['转化率(conversion)']) for record in records if record['转化率(conversion)'].strip() and record['转化率(conversion)'].replace('.', '', 1).isdigit() and float(record['转化率(conversion)']) < 1]

    if valid_conversion_rates:
        max_conversion_rate = max(valid_conversion_rates)
        max_conversion_rate_percentage = int(max_conversion_rate * 100)
        max_conversion_rate_formatted = f"{max_conversion_rate_percentage}%"
    else:
        max_conversion_rate_formatted = "-" # Or any other placeholder for missing data

    # 计算全部的奖金池金额
    total_bonus_pool = int(sum(float(record['奖金池']) for record in records if record['奖金池'].replace('.', '', 1).isdigit()))
    total_bonus_pool_str = str(total_bonus_pool)
    total_bonus_pool = preprocess_amount(total_bonus_pool_str)

    max_accumulated_amount = preprocess_amount(max_accumulated_amount)
    max_average_price_str = str(max_average_price)
    max_average_price = preprocess_amount(max_average_price_str)

    for record in records:
        contract_id = record['合同ID(_id)']
        
        record["管家累计金额"] = preprocess_amount(record["管家累计金额"])
        record["平均客单价(average)"] = preprocess_amount(record["平均客单价(average)"])     
        record["转化率(conversion)"] = preprocess_rate(record["转化率(conversion)"])
                        
        if record['是否发送通知'] == 'N' and send_status.get(contract_id) != '发送成功':
            next_msg = '恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩 \U0001F389\U0001F389\U0001F389' if '无' in record["备注"] else f'{record["备注"]}'
            msg = f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8
恭喜 {record["管家(serviceHousekeeper)"]} 签约合同 {record["合同编号(contractdocNum)"]} 并完成线上收款\U0001F389\U0001F389\U0001F389

本单为活动期间平台累计签约第 {record["活动期内第几个合同"]} 单，个人累计签约第 {record["管家累计单数"]} 单。

\U0001F33B {record["管家(serviceHousekeeper)"]}累计签约 {record["管家累计金额"]} 元
\U0001F33B 平均客单价 {record["平均客单价(average)"]} 元
\U0001F33B 转化率 {record["转化率(conversion)"]}

\U0001F947 平台最高累计签约 {max_accumulated_amount} 元
\U0001F947 最高客单价 {max_average_price} 元
\U0001F947 最高转化率 {max_conversion_rate_formatted}

\U0001F44A {next_msg}。

\U0001F3C6 当前奖金池已累计 {total_bonus_pool} 元。
'''
            logging.info(f"Constructed message: {msg}")

            send_wecom_message(WECOM_GROUP_NAME_BJ_MAY, msg)
            # time.sleep(2)  # 添加3秒的延迟

            if record['激活奖励状态'] == '1':
                jiangli_msg = generate_award_message(record, awards_mapping)
                send_wechat_message(CAMPAIGN_CONTACT_BJ_MAY, jiangli_msg)

            update_send_status(status_filename, contract_id, '发送成功')
            # time.sleep(2)  # 添加3秒的延迟

            record['是否发送通知'] = 'Y'
            updated = True
            logging.info(f"Notification sent for contract INFO: {record['管家(serviceHousekeeper)']}, {record['合同ID(_id)']}")

    if updated:
        write_performance_data_to_csv(performance_data_filename, records, list(records[0].keys()))
        logging.info("PerformanceData.csv updated with notification status.")
    
def notify_awards(performance_data_filename, status_filename):
    """通知奖励并更新性能数据文件，同时跟踪发送状态"""
    records = read_performance_data_from_csv(performance_data_filename)
    send_status = load_send_status(status_filename)
    updated = False

    awards_mapping = {
        '开门红': '166',
        '接好运': '166',
        '达标奖': '200',
        '优秀奖': '600',
        '精英奖': '1600'
    }

    for record in records:
        contract_id = record['合同ID(_id)']
        if record['是否发送通知'] == 'N' and send_status.get(contract_id) != '发送成功':
            next_msg = '，恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩[庆祝][庆祝][庆祝]' if '无' in record["下一级奖项所需金额差"] else f'，{record["下一级奖项所需金额差"]}'
            msg = f'''开工大吉[爆竹][爆竹][爆竹]
恭喜{record["管家(serviceHousekeeper)"]}签约合同{record["合同编号(contractdocNum)"]}并完成线上收款[烟花][烟花][烟花]

本单为本月平台累计签约第{record["活动期内第几个合同"]}单，个人累计签约第{record["管家累计单数"]}单，累计签约金额{record["管家累计金额"]}元{next_msg}'''
            
            send_wechat_message(WECHAT_GROUP_NAME, msg)

            if record['激活奖励状态'] == '1':
                jiangli_msg = generate_award_message(record, awards_mapping)
                send_wechat_message(CAMPAIGN_CONTACT_WECHAT_NAME, jiangli_msg)

            update_send_status(status_filename, contract_id, '发送成功')
            time.sleep(3)  # 添加3秒的延迟

            record['是否发送通知'] = 'Y'
            updated = True
            logging.info(f"Notification sent for contract INFO: {record['管家(serviceHousekeeper)']}, {record['合同ID(_id)']}")

    if updated:
        write_performance_data_to_csv(performance_data_filename, records, list(records[0].keys()))
        logging.info("PerformanceData.csv updated with notification status.")

def generate_award_message_shanghai(record, awards_mapping):
    service_housekeeper = record["管家(serviceHousekeeper)"]
    contract_number = record["合同编号(contractdocNum)"]
    award_messages = []
    for award in record["奖励类型"].split(', '):
        if award in awards_mapping:
            award_info = awards_mapping[award]
            award_messages.append(f'达成 {award} 奖励条件，获得签约奖励 {award_info}元 [红包][红包][红包]')
    return f'{service_housekeeper} 签约合同 {contract_number}\n\n' + '\n'.join(award_messages)

def notify_awards_shanghai(performance_data_filename, status_filename):
    """通知奖励并更新活动台账数据文件，同时跟踪发送状态"""
    records = read_performance_data_from_csv(performance_data_filename)
    send_status = load_send_status(status_filename)
    updated = False

    awards_mapping = {
        '签约奖励-50': '50',
        '签约奖励-100': '100'
    }

    for record in records:
        contract_id = record['合同ID(_id)']
        if record['是否发送通知'] == 'N' and send_status.get(contract_id) != '发送成功':
            next_msg = record["备注"]
            msg = f'''[玫瑰][礼物][礼物][爆竹][爆竹][爆竹][礼物][礼物]
恭喜 {record["管家(serviceHousekeeper)"]} 成功签约，合同编号为 {record["合同编号(contractdocNum)"]} 合同金额为 {record["合同金额(adjustRefundMoney)"]}，并完成线上收款[烟花][烟花][烟花]

本单为“春暖花开”活动期间累计签约第{record["活动期内第几个合同"]}单，{record["管家(serviceHousekeeper)"]}个人累计签约第{record["管家累计单数"]}单，累计签约金额{record["管家累计金额"]}元。
'''
            
            logging.info(f"Constructed message: {msg}")
            
            # send_wechat_message(WECHAT_GROUP_NAME_SHANGHAI, msg)

            if record['激活奖励状态'] == '1':
                jiangli_msg = generate_award_message_shanghai(record, awards_mapping)
                logging.info(f"Generated award message: {jiangli_msg}")
                # send_wechat_message(CAMPAIGN_CONTACT_WECHAT_NAME_SHANGHAI, jiangli_msg)

            update_send_status(status_filename, contract_id, '发送成功')
            time.sleep(1)  # 添加3秒的延迟

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

        online_icon = "🟢"
        offline_icon = "🔴"
        
        status = update_content[0] if update_content else ""

        # 根据提取的状态决定使用哪个 Emoji
        if status == "上线":
            status_icon = online_icon
        elif status == "下线":
            status_icon = offline_icon
        else:
            status_icon = ""  # 如果状态不是上线或下线，不使用图标
            
        # message = f"技师状态变更：\n技师姓名：{technician_name}\n公司名称：{company_name}\n更新时间：{change_time}\n更新内容：{update_content}"
        message = f"您好，公司的管家：{technician_name}，在{simplified_time} {status_icon} {update_content} 了。"

        if change_id not in send_status:
            
            send_wechat_message(company_name, message)
            # send_wechat_message('文件传输助手', message)
            
            send_to_webhook(message)
            
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
