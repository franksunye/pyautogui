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
from modules.file_utils import load_send_status, update_send_status, get_all_records_from_csv, write_performance_data_to_csv
from datetime import datetime, timezone

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

def notify_awards_ctt1mc_shanghai(performance_data_filename, status_filename,contract_data):
    """通知奖励并更新性能数据文件，同时跟踪发送状态"""
    records = get_all_records_from_csv(performance_data_filename)
    send_status = load_send_status(status_filename)
    updated = False

    awards_mapping = {
        '基础奖': '100',
        '达标奖': '200',
        '优秀奖': '400',
        '精英奖': '800'
    }

    max_accumulated_amount = max(float(record['管家累计金额']) for record in records)
    # max_average_price = max(int(float(record['平均客单价(average)'])) for record in records if record['平均客单价(average)'].strip() and record['平均客单价(average)'].replace('.', '', 1).isdigit())
    max_average_price = max(int(float(record['平均客单价(average)'])) for record in contract_data if record['平均客单价(average)'].strip() and record['平均客单价(average)'].replace('.', '', 1).isdigit())

    max_conversion_rate = max(record['转化率(conversion)'] for record in contract_data)
    # max_conversion_rate = max(record['转化率(conversion)'] for record in records)
    # valid_conversion_rates = [float(record['转化率(conversion)']) for record in records if record['转化率(conversion)'].strip() and record['转化率(conversion)'].replace('.', '', 1).isdigit() and float(record['转化率(conversion)']) < 1]
    valid_conversion_rates = [float(record['转化率(conversion)']) for record in contract_data if record['转化率(conversion)'].strip() and record['转化率(conversion)'].replace('.', '', 1).isdigit() and float(record['转化率(conversion)']) <= 1]

    if valid_conversion_rates:
        max_conversion_rate = max(valid_conversion_rates)
        max_conversion_rate_percentage = int(max_conversion_rate * 100)
        max_conversion_rate_formatted = f"{max_conversion_rate_percentage}%"
    else:
        max_conversion_rate_formatted = "-" # Or any other placeholder for missing data

    total_bonus_pool = int(sum(float(record['奖金池']) for record in records if record['奖金池'].replace('.', '', 1).isdigit()))
    total_bonus_pool_str = str(total_bonus_pool)
    total_bonus_pool = preprocess_amount(total_bonus_pool_str)

    max_accumulated_amount_str = str(max_accumulated_amount)
    max_accumulated_amount = preprocess_amount(max_accumulated_amount_str)
    max_average_price_str = str(max_average_price)
    max_average_price = preprocess_amount(max_average_price_str)

    for record in records:
        contract_id = record['合同ID(_id)']
        
        processed_accumulated_amount = preprocess_amount(record["管家累计金额"])
        processed_average_price = preprocess_amount(record["平均客单价(average)"])
        processed_conversion_rate = preprocess_rate(record["转化率(conversion)"])
                        
        if record['是否发送通知'] == 'N' and send_status.get(contract_id) != '发送成功':
            next_msg = '恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩 \U0001F389\U0001F389\U0001F389' if '无' in record["备注"] else f'{record["备注"]}'
            msg = f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8
恭喜 {record["管家(serviceHousekeeper)"]} 签约合同 {record["合同编号(contractdocNum)"]} 并完成线上收款\U0001F389\U0001F389\U0001F389

本单为活动期间平台累计签约第 {record["活动期内第几个合同"]} 单，个人累计签约第 {record["管家累计单数"]} 单。

\U0001F33B {record["管家(serviceHousekeeper)"]}累计签约 {processed_accumulated_amount} 元
\U0001F33B 平均客单价 {processed_average_price} 元
\U0001F33B 转化率 {processed_conversion_rate}

\U0001F947 平台最高累计签约 {max_accumulated_amount} 元
\U0001F947 平台最高平均客单价 {max_average_price} 元
\U0001F947 平台最高转化率 {max_conversion_rate_formatted}

\U0001F44A {next_msg}。

