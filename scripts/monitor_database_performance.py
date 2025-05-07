#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库性能监控脚本
监控数据库性能并生成报告
"""

import os
import sys
import argparse
import logging
import time
import sqlite3
import json
import csv
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from modules.db_config import DATABASE_PATH
from modules.performance_data_manager import (
    get_all_performance_data,
    get_performance_data_by_campaign,
    get_performance_data_by_housekeeper,
    get_unique_contract_ids
)

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='监控数据库性能并生成报告')
    parser.add_argument('--output', type=str, default='database_performance_report.csv', help='性能报告输出文件')
    parser.add_argument('--json', type=str, default='database_performance_report.json', help='JSON格式性能报告输出文件')
    parser.add_argument('--iterations', type=int, default=5, help='每个测试的迭代次数')
    parser.add_argument('--verbose', action='store_true', help='显示详细日志')
    return parser.parse_args()

def get_database_size():
    """获取数据库文件大小"""
    try:
        size_bytes = os.path.getsize(DATABASE_PATH)
        size_kb = size_bytes / 1024
        size_mb = size_kb / 1024
        return size_bytes, size_kb, size_mb
    except Exception as e:
        logger.error(f"获取数据库大小失败: {e}")
        return 0, 0, 0

def get_table_count():
    """获取数据库表数量"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        logger.error(f"获取表数量失败: {e}")
        return 0

