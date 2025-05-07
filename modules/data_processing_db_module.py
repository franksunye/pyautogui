#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据处理模块的数据库版本
处理合同数据并将结果保存到数据库中
"""

import logging
from datetime import datetime
import sys
import os
from modules.log_config import setup_logging
from modules.performance_data_manager import (
    PerformanceData, get_performance_data_by_contract_id, get_unique_contract_ids
)

# 设置日志
setup_logging()

def process_data_to_db(contract_data, campaign_id, province_code, existing_contract_ids=None):
    """
    处理合同数据并将结果保存到数据库中

    Args:
        contract_data: 合同数据列表
        campaign_id: 活动ID，如"BJ-2025-05"
        province_code: 省份代码，如"110000"
        existing_contract_ids: 已存在的合同ID集合

    Returns:
        processed_count: 处理的合同数量
    """
    if existing_contract_ids is None:
        # 如果没有提供已存在的合同ID集合，则从数据库中获取
        existing_contract_ids = get_unique_contract_ids()

    logging.info(f"Starting data processing with {len(existing_contract_ids)} existing contract IDs.")

    # 初始化合同计数器，从已存在的合同ID数量开始
    contract_count_in_activity = len(existing_contract_ids) + 1

    # 初始化管家合同数据字典
    housekeeper_contracts = {}

    # 初始化已处理的合同ID集合
    processed_contract_ids = set()

    # 处理的合同数量
    processed_count = 0

    # 遍历合同数据
    logging.info("Starting to process contract data...")

    for contract in contract_data:
        # 获取合同ID
        contract_id = contract['合同ID(_id)'].strip()

        # 如果合同ID已经存在于已处理的合同ID集合中，则跳过此合同的处理
        if contract_id in processed_contract_ids:
            logging.debug(f"Skipping duplicate contract ID: {contract_id}")
            continue

        # 如果合同ID已经存在于已存在的合同ID集合中，则跳过此合同的处理
        if contract_id in existing_contract_ids:
            logging.debug(f"Skipping existing contract ID: {contract_id}")
            continue

        # 获取管家
        housekeeper = contract['管家(serviceHousekeeper)'].strip()

        # 获取合同金额
        contract_amount = float(contract['合同金额(adjustRefundMoney)']) if contract['合同金额(adjustRefundMoney)'] else 0.0

        # 获取支付金额
        paid_amount = float(contract['支付金额(paidAmount)']) if contract['支付金额(paidAmount)'] else 0.0

        # 计算差额
        difference = float(contract['差额(difference)']) if contract['差额(difference)'] else 0.0

        # 获取门槛金额
        doorsill = float(contract['Doorsill']) if contract['Doorsill'] else 0.0

        # 初始化管家合同数据
        if housekeeper not in housekeeper_contracts:
            housekeeper_contracts[housekeeper] = {
                'count': 0,
                'total_amount': 0.0,
                'performance_amount': 0.0,
                'contracts': []
            }

        # 更新管家合同数据
        housekeeper_contracts[housekeeper]['count'] += 1
        housekeeper_contracts[housekeeper]['total_amount'] += contract_amount

        # 计算计入业绩金额（根据业务规则，可能有上限）
        # 北京和上海的业绩金额上限可能不同，这里使用通用的10万上限
        performance_amount = min(contract_amount, 100000)  # 假设上限为10万
        housekeeper_contracts[housekeeper]['performance_amount'] += performance_amount

        # 计算奖励状态、类型和名称（这里简化处理，实际应根据业务规则计算）
        reward_status = 0
        reward_type = ""
        reward_name = ""

        # 计算奖金池（这里简化处理，实际应根据业务规则计算）
        # 上海使用0.2%的比例计算奖金池
        bonus_pool = contract_amount * 0.002 if campaign_id.startswith("SH-") else 0.0

        # 计算备注（这里简化处理，实际应根据业务规则计算）
        remark = f"距离达成节节高奖励条件还需 {max(5 - housekeeper_contracts[housekeeper]['count'], 0)} 单"

        # 获取转化率和平均客单价
        conversion = float(contract['转化率(conversion)']) if contract['转化率(conversion)'] else 0.0
        average = float(contract['平均客单价(average)']) if contract['平均客单价(average)'] else 0.0

        # 创建签约台账数据对象
        performance_data = PerformanceData(
            campaign_id=campaign_id,
            contract_id=contract_id,
            province_code=province_code,
            service_appointment_num=contract['工单编号(serviceAppointmentNum)'],
            status=int(contract['Status']) if contract['Status'] else 0,
            housekeeper=housekeeper,
            contract_doc_num=contract['合同编号(contractdocNum)'],
            contract_amount=contract_amount,
            paid_amount=paid_amount,
            difference=difference,
            state=int(contract['State']) if contract['State'] else 0,
            create_time=contract['创建时间(createTime)'],
            org_name=contract['服务商(orgName)'],
            signed_date=contract['签约时间(signedDate)'],
            doorsill=doorsill,
            trade_in=int(contract['款项来源类型(tradeIn)']) if contract['款项来源类型(tradeIn)'] else 0,
            conversion=conversion,
            average=average,
            contract_number_in_activity=contract_count_in_activity,
            housekeeper_total_amount=housekeeper_contracts[housekeeper]['total_amount'],
            housekeeper_contract_count=housekeeper_contracts[housekeeper]['count'],
            bonus_pool=bonus_pool,
            performance_amount=performance_amount,
            reward_status=reward_status,
            reward_type=reward_type,
            reward_name=reward_name,
            notification_sent="N",  # 默认未发送通知
            remark=remark,
            register_time=datetime.now().strftime('%Y-%m-%d')
        )

        # 保存到数据库
        performance_data.save()

        # 更新已处理的合同ID集合
        processed_contract_ids.add(contract_id)

        # 更新合同计数器
        contract_count_in_activity += 1

        # 更新处理的合同数量
        processed_count += 1

    logging.info(f"Processed {processed_count} contracts.")

    return processed_count

def process_beijing_data_to_db(contract_data, campaign_id="BJ-2025-05", province_code="110000"):
    """
    处理北京合同数据并将结果保存到数据库中

    Args:
        contract_data: 合同数据列表
        campaign_id: 活动ID，默认为"BJ-2025-05"
        province_code: 省份代码，默认为"110000"

    Returns:
        processed_count: 处理的合同数量
    """
    logging.info(f"Processing Beijing data to DB with campaign_id={campaign_id}, province_code={province_code}")
    return process_data_to_db(contract_data, campaign_id, province_code)

def process_shanghai_data_to_db(contract_data, campaign_id="SH-2025-04", province_code="310000"):
    """
    处理上海合同数据并将结果保存到数据库中

    Args:
        contract_data: 合同数据列表
        campaign_id: 活动ID，默认为"SH-2025-04"
        province_code: 省份代码，默认为"310000"

    Returns:
        processed_count: 处理的合同数量
    """
    return process_data_to_db(contract_data, campaign_id, province_code)

def import_csv_to_db(csv_file, campaign_id, province_code):
    """
    从CSV文件导入数据到数据库

    Args:
        csv_file: CSV文件路径
        campaign_id: 活动ID，如"BJ-2025-05"
        province_code: 省份代码，如"110000"

    Returns:
        success: 是否成功
    """
    import csv

    if not os.path.exists(csv_file):
        logging.error(f"CSV文件不存在: {csv_file}")
        return False

    try:
        # 读取CSV文件
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            logging.warning(f"CSV文件为空: {csv_file}")
            return False

        # 处理数据并保存到数据库
        processed_count = process_data_to_db(rows, campaign_id, province_code)

        logging.info(f"成功导入 {processed_count} 条记录: {csv_file}")
        return True

    except Exception as e:
        logging.error(f"导入数据失败: {e}")
        return False
