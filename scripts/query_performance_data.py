#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
签约台账数据查询工具
查询数据库中的签约台账数据
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
    get_performance_data_by_id,
    get_performance_data_by_contract_id,
    get_performance_data_by_campaign,
    get_performance_data_by_housekeeper,
    get_performance_data_count
)

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='查询数据库中的签约台账数据')
    
    # 查询选项
    query_group = parser.add_argument_group('查询选项')
    query_group.add_argument('--all', action='store_true', help='查询所有数据')
    query_group.add_argument('--id', type=int, help='按ID查询')
    query_group.add_argument('--contract', type=str, help='按合同ID查询')
    query_group.add_argument('--campaign', type=str, help='按活动ID查询')
    query_group.add_argument('--housekeeper', type=str, help='按管家查询')
    query_group.add_argument('--count', action='store_true', help='只返回记录数量')
    
    # 输出选项
    output_group = parser.add_argument_group('输出选项')
    output_group.add_argument('--output', type=str, help='输出文件路径')
    output_group.add_argument('--format', type=str, choices=['csv', 'json', 'text'], default='text', help='输出格式')
    output_group.add_argument('--limit', type=int, default=100, help='限制输出记录数量')
    
    parser.add_argument('--verbose', action='store_true', help='显示详细日志')
    
    return parser.parse_args()

def query_data(args):
    """查询数据"""
    # 只返回记录数量
    if args.count:
        count = get_performance_data_count()
        logger.info(f"记录数量: {count}")
        return count, None
    
    # 按ID查询
    if args.id:
        logger.info(f"按ID查询: {args.id}")
        data = get_performance_data_by_id(args.id)
        if data:
            return 1, [data]
        else:
            logger.warning(f"未找到ID为 {args.id} 的记录")
            return 0, []
    
    # 按合同ID查询
    if args.contract:
        logger.info(f"按合同ID查询: {args.contract}")
        data = get_performance_data_by_contract_id(args.contract)
        if data:
            return 1, [data]
        else:
            logger.warning(f"未找到合同ID为 {args.contract} 的记录")
            return 0, []
    
    # 按活动ID查询
    if args.campaign:
        logger.info(f"按活动ID查询: {args.campaign}")
        data = get_performance_data_by_campaign(args.campaign)
        if data:
            return len(data), data[:args.limit]
        else:
            logger.warning(f"未找到活动ID为 {args.campaign} 的记录")
            return 0, []
    
    # 按管家查询
    if args.housekeeper:
        logger.info(f"按管家查询: {args.housekeeper}")
        data = get_performance_data_by_housekeeper(args.housekeeper)
        if data:
            return len(data), data[:args.limit]
        else:
            logger.warning(f"未找到管家为 {args.housekeeper} 的记录")
            return 0, []
    
    # 查询所有数据
    if args.all:
        logger.info("查询所有数据")
        data = get_all_performance_data()
        if data:
            return len(data), data[:args.limit]
        else:
            logger.warning("未找到任何记录")
            return 0, []
    
    # 未指定查询选项
    logger.error("未指定查询选项，请使用 --all, --id, --contract, --campaign, --housekeeper 或 --count 选项")
    return 0, []

def format_data_as_text(data):
    """将数据格式化为文本"""
    if not data:
        return "未找到记录"
    
    lines = []
    for item in data:
        lines.append(f"ID: {item.id}")
        lines.append(f"活动ID: {item.campaign_id}")
        lines.append(f"合同ID: {item.contract_id}")
        lines.append(f"省份代码: {item.province_code}")
        lines.append(f"管家: {item.housekeeper}")
        lines.append(f"合同编号: {item.contract_doc_num}")
        lines.append(f"合同金额: {item.contract_amount}")
        lines.append(f"支付金额: {item.paid_amount}")
        lines.append(f"差额: {item.difference}")
        lines.append(f"创建时间: {item.create_time}")
        lines.append(f"服务商: {item.org_name}")
        lines.append(f"签约时间: {item.signed_date}")
        lines.append(f"奖励状态: {item.reward_status}")
        lines.append(f"奖励类型: {item.reward_type}")
        lines.append(f"奖励名称: {item.reward_name}")
        lines.append(f"通知状态: {item.notification_sent}")
        lines.append(f"备注: {item.remark}")
        lines.append("-" * 50)
    
    return "\n".join(lines)

def format_data_as_csv(data):
    """将数据格式化为CSV"""
    if not data:
        return ""
    
    output = []
    
    # 添加标题行
    headers = [
        'ID', '活动ID', '合同ID', '省份代码', '工单编号', '状态', '管家', '合同编号',
        '合同金额', '支付金额', '差额', '状态', '创建时间', '服务商', '签约时间',
        '门槛', '款项来源类型', '转化率', '平均客单价', '活动期内第几个合同',
        '管家累计金额', '管家累计单数', '奖金池', '计入业绩金额',
        '奖励状态', '奖励类型', '奖励名称', '通知状态', '备注', '登记时间'
    ]
    output.append(','.join(headers))
    
    # 添加数据行
    for item in data:
        row = [
            str(item.id), item.campaign_id, item.contract_id, item.province_code,
            item.service_appointment_num, str(item.status), item.housekeeper, item.contract_doc_num,
            str(item.contract_amount), str(item.paid_amount), str(item.difference),
            str(item.state), item.create_time, item.org_name, item.signed_date,
            str(item.doorsill), str(item.trade_in), str(item.conversion), str(item.average),
            str(item.contract_number_in_activity), str(item.housekeeper_total_amount),
            str(item.housekeeper_contract_count), str(item.bonus_pool), str(item.performance_amount),
            str(item.reward_status), item.reward_type, item.reward_name, item.notification_sent,
            item.remark, item.register_time
        ]
        output.append(','.join(row))
    
    return '\n'.join(output)

def format_data_as_json(data):
    """将数据格式化为JSON"""
    if not data:
        return "[]"
    
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
    
    return json.dumps(json_data, indent=2, ensure_ascii=False)

def output_data(count, data, args):
    """输出数据"""
    # 只返回记录数量
    if args.count:
        print(f"记录数量: {count}")
        return
    
    # 格式化数据
    if args.format == 'text':
        formatted_data = format_data_as_text(data)
    elif args.format == 'csv':
        formatted_data = format_data_as_csv(data)
    elif args.format == 'json':
        formatted_data = format_data_as_json(data)
    else:
        logger.error(f"不支持的输出格式: {args.format}")
        return
    
    # 输出数据
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(formatted_data)
            logger.info(f"数据已写入: {args.output}")
        except Exception as e:
            logger.error(f"写入数据失败: {e}")
    else:
        print(f"找到 {count} 条记录，显示前 {min(count, args.limit)} 条:")
        print(formatted_data)

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("开始查询数据...")
    
    # 查询数据
    start_time = datetime.now()
    count, data = query_data(args)
    end_time = datetime.now()
    
    # 输出统计信息
    duration = (end_time - start_time).total_seconds()
    logger.info(f"查询完成，找到 {count} 条记录，耗时 {duration:.2f} 秒")
    
    # 输出数据
    output_data(count, data, args)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
