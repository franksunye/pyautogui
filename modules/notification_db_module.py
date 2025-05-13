#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通知模块的数据库版本
从数据库中获取数据并发送通知
"""

import logging
from modules.log_config import setup_logging
from task_manager import create_task
from modules.config import ENABLE_BADGE_MANAGEMENT, ELITE_HOUSEKEEPER, BADGE_NAME, ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_FEB
from modules.notification_utils import get_campaign_config
from modules.notification_templates import format_award_message
from modules.notification_templates import preprocess_amount, preprocess_rate

# 设置日志
setup_logging()

def notify_awards_may_beijing_db(performance_data_list):
    """
    从数据库中获取数据并发送北京5月奖励通知

    Args:
        performance_data_list: 从数据库中获取的性能数据列表
    """
    logging.info("Sending notifications for Beijing May awards (DB version)...")

    # 获取活动配置
    campaign_id = 'BJ-2025-05'
    config = get_campaign_config(campaign_id)
    notification_config = config.get('notification', {})

    # 获取通知相关配置
    group_name = notification_config.get('group_name')
    contact_name = notification_config.get('contact_name')
    awards_mapping = notification_config.get('awards_mapping', {})


    # 筛选出需要发送通知的记录
    records_to_notify = []
    for data in performance_data_list:
        # 如果未发送通知
        if data.notification_sent != "Y":
            records_to_notify.append(data)

    logging.info(f"Found {len(records_to_notify)} records to notify")

    # 发送通知
    for data in records_to_notify:
        # 准备数据
        housekeeper = data.housekeeper
        contract_doc_num = data.contract_doc_num
        contract_amount = data.contract_amount
        accumulated_amount = data.housekeeper_total_amount

        # 处理管家名称
        service_housekeeper = housekeeper
        if ENABLE_BADGE_MANAGEMENT and housekeeper in ELITE_HOUSEKEEPER:
            service_housekeeper = f'{BADGE_NAME}{housekeeper}'

        # 准备附加信息
        processed_accumulated_amount = preprocess_amount(accumulated_amount)
        processed_enter_performance_amount = preprocess_amount(data.performance_amount)
        next_msg = '恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩 \U0001F389\U0001F389\U0001F389' if '无' in data.remark else data.remark

        # 构建消息
        msg = f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8
恭喜 {service_housekeeper} 签约合同 {contract_doc_num} 并完成线上收款\U0001F389\U0001F389\U0001F389

\U0001F33B 本单为活动期间平台累计签约第 {data.contract_number_in_activity} 单，个人累计签约第 {data.housekeeper_contract_count} 单。

\U0001F33B {housekeeper}累计签约 {processed_accumulated_amount} 元{f', 累计计入业绩 {processed_enter_performance_amount} 元' if ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_FEB else ''}

\U0001F44A {next_msg}。
'''
        # 发送主通知
        create_task('send_wecom_message', group_name, msg)

        # 如果有奖励，发送奖励通知
        if data.reward_status == 1:
            # 构建奖励消息
            jiangli_msg = format_award_message(
                housekeeper,
                contract_doc_num,
                data.org_name,
                contract_amount,
                data.reward_type,
                data.reward_name,
                contact_name,
                awards_mapping
            )

            # 发送奖励消息
            create_task('send_wechat_message', contact_name, jiangli_msg)

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

    # 获取活动配置
    campaign_id = 'SH-2025-05'
    config = get_campaign_config(campaign_id)
    notification_config = config.get('notification', {})

    # 获取通知相关配置
    group_name = notification_config.get('group_name')
    contact_name = notification_config.get('contact_name')
    awards_mapping = notification_config.get('awards_mapping', {})


    # 筛选出需要发送通知的记录
    records_to_notify = []
    for data in performance_data_list:
        # 如果未发送通知
        if data.notification_sent != "Y":
            records_to_notify.append(data)

    logging.info(f"Found {len(records_to_notify)} records to notify")

    # 发送通知
    for data in records_to_notify:
        # 准备数据
        housekeeper = data.housekeeper
        contract_doc_num = data.contract_doc_num
        contract_amount = data.contract_amount
        accumulated_amount = data.housekeeper_total_amount
        conversion_rate = str(data.conversion)

        # 准备附加信息
        processed_accumulated_amount = preprocess_amount(accumulated_amount)
        processed_conversion_rate = preprocess_rate(conversion_rate)
        next_msg = '恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩 \U0001F389\U0001F389\U0001F389' if '无' in data.remark else f'{data.remark}'

        # 构建消息
        msg = f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8
恭喜 {housekeeper} 签约合同 {contract_doc_num} 并完成线上收款\U0001F389\U0001F389\U0001F389

\U0001F33B 本单为本月平台累计签约第 {data.contract_number_in_activity} 单，个人累计签约第 {data.housekeeper_contract_count} 单，

\U0001F33B {housekeeper}累计签约 {processed_accumulated_amount} 元，

\U0001F33B 转化率 {processed_conversion_rate}。

\U0001F44A {next_msg}。
'''
        # 发送主通知
        create_task('send_wecom_message', group_name, msg)

        # 如果有奖励，发送奖励通知
        if data.reward_status == 1:
            # 构建奖励消息
            jiangli_msg = format_award_message(
                housekeeper,
                contract_doc_num,
                data.org_name,
                contract_amount,
                data.reward_type,
                data.reward_name,
                contact_name,
                awards_mapping
            )

            # 发送奖励消息
            create_task('send_wechat_message', contact_name, jiangli_msg)

        # 更新通知状态
        data.notification_sent = "Y"
        data.save()

        logging.info(f"Notification sent for contract {contract_doc_num}")

    logging.info("Shanghai May awards notifications completed (DB version)")

def notify_awards_apr_beijing_db(performance_data_list):
    """
    从数据库中获取数据并发送北京4月奖励通知

    Args:
        performance_data_list: 从数据库中获取的性能数据列表
    """
    logging.info("Sending notifications for Beijing April awards (DB version)...")

    # 获取活动配置
    campaign_id = 'BJ-2025-04'
    config = get_campaign_config(campaign_id)
    notification_config = config.get('notification', {})

    # 获取通知相关配置
    group_name = notification_config.get('group_name')
    contact_name = notification_config.get('contact_name')
    awards_mapping = notification_config.get('awards_mapping', {})

    # 筛选出需要发送通知的记录
    records_to_notify = []
    for data in performance_data_list:
        # 如果奖励状态为1（有奖励）且未发送通知
        if data.reward_status == 1 and data.notification_sent != "Y":
            records_to_notify.append(data)

    logging.info(f"Found {len(records_to_notify)} records to notify")

    # 发送通知
    for data in records_to_notify:
        # 准备数据
        housekeeper = data.housekeeper
        contract_doc_num = data.contract_doc_num

        # 构建消息
        message = format_award_message(
            housekeeper,
            contract_doc_num,
            data.org_name,
            data.contract_amount,
            data.reward_type,
            data.reward_name,
            contact_name,
            awards_mapping
        )

        # 发送消息
        create_task('send_wecom_message', group_name, message)

        # 更新通知状态
        data.notification_sent = "Y"
        data.save()

        logging.info(f"Notification sent for contract {contract_doc_num}")

    logging.info("Beijing April awards notifications completed (DB version)")

def notify_awards_apr_shanghai_db(performance_data_list):
    """
    从数据库中获取数据并发送上海4月奖励通知

    Args:
        performance_data_list: 从数据库中获取的性能数据列表
    """
    logging.info("Sending notifications for Shanghai April awards (DB version)...")

    # 获取活动配置
    campaign_id = 'SH-2025-04'
    config = get_campaign_config(campaign_id)
    notification_config = config.get('notification', {})

    # 获取通知相关配置
    group_name = notification_config.get('group_name')
    contact_name = notification_config.get('contact_name')
    awards_mapping = notification_config.get('awards_mapping', {})

    # 筛选出需要发送通知的记录
    records_to_notify = []
    for data in performance_data_list:
        # 如果奖励状态为1（有奖励）且未发送通知
        if data.reward_status == 1 and data.notification_sent != "Y":
            records_to_notify.append(data)

    logging.info(f"Found {len(records_to_notify)} records to notify")

    # 发送通知
    for data in records_to_notify:
        # 准备数据
        housekeeper = data.housekeeper
        contract_doc_num = data.contract_doc_num

        # 构建消息
        message = format_award_message(
            housekeeper,
            contract_doc_num,
            data.org_name,
            data.contract_amount,
            data.reward_type,
            data.reward_name,
            contact_name,
            awards_mapping
        )

        # 发送消息
        create_task('send_wecom_message', group_name, message)

        # 更新通知状态
        data.notification_sent = "Y"
        data.save()

        logging.info(f"Notification sent for contract {contract_doc_num}")

    logging.info("Shanghai April awards notifications completed (DB version)")
