#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
结果比较模块
用于比较文件存储和数据库存储两种模式的结果
"""

import logging
from datetime import datetime
import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from modules.log_config import setup_logging

# 设置日志
setup_logging()

def convert_db_result_to_file_format(db_results):
    """
    将数据库结果转换为与文件格式相同的格式
    
    Args:
        db_results: 数据库结果列表，每个元素是一个PerformanceData对象
        
    Returns:
        file_format_results: 转换后的结果列表，每个元素是一个字典，格式与文件存储相同
    """
    file_format_results = []
    
    for db_result in db_results:
        # 创建与文件格式相同的字典
        file_format_result = {
            '活动编号': db_result.campaign_id,
            '合同ID(_id)': db_result.contract_id,
            '活动城市(province)': db_result.province_code,
            '工单编号(serviceAppointmentNum)': db_result.service_appointment_num,
            'Status': str(db_result.status),
            '管家(serviceHousekeeper)': db_result.housekeeper,
            '合同编号(contractdocNum)': db_result.contract_doc_num,
            '合同金额(adjustRefundMoney)': str(db_result.contract_amount),
            '支付金额(paidAmount)': str(db_result.paid_amount),
            '差额(difference)': str(db_result.difference),
            'State': str(db_result.state),
            '创建时间(createTime)': db_result.create_time,
            '服务商(orgName)': db_result.org_name,
            '签约时间(signedDate)': db_result.signed_date,
            'Doorsill': str(db_result.doorsill),
            '款项来源类型(tradeIn)': str(db_result.trade_in),
            '转化率(conversion)': str(db_result.conversion),
            '平均客单价(average)': str(db_result.average),
            '活动期内第几个合同': db_result.contract_number_in_activity,
            '管家累计单数': db_result.housekeeper_contract_count,
            '管家累计金额': db_result.housekeeper_total_amount,
            '奖金池': db_result.bonus_pool,
            '计入业绩金额': db_result.performance_amount,
            '激活奖励状态': db_result.reward_status,
            '奖励类型': db_result.reward_type,
            '奖励名称': db_result.reward_name,
            '是否发送通知': db_result.notification_sent,
            '备注': db_result.remark,
            '登记时间': db_result.register_time
        }
        
        file_format_results.append(file_format_result)
    
    return file_format_results

def compare_results(original_results, new_results, detailed=True):
    """
    比较原始实现和新实现的结果
    
    Args:
        original_results: 原始实现结果列表，每个元素是一个字典
        new_results: 新实现结果列表，每个元素是一个字典
        detailed: 是否输出详细比较结果，默认为True
        
    Returns:
        is_equal: 两种结果是否相等
        differences: 差异列表，每个元素是一个字符串，描述一个差异
    """
    # 按合同ID对结果进行排序
    original_results = sorted(original_results, key=lambda x: x['合同ID(_id)'])
    new_results = sorted(new_results, key=lambda x: x['合同ID(_id)'])
    
    # 检查结果数量是否相同
    if len(original_results) != len(new_results):
        logging.warning(f"结果数量不同: 原始实现 {len(original_results)}, 新实现 {len(new_results)}")
        return False, [f"结果数量不同: 原始实现 {len(original_results)}, 新实现 {len(new_results)}"]
    
    # 比较每个结果
    is_equal = True
    differences = []
    
    for i, (original_result, new_result) in enumerate(zip(original_results, new_results)):
        # 获取合同ID
        contract_id = original_result['合同ID(_id)']
        
        # 检查合同ID是否相同
        if contract_id != new_result['合同ID(_id)']:
            is_equal = False
            diff_msg = f"合同ID不同: 原始实现 {contract_id}, 新实现 {new_result['合同ID(_id)']}"
            differences.append(diff_msg)
            logging.warning(diff_msg)
            continue
        
        # 比较每个字段
        for key in original_result:
            # 跳过不需要比较的字段
            if key in ['是否发送通知', '登记时间']:
                continue
            
            # 获取字段值
            original_value = original_result[key]
            new_value = new_result[key]
            
            # 对于数值字段，转换为浮点数进行比较
            if key in ['合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'Doorsill', '管家累计金额', '奖金池', '计入业绩金额']:
                try:
                    original_value = float(original_value) if original_value else 0.0
                    new_value = float(new_value) if new_value else 0.0
                    
                    # 允许小数点后两位的误差
                    if abs(original_value - new_value) > 0.01:
                        is_equal = False
                        diff_msg = f"合同 {contract_id} 的 {key} 不同: 原始实现 {original_value}, 新实现 {new_value}"
                        differences.append(diff_msg)
                        if detailed:
                            logging.warning(diff_msg)
                except (ValueError, TypeError):
                    is_equal = False
                    diff_msg = f"合同 {contract_id} 的 {key} 无法转换为浮点数: 原始实现 {original_value}, 新实现 {new_value}"
                    differences.append(diff_msg)
                    if detailed:
                        logging.warning(diff_msg)
            # 对于整数字段，转换为整数进行比较
            elif key in ['Status', 'State', '活动期内第几个合同', '管家累计单数', '激活奖励状态']:
                try:
                    original_value = int(original_value) if original_value else 0
                    new_value = int(new_value) if new_value else 0
                    
                    if original_value != new_value:
                        is_equal = False
                        diff_msg = f"合同 {contract_id} 的 {key} 不同: 原始实现 {original_value}, 新实现 {new_value}"
                        differences.append(diff_msg)
                        if detailed:
                            logging.warning(diff_msg)
                except (ValueError, TypeError):
                    is_equal = False
                    diff_msg = f"合同 {contract_id} 的 {key} 无法转换为整数: 原始实现 {original_value}, 新实现 {new_value}"
                    differences.append(diff_msg)
                    if detailed:
                        logging.warning(diff_msg)
            # 对于字符串字段，直接比较
            else:
                if str(original_value) != str(new_value):
                    is_equal = False
                    diff_msg = f"合同 {contract_id} 的 {key} 不同: 原始实现 {original_value}, 新实现 {new_value}"
                    differences.append(diff_msg)
                    if detailed:
                        logging.warning(diff_msg)
    
    # 输出比较结果
    if is_equal:
        logging.info("原始实现和新实现的结果完全一致")
    else:
        logging.warning(f"原始实现和新实现的结果存在 {len(differences)} 处差异")
        if detailed:
            for i, diff in enumerate(differences):
                logging.warning(f"差异 {i+1}: {diff}")
    
    return is_equal, differences

def compare_db_results(original_db_results, new_db_results, detailed=True):
    """
    比较原始实现和新实现的数据库结果
    
    Args:
        original_db_results: 原始实现数据库结果列表，每个元素是一个PerformanceData对象
        new_db_results: 新实现数据库结果列表，每个元素是一个PerformanceData对象
        detailed: 是否输出详细比较结果，默认为True
        
    Returns:
        is_equal: 两种结果是否相等
        differences: 差异列表，每个元素是一个字符串，描述一个差异
    """
    # 将数据库结果转换为与文件格式相同的格式
    original_results = convert_db_result_to_file_format(original_db_results)
    new_results = convert_db_result_to_file_format(new_db_results)
    
    # 比较结果
    return compare_results(original_results, new_results, detailed)

def save_comparison_results(original_results, new_results, output_file):
    """
    保存比较结果到文件
    
    Args:
        original_results: 原始实现结果列表，每个元素是一个字典
        new_results: 新实现结果列表，每个元素是一个字典
        output_file: 输出文件路径
        
    Returns:
        is_equal: 两种结果是否相等
    """
    # 比较结果
    is_equal, differences = compare_results(original_results, new_results, detailed=False)
    
    # 按合同ID对结果进行排序
    original_results = sorted(original_results, key=lambda x: x['合同ID(_id)'])
    new_results = sorted(new_results, key=lambda x: x['合同ID(_id)'])
    
    # 构建比较结果
    comparison_result = {
        "is_equal": is_equal,
        "differences_count": len(differences),
        "differences": differences,
        "original_results_count": len(original_results),
        "new_results_count": len(new_results),
        "comparison_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original_results": original_results,
        "new_results": new_results
    }
    
    # 保存比较结果到文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(comparison_result, f, ensure_ascii=False, indent=2)
    
    logging.info(f"比较结果已保存到 {output_file}")
    
    return is_equal
