#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通用数据处理模块
支持文件存储和数据库存储两种模式

该模块提供了通用的数据处理函数，可以处理不同城市和月份的合同数据，
并支持文件存储和数据库存储两种模式。

主要功能：
1. 通用数据处理函数 process_data_generic
2. 北京4月包装函数 process_data_apr_beijing_generic
3. 北京5月包装函数 process_data_may_beijing_generic
4. 上海4月包装函数 process_data_apr_shanghai_generic
5. 上海5月包装函数 process_data_may_shanghai_generic
"""

import logging
from datetime import datetime, date
import os
from modules.log_config import setup_logging
from modules.performance_data_manager import (
    PerformanceData, get_unique_contract_ids
)
from modules.reward_calculation import determine_rewards_generic

# 设置日志
setup_logging()

def process_data_generic(
    contract_data,
    existing_contract_ids,
    housekeeper_award_lists,
    config_key,
    use_database=False,
    campaign_id=None,
    province_code=None,
    use_combined_key=False
):
    """
    通用数据处理函数，支持文件存储和数据库存储两种模式。

    Args:
        contract_data: 合同数据列表
        existing_contract_ids: 已存在的合同ID集合
        housekeeper_award_lists: 管家奖励列表
        config_key: 配置键名，用于从REWARD_CONFIGS中获取对应配置
        use_database: 是否使用数据库存储
        campaign_id: 活动ID，仅在use_database=True时使用
        province_code: 省份代码，仅在use_database=True时使用
        use_combined_key: 是否使用组合键（上海特有的功能）

    Returns:
        如果use_database为False，返回处理后的性能数据列表
        如果use_database为True，返回处理的合同数量
    """
    logging.info(f"Starting generic data processing with {len(existing_contract_ids)} existing contract IDs.")
    logging.debug(f"Config key: {config_key}, Use database: {use_database}")

    if use_database and (campaign_id is None or province_code is None):
        raise ValueError("Campaign ID and province code are required when using database storage")

    # 初始化性能数据列表（文件存储模式使用）
    performance_data = []

    # 初始化处理的合同数量（数据库存储模式使用）
    processed_count = 0

    # 初始化合同计数器，从已存在的合同ID数量开始
    contract_count_in_activity = len(existing_contract_ids) + 1

    # 初始化管家合同数据字典
    housekeeper_contracts = {}

    # 初始化已处理的合同ID集合
    processed_contract_ids = set()

    # 初始化工单编号累计金额字典
    service_appointment_amounts = {}

    # 确定奖金池计算比例（上海使用0.2%的比例计算奖金池）
    bonus_pool_ratio = 0.002 if config_key.startswith("SH-") else 0.0

    # 遍历合同数据
    logging.info("Starting to process contract data...")

    for contract in contract_data:
        # 获取合同ID并转换为字符串
        contract_id = str(contract['合同ID(_id)'])

        # 检查合同ID是否已处理过，如果已经处理过，则跳过当前循环的剩余部分，进入下一次循环
        if contract_id in processed_contract_ids:
            logging.debug(f"Skipping duplicate contract ID: {contract_id}")
            continue

        # 获取管家
        housekeeper = contract['管家(serviceHousekeeper)'].strip()

        # 上海特有的功能：使用组合键（管家+服务商）
        if use_combined_key:
            service_provider = contract['服务商(orgName)'].strip()
            unique_housekeeper_key = f"{housekeeper}_{service_provider}"
        else:
            unique_housekeeper_key = housekeeper

        # 初始化管家合同数据
        if unique_housekeeper_key not in housekeeper_contracts:
            housekeeper_contracts[unique_housekeeper_key] = {
                'count': 0,
                'total_amount': 0.0,
                'performance_amount': 0.0,
                'contracts': [],
                'awarded': []  # 添加awarded字段，用于记录已获得的奖励
            }

        # 更新管家合同数量和当前合同的金额
        housekeeper_contracts[unique_housekeeper_key]['count'] += 1
        current_contract_amount = float(contract['合同金额(adjustRefundMoney)'])

        # 获取工单编号(serviceAppointmentNum)
        service_appointment_num = contract['工单编号(serviceAppointmentNum)']

        # 初始化工单编号累计金额
        if service_appointment_num not in service_appointment_amounts:
            service_appointment_amounts[service_appointment_num] = 0

        # 更新工单编号累计金额
        service_appointment_amounts[service_appointment_num] += current_contract_amount

        # 更新管家合同总金额
        housekeeper_contracts[unique_housekeeper_key]['total_amount'] += current_contract_amount

        # 计算计入业绩金额（根据业务规则，可能有上限）
        # 从配置中获取单个合同金额上限
        from modules.config import REWARD_CONFIGS
        performance_amount_cap = REWARD_CONFIGS[config_key]['performance_limits']['single_contract_cap'] \
            if REWARD_CONFIGS[config_key]['performance_limits']['enable_cap'] else current_contract_amount

        # 计算计入业绩金额
        performance_amount = min(current_contract_amount, performance_amount_cap)

        # 更新管家计入业绩金额
        housekeeper_contracts[unique_housekeeper_key]['performance_amount'] += performance_amount

        # 计算奖励
        reward_types, reward_names, next_reward_gap = determine_rewards_generic(
            contract_count_in_activity,
            housekeeper_contracts[unique_housekeeper_key],
            current_contract_amount,
            config_key
        )

        # 如果合同ID已经存在于已处理的合同ID集合中，则跳过此合同的处理
        if contract_id in existing_contract_ids:
            logging.debug(f"Skipping existing contract ID: {contract_id}")
            processed_contract_ids.add(contract_id)
            continue

        # 设置奖励状态
        active_status = 1 if reward_types else 0

        # 计算奖金池
        bonus_pool = current_contract_amount * bonus_pool_ratio

        # 获取转化率和平均客单价
        conversion = float(contract['转化率(conversion)']) if '转化率(conversion)' in contract and contract['转化率(conversion)'] else 0.0
        average = float(contract['平均客单价(average)']) if '平均客单价(average)' in contract and contract['平均客单价(average)'] else 0.0

        # 根据存储模式处理数据
        if use_database:
            # 数据库存储模式
            performance_data_obj = PerformanceData(
                campaign_id=campaign_id,
                contract_id=contract_id,
                province_code=province_code,
                service_appointment_num=service_appointment_num,
                status=int(contract['Status']) if contract['Status'] else 0,
                housekeeper=housekeeper,
                contract_doc_num=contract['合同编号(contractdocNum)'],
                contract_amount=current_contract_amount,
                paid_amount=float(contract['支付金额(paidAmount)']) if contract['支付金额(paidAmount)'] else 0.0,
                difference=float(contract['差额(difference)']) if contract['差额(difference)'] else 0.0,
                state=int(contract['State']) if contract['State'] else 0,
                create_time=contract['创建时间(createTime)'],
                org_name=contract['服务商(orgName)'],
                signed_date=contract['签约时间(signedDate)'],
                doorsill=float(contract['Doorsill']) if contract['Doorsill'] else 0.0,
                trade_in=int(contract['款项来源类型(tradeIn)']) if contract['款项来源类型(tradeIn)'] else 0,
                conversion=conversion,
                average=average,
                contract_number_in_activity=contract_count_in_activity,
                housekeeper_total_amount=housekeeper_contracts[unique_housekeeper_key]['total_amount'],
                housekeeper_contract_count=housekeeper_contracts[unique_housekeeper_key]['count'],
                bonus_pool=bonus_pool,
                performance_amount=housekeeper_contracts[unique_housekeeper_key]['performance_amount'],
                reward_status=active_status,
                reward_type=reward_types,
                reward_name=reward_names,
                notification_sent="N",  # 默认未发送通知
                remark=next_reward_gap if next_reward_gap else '无',
                register_time=date.today().strftime("%Y-%m-%d")
            )

            # 保存到数据库
            performance_data_obj.save()

            # 更新处理的合同数量
            processed_count += 1
        else:
            # 文件存储模式
            # 构建性能数据记录
            performance_entry = {
                '活动编号': config_key,
                '合同ID(_id)': contract_id,
                '活动城市(province)': contract['活动城市(province)'],
                '工单编号(serviceAppointmentNum)': service_appointment_num,
                'Status': contract['Status'],
                '管家(serviceHousekeeper)': housekeeper,
                '合同编号(contractdocNum)': contract['合同编号(contractdocNum)'],
                '合同金额(adjustRefundMoney)': contract['合同金额(adjustRefundMoney)'],
                '支付金额(paidAmount)': contract['支付金额(paidAmount)'],
                '差额(difference)': contract['差额(difference)'],
                'State': contract['State'],
                '创建时间(createTime)': contract['创建时间(createTime)'],
                '服务商(orgName)': contract['服务商(orgName)'],
                '签约时间(signedDate)': contract['签约时间(signedDate)'],
                'Doorsill': contract['Doorsill'],
                '款项来源类型(tradeIn)': contract['款项来源类型(tradeIn)'],
                '转化率(conversion)': contract['转化率(conversion)'] if '转化率(conversion)' in contract else '',
                '平均客单价(average)': contract['平均客单价(average)'] if '平均客单价(average)' in contract else '',
                '活动期内第几个合同': contract_count_in_activity,
                '管家累计单数': housekeeper_contracts[unique_housekeeper_key]['count'],
                '管家累计金额': housekeeper_contracts[unique_housekeeper_key]['total_amount'],
                '奖金池': bonus_pool,
                '计入业绩金额': housekeeper_contracts[unique_housekeeper_key]['performance_amount'],
                '激活奖励状态': active_status,
                '奖励类型': reward_types,
                '奖励名称': reward_names,
                '是否发送通知': 'N',
                '备注': next_reward_gap if next_reward_gap else '无',
                '登记时间': date.today().strftime("%Y-%m-%d"),
            }

            # 添加到性能数据列表
            performance_data.append(performance_entry)

        # 更新已处理的合同ID集合
        processed_contract_ids.add(contract_id)

        # 更新合同计数器
        contract_count_in_activity += 1

    # 根据存储方式返回不同的结果
    if use_database:
        logging.info(f"Processed {processed_count} contracts to database.")
        return processed_count
    else:
        logging.info(f"Processed {len(performance_data)} contracts to file.")
        return performance_data


def process_data_apr_beijing_generic(contract_data, existing_contract_ids, housekeeper_award_lists, use_database=False):
    """
    使用通用数据处理函数处理2025年4月北京活动的数据。

    Args:
        contract_data: 合同数据列表
        existing_contract_ids: 已存在的合同ID集合
        housekeeper_award_lists: 管家奖励列表
        use_database: 是否使用数据库存储

    Returns:
        如果use_database为False，返回处理后的性能数据列表
        如果use_database为True，返回处理的合同数量
    """
    logging.info("Processing April Beijing data with generic function")
    return process_data_generic(
        contract_data,
        existing_contract_ids,
        housekeeper_award_lists,
        "BJ-2025-04",
        use_database,
        "BJ-2025-04" if use_database else None,
        "110000" if use_database else None,
        False  # 北京不使用组合键
    )


def process_data_may_beijing_generic(contract_data, existing_contract_ids, housekeeper_award_lists, use_database=False):
    """
    使用通用数据处理函数处理2025年5月北京活动的数据。

    Args:
        contract_data: 合同数据列表
        existing_contract_ids: 已存在的合同ID集合
        housekeeper_award_lists: 管家奖励列表
        use_database: 是否使用数据库存储

    Returns:
        如果use_database为False，返回处理后的性能数据列表
        如果use_database为True，返回处理的合同数量
    """
    logging.info("Processing May Beijing data with generic function")
    return process_data_generic(
        contract_data,
        existing_contract_ids,
        housekeeper_award_lists,
        "BJ-2025-05",
        use_database,
        "BJ-2025-05" if use_database else None,
        "110000" if use_database else None,
        False  # 北京不使用组合键
    )


def process_data_apr_shanghai_generic(contract_data, existing_contract_ids, housekeeper_award_lists, use_database=False):
    """
    使用通用数据处理函数处理2025年4月上海活动的数据。

    Args:
        contract_data: 合同数据列表
        existing_contract_ids: 已存在的合同ID集合
        housekeeper_award_lists: 管家奖励列表
        use_database: 是否使用数据库存储

    Returns:
        如果use_database为False，返回处理后的性能数据列表
        如果use_database为True，返回处理的合同数量
    """
    logging.info("Processing April Shanghai data with generic function")
    return process_data_generic(
        contract_data,
        existing_contract_ids,
        housekeeper_award_lists,
        "SH-2025-04",
        use_database,
        "SH-2025-04" if use_database else None,
        "310000" if use_database else None,
        True  # 上海使用组合键
    )


def process_data_may_shanghai_generic(contract_data, existing_contract_ids, housekeeper_award_lists, use_database=False):
    """
    使用通用数据处理函数处理2025年5月上海活动的数据。

    Args:
        contract_data: 合同数据列表
        existing_contract_ids: 已存在的合同ID集合
        housekeeper_award_lists: 管家奖励列表
        use_database: 是否使用数据库存储

    Returns:
        如果use_database为False，返回处理后的性能数据列表
        如果use_database为True，返回处理的合同数量
    """
    logging.info("Processing May Shanghai data with generic function")
    return process_data_generic(
        contract_data,
        existing_contract_ids,
        housekeeper_award_lists,
        "SH-2025-05",
        use_database,
        "SH-2025-05" if use_database else None,
        "310000" if use_database else None,
        True  # 上海使用组合键
    )


# 数据库处理函数的包装函数

def process_beijing_data_to_db_generic(contract_data, campaign_id="BJ-2025-05", province_code="110000"):
    """
    使用通用数据处理函数处理北京合同数据并将结果保存到数据库中。

    这是一个便捷函数，调用通用的process_data_generic函数处理北京的合同数据。
    它使用默认的活动ID和省份代码，简化调用。

    Args:
        contract_data: 合同数据列表，每个元素是一个包含合同信息的字典
        campaign_id: 活动ID，默认为"BJ-2025-05"
        province_code: 省份代码，默认为"110000"（北京）

    Returns:
        int: 处理的合同数量
    """
    logging.info(f"Processing Beijing data to DB with campaign_id={campaign_id}, province_code={province_code}")

    # 从数据库获取已存在的合同ID
    from modules.performance_data_manager import get_unique_contract_ids
    existing_contract_ids = get_unique_contract_ids()

    # 使用通用数据处理函数
    return process_data_generic(
        contract_data,
        existing_contract_ids,
        {},  # 空的管家奖励列表，将在函数内部初始化
        campaign_id,  # 使用活动ID作为配置键
        True,  # 使用数据库存储
        campaign_id,
        province_code,
        campaign_id.startswith("SH-")  # 如果是上海，则使用组合键
    )


def process_shanghai_data_to_db_generic(contract_data, campaign_id="SH-2025-04", province_code="310000"):
    """
    使用通用数据处理函数处理上海合同数据并将结果保存到数据库中。

    这是一个便捷函数，调用通用的process_data_generic函数处理上海的合同数据。
    它使用默认的活动ID和省份代码，简化调用。

    Args:
        contract_data: 合同数据列表，每个元素是一个包含合同信息的字典
        campaign_id: 活动ID，默认为"SH-2025-04"
        province_code: 省份代码，默认为"310000"（上海）

    Returns:
        int: 处理的合同数量
    """
    logging.info(f"Processing Shanghai data to DB with campaign_id={campaign_id}, province_code={province_code}")

    # 从数据库获取已存在的合同ID
    from modules.performance_data_manager import get_unique_contract_ids
    existing_contract_ids = get_unique_contract_ids()

    # 使用通用数据处理函数
    return process_data_generic(
        contract_data,
        existing_contract_ids,
        {},  # 空的管家奖励列表，将在函数内部初始化
        campaign_id,  # 使用活动ID作为配置键
        True,  # 使用数据库存储
        campaign_id,
        province_code,
        True  # 上海使用组合键
    )