def get_record_count():
    """获取数据库记录数量"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM performance_data")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        logger.error(f"获取记录数量失败: {e}")
        return 0

def measure_query_time(func, *args, iterations=5):
    """测量查询时间"""
    total_time = 0
    results = []
    
    for i in range(iterations):
        start_time = time.time()
        result = func(*args)
        end_time = time.time()
        
        if isinstance(result, list):
            results = result
        else:
            results = [result]
        
        duration = end_time - start_time
        total_time += duration
        
        logger.debug(f"迭代 {i+1}: {duration:.6f} 秒, 结果数量: {len(results)}")
    
    avg_time = total_time / iterations
    return avg_time, len(results)

def run_performance_tests(iterations=5, verbose=False):
    """运行性能测试"""
    logger.info("开始运行性能测试...")
    
    # 获取数据库信息
    size_bytes, size_kb, size_mb = get_database_size()
    table_count = get_table_count()
    record_count = get_record_count()
    
    logger.info(f"数据库大小: {size_mb:.2f} MB ({size_kb:.2f} KB)")
    logger.info(f"表数量: {table_count}")
    logger.info(f"记录数量: {record_count}")
    
    # 测试结果
    results = []
    
    # 测试1: 获取所有数据
    logger.info("测试1: 获取所有数据")
    avg_time, result_count = measure_query_time(get_all_performance_data, iterations=iterations)
    logger.info(f"平均耗时: {avg_time:.6f} 秒, 结果数量: {result_count}")
    results.append({
        'test_name': '获取所有数据',
        'avg_time': avg_time,
        'result_count': result_count
    })
    
    # 测试2: 按活动ID查询
    logger.info("测试2: 按活动ID查询")
    campaign_ids = ["BJ-2025-05", "BJ-2025-04", "SH-2025-05", "SH-2025-04"]
    for campaign_id in campaign_ids:
        avg_time, result_count = measure_query_time(get_performance_data_by_campaign, campaign_id, iterations=iterations)
        logger.info(f"活动ID {campaign_id} - 平均耗时: {avg_time:.6f} 秒, 结果数量: {result_count}")
        results.append({
            'test_name': f'按活动ID查询 ({campaign_id})',
            'avg_time': avg_time,
            'result_count': result_count
        })
    
    # 测试3: 按管家查询
    logger.info("测试3: 按管家查询")
    housekeepers = ["石王磊", "魏亮", "张晓磊"]
    for housekeeper in housekeepers:
        avg_time, result_count = measure_query_time(get_performance_data_by_housekeeper, housekeeper, iterations=iterations)
        logger.info(f"管家 {housekeeper} - 平均耗时: {avg_time:.6f} 秒, 结果数量: {result_count}")
        results.append({
            'test_name': f'按管家查询 ({housekeeper})',
            'avg_time': avg_time,
            'result_count': result_count
        })
    
    # 测试4: 获取唯一合同ID
    logger.info("测试4: 获取唯一合同ID")
    avg_time, result_count = measure_query_time(get_unique_contract_ids, iterations=iterations)
    logger.info(f"平均耗时: {avg_time:.6f} 秒, 结果数量: {result_count}")
    results.append({
        'test_name': '获取唯一合同ID',
        'avg_time': avg_time,
        'result_count': result_count
    })
    
    # 测试5: 原始SQL查询
    logger.info("测试5: 原始SQL查询")
    
    # 连接数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 测试5.1: 简单查询
    sql = "SELECT * FROM performance_data LIMIT 100"
    total_time = 0
    for i in range(iterations):
        start_time = time.time()
        cursor.execute(sql)
        rows = cursor.fetchall()
        end_time = time.time()
        duration = end_time - start_time
        total_time += duration
        logger.debug(f"迭代 {i+1}: {duration:.6f} 秒, 结果数量: {len(rows)}")
    
    avg_time = total_time / iterations
    logger.info(f"简单查询 - 平均耗时: {avg_time:.6f} 秒, 结果数量: {len(rows)}")
    results.append({
        'test_name': '简单查询 (LIMIT 100)',
        'avg_time': avg_time,
        'result_count': len(rows)
    })
    
    # 测试5.2: 复杂查询
    sql = """
    SELECT campaign_id, housekeeper, COUNT(*) as contract_count, SUM(contract_amount) as total_amount
    FROM performance_data
    GROUP BY campaign_id, housekeeper
    ORDER BY total_amount DESC
    """
    total_time = 0
    for i in range(iterations):
        start_time = time.time()
        cursor.execute(sql)
        rows = cursor.fetchall()
        end_time = time.time()
        duration = end_time - start_time
        total_time += duration
        logger.debug(f"迭代 {i+1}: {duration:.6f} 秒, 结果数量: {len(rows)}")
    
    avg_time = total_time / iterations
    logger.info(f"复杂查询 - 平均耗时: {avg_time:.6f} 秒, 结果数量: {len(rows)}")
    results.append({
        'test_name': '复杂查询 (GROUP BY, ORDER BY)',
        'avg_time': avg_time,
        'result_count': len(rows)
    })
    
    # 关闭数据库连接
    conn.close()
    
    # 返回结果
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'database_size_bytes': size_bytes,
        'database_size_kb': size_kb,
        'database_size_mb': size_mb,
        'table_count': table_count,
        'record_count': record_count,
        'tests': results
    }

def write_csv_report(report, output_file):
    """写入CSV格式的性能报告"""
    try:
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            
            # 写入标题
            writer.writerow(['性能测试报告'])
            writer.writerow([f'生成时间: {report["timestamp"]}'])
            writer.writerow([])
            
            # 写入数据库信息
            writer.writerow(['数据库信息'])
            writer.writerow(['大小 (字节)', '大小 (KB)', '大小 (MB)', '表数量', '记录数量'])
            writer.writerow([
                report['database_size_bytes'],
                f"{report['database_size_kb']:.2f}",
                f"{report['database_size_mb']:.2f}",
                report['table_count'],
                report['record_count']
            ])
            writer.writerow([])
            
            # 写入测试结果
            writer.writerow(['测试结果'])
            writer.writerow(['测试名称', '平均耗时 (秒)', '结果数量'])
            for test in report['tests']:
                writer.writerow([
                    test['test_name'],
                    f"{test['avg_time']:.6f}",
                    test['result_count']
                ])
        
        logger.info(f"CSV报告已写入: {output_file}")
    except Exception as e:
        logger.error(f"写入CSV报告失败: {e}")

def write_json_report(report, output_file):
    """写入JSON格式的性能报告"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        logger.info(f"JSON报告已写入: {output_file}")
    except Exception as e:
        logger.error(f"写入JSON报告失败: {e}")

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("开始监控数据库性能...")
    
    # 运行性能测试
    start_time = datetime.now()
    report = run_performance_tests(iterations=args.iterations, verbose=args.verbose)
    end_time = datetime.now()
    
    # 输出统计信息
    duration = (end_time - start_time).total_seconds()
    logger.info(f"性能测试完成，耗时 {duration:.2f} 秒")
    
    # 写入报告
    write_csv_report(report, args.output)
    write_json_report(report, args.json)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
