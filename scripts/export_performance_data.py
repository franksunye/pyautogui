#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
签约台账数据导出工具
将数据库中的签约台账数据导出为CSV或JSON格式
"""

import os
import sys
import argparse
import logging
import csv
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from modules.performance_data_manager import (
    get_all_performance_data,
    get_performance_data_by_campaign,
    get_performance_data_by_housekeeper,
    get_performance_data_count
)

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='将数据库中的签约台账数据导出为CSV或JSON格式')
    
    # 查询选项
    query_group = parser.add_argument_group('查询选项')
    query_group.add_argument('--all', action='store_true', help='导出所有数据')
    query_group.add_argument('--campaign', type=str, help='按活动ID导出')
    query_group.add_argument('--housekeeper', type=str, help='按管家导出')
    
    # 输出选项
    output_group = parser.add_argument_group('输出选项')
    output_group.add_argument('--output', type=str, required=True, help='输出文件路径')
    output_group.add_argument('--format', type=str, choices=['csv', 'json'], default='csv', help='输出格式')
    
    parser.add_argument('--verbose', action='store_true', help='显示详细日志')
    
    return parser.parse_args()

def query_data(args):
    """查询数据"""
    # 按活动ID查询
    if args.campaign:
        logger.info(f"按活动ID查询: {args.campaign}")
        data = get_performance_data_by_campaign(args.campaign)
        if data:
            return len(data), data
        else:
            logger.warning(f"未找到活动ID为 {args.campaign} 的记录")
            return 0, []
    
    # 按管家查询
    if args.housekeeper:
        logger.info(f"按管家查询: {args.housekeeper}")
        data = get_performance_data_by_housekeeper(args.housekeeper)
        if data:
            return len(data), data
        else:
            logger.warning(f"未找到管家为 {args.housekeeper} 的记录")
            return 0, []
    
    # 查询所有数据
    if args.all:
        logger.info("查询所有数据")
        data = get_all_performance_data()
        if data:
            return len(data), data
        else:
            logger.warning("未找到任何记录")
            return 0, []
    
    # 未指定查询选项
    logger.error("未指定查询选项，请使用 --all, --campaign 或 --housekeeper 选项")
    return 0, []

def export_as_csv(data, output_file):
    """导出为CSV格式"""
    try:
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            # 定义CSV标题
            fieldnames = [
                'ID', '活动ID', '合同ID', '省份代码', '工单编号', '状态', '管家', '合同编号',
                '合同金额', '支付金额', '差额', '状态值', '创建时间', '服务商', '签约时间',
                '门槛', '款项来源类型', '转化率', '平均客单价', '活动期内第几个合同',
                '管家累计金额', '管家累计单数', '奖金池', '计入业绩金额',
                '奖励状态', '奖励类型', '奖励名称', '通知状态', '备注', '登记时间'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            # 写入数据
            for item in data:
                writer.writerow({
                    'ID': item.id,
                    '活动ID': item.campaign_id,
                    '合同ID': item.contract_id,
                    '省份代码': item.province_code,
                    '工单编号': item.service_appointment_num,
                    '状态': item.status,
                    '管家': item.housekeeper,
                    '合同编号': item.contract_doc_num,
                    '合同金额': item.contract_amount,
                    '支付金额': item.paid_amount,
                    '差额': item.difference,
                    '状态值': item.state,
                    '创建时间': item.create_time,
                    '服务商': item.org_name,
                    '签约时间': item.signed_date,
                    '门槛': item.doorsill,
                    '款项来源类型': item.trade_in,
                    '转化率': item.conversion,
                    '平均客单价': item.average,
                    '活动期内第几个合同': item.contract_number_in_activity,
                    '管家累计金额': item.housekeeper_total_amount,
                    '管家累计单数': item.housekeeper_contract_count,
                    '奖金池': item.bonus_pool,
                    '计入业绩金额': item.performance_amount,
                    '奖励状态': item.reward_status,
                    '奖励类型': item.reward_type,
                    '奖励名称': item.reward_name,
                    '通知状态': item.notification_sent,
                    '备注': item.remark,
                    '登记时间': item.register_time
                })
        
        logger.info(f"数据已导出为CSV格式: {output_file}")
        return True
    except Exception as e:
        logger.error(f"导出CSV失败: {e}")
        return False

def export_as_json(data, output_file):
    """导出为JSON格式"""
    try:
        json_data = []
        for item in data:
            json_data.append({
                'id': item.id,
                'campaign_id': item.campaign_id,
                'contract_id': item.contract_id,
                'province_code': item.province_code,
                'service_appointment_num': item.service_appointment_num,
                'status': item.status,
                'housekeeper': item.housekeeper,
                'contract_doc_num': item.contract_doc_num,
                'contract_amount': item.contract_amount,
                'paid_amount': item.paid_amount,
                'difference': item.difference,
                'state': item.state,
                'create_time': item.create_time,
                'org_name': item.org_name,
                'signed_date': item.signed_date,
                'doorsill': item.doorsill,
                'trade_in': item.trade_in,
                'conversion': item.conversion,
                'average': item.average,
                'contract_number_in_activity': item.contract_number_in_activity,
                'housekeeper_total_amount': item.housekeeper_total_amount,
                'housekeeper_contract_count': item.housekeeper_contract_count,
                'bonus_pool': item.bonus_pool,
                'performance_amount': item.performance_amount,
                'reward_status': item.reward_status,
                'reward_type': item.reward_type,
                'reward_name': item.reward_name,
                'notification_sent': item.notification_sent,
                'remark': item.remark,
                'register_time': item.register_time
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"数据已导出为JSON格式: {output_file}")
        return True
    except Exception as e:
        logger.error(f"导出JSON失败: {e}")
        return False

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("开始导出数据...")
    
    # 查询数据
    start_time = datetime.now()
    count, data = query_data(args)
    
    if count == 0:
        logger.error("未找到数据，导出中止")
        return 1
    
    # 导出数据
    if args.format == 'csv':
        success = export_as_csv(data, args.output)
    elif args.format == 'json':
        success = export_as_json(data, args.output)
    else:
        logger.error(f"不支持的输出格式: {args.format}")
        return 1
    
    end_time = datetime.now()
    
    # 输出统计信息
    duration = (end_time - start_time).total_seconds()
    if success:
        logger.info(f"导出完成，共导出 {count} 条记录，耗时 {duration:.2f} 秒")
        return 0
    else:
        logger.error("导出失败")
        return 1

if __name__ == '__main__':
    sys.exit(main())
