#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
仪表板模块
提供仪表板数据查询功能
"""

import os
import csv
import logging
from modules.performance_data_manager import get_performance_data_by_campaign

# 设置日志
logger = logging.getLogger(__name__)

def get_dashboard_data_from_file(file_path):
    """
    从文件中获取仪表板数据
    
    Args:
        file_path: 性能数据文件路径
        
    Returns:
        dict: 仪表板数据
    """
    logger.info(f"从文件获取仪表板数据: {file_path}")
    
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        return {
            'total_contracts': 0,
            'total_amount': 0,
            'rewards': []
        }
    
    try:
        # 读取CSV文件
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            records = list(reader)
        
        # 计算合同总数
        total_contracts = len(records)
        
        # 计算合同总金额
        total_amount = sum(float(record.get('合同金额(adjustRefundMoney)', 0)) for record in records)
        
        # 统计奖励
        rewards = {}
        for record in records:
            reward_type = record.get('奖励类型', '')
            reward_name = record.get('奖励名称', '')
            
            if reward_type and reward_name:
                key = f"{reward_type}_{reward_name}"
                if key not in rewards:
                    rewards[key] = {
                        'type': reward_type,
                        'name': reward_name,
                        'count': 0
                    }
                rewards[key]['count'] += 1
        
        # 转换为列表
        rewards_list = list(rewards.values())
        
        return {
            'total_contracts': total_contracts,
            'total_amount': total_amount,
            'rewards': rewards_list
        }
    
    except Exception as e:
        logger.error(f"获取仪表板数据失败: {str(e)}")
        return {
            'total_contracts': 0,
            'total_amount': 0,
            'rewards': []
        }

def get_dashboard_data_from_db(campaign_id):
    """
    从数据库中获取仪表板数据
    
    Args:
        campaign_id: 活动ID
        
    Returns:
        dict: 仪表板数据
    """
    logger.info(f"从数据库获取仪表板数据: {campaign_id}")
    
    try:
        # 获取性能数据
        records = get_performance_data_by_campaign(campaign_id)
        
        # 计算合同总数
        total_contracts = len(records)
        
        # 计算合同总金额
        total_amount = sum(float(record.contract_amount) for record in records)
        
        # 统计奖励
        rewards = {}
        for record in records:
            reward_type = record.reward_type
            reward_name = record.reward_name
            
            if reward_type and reward_name:
                key = f"{reward_type}_{reward_name}"
                if key not in rewards:
                    rewards[key] = {
                        'type': reward_type,
                        'name': reward_name,
                        'count': 0
                    }
                rewards[key]['count'] += 1
        
        # 转换为列表
        rewards_list = list(rewards.values())
        
        return {
            'total_contracts': total_contracts,
            'total_amount': total_amount,
            'rewards': rewards_list
        }
    
    except Exception as e:
        logger.error(f"获取仪表板数据失败: {str(e)}")
        return {
            'total_contracts': 0,
            'total_amount': 0,
            'rewards': []
        }
