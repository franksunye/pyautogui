"""
通知工具函数模块

提供通用的通知发送函数，用于发送不同类型的通知。
"""

import logging
import time
from task_manager import create_task
from modules.config import (
    CAMPAIGN_CONFIGS,
    DEFAULT_NOTIFICATION_CONFIG,
    WEBHOOK_URL_DEFAULT
)
import requests

def send_contract_notification(
    channel, recipient, message, reward_status=0, 
    reward_message=None, reward_recipient=None, delay=3
):
    """
    发送合同通知
    
    Args:
        channel: 通知渠道 ('wecom' 或 'wechat')
        recipient: 接收者 (群名称或联系人)
        message: 通知消息
        reward_status: 奖励状态 (0=无奖励, 1=有奖励)
        reward_message: 奖励消息 (如果有)
        reward_recipient: 奖励消息接收者 (如果有)
        delay: 发送后延迟时间(秒)
    
    Returns:
        bool: 是否成功发送
    """
    try:
        # 发送主通知
        if channel == 'wecom':
            create_task('send_wecom_message', recipient, message)
        elif channel == 'wechat':
            create_task('send_wechat_message', recipient, message)
        else:
            logging.error(f"Unknown channel: {channel}")
            return False
        
        # 延迟
        time.sleep(delay)
        
        # 如果有奖励，发送奖励通知
        if reward_status == 1 and reward_message and reward_recipient:
            create_task('send_wechat_message', reward_recipient, reward_message)
        
        return True
    except Exception as e:
        logging.error(f"Failed to send notification: {e}")
        return False

def send_webhook_notification(message, webhook_url=WEBHOOK_URL_DEFAULT):
    """
    发送Webhook通知
    
    Args:
        message: 通知消息
        webhook_url: Webhook URL
    
    Returns:
        bool: 是否成功发送
    """
    post_data = {
        'msgtype': "text",
        'text': {
            'content': message,
        },
    }

    try:
        response = requests.post(webhook_url, json=post_data)
        response.raise_for_status()
        logging.info(f"Webhook notification sent successfully: {response.status_code}")
        return True
    except Exception as e:
        logging.error(f"Failed to send webhook notification: {e}")
        return False

def get_campaign_config(campaign_id):
    """
    获取活动配置
    
    Args:
        campaign_id: 活动ID (例如 'BJ-2025-05')
    
    Returns:
        dict: 活动配置
    """
    # 尝试从配置中获取特定活动的配置
    config = CAMPAIGN_CONFIGS.get(campaign_id)
    
    # 如果找不到特定配置，使用默认配置
    if not config:
        city_code = campaign_id.split('-')[0]
        config = DEFAULT_NOTIFICATION_CONFIG.get(city_code, DEFAULT_NOTIFICATION_CONFIG['BJ'])
        logging.warning(f"No specific config found for {campaign_id}, using default config for {city_code}")
    
    return config

def notify_contract_signing(contract_data, campaign_id):
    """
    发送合同签约通知
    
    Args:
        contract_data: 合同数据 (文件版或数据库版)
        campaign_id: 活动ID (例如 'BJ-2025-05')
    
    Returns:
        bool: 是否成功发送
    """
    # 获取活动配置
    config = get_campaign_config(campaign_id)
    notification_config = config.get('notification', {})
    
    # 获取接收者和延迟时间
    recipient = notification_config.get('group_name')
    contact_name = notification_config.get('contact_name')
    delay_seconds = notification_config.get('delay_seconds', 3)
    
    # 发送通知
    return send_contract_notification(
        'wecom',
        recipient,
        contract_data.get('message'),
        contract_data.get('reward_status', 0),
        contract_data.get('reward_message'),
        contact_name,
        delay_seconds
    )