\U0001F3C6 当前奖金池已累计 {total_bonus_pool} 元。
'''
            # logging.info(f"Constructed message: {msg}")

            # send_wecom_message(WECOM_GROUP_NAME_SH_MAY, msg)
            time.sleep(2)

            if record['激活奖励状态'] == '1':
                jiangli_msg = generate_award_message(record, awards_mapping)
                # send_wechat_message(CAMPAIGN_CONTACT_SH_MAY, jiangli_msg)

            update_send_status(status_filename, contract_id, '发送成功')
            time.sleep(2)

            record['是否发送通知'] = 'Y'
            updated = True
            logging.info(f"Notification sent for contract INFO: {record['管家(serviceHousekeeper)']}, {record['合同ID(_id)']}")

    if updated:
        write_performance_data_to_csv(performance_data_filename, records, list(records[0].keys()))
        logging.info("PerformanceData.csv updated with notification status.")
  
def notify_awards_ctt1mc_beijing(performance_data_filename, status_filename, contract_data):
    """通知奖励并更新性能数据文件，同时跟踪发送状态"""
    records = get_all_records_from_csv(performance_data_filename)
    send_status = load_send_status(status_filename)
    updated = False

    awards_mapping = {
        '达标奖': '200',
        '优秀奖': '400',
        '精英奖': '1200'
    }

    max_accumulated_amount = max(float(record['管家累计金额']) for record in records)
    # max_average_price = max(int(float(record['平均客单价(average)'])) for record in records if record['平均客单价(average)'].strip() and record['平均客单价(average)'].replace('.', '', 1).isdigit())
    max_average_price = max(int(float(record['平均客单价(average)'])) for record in contract_data if record['平均客单价(average)'].strip() and record['平均客单价(average)'].replace('.', '', 1).isdigit())

    max_conversion_rate = max(record['转化率(conversion)'] for record in contract_data)
    # max_conversion_rate = max(record['转化率(conversion)'] for record in records)
    # valid_conversion_rates = [float(record['转化率(conversion)']) for record in records if record['转化率(conversion)'].strip() and record['转化率(conversion)'].replace('.', '', 1).isdigit() and float(record['转化率(conversion)']) < 1]
    valid_conversion_rates = [float(record['转化率(conversion)']) for record in contract_data if record['转化率(conversion)'].strip() and record['转化率(conversion)'].replace('.', '', 1).isdigit() and float(record['转化率(conversion)']) <= 1]

    if valid_conversion_rates:
        max_conversion_rate = max(valid_conversion_rates)
        max_conversion_rate_percentage = int(max_conversion_rate * 100)
        max_conversion_rate_formatted = f"{max_conversion_rate_percentage}%"
    else:
        max_conversion_rate_formatted = "-" # Or any other placeholder for missing data

    total_bonus_pool = int(sum(float(record['奖金池']) for record in records if record['奖金池'].replace('.', '', 1).isdigit()))
    total_bonus_pool_str = str(total_bonus_pool)
    total_bonus_pool = preprocess_amount(total_bonus_pool_str)

    max_accumulated_amount_str = str(max_accumulated_amount)
    max_accumulated_amount = preprocess_amount(max_accumulated_amount_str)
    max_average_price_str = str(max_average_price)
    max_average_price = preprocess_amount(max_average_price_str)

    for record in records:
        contract_id = record['合同ID(_id)']
        
        processed_accumulated_amount = preprocess_amount(record["管家累计金额"])
        processed_average_price = preprocess_amount(record["平均客单价(average)"])
        processed_conversion_rate = preprocess_rate(record["转化率(conversion)"])
                        
        if record['是否发送通知'] == 'N' and send_status.get(contract_id) != '发送成功':
            next_msg = '恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩 \U0001F389\U0001F389\U0001F389' if '无' in record["备注"] else f'{record["备注"]}'
            msg = f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8
恭喜 {record["管家(serviceHousekeeper)"]} 签约合同 {record["合同编号(contractdocNum)"]} 并完成线上收款\U0001F389\U0001F389\U0001F389

本单为活动期间平台累计签约第 {record["活动期内第几个合同"]} 单，个人累计签约第 {record["管家累计单数"]} 单。

\U0001F33B {record["管家(serviceHousekeeper)"]}累计签约 {processed_accumulated_amount} 元
\U0001F33B 平均客单价 {processed_average_price} 元
\U0001F33B 转化率 {processed_conversion_rate}

\U0001F947 平台最高累计签约 {max_accumulated_amount} 元
\U0001F947 平台最高平均客单价 {max_average_price} 元
\U0001F947 平台最高转化率 {max_conversion_rate_formatted}

\U0001F44A {next_msg}。

\U0001F3C6 当前奖金池已累计 {total_bonus_pool} 元。
'''
            # logging.info(f"Constructed message: {msg}")

            # send_wecom_message(WECOM_GROUP_NAME_BJ_MAY, msg)
            # time.sleep(2)  # 添加3秒的延迟

            if record['激活奖励状态'] == '1':
                jiangli_msg = generate_award_message(record, awards_mapping)
                # send_wechat_message(CAMPAIGN_CONTACT_BJ_MAY, jiangli_msg)

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
    records = get_all_records_from_csv(performance_data_filename)
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
    records = get_all_records_from_csv(performance_data_filename)
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
            
            # logging.info(f"Constructed message: {msg}")
            
            send_wechat_message(WECHAT_GROUP_NAME_SHANGHAI, msg)

            if record['激活奖励状态'] == '1':
                jiangli_msg = generate_award_message_shanghai(record, awards_mapping)
                # logging.info(f"Generated award message: {jiangli_msg}")
                send_wechat_message(CAMPAIGN_CONTACT_WECHAT_NAME_SHANGHAI, jiangli_msg)

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
            
            post_text_to_webhook(message)
            
            update_send_status(status_filename, change_id, '通知成功')
            
            logging.info(f"Notification sent for technician status change: {change_id}")

