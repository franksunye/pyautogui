#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通知等价性测试脚本

该脚本用于测试文件存储和数据库存储两种方式下的通知等价性。
它执行以下步骤：
1. 创建测试数据
2. 使用文件存储方式发送通知
3. 使用数据库存储方式发送通知
4. 比较两种方式的通知内容
5. 生成比较报告

使用方法：
python scripts/test_notification_equivalence.py
"""

import os
import sys
import json
import logging
import csv
import time
from datetime import datetime
import tempfile
from unittest.mock import patch, MagicMock, call

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
import modules.config
from modules.file_utils import write_performance_data_to_csv, get_all_records_from_csv
from modules.data_processing_module import process_data_may_beijing
from modules.data_processing_db_module import process_beijing_data_to_db
from modules.notification_module import notify_awards_may_beijing
from modules.notification_db_module import notify_awards_may_beijing_db
from modules.performance_data_manager import (
    PerformanceData, get_performance_data_by_id, get_performance_data_by_contract_id,
    get_performance_data_by_campaign, get_all_performance_data, delete_performance_data
)

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

# 性能数据CSV文件头
performance_data_headers = [
    '活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)',
    'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)',
    '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)',
    'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)',
    'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)',
    '活动期内第几个合同', '管家累计单数', '管家累计金额', '奖金池', '计入业绩金额',
    '激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间'
]

def create_test_data_beijing_may():
    """创建北京5月测试数据"""
    return [
        {
            '合同ID(_id)': 'test_notify_bj_may_001',
            '活动城市(province)': '110000',
            '工单编号(serviceAppointmentNum)': 'GD2025045495',
            'Status': '1',
            '管家(serviceHousekeeper)': '石王磊',
            '合同编号(contractdocNum)': 'YHWX-BJ-JDHS-2025050001',
            '合同金额(adjustRefundMoney)': '30548.8',
            '支付金额(paidAmount)': '15274.4',
            '差额(difference)': '15274.4',
            'State': '1',
            '创建时间(createTime)': '2025-05-01T11:36:22.444+08:00',
            '服务商(orgName)': '北京久盾宏盛建筑工程有限公司',
            '签约时间(signedDate)': '2025-05-01T11:42:07.904+08:00',
            'Doorsill': '15274.4',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '',
            '平均客单价(average)': ''
        },
        {
            '合同ID(_id)': 'test_notify_bj_may_002',
            '活动城市(province)': '110000',
            '工单编号(serviceAppointmentNum)': 'GD2025045496',
            'Status': '1',
            '管家(serviceHousekeeper)': '石王磊',
            '合同编号(contractdocNum)': 'YHWX-BJ-JDHS-2025050002',
            '合同金额(adjustRefundMoney)': '2500',
            '支付金额(paidAmount)': '1250',
            '差额(difference)': '1250',
            'State': '1',
            '创建时间(createTime)': '2025-05-02T10:30:22.444+08:00',
            '服务商(orgName)': '北京久盾宏盛建筑工程有限公司',
            '签约时间(signedDate)': '2025-05-02T10:35:07.904+08:00',
            'Doorsill': '1250',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '',
            '平均客单价(average)': ''
        },
        {
            '合同ID(_id)': 'test_notify_bj_may_006',
            '活动城市(province)': '110000',
            '工单编号(serviceAppointmentNum)': 'GD2025045500',
            'Status': '1',
            '管家(serviceHousekeeper)': '李明',
            '合同编号(contractdocNum)': 'YHWX-BJ-JDHS-2025050006',
            '合同金额(adjustRefundMoney)': '6666',
            '支付金额(paidAmount)': '3333',
            '差额(difference)': '3333',
            'State': '1',
            '创建时间(createTime)': '2025-05-06T11:30:22.444+08:00',
            '服务商(orgName)': '北京久盾宏盛建筑工程有限公司',
            '签约时间(signedDate)': '2025-05-06T11:35:07.904+08:00',
            'Doorsill': '3333',
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

def compare_notification_messages(file_messages, db_messages):
    """比较文件存储和数据库存储的通知消息"""
    logger.info("比较通知消息...")

    if len(file_messages) != len(db_messages):
        logger.warning(f"通知消息数量不一致: 文件={len(file_messages)}, 数据库={len(db_messages)}")
        return False, {"message_count_mismatch": f"文件={len(file_messages)}, 数据库={len(db_messages)}"}

    differences = {}
    for i, (file_msg, db_msg) in enumerate(zip(file_messages, db_messages)):
        if file_msg != db_msg:
            differences[f"message_{i}"] = {
                "file_message": file_msg,
                "db_message": db_msg
            }
            logger.warning(f"消息 {i} 不一致")
            logger.warning(f"文件消息: {file_msg}")
            logger.warning(f"数据库消息: {db_msg}")

    if differences:
        return False, differences
    else:
        logger.info("所有通知消息完全一致")
        return True, {}

def main():
    """主函数"""
    print("开始通知等价性测试")
    logger.info("开始通知等价性测试")

    # 清理测试数据
    clean_test_data()

    # 创建测试数据
    test_data = create_test_data_beijing_may()
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

    # 创建临时文件保存处理结果
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    write_performance_data_to_csv(temp_file.name, file_processed_data, performance_data_headers)
    logger.info(f"文件存储结果已保存到临时文件: {temp_file.name}")

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

    # 从数据库获取处理后的数据
    db_processed_data = get_performance_data_by_campaign(campaign_id)
    db_processed_data = [data for data in db_processed_data
                        if data.contract_id.startswith('test_notify_bj_may_')]

    logger.info(f"从数据库获取了 {len(db_processed_data)} 条数据")

    # 3. 使用Mock捕获通知消息
    file_messages = []
    db_messages = []

    # 使用文件存储方式发送通知
    with patch('modules.notification_module.create_task') as mock_create_task:
        # 设置mock的返回值
        mock_create_task.return_value = 1

        # 调用通知函数
        notify_awards_may_beijing(temp_file.name)

        # 获取调用参数
        for call_args in mock_create_task.call_args_list:
            if call_args[0][0] == 'send_wecom_message':
                file_messages.append(call_args[0][2])  # 消息内容是第三个参数

    logger.info(f"文件存储方式发送了 {len(file_messages)} 条通知消息")
    for i, msg in enumerate(file_messages):
        logger.info(f"文件消息 {i+1}:\n{msg}")

    # 使用数据库存储方式发送通知
    with patch('modules.notification_db_module.create_task') as mock_create_task:
        # 设置mock的返回值
        mock_create_task.return_value = 1

        # 调用通知函数
        notify_awards_may_beijing_db(db_processed_data)

        # 获取调用参数
        for call_args in mock_create_task.call_args_list:
            if call_args[0][0] == 'send_wecom_message':
                db_messages.append(call_args[0][2])  # 消息内容是第三个参数

    logger.info(f"数据库存储方式发送了 {len(db_messages)} 条通知消息")
    for i, msg in enumerate(db_messages):
        logger.info(f"数据库消息 {i+1}:\n{msg}")

    # 4. 比较通知消息
    is_equal, differences = compare_notification_messages(file_messages, db_messages)

    # 5. 输出结果
    if is_equal:
        logger.info("通知等价性测试通过: 文件存储和数据库存储的通知消息完全一致")
    else:
        logger.warning("通知等价性测试失败: 文件存储和数据库存储的通知消息存在差异")
        logger.warning(f"差异详情: {differences}")

    # 6. 清理临时文件
    try:
        os.unlink(temp_file.name)
        logger.info(f"已删除临时文件: {temp_file.name}")
    except Exception as e:
        logger.warning(f"删除临时文件失败: {e}")

    # 7. 清理测试数据
    clean_test_data()

    logger.info("通知等价性测试完成")

if __name__ == "__main__":
    main()
