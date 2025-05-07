#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据迁移脚本
将历史签约台账数据从CSV文件迁移到数据库
"""

import os
import sys
import argparse
import logging
import glob
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from scripts.create_performance_data_table import create_performance_data_table
from modules.file_utils import get_all_records_from_csv
from modules.data_processing_db_module import process_data_to_db
from modules.performance_data_manager import get_unique_contract_ids, get_performance_data_count

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='将历史签约台账数据从CSV文件迁移到数据库')
    parser.add_argument('--dir', type=str, default='state', help='CSV文件目录')
    parser.add_argument('--pattern', type=str, default='*.csv', help='CSV文件匹配模式')
    parser.add_argument('--dry-run', action='store_true', help='仅模拟运行，不实际迁移数据')
    parser.add_argument('--force', action='store_true', help='强制迁移，即使数据已存在')
    parser.add_argument('--verbose', action='store_true', help='显示详细日志')
    return parser.parse_args()

def get_campaign_info(filename):
    """根据文件名获取活动信息"""
    # 从文件名中提取活动信息
    basename = os.path.basename(filename)
    
    # 默认值
    campaign_id = "UNKNOWN"
    province_code = "000000"
    
    # 北京5月
    if "BJ-May" in basename or "BJ-05" in basename:
        campaign_id = "BJ-2025-05"
        province_code = "110000"
    # 北京4月
    elif "BJ-Apr" in basename or "BJ-04" in basename:
        campaign_id = "BJ-2025-04"
        province_code = "110000"
    # 上海5月
    elif "SH-May" in basename or "SH-05" in basename:
        campaign_id = "SH-2025-05"
        province_code = "310000"
    # 上海4月
    elif "SH-Apr" in basename or "SH-04" in basename:
        campaign_id = "SH-2025-04"
        province_code = "310000"
    
    return campaign_id, province_code

def migrate_file(filename, existing_contract_ids, dry_run=False, force=False, verbose=False):
    """迁移单个文件的数据"""
    logger.info(f"处理文件: {filename}")
    
    # 获取活动信息
    campaign_id, province_code = get_campaign_info(filename)
    logger.info(f"活动ID: {campaign_id}, 省份代码: {province_code}")
    
    # 读取CSV文件
    try:
        records = get_all_records_from_csv(filename)
        logger.info(f"从文件中读取了 {len(records)} 条记录")
    except Exception as e:
        logger.error(f"读取文件 {filename} 失败: {e}")
        return 0
    
    # 如果是仅模拟运行，则不实际迁移数据
    if dry_run:
        logger.info(f"[模拟] 将迁移 {len(records)} 条记录到数据库")
        return len(records)
    
    # 处理数据
    try:
        if force:
            # 强制迁移，忽略已存在的合同ID
            processed_count = process_data_to_db(records, campaign_id, province_code)
        else:
            # 使用已存在的合同ID过滤
            processed_count = process_data_to_db(records, campaign_id, province_code, existing_contract_ids)
        
        logger.info(f"成功迁移 {processed_count} 条记录到数据库")
        return processed_count
    except Exception as e:
        logger.error(f"迁移数据失败: {e}")
        return 0

def migrate_all_files(directory, pattern, dry_run=False, force=False, verbose=False):
    """迁移所有匹配的文件"""
    # 获取所有匹配的文件
    file_pattern = os.path.join(directory, pattern)
    files = glob.glob(file_pattern)
    
    if not files:
        logger.warning(f"没有找到匹配的文件: {file_pattern}")
        return 0
    
    logger.info(f"找到 {len(files)} 个匹配的文件")
    
    # 获取已存在的合同ID
    existing_contract_ids = get_unique_contract_ids() if not force else set()
    logger.info(f"数据库中已有 {len(existing_contract_ids)} 个合同ID")
    
    # 记录迁移前的数据数量
    before_count = get_performance_data_count()
    logger.info(f"迁移前数据库中有 {before_count} 条记录")
    
    # 迁移所有文件
    total_processed = 0
    for filename in files:
        processed = migrate_file(filename, existing_contract_ids, dry_run, force, verbose)
        total_processed += processed
        
        # 更新已存在的合同ID
        if not dry_run and not force:
            existing_contract_ids = get_unique_contract_ids()
    
    # 记录迁移后的数据数量
    if not dry_run:
        after_count = get_performance_data_count()
        logger.info(f"迁移后数据库中有 {after_count} 条记录")
        logger.info(f"数据库中增加了 {after_count - before_count} 条记录")
    
    return total_processed

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("开始数据迁移...")
    logger.info(f"参数: 目录={args.dir}, 模式={args.pattern}, 仅模拟={args.dry_run}, 强制={args.force}")
    
    # 创建数据库表
    if not args.dry_run:
        create_performance_data_table()
    
    # 迁移所有文件
    start_time = datetime.now()
    total_processed = migrate_all_files(args.dir, args.pattern, args.dry_run, args.force, args.verbose)
    end_time = datetime.now()
    
    # 输出统计信息
    duration = (end_time - start_time).total_seconds()
    logger.info(f"数据迁移完成，共处理 {total_processed} 条记录，耗时 {duration:.2f} 秒")
    
    if args.dry_run:
        logger.info("这是一次模拟运行，没有实际迁移数据")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