def notify_contact_timeout_changes(contact_timeout_data):
    """
    通知工单联络超时的信息。

    :param contact_timeout_data: 工单联络超时数据
    """
    messages = []
    message_count = 1  # 初始化消息计数器
    
    for data in contact_timeout_data:
        order_number = data[0]
        housekeeper = data[2]
        assign_time = data[3]

        # 解析分单时间
        parsed_time = datetime.strptime(assign_time, "%Y-%m-%dT%H:%M:%S%z")
        # 将分单时间转换为本地时间
        local_assign_time = parsed_time.astimezone()
        
        # 计算时间差
        time_difference = datetime.now(timezone.utc) - local_assign_time
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        # 构建消息
        simplified_time = parsed_time.strftime("%Y-%m-%d %H:%M")
        time_difference_str = f"{days}天 {hours}小时 {minutes}分钟"
        message_number = f"{message_count:02d}"  # 格式化编号，始终为两位数
        message = f"{message_number}. 工单编号：{order_number}，管家：{housekeeper}，分单时间：{simplified_time}，已超时：{time_difference_str}"
        messages.append(message)
        message_count += 1  # 消息计数器增加
    
    if messages:
        full_message = "\n".join(messages)
        # print(full_message)  # 打印完整的消息
        
        post_text_to_webhook(full_message, WEBHOOK_URL_CONTACT_TIMEOUT)

def notify_contact_timeout_changes_markdown(contact_timeout_data):
    """
    通知工单联络超时的信息。

    :param contact_timeout_data: 工单联络超时数据
    """
    messages = []
    message_count = 0  # 初始化消息计数器
    days_colors = ["info", "comment", "warning"]  # 每天的超时信息对应的颜色

    # 构建消息标题
    total_messages = len(contact_timeout_data)
    title = f"联系超时汇总（上周）共计 {total_messages} 条"
    title_message = f"# {title}"
    messages.append(title_message)

    for data in contact_timeout_data:
        message_count += 1
        order_number = data[0]
        housekeeper = data[2]
        assign_time = data[3]

        # 解析分单时间
        parsed_time = datetime.strptime(assign_time, "%Y-%m-%dT%H:%M:%S%z")
        # 将分单时间转换为本地时间
        local_assign_time = parsed_time.astimezone()
        
        # 计算时间差
        time_difference = datetime.now(timezone.utc) - local_assign_time
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        # 构建消息
        simplified_time = parsed_time.strftime("%Y-%m-%d %H:%M")
        time_difference_str = f"{days}天 {hours}小时 {minutes}分钟"
        message_number = f"{message_count:02d}"  # 格式化编号，始终为两位数

        # 选择颜色
        color_index = days % len(days_colors)
        color = days_colors[color_index]

        # 消息内容
        message = f"{message_number}. 工单编号：{order_number}，管家：{housekeeper}，分单时间：{simplified_time}，已超时：{time_difference_str}"
        message = f"<font color=\"{color}\">{message}</font>"
        messages.append(message)
    
    if messages:
        full_message = "\n".join(messages)
        # print(full_message)  # 打印完整的消息
        
        post_markdown_to_webhook(full_message, WEBHOOK_URL_CONTACT_TIMEOUT)
        
