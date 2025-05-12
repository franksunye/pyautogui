#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
上海5月数据等价性验证脚本

该脚本用于验证上海5月数据在文件存储和数据库存储两种方式下的处理结果是否完全一致。
它执行以下步骤：
1. 获取上海5月的测试数据
2. 使用文件存储方式处理数据
3. 使用数据库存储方式处理数据
4. 比较两种方式的处理结果
5. 生成比较报告

使用方法：
python scripts/verify_shanghai_may_equivalence.py
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
from modules.data_processing_module import process_data_may_shanghai
from modules.data_processing_db_module import process_data_to_db
from modules.file_utils import (
    get_all_records_from_csv, write_performance_data_to_csv
)
from modules.performance_data_manager import (
    get_performance_data_by_campaign, get_performance_data_by_contract_id,
    delete_performance_data
)
from tests.test_utils.result_comparison import compare_results, save_comparison_results

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

def create_test_data_shanghai_may():
    """创建上海5月测试数据"""
    return [
        {
            '合同ID(_id)': 'test_equiv_sh_may_001',
            '活动城市(province)': '310000',
            '工单编号(serviceAppointmentNum)': 'GD2025045001',
            'Status': '1',
            '管家(serviceHousekeeper)': '张三',
            '合同编号(contractdocNum)': 'YHWX-SH-JDHS-2025050001',
            '合同金额(adjustRefundMoney)': '25000.0',
            '支付金额(paidAmount)': '12500.0',
            '差额(difference)': '12500.0',
            'State': '1',
            '创建时间(createTime)': '2025-05-01T10:30:00.000+08:00',
            '服务商(orgName)': '上海久盾宏盛建筑工程有限公司',
            '签约时间(signedDate)': '2025-05-01T10:35:00.000+08:00',
            'Doorsill': '12500.0',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '',
            '平均客单价(average)': ''
        },
        {
            '合同ID(_id)': 'test_equiv_sh_may_002',
            '活动城市(province)': '310000',
            '工单编号(serviceAppointmentNum)': 'GD2025045002',
            'Status': '1',
            '管家(serviceHousekeeper)': '李四',
            '合同编号(contractdocNum)': 'YHWX-SH-JDHS-2025050002',
            '合同金额(adjustRefundMoney)': '36000.0',
            '支付金额(paidAmount)': '18000.0',
            '差额(difference)': '18000.0',
            'State': '1',
            '创建时间(createTime)': '2025-05-02T11:30:00.000+08:00',
            '服务商(orgName)': '上海久盾宏盛建筑工程有限公司',
            '签约时间(signedDate)': '2025-05-02T11:35:00.000+08:00',
            'Doorsill': '18000.0',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '',
            '平均客单价(average)': ''
        },
        {
            '合同ID(_id)': 'test_equiv_sh_may_003',
            '活动城市(province)': '310000',
            '工单编号(serviceAppointmentNum)': 'GD2025045003',
            'Status': '1',
            '管家(serviceHousekeeper)': '王五',
            '合同编号(contractdocNum)': 'YHWX-SH-JDHS-2025050003',
            '合同金额(adjustRefundMoney)': '6000.0',
            '支付金额(paidAmount)': '3000.0',
            '差额(difference)': '3000.0',
            'State': '1',
            '创建时间(createTime)': '2025-05-03T14:30:00.000+08:00',
            '服务商(orgName)': '上海久盾宏盛建筑工程有限公司',
            '签约时间(signedDate)': '2025-05-03T14:35:00.000+08:00',
            'Doorsill': '3000.0',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '',
            '平均客单价(average)': ''
        },
        {
            '合同ID(_id)': 'test_equiv_sh_may_004',
            '活动城市(province)': '310000',
            '工单编号(serviceAppointmentNum)': 'GD2025045004',
            'Status': '1',
            '管家(serviceHousekeeper)': '赵六',
            '合同编号(contractdocNum)': 'YHWX-SH-JDHS-2025050004',
            '合同金额(adjustRefundMoney)': '50000.0',
            '支付金额(paidAmount)': '25000.0',
            '差额(difference)': '25000.0',
            'State': '1',
            '创建时间(createTime)': '2025-05-04T16:30:00.000+08:00',
            '服务商(orgName)': '上海久盾宏盛建筑工程有限公司',
            '签约时间(signedDate)': '2025-05-04T16:35:00.000+08:00',
            'Doorsill': '25000.0',
            '款项来源类型(tradeIn)': '1',
            '转化率(conversion)': '',
            '平均客单价(average)': ''
        }
    ]

