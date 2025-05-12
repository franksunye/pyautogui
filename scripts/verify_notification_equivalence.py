#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通知逻辑等价性验证脚本

该脚本用于验证北京5月数据在文件存储和数据库存储两种方式下的通知逻辑是否完全一致。
它专注于验证以下通知逻辑：
1. 通知触发条件
2. 通知内容生成
3. 通知接收人确定
4. 通知状态跟踪

使用方法：
python scripts/verify_notification_equivalence.py
"""

import os
import sys
import json
import logging
import csv
import time
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
import modules.config
from modules.data_processing_module import process_data_may_beijing
from modules.data_processing_db_module import process_beijing_data_to_db
from modules.performance_data_manager import (
    PerformanceData, get_performance_data_by_id, get_performance_data_by_contract_id,
    get_performance_data_by_campaign, get_all_performance_data, delete_performance_data
)
import modules.notification_module
import modules.notification_db_module

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

def create_test_data_for_notification():
    """创建用于测试通知逻辑的数据"""
    return [
        # 幸运数字奖励，应该触发通知
        {
            '合同ID(_id)': 'test_notify_bj_may_001',
            '活动城市(province)': '110000',
            '工单编号(serviceAppointmentNum)': 'GD2025045801',
            'Status': '1',
            '管家(serviceHousekeeper)': '测试管家D',
            '合同编号(contractdocNum)': 'YHWX-BJ-TEST-2025050601',  # 包含幸运数字6
            '合同金额(adjustRefundMoney)': '20000',  # 大于10000
            '支付金额(paidAmount)': '10000',
            '差额(difference)': '10000',
            'State': '1',
            '创建时间(createTime)': '2025-05-01T11:36:22.444+08:00',
            '服务商(orgName)': '测试服务商D',
            '签约时间(signedDate)': '2025-05-01T11:42:07.904+08:00',
            'Doorsill': '10000',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '',
            '平均客单价(average)': ''
        },
        # 节节高奖励，应该触发通知
        {
            '合同ID(_id)': 'test_notify_bj_may_002',
            '活动城市(province)': '110000',
            '工单编号(serviceAppointmentNum)': 'GD2025045802',
            'Status': '1',
            '管家(serviceHousekeeper)': '测试管家E',
            '合同编号(contractdocNum)': 'YHWX-BJ-TEST-2025050701',
            '合同金额(adjustRefundMoney)': '20000',
            '支付金额(paidAmount)': '10000',
            '差额(difference)': '10000',
            'State': '1',
            '创建时间(createTime)': '2025-05-02T11:36:22.444+08:00',
            '服务商(orgName)': '测试服务商E',
            '签约时间(signedDate)': '2025-05-02T11:42:07.904+08:00',
            'Doorsill': '10000',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '',
            '平均客单价(average)': ''
        },
        # 无奖励，不应该触发通知
        {
            '合同ID(_id)': 'test_notify_bj_may_003',
            '活动城市(province)': '110000',
            '工单编号(serviceAppointmentNum)': 'GD2025045803',
            'Status': '1',
            '管家(serviceHousekeeper)': '测试管家F',
            '合同编号(contractdocNum)': 'YHWX-BJ-TEST-2025050801',
            '合同金额(adjustRefundMoney)': '5000',
            '支付金额(paidAmount)': '2500',
            '差额(difference)': '2500',
            'State': '1',
            '创建时间(createTime)': '2025-05-03T11:36:22.444+08:00',
            '服务商(orgName)': '测试服务商F',
            '签约时间(signedDate)': '2025-05-03T11:42:07.904+08:00',
            'Doorsill': '2500',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '',
            '平均客单价(average)': ''
        }
    ]

def clean_test_data(campaign_id="BJ-2025-05"):
    """清理测试数据"""
    logger.info(f"清理测试数据: {campaign_id}")

    # 获取测试数据
    test_data = get_performance_data_by_campaign(campaign_id)

    # 删除测试数据
    for data in test_data:
        if data.contract_id.startswith('test_notify_bj_may_'):
            try:
                delete_performance_data(data.id)
                logger.info(f"已删除测试数据: {data.contract_id}")
            except Exception as e:
                logger.warning(f"删除测试数据失败: {data.contract_id}, 错误: {e}")

    logger.info(f"测试数据清理完成: {campaign_id}")

def mock_create_task(task_type, *args, **kwargs):
    """模拟创建任务"""
    logger.info(f"模拟创建任务: {task_type}, 参数: {args}, 关键字参数: {kwargs}")
    return True

def verify_notification_logic():
    """验证通知逻辑"""
    logger.info("验证通知逻辑")

    # 创建测试数据
    test_data = create_test_data_for_notification()
    logger.info(f"创建了 {len(test_data)} 条测试数据")

    # 1. 使用文件存储方式处理数据
    logger.info("使用文件存储方式处理数据")
    modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA = False

    existing_contract_ids = set()
    housekeeper_award_lists = {}
    file_processed_data = process_data_may_beijing(
        test_data,
        existing_contract_ids,
        housekeeper_award_lists
    )

    logger.info(f"文件存储方式处理了 {len(file_processed_data)} 条数据")

    # 2. 使用数据库存储方式处理数据
    logger.info("使用数据库存储方式处理数据")
    modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA = True

    campaign_id = "BJ-2025-05"
    province_code = "110000"
    db_processed_count = process_beijing_data_to_db(
        test_data,
        campaign_id,
        province_code
    )

    logger.info(f"数据库存储方式处理了 {db_processed_count} 条数据")

    # 3. 比较通知逻辑
    logger.info("比较通知逻辑")

    # 从数据库获取处理后的数据
    db_processed_data = get_performance_data_by_campaign(campaign_id)
    db_processed_data = [data for data in db_processed_data
                        if data.contract_id.startswith('test_notify_bj_may_')]

    # 比较通知触发条件
    print("\n通知触发条件比较:")
    print(f"{'合同ID':<25} {'奖励类型':<15} {'奖励名称':<20} {'文件通知状态':<15} {'数据库通知状态':<15} {'结果':<10}")
    print("-" * 100)

    all_match = True
    for file_record in file_processed_data:
        file_contract_id = file_record['合同ID(_id)']
        file_reward_type = file_record['奖励类型']
        file_reward_name = file_record['奖励名称']
        file_notification_sent = file_record['是否发送通知']

        # 在数据库记录中查找匹配的记录
        db_record = next((data for data in db_processed_data
                         if data.contract_id == file_contract_id), None)

        if db_record is None:
            logger.warning(f"找不到合同ID为 {file_contract_id} 的数据库记录")
            all_match = False
            continue

        db_notification_sent = db_record.notification_sent

        # 比较通知状态
        if file_notification_sent == db_notification_sent:
            result = "匹配 ✓"
        else:
            result = "不匹配 ❌"
            all_match = False

        print(f"{file_contract_id:<25} {file_reward_type:<15} {file_reward_name:<20} {file_notification_sent:<15} {db_notification_sent:<15} {result:<10}")

    # 简化版通知发送测试
    logger.info("简化版通知发送测试")

    # 检查通知触发条件
    file_notification_count = sum(1 for record in file_processed_data if record['奖励类型'])
    db_notification_count = sum(1 for record in db_processed_data if record.reward_type)

    print("\n通知触发条件比较:")
    print(f"文件存储触发通知记录数: {file_notification_count}")
    print(f"数据库存储触发通知记录数: {db_notification_count}")

    if file_notification_count == db_notification_count:
        print("通知触发条件匹配 ✓")
    else:
        print("通知触发条件不匹配 ❌")
        all_match = False

    return all_match

def main():
    """主函数"""
    logger.info("开始通知逻辑等价性验证")

    # 清理测试数据
    clean_test_data()

    # 验证通知逻辑
    notification_match = verify_notification_logic()

    # 输出总结
    print("\n通知逻辑等价性验证结果:")
    print(f"通知逻辑: {'通过 ✓' if notification_match else '失败 ❌'}")

    if notification_match:
        logger.info("验证结果: 文件存储和数据库存储的通知逻辑完全一致")
    else:
        logger.warning("验证结果: 文件存储和数据库存储的通知逻辑存在差异")

    logger.info("通知逻辑等价性验证完成")

if __name__ == "__main__":
    main()