def post_text_to_webhook(message, webhook_url=WEBHOOK_URL_DEFAULT):  # WEBHOOK_URL_DEFAULT 是默认的 Webhook URL
    post_data = {
        'msgtype': "text",
        'text': {
            'content': message,
            # 'mentioned_mobile_list': [PHONE_NUMBER],
        },
    }
   
    try:
        # 发送POST请求
        response = requests.post(webhook_url, json=post_data)
        response.raise_for_status() # 如果响应状态码不是200，则引发异常
        logging.info(f"sendToWebhook: Response status: {response.status_code}")
        # logging.info(f"sendToWebhook: Response headers: {response.headers}")
        # logging.info(f"sendToWebhook: Response data: {response.json()}")
    except requests.exceptions.RequestException as e:
        logging.error(f"sendToWebhook: 发送到Webhook时发生错误: {e}")

def post_markdown_to_webhook(message, webhook_url):
    """
    发送Markdown格式的消息到企业微信的Webhook。
    
    :param message: 要发送的Markdown格式的消息
    :param webhook_url: Webhook的URL
    """
    post_data = {
        'msgtype': 'markdown',
        'markdown': {
            'content': message
        }
    }
    
    try:
        # 发送POST请求
        response = requests.post(webhook_url, json=post_data)
        response.raise_for_status()  # 如果响应状态码不是200，则引发异常
        logging.info(f"PostMarkdownToWebhook: Response status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"PostMarkdownToWebhook: 发送到Webhook时发生错误: {e}")
        
        
def notify_contact_timeout_changes_template_card(contact_timeout_data):
    """
    通知工单联络超时的信息，使用企业微信的template_card格式。

    :param contact_timeout_data: 工单联络超时数据
    """
    message_count = 0  # 初始化消息计数器
    horizontal_content_list = []

    # 构建消息标题
    total_messages = len(contact_timeout_data)
    title = "联系超时汇总（上周）共计 {} 条".format(total_messages)

    for data in contact_timeout_data[:6]:  # 只处理前6条数据
        message_count += 1
        order_number = data[0][-6:]  # 仅保留工单编号的后6位
        housekeeper = data[2]
        assign_time = data[3]

        # 解析分单时间
        parsed_time = datetime.strptime(assign_time, "%Y-%m-%dT%H:%M:%S%z")
        # 将分单时间转换为本地时间
        local_assign_time = parsed_time.astimezone()
        
        # 计算时间差
        time_difference = datetime.now(timezone.utc) - local_assign_time
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        # 构建消息
        simplified_time = parsed_time.strftime("%Y-%m-%d %H")
        time_difference_str = "{}天 {}小时".format(days, hours)
        message_number = "{:02d}".format(message_count)  # 格式化编号，始终为两位数

        # 消息内容
        horizontal_content_list.append({
            "keyname": "{}. 单号".format(message_number),
            "value": "{}，{}，{}，超：{}".format(order_number, housekeeper, simplified_time, time_difference_str)
        })
    
    if horizontal_content_list:
        post_template_card_to_webhook(title, total_messages, horizontal_content_list, WEBHOOK_URL_CONTACT_TIMEOUT)

def post_template_card_to_webhook(title, total_messages, horizontal_content_list, webhook_url):
    """
    发送template_card格式的消息到企业微信的Webhook。
    
    :param title: 消息标题
    :param total_messages: 总消息数
    :param horizontal_content_list: 二级标题+文本列表
    :param webhook_url: Webhook的URL
    """
    post_data = {
        "msgtype": "template_card",
        "template_card": {
            "card_type": "text_notice",
            "source": {
                "icon_url": "http://metabase.fsgo365.cn:3000/app/assets/img/favicon.ico",
                "desc": "修链Metabase",
                "desc_color": 0
            },
            "main_title": {
                "title": "联系超时汇总（上周）报告",
                "desc": "超时时间的规则为1小时以内，晚上10点后的工单，第二天上午8点前需要联系..."
            },
            "emphasis_content": {
                "title": "{}".format(total_messages),
                "desc": "联系超时汇总（上周）共计"
            },
            "horizontal_content_list": horizontal_content_list,
            "jump_list": [
                {
                    "type": 1,
                    "url": "http://metabase.fsgo365.cn:3000/question/980",
                    "title": "超时工单列表"
                }
            ],
            "card_action": {
                "type": 1,
                "url": "http://metabase.fsgo365.cn:3000/question/980"
            }
        }
    }
    
    try:
        # 发送POST请求
        response = requests.post(webhook_url, json=post_data)
        response.raise_for_status()  # 如果响应状态码不是200，则引发异常
        logging.info(f"PostTemplateCardToWebhook: Response status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"PostTemplateCardToWebhook: 发送到Webhook时发生错误: {e}")