def clean_test_data(campaign_id="SH-2025-05"):
    """清理测试数据"""
    logger.info(f"清理测试数据: {campaign_id}")

    # 获取测试数据
    test_data = get_performance_data_by_campaign(campaign_id)

    # 删除测试数据
    for data in test_data:
        if data.contract_id.startswith('test_equiv_sh_may_'):
            try:
                delete_performance_data(data.id)
                logger.info(f"已删除测试数据: {data.contract_id}")
            except Exception as e:
                logger.warning(f"删除测试数据失败: {data.contract_id}, 错误: {e}")

    logger.info(f"测试数据清理完成: {campaign_id}")

def compare_data_fields(file_record, db_record):
    """比较文件记录和数据库记录的字段值"""
    logger.info(f"比较合同ID为 {file_record['合同ID(_id)']} 的记录")

    # 字段映射
    field_mapping = {
        '活动编号': 'campaign_id',
        '合同ID(_id)': 'contract_id',
        '活动城市(province)': 'province_code',
        '工单编号(serviceAppointmentNum)': 'service_appointment_num',
        'Status': 'status',
        '管家(serviceHousekeeper)': 'housekeeper',
        '合同编号(contractdocNum)': 'contract_doc_num',
        '合同金额(adjustRefundMoney)': 'contract_amount',
        '支付金额(paidAmount)': 'paid_amount',
        '差额(difference)': 'difference',
        'State': 'state',
        '创建时间(createTime)': 'create_time',
        '服务商(orgName)': 'org_name',
        '签约时间(signedDate)': 'signed_date',
        'Doorsill': 'doorsill',
        '款项来源类型(tradeIn)': 'trade_in',
        '转化率(conversion)': 'conversion',
        '平均客单价(average)': 'average',
        '活动期内第几个合同': 'contract_number_in_activity',
        '管家累计金额': 'housekeeper_total_amount',
        '管家累计单数': 'housekeeper_contract_count',
        '奖金池': 'bonus_pool',
        '计入业绩金额': 'performance_amount',
        '激活奖励状态': 'reward_status',
        '奖励类型': 'reward_type',
        '奖励名称': 'reward_name',
        '是否发送通知': 'notification_sent',
        '备注': 'remark',
        '登记时间': 'register_time'
    }

    # 比较字段值
    mismatches = []
    print(f"\n比较合同ID为 {file_record['合同ID(_id)']} 的记录:")
    print(f"{'字段':<20} {'文件值':<30} {'数据库值':<30} {'结果':<10}")
    print("-" * 90)

    for file_field, db_field in field_mapping.items():
        if file_field in file_record:
            file_value = file_record[file_field]
            db_value = getattr(db_record, db_field)

            # 处理数值类型
            if file_field in ['合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)',
                             '管家累计金额', '计入业绩金额', '奖金池']:
                file_value_orig = file_value
                db_value_orig = db_value
                file_value = float(file_value) if file_value else 0.0
                db_value = float(db_value) if db_value is not None else 0.0
                # 允许小数点后两位的误差
                if abs(file_value - db_value) > 0.01:
                    mismatches.append((file_field, file_value, db_field, db_value))
                    result = "不匹配 ❌"
                else:
                    result = "匹配 ✓"
                print(f"{file_field:<20} {file_value_orig:<30} {db_value_orig:<30} {result:<10}")
            # 处理空值和0值
            elif file_field in ['转化率(conversion)', '平均客单价(average)']:
                file_value_orig = file_value
                db_value_orig = db_value

                # 将空字符串和None视为等价
                if (not file_value or file_value == '') and (not db_value or db_value == 0 or db_value == '0' or db_value == '0.0'):
                    result = "匹配 ✓"
                else:
                    mismatches.append((file_field, file_value, db_field, db_value))
                    result = "不匹配 ❌"
                print(f"{file_field:<20} {file_value_orig:<30} {db_value_orig:<30} {result:<10}")
            # 处理Doorsill字段
            elif file_field == 'Doorsill':
                file_value_orig = file_value
                db_value_orig = db_value
                file_value = float(file_value) if file_value else 0.0
                db_value = float(db_value) if db_value is not None else 0.0
                # 允许小数点后两位的误差
                if abs(file_value - db_value) > 0.01:
                    mismatches.append((file_field, file_value, db_field, db_value))
                    result = "不匹配 ❌"
                else:
                    result = "匹配 ✓"
                print(f"{file_field:<20} {file_value_orig:<30} {db_value_orig:<30} {result:<10}")
            else:
                # 处理其他类型
                if str(file_value) != str(db_value):
                    mismatches.append((file_field, file_value, db_field, db_value))
                    result = "不匹配 ❌"
                else:
                    result = "匹配 ✓"
                print(f"{file_field:<20} {file_value:<30} {db_value:<30} {result:<10}")

    return mismatches

