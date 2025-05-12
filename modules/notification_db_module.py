#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通知模块的数据库版本
从数据库中获取数据并发送通知
"""

import logging
import time
from modules.log_config import setup_logging
from task_manager import create_task, get_task_status
from modules.config import ENABLE_BADGE_MANAGEMENT, ELITE_HOUSEKEEPER, BADGE_NAME, ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_FEB

def preprocess_rate(rate):
    """
    处理比率数据，格式化为百分比字符串

    Args:
        rate: 比率数据，可以是字符串或数字

    Returns:
        str: 格式化后的百分比字符串
    """
    # 检查比率数据是否为空或不是有效的浮点数
    if isinstance(rate, str):
        if rate.strip() and rate.replace('.', '', 1).isdigit():
            rate_float = float(rate)
        else:
            return "-"
    elif isinstance(rate, (int, float)):
        rate_float = float(rate)
    else:
        return "-"

    # 如果rate大于等于1，返回"100%"
    if rate_float >= 1:
        return "100%"
    else:
        # 将比率数据转换为浮点数，然后乘以100得到百分比
        return f"{int(rate_float * 100)}%"

def preprocess_amount(amount):
    """
    处理金额数据，格式化为带千位分隔符的整数字符串

    Args:
        amount: 金额数据，可以是字符串或数字

    Returns:
        str: 格式化后的金额字符串
    """
    # 检查金额数据是否为空或不是有效的浮点数
    if isinstance(amount, str):
        if amount.strip() and amount.replace('.', '', 1).isdigit():
            amount_float = float(amount)
        else:
            return "0"
    elif isinstance(amount, (int, float)):
        amount_float = float(amount)
    else:
        return "0"

    # 将金额数据转换为浮点数，然后格式化为带有千位符号的整数字符串
    return f"{int(amount_float):,d}"

def format_award_message(housekeeper, contract_doc_num, org_name, contract_amount, reward_type, reward_name, campaign_contact):
    """
    格式化奖励消息

    Args:
        housekeeper: 管家
        contract_doc_num: 合同编号
        org_name: 服务商
        contract_amount: 合同金额
        reward_type: 奖励类型
        reward_name: 奖励名称
        campaign_contact: 活动联系人

    Returns:
        message: 格式化后的消息
    """
    award_messages = []

    # 上海5月的奖励金额映射
    awards_mapping = {
        '接好运': '36',
        '接好运万元以上': '66',
        '基础奖': '200',
        '达标奖': '300',
        '优秀奖': '400',
        '精英奖': '800',
    }

    # 检查是否启用徽章管理
    if ENABLE_BADGE_MANAGEMENT and (housekeeper in ELITE_HOUSEKEEPER):
        # 如果管家在精英管家列表里面，添加徽章和进行精英连击双倍奖励计算与提示
        service_housekeeper = f'{BADGE_NAME}{housekeeper}'
        if reward_type and reward_name:
            try:
                # 使用奖励名称查找对应的奖励金额
                award_info = awards_mapping.get(reward_name, reward_type)
                award_info_double = str(int(award_info) * 2)
                award_messages.append(f'达成 {reward_name} 奖励条件，奖励金额 {award_info} 元，同时触发"精英连击双倍奖励"，奖励金额\U0001F680直升至 {award_info_double} 元！\U0001F9E7\U0001F9E7\U0001F9E7')
            except ValueError:
                award_messages.append(f'达成{reward_name}奖励条件，获得签约奖励{award_info}元 \U0001F9E7\U0001F9E7\U0001F9E7')
    else:
        # 不启用徽章功能
        service_housekeeper = housekeeper
        if reward_type and reward_name:
            # 使用奖励名称查找对应的奖励金额
            award_info = awards_mapping.get(reward_name, reward_type)
            award_messages.append(f'达成{reward_name}奖励条件，获得签约奖励{award_info}元 \U0001F9E7\U0001F9E7\U0001F9E7')

    return f'{service_housekeeper}签约合同{contract_doc_num}\n\n' + '\n'.join(award_messages)
from modules.config import (
    WECOM_GROUP_NAME_BJ_MAY, CAMPAIGN_CONTACT_BJ_MAY,
    WECOM_GROUP_NAME_SH_MAY, CAMPAIGN_CONTACT_SH_MAY,
    WECOM_GROUP_NAME_BJ_APR, CAMPAIGN_CONTACT_BJ_APR,
    WECOM_GROUP_NAME_SH_APR, CAMPAIGN_CONTACT_SH_APR
)

# 设置日志
setup_logging()

def notify_awards_may_beijing_db(performance_data_list):
    """
    从数据库中获取数据并发送北京5月奖励通知

    Args:
        performance_data_list: 从数据库中获取的性能数据列表
    """
    logging.info("Sending notifications for Beijing May awards (DB version)...")

    # 筛选出需要发送通知的记录
    records_to_notify = []
    for data in performance_data_list:
        # 如果未发送通知
        if data.notification_sent != "Y":
            records_to_notify.append(data)

    logging.info(f"Found {len(records_to_notify)} records to notify")

    # 发送通知
    for data in records_to_notify:
        # 处理管家名称
        service_housekeeper = data.housekeeper
        if ENABLE_BADGE_MANAGEMENT and service_housekeeper in ELITE_HOUSEKEEPER:
            service_housekeeper = f'{BADGE_NAME}{service_housekeeper}'

        # 处理金额数据
        processed_accumulated_amount = preprocess_amount(data.housekeeper_total_amount)
        processed_enter_performance_amount = preprocess_amount(data.performance_amount)

        # 构建"签约喜报"消息
        next_msg = '恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩 \U0001F389\U0001F389\U0001F389' if '无' in data.remark else data.remark
        msg = f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8
恭喜 {service_housekeeper} 签约合同 {data.contract_doc_num} 并完成线上收款\U0001F389\U0001F389\U0001F389

\U0001F33B 本单为活动期间平台累计签约第 {data.contract_number_in_activity} 单，个人累计签约第 {data.housekeeper_contract_count} 单。

\U0001F33B {data.housekeeper}累计签约 {processed_accumulated_amount} 元{f', 累计计入业绩 {processed_enter_performance_amount} 元' if ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_FEB else ''}

\U0001F44A {next_msg}。
'''
        # 发送"签约喜报"消息
        create_task('send_wecom_message', WECOM_GROUP_NAME_BJ_MAY, msg)
        time.sleep(3)  # 添加3秒的延迟

        # 如果有奖励，发送奖励消息
        if data.reward_status == 1:
            # 构建奖励消息
            jiangli_msg = format_award_message(
                data.housekeeper,
                data.contract_doc_num,
                data.org_name,
                data.contract_amount,
                data.reward_type,
                data.reward_name,
                CAMPAIGN_CONTACT_BJ_MAY
            )

            # 发送奖励消息
            create_task('send_wechat_message', CAMPAIGN_CONTACT_BJ_MAY, jiangli_msg)

        # 更新通知状态
        data.notification_sent = "Y"
        data.save()

        # 确保合同ID至少有4个字符，否则使用完整ID
        contract_id = data.contract_id
        contract_id_display = contract_id[-4:] if len(contract_id) >= 4 else contract_id
        logging.info(f"Notification sent for contract ID: {contract_id_display}")

    logging.info("Beijing May awards notifications completed (DB version)")

def notify_awards_may_shanghai_db(performance_data_list):
    """
    从数据库中获取数据并发送上海5月奖励通知

    Args:
        performance_data_list: 从数据库中获取的性能数据列表
    """
    logging.info("Sending notifications for Shanghai May awards (DB version)...")

    # 筛选出需要发送通知的记录
    records_to_notify = []
    for data in performance_data_list:
        # 如果未发送通知
        if data.notification_sent != "Y":
            records_to_notify.append(data)

    logging.info(f"Found {len(records_to_notify)} records to notify")

    # 发送通知
    for data in records_to_notify:
        # 获取管家姓名和合同编号
        service_housekeeper = data.housekeeper
        contract_doc_num = data.contract_doc_num

        # 构建"签约喜报"消息
        processed_amount = preprocess_amount(data.contract_amount)
        processed_accumulated_amount = preprocess_amount(data.housekeeper_total_amount)

        # 确定下一个奖励提示
        next_msg = '恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩 \U0001F389\U0001F389\U0001F389' if '无' in data.remark else f'{data.remark}'

        # 处理转化率
        processed_conversion_rate = preprocess_rate(str(data.conversion))

        # 构建签约喜报消息
        msg = f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8
恭喜 {service_housekeeper} 签约合同 {contract_doc_num} 并完成线上收款\U0001F389\U0001F389\U0001F389

\U0001F33B 本单为本月平台累计签约第 {data.contract_number_in_activity} 单，个人累计签约第 {data.housekeeper_contract_count} 单，

\U0001F33B {data.housekeeper}累计签约 {processed_accumulated_amount} 元，

\U0001F33B 转化率 {processed_conversion_rate}。

\U0001F44A {next_msg}。
'''
        # 发送"签约喜报"消息
        create_task('send_wecom_message', WECOM_GROUP_NAME_SH_MAY, msg)
        time.sleep(2)  # 添加2秒的延迟，与文件版本保持一致

        # 如果有奖励，发送奖励消息
        if data.reward_status == 1:
            # 构建奖励消息
            jiangli_msg = format_award_message(
                data.housekeeper,
                data.contract_doc_num,
                data.org_name,
                data.contract_amount,
                data.reward_type,
                data.reward_name,
                CAMPAIGN_CONTACT_SH_MAY
            )

            # 发送奖励消息
            create_task('send_wechat_message', CAMPAIGN_CONTACT_SH_MAY, jiangli_msg)

        # 更新通知状态
        data.notification_sent = "Y"
        data.save()

        logging.info(f"Notification sent for contract {data.contract_doc_num}")

    logging.info("Shanghai May awards notifications completed (DB version)")

def notify_awards_apr_beijing_db(performance_data_list):
    """
    从数据库中获取数据并发送北京4月奖励通知

    Args:
        performance_data_list: 从数据库中获取的性能数据列表
    """
    logging.info("Sending notifications for Beijing April awards (DB version)...")

    # 筛选出需要发送通知的记录
    records_to_notify = []
    for data in performance_data_list:
        # 如果奖励状态为1（有奖励）且未发送通知
        if data.reward_status == 1 and data.notification_sent != "Y":
            records_to_notify.append(data)

    logging.info(f"Found {len(records_to_notify)} records to notify")

    # 发送通知
    for data in records_to_notify:
        # 构建消息
        message = format_award_message(
            data.housekeeper,
            data.contract_doc_num,
            data.org_name,
            data.contract_amount,
            data.reward_type,
            data.reward_name,
            CAMPAIGN_CONTACT_BJ_APR
        )

        # 发送消息
        create_task('send_wecom_message', WECOM_GROUP_NAME_BJ_APR, message)

        # 更新通知状态
        data.notification_sent = "Y"
        data.save()

        logging.info(f"Notification sent for contract {data.contract_doc_num}")

    logging.info("Beijing April awards notifications completed (DB version)")

def notify_awards_apr_shanghai_db(performance_data_list):
    """
    从数据库中获取数据并发送上海4月奖励通知

    Args:
        performance_data_list: 从数据库中获取的性能数据列表
    """
    logging.info("Sending notifications for Shanghai April awards (DB version)...")

    # 筛选出需要发送通知的记录
    records_to_notify = []
    for data in performance_data_list:
        # 如果奖励状态为1（有奖励）且未发送通知
        if data.reward_status == 1 and data.notification_sent != "Y":
            records_to_notify.append(data)

    logging.info(f"Found {len(records_to_notify)} records to notify")

    # 发送通知
    for data in records_to_notify:
        # 构建消息
        message = format_award_message(
            data.housekeeper,
            data.contract_doc_num,
            data.org_name,
            data.contract_amount,
            data.reward_type,
            data.reward_name,
            CAMPAIGN_CONTACT_SH_APR
        )

        # 发送消息
        create_task('send_wecom_message', WECOM_GROUP_NAME_SH_APR, message)

        # 更新通知状态
        data.notification_sent = "Y"
        data.save()

        logging.info(f"Notification sent for contract {data.contract_doc_num}")

    logging.info("Shanghai April awards notifications completed (DB version)")
