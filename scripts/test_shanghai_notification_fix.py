#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试上海通知消息转化率显示修复
"""

import os
import sys
import logging
from unittest.mock import patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
import modules.config
from modules.data_processing_db_module import process_data_to_db
from modules.notification_db_module import notify_awards_may_shanghai_db
from modules.performance_data_manager import (
    get_performance_data_by_campaign,
    delete_performance_data
)

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

def create_test_data():
    """创建测试数据"""
    return [
        {
            '合同ID(_id)': 'test_fix_sh_may_001',
            '活动城市(province)': '310000',
            '工单编号(serviceAppointmentNum)': 'GD2025045201',
            'Status': '1',
            '管家(serviceHousekeeper)': '金乐乐',
            '合同编号(contractdocNum)': 'YHWX-SH-RJTFSGC-2025050024',
            '合同金额(adjustRefundMoney)': '21995.0',
            '支付金额(paidAmount)': '10997.5',
            '差额(difference)': '10997.5',
            'State': '1',
            '创建时间(createTime)': '2025-05-01T10:30:00.000+08:00',
            '服务商(orgName)': '上海日进天丰建筑工程有限公司',
            '签约时间(signedDate)': '2025-05-01T10:35:00.000+08:00',
            'Doorsill': '10997.5',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '0.5',
            '平均客单价(average)': '20000'
        }
    ]

def clean_test_data(campaign_id="SH-2025-05"):
    """清理测试数据"""
    logger.info(f"清理测试数据: {campaign_id}")

    # 获取数据库中的测试数据
    db_data = get_performance_data_by_campaign(campaign_id)
    test_data = [data for data in db_data if data.contract_id.startswith('test_fix_sh_may_')]

    # 删除测试数据
    deleted_count = 0
    for data in test_data:
        delete_performance_data(data.id)
        deleted_count += 1
        logger.info(f"已删除测试数据: {data.contract_id}")

    if deleted_count > 0:
        logger.info(f"已删除 {deleted_count} 条测试数据")

    logger.info(f"测试数据清理完成: {campaign_id}")

def test_notification_fix():
    """测试通知修复"""
    logger.info("开始测试上海通知消息转化率显示修复")

    # 清理测试数据
    clean_test_data()

    # 创建测试数据
    test_data = create_test_data()
    logger.info(f"创建了 {len(test_data)} 条测试数据")

    # 处理数据并保存到数据库
    campaign_id = "SH-2025-05"
    province_code = "310000"

    # 使用数据库存储方式处理数据
    processed_count = process_data_to_db(test_data, campaign_id, province_code)
    logger.info(f"数据库存储方式处理了 {processed_count} 条数据")

    # 从数据库获取处理后的数据
    db_data = get_performance_data_by_campaign(campaign_id)
    db_data = [data for data in db_data if data.contract_id.startswith('test_fix_sh_may_')]

    logger.info(f"从数据库获取了 {len(db_data)} 条数据")

    # 使用Mock捕获通知消息
    with patch('modules.notification_db_module.create_task') as mock_create_task:
        # 设置mock的返回值
        mock_create_task.return_value = 1

        # 调用通知函数
        notify_awards_may_shanghai_db(db_data)

        # 获取调用参数
        messages = []
        for call_args in mock_create_task.call_args_list:
            if call_args[0][0] == 'send_wecom_message':
                messages.append(call_args[0][2])  # 消息内容是第三个参数

        logger.info(f"发送了 {len(messages)} 条通知消息")

        # 检查消息内容
        for i, msg in enumerate(messages):
            logger.info(f"消息 {i+1}:\n{msg}")

            # 检查转化率是否正确显示
            if "转化率 50%" in msg:
                logger.info("转化率显示正确: 50%")
            else:
                logger.error(f"转化率显示错误，消息内容: {msg}")
                return False

    logger.info("测试通过: 上海通知消息转化率显示修复成功")
    return True

if __name__ == "__main__":
    success = test_notification_fix()
    sys.exit(0 if success else 1)
