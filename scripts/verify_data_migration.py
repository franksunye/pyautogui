#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据迁移验证脚本
验证历史签约台账数据从CSV文件迁移到数据库的完整性
"""

import os
import sys
import argparse
import logging
import glob
import csv
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from modules.file_utils import get_all_records_from_csv
from modules.performance_data_manager import (
    get_performance_data_by_contract_id,
    get_performance_data_by_campaign,
    get_all_performance_data
)

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='验证历史签约台账数据从CSV文件迁移到数据库的完整性')
    parser.add_argument('--dir', type=str, default='state', help='CSV文件目录')
    parser.add_argument('--pattern', type=str, default='*.csv', help='CSV文件匹配模式')
    parser.add_argument('--output', type=str, default='migration_verification_report.csv', help='验证报告输出文件')
    parser.add_argument('--verbose', action='store_true', help='显示详细日志')
    return parser.parse_args()

def get_campaign_info(filename):
    """根据文件名获取活动信息"""
    # 从文件名中提取活动信息
    basename = os.path.basename(filename)
    
    # 默认值
    campaign_id = "UNKNOWN"
    
    # 北京5月
    if "BJ-May" in basename or "BJ-05" in basename:
        campaign_id = "BJ-2025-05"
    # 北京4月
    elif "BJ-Apr" in basename or "BJ-04" in basename:
        campaign_id = "BJ-2025-04"
    # 上海5月
    elif "SH-May" in basename or "SH-05" in basename:
        campaign_id = "SH-2025-05"
    # 上海4月
    elif "SH-Apr" in basename or "SH-04" in basename:
        campaign_id = "SH-2025-04"
    
    return campaign_id

def verify_file(filename, verbose=False):
    """验证单个文件的数据迁移"""
    logger.info(f"验证文件: {filename}")
    
    # 获取活动信息
    campaign_id = get_campaign_info(filename)
    logger.info(f"活动ID: {campaign_id}")
    
    # 读取CSV文件
    try:
        file_records = get_all_records_from_csv(filename)
        logger.info(f"从文件中读取了 {len(file_records)} 条记录")
    except Exception as e:
        logger.error(f"读取文件 {filename} 失败: {e}")
        return [], 0, 0, 0
    
    # 获取数据库中的记录
    db_records = get_performance_data_by_campaign(campaign_id)
    logger.info(f"从数据库中读取了 {len(db_records)} 条记录")
    
    # 创建合同ID到记录的映射
    file_records_map = {record['合同ID(_id)']: record for record in file_records}
    db_records_map = {record.contract_id: record for record in db_records}
    
    # 统计
    total_in_file = len(file_records)
    total_in_db = len(db_records)
    matched = 0
    mismatched = []
    
    # 验证每个文件中的记录是否在数据库中
    for contract_id, file_record in file_records_map.items():
        if contract_id in db_records_map:
            db_record = db_records_map[contract_id]
            
            # 验证关键字段
            if (
                str(db_record.contract_amount) == str(file_record['合同金额(adjustRefundMoney)']) and
                db_record.housekeeper == file_record['管家(serviceHousekeeper)'] and
                db_record.contract_doc_num == file_record['合同编号(contractdocNum)']
            ):
                matched += 1
                if verbose:
                    logger.debug(f"记录匹配: {contract_id}")
            else:
                mismatched.append({
                    'contract_id': contract_id,
                    'file_housekeeper': file_record['管家(serviceHousekeeper)'],
                    'db_housekeeper': db_record.housekeeper,
                    'file_contract_amount': file_record['合同金额(adjustRefundMoney)'],
                    'db_contract_amount': db_record.contract_amount,
                    'file_contract_doc_num': file_record['合同编号(contractdocNum)'],
                    'db_contract_doc_num': db_record.contract_doc_num
                })
                if verbose:
                    logger.warning(f"记录不匹配: {contract_id}")
        else:
            mismatched.append({
                'contract_id': contract_id,
                'file_housekeeper': file_record['管家(serviceHousekeeper)'],
                'db_housekeeper': 'N/A',
                'file_contract_amount': file_record['合同金额(adjustRefundMoney)'],
                'db_contract_amount': 'N/A',
                'file_contract_doc_num': file_record['合同编号(contractdocNum)'],
                'db_contract_doc_num': 'N/A'
            })
            if verbose:
                logger.warning(f"记录在数据库中不存在: {contract_id}")
    
    # 计算匹配率
    match_rate = matched / total_in_file * 100 if total_in_file > 0 else 0
    logger.info(f"匹配记录: {matched}/{total_in_file} ({match_rate:.2f}%)")
    
    return mismatched, total_in_file, total_in_db, matched

def verify_all_files(directory, pattern, output_file, verbose=False):
    """验证所有匹配的文件"""
    # 获取所有匹配的文件
    file_pattern = os.path.join(directory, pattern)
    files = glob.glob(file_pattern)
    
    if not files:
        logger.warning(f"没有找到匹配的文件: {file_pattern}")
        return
    
    logger.info(f"找到 {len(files)} 个匹配的文件")
    
    # 验证所有文件
    all_mismatched = []
    total_in_file = 0
    total_in_db = 0
    total_matched = 0
    
    for filename in files:
        mismatched, file_count, db_count, matched = verify_file(filename, verbose)
        all_mismatched.extend(mismatched)
        total_in_file += file_count
        total_in_db += db_count
        total_matched += matched
    
    # 计算总体匹配率
    total_match_rate = total_matched / total_in_file * 100 if total_in_file > 0 else 0
    logger.info(f"总体匹配记录: {total_matched}/{total_in_file} ({total_match_rate:.2f}%)")
    
    # 输出验证报告
    if all_mismatched:
        logger.warning(f"发现 {len(all_mismatched)} 条不匹配的记录，详情见报告: {output_file}")
        write_verification_report(all_mismatched, output_file)
    else:
        logger.info("所有记录都匹配")
    
    # 输出总结
    logger.info(f"验证完成，文件中总记录数: {total_in_file}，数据库中总记录数: {total_in_db}，匹配记录数: {total_matched}")

def write_verification_report(mismatched, output_file):
    """写入验证报告"""
    try:
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'contract_id', 'file_housekeeper', 'db_housekeeper',
                'file_contract_amount', 'db_contract_amount',
                'file_contract_doc_num', 'db_contract_doc_num'
            ])
            writer.writeheader()
            writer.writerows(mismatched)
        logger.info(f"验证报告已写入: {output_file}")
    except Exception as e:
        logger.error(f"写入验证报告失败: {e}")

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("开始验证数据迁移...")
    logger.info(f"参数: 目录={args.dir}, 模式={args.pattern}, 输出={args.output}")
    
    # 验证所有文件
    start_time = datetime.now()
    verify_all_files(args.dir, args.pattern, args.output, args.verbose)
    end_time = datetime.now()
    
    # 输出统计信息
    duration = (end_time - start_time).total_seconds()
    logger.info(f"验证完成，耗时 {duration:.2f} 秒")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