def main():
    """主函数"""
    logger.info("开始上海5月数据等价性验证")

    # 清理测试数据
    clean_test_data()

    # 创建测试数据
    test_data = create_test_data_shanghai_may()
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

    # 3. 比较两种方式的处理结果
    logger.info("比较两种方式的处理结果")

    # 从数据库获取处理后的数据
    db_processed_data = get_performance_data_by_campaign(campaign_id)
    db_processed_data = [data for data in db_processed_data
                        if data.contract_id.startswith('test_equiv_sh_may_')]

    logger.info(f"从数据库获取了 {len(db_processed_data)} 条数据")

    # 从文件获取处理后的数据
    file_data = get_all_records_from_csv(temp_file.name)

    logger.info(f"从文件获取了 {len(file_data)} 条数据")

    # 比较数据数量
    if len(file_data) != len(db_processed_data):
        logger.warning(f"数据数量不一致: 文件={len(file_data)}, 数据库={len(db_processed_data)}")
    else:
        logger.info(f"数据数量一致: {len(file_data)}")

    # 比较每条记录的字段值
    all_mismatches = []

    for file_record in file_data:
        file_contract_id = file_record['合同ID(_id)']

        # 在数据库记录中查找匹配的记录
        db_record = next((data for data in db_processed_data
                         if data.contract_id == file_contract_id), None)

        if db_record is None:
            logger.warning(f"找不到合同ID为 {file_contract_id} 的数据库记录")
            continue

        # 比较字段值
        mismatches = compare_data_fields(file_record, db_record)

        if mismatches:
            logger.warning(f"合同ID为 {file_contract_id} 的记录存在 {len(mismatches)} 处不匹配")
            all_mismatches.extend([(file_contract_id, *mismatch) for mismatch in mismatches])
        else:
            logger.info(f"合同ID为 {file_contract_id} 的记录完全匹配")

    # 4. 生成比较报告
    logger.info("生成比较报告")

    # 将数据库数据转换为与文件数据相同的格式，用于比较工具
    db_data_converted = []
    for db_record in db_processed_data:
        record = {}
        for file_field, db_field in {
            '活动编号': 'campaign_id',
            '合同ID(_id)': 'contract_id',
            '活动城市(province)': 'province_code',
            '工单编号(serviceAppointmentNum)': 'service_appointment_num',
            'Status': 'status',
            '管家(serviceHousekeeper)': 'housekeeper',
            '合同编号(contractdocNum)': 'contract_doc_num',
            '合同金额(adjustRefundMoney)': 'contract_amount',
            '支付金额(paidAmount)': 'paid_amount',
            '差额(difference)': 'difference',
            'State': 'state',
            '创建时间(createTime)': 'create_time',
            '服务商(orgName)': 'org_name',
            '签约时间(signedDate)': 'signed_date',
            'Doorsill': 'doorsill',
            '款项来源类型(tradeIn)': 'trade_in',
            '转化率(conversion)': 'conversion',
            '平均客单价(average)': 'average',
            '活动期内第几个合同': 'contract_number_in_activity',
            '管家累计金额': 'housekeeper_total_amount',
            '管家累计单数': 'housekeeper_contract_count',
            '奖金池': 'bonus_pool',
            '计入业绩金额': 'performance_amount',
            '激活奖励状态': 'reward_status',
            '奖励类型': 'reward_type',
            '奖励名称': 'reward_name',
            '是否发送通知': 'notification_sent',
            '备注': 'remark',
            '登记时间': 'register_time'
        }.items():
            record[file_field] = str(getattr(db_record, db_field)) if getattr(db_record, db_field) is not None else ''
        db_data_converted.append(record)

    # 使用比较工具比较结果
    is_equal, differences = compare_results(file_data, db_data_converted)

    # 保存比较结果
    output_file = 'tests/test_data/shanghai_may_equivalence_results.json'
    save_comparison_results(file_data, db_data_converted, output_file)

    logger.info(f"比较结果已保存到: {output_file}")

    # 5. 输出总结
    if is_equal:
        logger.info("验证结果: 文件存储和数据库存储的处理结果完全一致")
    else:
        logger.warning(f"验证结果: 文件存储和数据库存储的处理结果存在 {len(differences)} 处差异")
        logger.warning(f"差异详情: {differences}")

    if all_mismatches:
        logger.warning(f"字段比较发现 {len(all_mismatches)} 处不匹配")
        for contract_id, file_field, file_value, db_field, db_value in all_mismatches:
            logger.warning(f"合同ID: {contract_id}, 字段: {file_field}, 文件值: {file_value}, 数据库值: {db_value}")
    else:
        logger.info("字段比较未发现不匹配")

    # 6. 清理临时文件
    try:
        os.unlink(temp_file.name)
        logger.info(f"已删除临时文件: {temp_file.name}")
    except Exception as e:
        logger.warning(f"删除临时文件失败: {e}")

    logger.info("上海5月数据等价性验证完成")

if __name__ == "__main__":
    main()
