#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通知模块的数据库版本
从数据库中获取数据并发送通知
"""

import logging
from modules.log_config import setup_logging
from task_manager import create_task, get_task_status

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
    message = f"{housekeeper}签约合同{contract_doc_num}\n\n"

    if reward_type and reward_name:
        message += f"达成{reward_name}奖励条件，获得签约奖励{reward_type}元 \U0001F9E7\U0001F9E7\U0001F9E7"

    return message
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
            CAMPAIGN_CONTACT_BJ_MAY
        )

        # 发送消息
        create_task('send_wecom_message', WECOM_GROUP_NAME_BJ_MAY, message)

        # 更新通知状态
        data.notification_sent = "Y"
        data.save()

        logging.info(f"Notification sent for contract {data.contract_doc_num}")

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
            CAMPAIGN_CONTACT_SH_MAY
        )

        # 发送消息
        create_task('send_wecom_message', WECOM_GROUP_NAME_SH_MAY, message)

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
