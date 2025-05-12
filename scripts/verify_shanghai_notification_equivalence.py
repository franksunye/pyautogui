#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
上海5月通知逻辑等价性验证脚本

该脚本用于验证上海5月数据在文件存储和数据库存储两种方式下的通知逻辑是否完全一致。
它执行以下步骤：
1. 创建测试数据
2. 使用文件存储方式处理数据并生成通知
3. 使用数据库存储方式处理数据并生成通知
4. 比较两种方式的通知内容
5. 生成比较报告

使用方法：
python scripts/verify_shanghai_notification_equivalence.py
"""

import os
import sys
import logging
import time
from datetime import datetime
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
import modules.config
from modules.data_processing_module import process_data_may_shanghai
from modules.data_processing_db_module import process_data_to_db
from modules.notification_module import notify_awards_may_shanghai
from modules.notification_db_module import notify_awards_may_shanghai_db
from modules.file_utils import (
    get_all_records_from_csv, write_performance_data_to_csv
)
from modules.performance_data_manager import (
    get_performance_data_by_campaign, get_performance_data_by_contract_id,
    delete_performance_data
)

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

# 性能数据表头
performance_data_headers = [
    '活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)',
    'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)',
    '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)',
    'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)',
    'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)',
    '活动期内第几个合同', '管家累计金额', '管家累计单数', '奖金池',
    '计入业绩金额', '激活奖励状态', '奖励类型', '奖励名称',
    '是否发送通知', '备注', '登记时间'
]

def create_test_data_for_notification():
    """创建用于通知测试的数据"""
    return [
        {
            '合同ID(_id)': 'test_notify_sh_may_001',
            '活动城市(province)': '310000',
            '工单编号(serviceAppointmentNum)': 'GD2025045101',
            'Status': '1',
            '管家(serviceHousekeeper)': '张三',
            '合同编号(contractdocNum)': 'YHWX-SH-JDHS-2025050101',
            '合同金额(adjustRefundMoney)': '25000.0',
            '支付金额(paidAmount)': '12500.0',
            '差额(difference)': '12500.0',
            'State': '1',
            '创建时间(createTime)': '2025-05-01T10:30:00.000+08:00',
            '服务商(orgName)': '上海久盾宏盛建筑工程有限公司',
            '签约时间(signedDate)': '2025-05-01T10:35:00.000+08:00',
            'Doorsill': '12500.0',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '0.5',
            '平均客单价(average)': '20000'
        },
        {
            '合同ID(_id)': 'test_notify_sh_may_002',
            '活动城市(province)': '310000',
            '工单编号(serviceAppointmentNum)': 'GD2025045102',
            'Status': '1',
            '管家(serviceHousekeeper)': '李四',
            '合同编号(contractdocNum)': 'YHWX-SH-JDHS-2025050102',
            '合同金额(adjustRefundMoney)': '36000.0',
            '支付金额(paidAmount)': '18000.0',
            '差额(difference)': '18000.0',
            'State': '1',
            '创建时间(createTime)': '2025-05-02T11:30:00.000+08:00',
            '服务商(orgName)': '上海久盾宏盛建筑工程有限公司',
            '签约时间(signedDate)': '2025-05-02T11:35:00.000+08:00',
            'Doorsill': '18000.0',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '0.75',
            '平均客单价(average)': '25000'
        },
        {
            '合同ID(_id)': 'test_notify_sh_may_003',
            '活动城市(province)': '310000',
            '工单编号(serviceAppointmentNum)': 'GD2025045103',
            'Status': '1',
            '管家(serviceHousekeeper)': '王五',
            '合同编号(contractdocNum)': 'YHWX-SH-JDHS-2025050103',
            '合同金额(adjustRefundMoney)': '6000.0',
            '支付金额(paidAmount)': '3000.0',
            '差额(difference)': '3000.0',
            'State': '1',
            '创建时间(createTime)': '2025-05-03T14:30:00.000+08:00',
            '服务商(orgName)': '上海久盾宏盛建筑工程有限公司',
            '签约时间(signedDate)': '2025-05-03T14:35:00.000+08:00',
            'Doorsill': '3000.0',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '1.0',
            '平均客单价(average)': '30000'
        }
    ]

def clean_test_data(campaign_id="SH-2025-05"):
    """清理测试数据"""
    logger.info(f"清理测试数据: {campaign_id}")

    # 获取测试数据
    test_data = get_performance_data_by_campaign(campaign_id)

    # 删除测试数据
    for data in test_data:
        if data.contract_id.startswith('test_notify_sh_may_'):
            try:
                delete_performance_data(data.id)
                logger.info(f"已删除测试数据: {data.contract_id}")
            except Exception as e:
                logger.warning(f"删除测试数据失败: {data.contract_id}, 错误: {e}")

    logger.info(f"测试数据清理完成: {campaign_id}")

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
    file_processed_data = process_data_may_shanghai(
        test_data,
        existing_contract_ids,
        housekeeper_award_lists
    )

    logger.info(f"文件存储方式处理了 {len(file_processed_data)} 条数据")

    # 创建临时文件保存处理结果
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    write_performance_data_to_csv(temp_file.name, file_processed_data, performance_data_headers)
    logger.info(f"文件存储结果已保存到临时文件: {temp_file.name}")

    # 2. 使用数据库存储方式处理数据
    logger.info("使用数据库存储方式处理数据")
    modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA = True

    campaign_id = "SH-2025-05"
    province_code = "310000"
    db_processed_count = process_data_to_db(
        test_data,
        campaign_id,
        province_code
    )

    logger.info(f"数据库存储方式处理了 {db_processed_count} 条数据")

    # 3. 验证通知逻辑
    logger.info("验证通知逻辑")

    # 使用mock替换create_task函数，以捕获通知内容
    with patch('modules.notification_module.create_task') as mock_create_task_file, \
         patch('modules.notification_db_module.create_task') as mock_create_task_db:

        # 设置奖励状态为1（有奖励）
        # 文件存储方式
        file_data = get_all_records_from_csv(temp_file.name)
        for record in file_data:
            record['激活奖励状态'] = '1'
            record['奖励类型'] = '幸运数字'
            record['奖励名称'] = '接好运'
            record['是否发送通知'] = 'N'
        write_performance_data_to_csv(temp_file.name, file_data, performance_data_headers)

        # 数据库存储方式
        db_data = get_performance_data_by_campaign(campaign_id)
        for data in db_data:
            if data.contract_id.startswith('test_notify_sh_may_'):
                data.reward_status = 1
                data.reward_type = '幸运数字'
                data.reward_name = '接好运'
                data.notification_sent = 'N'
                data.save()

        # 执行通知逻辑
        # 文件存储方式
        notify_awards_may_shanghai(temp_file.name)

        # 数据库存储方式
        db_data = get_performance_data_by_campaign(campaign_id)
        # 只处理测试数据
        test_db_data = [data for data in db_data if data.contract_id.startswith('test_notify_sh_may_')]
        notify_awards_may_shanghai_db(test_db_data)

        # 获取通知内容
        file_notification_calls = mock_create_task_file.call_args_list
        db_notification_calls = mock_create_task_db.call_args_list

        # 比较通知数量
        file_notification_count = len(file_notification_calls)
        db_notification_count = len(db_notification_calls)

        logger.info(f"文件存储方式发送了 {file_notification_count} 条通知")
        logger.info(f"数据库存储方式发送了 {db_notification_count} 条通知")

        # 比较通知内容
        notification_match = True

        if file_notification_count != db_notification_count:
            logger.warning(f"通知数量不一致: 文件={file_notification_count}, 数据库={db_notification_count}")
            notification_match = False
        else:
            logger.info(f"通知数量一致: {file_notification_count}")

            # 比较每条通知的内容
            for i in range(file_notification_count):
                file_call = file_notification_calls[i]
                db_call = db_notification_calls[i]

                # 比较通知类型
                if file_call[0][0] != db_call[0][0]:
                    logger.warning(f"通知类型不一致: 文件={file_call[0][0]}, 数据库={db_call[0][0]}")
                    notification_match = False

                # 比较通知接收人
                if file_call[0][1] != db_call[0][1]:
                    logger.warning(f"通知接收人不一致: 文件={file_call[0][1]}, 数据库={db_call[0][1]}")
                    notification_match = False

                # 比较通知内容
                file_message = file_call[0][2]
                db_message = db_call[0][2]

                # 打印通知内容进行比较
                print(f"\n通知 {i+1} 比较:")
                print(f"文件通知内容: {file_message}")
                print(f"数据库通知内容: {db_message}")

                if file_message != db_message:
                    logger.warning(f"通知内容不一致: 文件={file_message}, 数据库={db_message}")
                    notification_match = False
                else:
                    logger.info(f"通知 {i+1} 内容一致")

    # 4. 清理临时文件
    try:
        os.unlink(temp_file.name)
        logger.info(f"已删除临时文件: {temp_file.name}")
    except Exception as e:
        logger.warning(f"删除临时文件失败: {e}")

    return notification_match

def main():
    """主函数"""
    logger.info("开始上海5月通知逻辑等价性验证")

    # 清理测试数据
    clean_test_data()

    # 验证通知逻辑
    notification_match = verify_notification_logic()

    # 输出总结
    print("\n上海5月通知逻辑等价性验证结果:")
    print(f"通知逻辑: {'通过 ✓' if notification_match else '失败 ❌'}")

    if notification_match:
        logger.info("验证结果: 文件存储和数据库存储的通知逻辑完全一致")
    else:
        logger.warning("验证结果: 文件存储和数据库存储的通知逻辑存在差异")

    logger.info("上海5月通知逻辑等价性验证完成")

if __name__ == "__main__":
    main()
