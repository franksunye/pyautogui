#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库优化脚本
优化数据库性能并生成报告
"""

import os
import sys
import argparse
import logging
import time
import sqlite3
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from modules.db_config import DATABASE_PATH

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='优化数据库性能并生成报告')
    parser.add_argument('--backup', action='store_true', help='在优化前备份数据库')
    parser.add_argument('--backup-dir', type=str, default='backups', help='备份目录')
    parser.add_argument('--report', type=str, default='database_optimization_report.json', help='优化报告输出文件')
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

def backup_database(backup_dir):
    """备份数据库"""
    try:
        # 创建备份目录
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # 生成备份文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f"tasks_backup_{timestamp}.db")
        
        # 复制数据库文件
        import shutil
        shutil.copy2(DATABASE_PATH, backup_file)
        
        logger.info(f"数据库已备份到: {backup_file}")
        return backup_file
    except Exception as e:
        logger.error(f"备份数据库失败: {e}")
        return None

def analyze_database():
    """分析数据库"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # 获取表信息
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        table_info = []
        for table in tables:
            table_name = table[0]
            
            # 获取表记录数
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            record_count = cursor.fetchone()[0]
            
            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            # 获取索引
            cursor.execute(f"PRAGMA index_list({table_name})")
            indexes = cursor.fetchall()
            
            index_info = []
            for index in indexes:
                index_name = index[1]
                
                # 获取索引列
                cursor.execute(f"PRAGMA index_info({index_name})")
                index_columns = cursor.fetchall()
                
                index_info.append({
                    'name': index_name,
                    'unique': bool(index[2]),
                    'columns': [col[2] for col in index_columns]
                })
            
            table_info.append({
                'name': table_name,
                'record_count': record_count,
                'columns': [{'name': col[1], 'type': col[2], 'notnull': bool(col[3]), 'pk': bool(col[5])} for col in columns],
                'indexes': index_info
            })
        
        conn.close()
        return table_info
    except Exception as e:
        logger.error(f"分析数据库失败: {e}")
        return []

def optimize_database():
    """优化数据库"""
    try:
        # 记录优化前的大小
        before_size_bytes, before_size_kb, before_size_mb = get_database_size()
        logger.info(f"优化前数据库大小: {before_size_mb:.2f} MB ({before_size_kb:.2f} KB)")
        
        # 连接数据库
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # 开始优化
        optimizations = []
        
        # 1. 运行VACUUM
        logger.info("运行VACUUM...")
        start_time = time.time()
        cursor.execute("VACUUM")
        end_time = time.time()
        duration = end_time - start_time
        
        optimizations.append({
            'name': 'VACUUM',
            'duration': duration,
            'description': '整理数据库文件，减少文件大小'
        })
        logger.info(f"VACUUM完成，耗时: {duration:.2f} 秒")
        
        # 2. 运行ANALYZE
        logger.info("运行ANALYZE...")
        start_time = time.time()
        cursor.execute("ANALYZE")
        end_time = time.time()
        duration = end_time - start_time
        
        optimizations.append({
            'name': 'ANALYZE',
            'duration': duration,
            'description': '收集统计信息，优化查询计划'
        })
        logger.info(f"ANALYZE完成，耗时: {duration:.2f} 秒")
        
        # 3. 重建索引
        logger.info("重建索引...")
        
        # 获取所有索引
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = cursor.fetchall()
        
        for index in indexes:
            index_name = index[0]
            
            # 获取索引信息
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE name='{index_name}'")
            index_sql = cursor.fetchone()[0]
            
            # 删除并重建索引
            start_time = time.time()
            cursor.execute(f"DROP INDEX IF EXISTS {index_name}")
            cursor.execute(index_sql)
            end_time = time.time()
            duration = end_time - start_time
            
            optimizations.append({
                'name': f'重建索引 {index_name}',
                'duration': duration,
                'description': f'删除并重建索引 {index_name}'
            })
            logger.info(f"重建索引 {index_name} 完成，耗时: {duration:.2f} 秒")
        
        # 提交更改
        conn.commit()
        
        # 关闭数据库连接
        conn.close()
        
        # 记录优化后的大小
        after_size_bytes, after_size_kb, after_size_mb = get_database_size()
        logger.info(f"优化后数据库大小: {after_size_mb:.2f} MB ({after_size_kb:.2f} KB)")
        
        # 计算节省的空间
        saved_bytes = before_size_bytes - after_size_bytes
        saved_kb = before_size_kb - after_size_kb
        saved_mb = before_size_mb - after_size_mb
        
        if saved_bytes > 0:
            logger.info(f"节省了 {saved_mb:.2f} MB ({saved_kb:.2f} KB)")
        else:
            logger.info("数据库大小没有变化")
        
        # 返回优化结果
        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'before_size_bytes': before_size_bytes,
            'before_size_kb': before_size_kb,
            'before_size_mb': before_size_mb,
            'after_size_bytes': after_size_bytes,
            'after_size_kb': after_size_kb,
            'after_size_mb': after_size_mb,
            'saved_bytes': saved_bytes,
            'saved_kb': saved_kb,
            'saved_mb': saved_mb,
            'optimizations': optimizations
        }
    except Exception as e:
        logger.error(f"优化数据库失败: {e}")
        return None

def write_report(report, output_file):
    """写入优化报告"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        logger.info(f"优化报告已写入: {output_file}")
    except Exception as e:
        logger.error(f"写入优化报告失败: {e}")

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("开始优化数据库...")
    
    # 备份数据库
    if args.backup:
        backup_file = backup_database(args.backup_dir)
        if not backup_file:
            logger.warning("数据库备份失败，继续优化...")
    
    # 分析数据库
    logger.info("分析数据库...")
    table_info = analyze_database()
    
    # 优化数据库
    logger.info("优化数据库...")
    start_time = datetime.now()
    optimization_result = optimize_database()
    end_time = datetime.now()
    
    if not optimization_result:
        logger.error("数据库优化失败")
        return 1
    
    # 输出统计信息
    duration = (end_time - start_time).total_seconds()
    logger.info(f"数据库优化完成，耗时 {duration:.2f} 秒")
    
    # 合并报告
    report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'duration': duration,
        'table_info': table_info,
        'optimization_result': optimization_result
    }
    
    # 写入报告
    write_report(report, args.report)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
