"""
通知模板函数模块

提供各种通知模板的函数，用于生成不同类型的通知消息。
"""

from datetime import datetime

def preprocess_amount(amount):
    """
    处理金额格式
    
    Args:
        amount: 金额
    
    Returns:
        str: 格式化后的金额
    """
    try:
        return f"{float(amount):,.2f}".replace(',', ',')
    except (ValueError, TypeError):
        return str(amount)

def preprocess_rate(rate):
    """
    处理转化率格式
    
    Args:
        rate: 转化率
    
    Returns:
        str: 格式化后的转化率
    """
    try:
        # 如果是百分比格式，直接返回
        if isinstance(rate, str) and '%' in rate:
            return rate
        
        # 尝试转换为浮点数并格式化为百分比
        value = float(rate)
        if value > 1:  # 如果大于1，假设已经是百分比值
            return f"{value:.2f}%"
        else:
            return f"{value * 100:.2f}%"
    except (ValueError, TypeError):
        return str(rate)

def format_contract_signing_message(
    housekeeper, contract_doc_num, contract_amount, 
    conversion_rate, accumulated_amount, next_reward_msg
):
    """
    格式化合同签约消息
    
    Args:
        housekeeper: 管家姓名
        contract_doc_num: 合同编号
        contract_amount: 合同金额
        conversion_rate: 转化率
        accumulated_amount: 累计金额
        next_reward_msg: 下一个奖励提示
    
    Returns:
        str: 格式化后的消息
    """
    # 处理金额格式
    processed_amount = preprocess_amount(contract_amount)
    processed_accumulated_amount = preprocess_amount(accumulated_amount)
    processed_conversion_rate = preprocess_rate(conversion_rate)
    
    # 构建消息
    msg = f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8
恭喜 {housekeeper} 签约合同 {contract_doc_num} 并完成线上收款\U0001F389\U0001F389\U0001F389
合同金额：{processed_amount} 元
转化率：{processed_conversion_rate}
累计业绩：{processed_accumulated_amount} 元

\U0001F44A {next_reward_msg}。
'''
    return msg

def format_award_message(
    housekeeper, contract_doc_num, org_name, 
    contract_amount, reward_type, reward_name, 
    campaign_contact, awards_mapping
):
    """
    格式化奖励消息
    
    Args:
        housekeeper: 管家姓名
        contract_doc_num: 合同编号
        org_name: 服务商名称
        contract_amount: 合同金额
        reward_type: 奖励类型
        reward_name: 奖励名称
        campaign_contact: 活动联系人
        awards_mapping: 奖励金额映射
    
    Returns:
        str: 格式化后的消息
    """
    award_messages = []
    
    # 分割奖励类型和名称
    reward_types = reward_type.split(',') if reward_type else []
    reward_names = reward_name.split(',') if reward_name else []
    
    # 构建奖励消息
    for i, reward_name in enumerate(reward_names):
        reward_name = reward_name.strip()
        award_info = awards_mapping.get(reward_name, '未知')
        award_messages.append(f'达成{reward_name}奖励条件，获得签约奖励{award_info}元 \U0001F9E7\U0001F9E7\U0001F9E7')
    
    return f'{housekeeper}签约合同{contract_doc_num}\n\n' + '\n'.join(award_messages)

def format_technician_status_message(technician_name, status_time, status, status_content):
    """
    格式化技师状态变更消息
    
    Args:
        technician_name: 技师姓名
        status_time: 状态变更时间
        status: 状态 ('上线' 或 '下线')
        status_content: 状态内容
    
    Returns:
        str: 格式化后的消息
    """
    # 状态图标
    status_icon = "🟢" if status == "上线" else "🔴" if status == "下线" else ""
    
    # 如果status_time是ISO格式的时间字符串，转换为更友好的格式
    if isinstance(status_time, str) and 'T' in status_time:
        try:
            parsed_time = datetime.strptime(status_time, "%Y-%m-%dT%H:%M:%S.%f%z")
            status_time = parsed_time.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            pass
    
    # 构建消息
    message = f"您好，公司的管家：{technician_name}，在{status_time} {status_icon} {status_content} 了。"
    
    return message
