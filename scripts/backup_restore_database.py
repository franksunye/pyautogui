#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库备份和恢复脚本
备份和恢复SQLite数据库
"""

import os
import sys
import argparse
import logging
import sqlite3
import shutil
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
    parser = argparse.ArgumentParser(description='备份和恢复SQLite数据库')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 备份命令
    backup_parser = subparsers.add_parser('backup', help='备份数据库')
    backup_parser.add_argument('--output-dir', type=str, default='backups', help='备份目录')
    backup_parser.add_argument('--name', type=str, help='备份文件名（不包含扩展名）')
    
    # 恢复命令
    restore_parser = subparsers.add_parser('restore', help='恢复数据库')
    restore_parser.add_argument('--input', type=str, required=True, help='备份文件路径')
    restore_parser.add_argument('--force', action='store_true', help='强制恢复，不提示确认')
    
    # 列出备份命令
    list_parser = subparsers.add_parser('list', help='列出所有备份')
    list_parser.add_argument('--backup-dir', type=str, default='backups', help='备份目录')
    
    # 验证备份命令
    verify_parser = subparsers.add_parser('verify', help='验证备份')
    verify_parser.add_argument('--input', type=str, required=True, help='备份文件路径')
    
    parser.add_argument('--verbose', action='store_true', help='显示详细日志')
    
    return parser.parse_args()

def get_database_info(db_path):
    """获取数据库信息"""
    try:
        # 获取文件大小
        size_bytes = os.path.getsize(db_path)
        size_kb = size_bytes / 1024
        size_mb = size_kb / 1024
        
        # 获取修改时间
        mod_time = os.path.getmtime(db_path)
        mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取表数量
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]
        
        # 获取记录数量
        record_count = 0
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT count(*) FROM {table_name}")
            record_count += cursor.fetchone()[0]
        
        # 关闭数据库连接
        conn.close()
        
        return {
            'path': db_path,
            'size_bytes': size_bytes,
            'size_kb': size_kb,
            'size_mb': size_mb,
            'mod_time': mod_time,
            'mod_time_str': mod_time_str,
            'table_count': table_count,
            'record_count': record_count
        }
    except Exception as e:
        logger.error(f"获取数据库信息失败: {e}")
        return None

def backup_database(output_dir, name=None):
    """备份数据库"""
    try:
        # 创建备份目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"创建备份目录: {output_dir}")
        
        # 生成备份文件名
        if name:
            backup_file = os.path.join(output_dir, f"{name}.db")
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(output_dir, f"tasks_backup_{timestamp}.db")
        
        # 获取数据库信息
        db_info = get_database_info(DATABASE_PATH)
        if not db_info:
            logger.error("获取数据库信息失败，备份中止")
            return None
        
        logger.info(f"数据库大小: {db_info['size_mb']:.2f} MB")
        logger.info(f"表数量: {db_info['table_count']}")
        logger.info(f"记录数量: {db_info['record_count']}")
        
        # 复制数据库文件
        shutil.copy2(DATABASE_PATH, backup_file)
        logger.info(f"数据库已备份到: {backup_file}")
        
        # 验证备份
        if not verify_backup(backup_file):
            logger.error("备份验证失败，备份可能已损坏")
            return None
        
        return backup_file
    except Exception as e:
        logger.error(f"备份数据库失败: {e}")
        return None

def restore_database(input_file, force=False):
    """恢复数据库"""
    try:
        # 检查备份文件是否存在
        if not os.path.exists(input_file):
            logger.error(f"备份文件不存在: {input_file}")
            return False
        
        # 验证备份
        if not verify_backup(input_file):
            logger.error("备份验证失败，恢复中止")
            return False
        
        # 获取备份信息
        backup_info = get_database_info(input_file)
        if not backup_info:
            logger.error("获取备份信息失败，恢复中止")
            return False
        
        logger.info(f"备份大小: {backup_info['size_mb']:.2f} MB")
        logger.info(f"备份表数量: {backup_info['table_count']}")
        logger.info(f"备份记录数量: {backup_info['record_count']}")
        
        # 获取当前数据库信息
        current_info = get_database_info(DATABASE_PATH)
        if current_info:
            logger.info(f"当前数据库大小: {current_info['size_mb']:.2f} MB")
            logger.info(f"当前数据库表数量: {current_info['table_count']}")
            logger.info(f"当前数据库记录数量: {current_info['record_count']}")
        
        # 确认恢复
        if not force:
            confirm = input("确定要恢复数据库吗？这将覆盖当前数据库。(y/n): ")
            if confirm.lower() != 'y':
                logger.info("恢复操作已取消")
                return False
        
        # 备份当前数据库
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        current_backup = f"tasks_before_restore_{timestamp}.db"
        shutil.copy2(DATABASE_PATH, current_backup)
        logger.info(f"当前数据库已备份到: {current_backup}")
        
        # 恢复数据库
        shutil.copy2(input_file, DATABASE_PATH)
        logger.info(f"数据库已从 {input_file} 恢复")
        
        # 验证恢复
        restored_info = get_database_info(DATABASE_PATH)
        if not restored_info:
            logger.error("获取恢复后的数据库信息失败")
            return False
        
        logger.info(f"恢复后数据库大小: {restored_info['size_mb']:.2f} MB")
        logger.info(f"恢复后数据库表数量: {restored_info['table_count']}")
        logger.info(f"恢复后数据库记录数量: {restored_info['record_count']}")
        
        return True
    except Exception as e:
        logger.error(f"恢复数据库失败: {e}")
        return False

def list_backups(backup_dir):
    """列出所有备份"""
    try:
        # 检查备份目录是否存在
        if not os.path.exists(backup_dir):
            logger.error(f"备份目录不存在: {backup_dir}")
            return []
        
        # 获取所有备份文件
        backup_files = []
        for file in os.listdir(backup_dir):
            if file.endswith('.db'):
                file_path = os.path.join(backup_dir, file)
                backup_info = get_database_info(file_path)
                if backup_info:
                    backup_files.append(backup_info)
        
        # 按修改时间排序
        backup_files.sort(key=lambda x: x['mod_time'], reverse=True)
        
        # 打印备份信息
        if backup_files:
            logger.info(f"找到 {len(backup_files)} 个备份:")
            for i, backup in enumerate(backup_files):
                logger.info(f"{i+1}. {os.path.basename(backup['path'])}")
                logger.info(f"   大小: {backup['size_mb']:.2f} MB")
                logger.info(f"   修改时间: {backup['mod_time_str']}")
                logger.info(f"   表数量: {backup['table_count']}")
                logger.info(f"   记录数量: {backup['record_count']}")
        else:
            logger.info(f"在 {backup_dir} 中没有找到备份")
        
        return backup_files
    except Exception as e:
        logger.error(f"列出备份失败: {e}")
        return []

def verify_backup(backup_file):
    """验证备份"""
    try:
        # 检查备份文件是否存在
        if not os.path.exists(backup_file):
            logger.error(f"备份文件不存在: {backup_file}")
            return False
        
        # 尝试连接数据库
        conn = sqlite3.connect(backup_file)
        cursor = conn.cursor()
        
        # 检查数据库完整性
        cursor.execute("PRAGMA integrity_check")
        integrity_result = cursor.fetchone()[0]
        
        # 检查数据库一致性
        cursor.execute("PRAGMA foreign_key_check")
        foreign_key_result = cursor.fetchall()
        
        # 关闭数据库连接
        conn.close()
        
        # 验证结果
        if integrity_result == 'ok' and not foreign_key_result:
            logger.info(f"备份验证成功: {backup_file}")
            return True
        else:
            logger.error(f"备份验证失败: {backup_file}")
            if integrity_result != 'ok':
                logger.error(f"完整性检查失败: {integrity_result}")
            if foreign_key_result:
                logger.error(f"外键检查失败: {foreign_key_result}")
            return False
    except Exception as e:
        logger.error(f"验证备份失败: {e}")
        return False

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 执行命令
    if args.command == 'backup':
        logger.info("开始备份数据库...")
        backup_file = backup_database(args.output_dir, args.name)
        if backup_file:
            logger.info(f"数据库备份成功: {backup_file}")
            return 0
        else:
            logger.error("数据库备份失败")
            return 1
    
    elif args.command == 'restore':
        logger.info(f"开始从 {args.input} 恢复数据库...")
        if restore_database(args.input, args.force):
            logger.info("数据库恢复成功")
            return 0
        else:
            logger.error("数据库恢复失败")
            return 1
    
    elif args.command == 'list':
        logger.info(f"列出 {args.backup_dir} 中的所有备份...")
        list_backups(args.backup_dir)
        return 0
    
    elif args.command == 'verify':
        logger.info(f"验证备份: {args.input}...")
        if verify_backup(args.input):
            logger.info("备份验证成功")
            return 0
        else:
            logger.error("备份验证失败")
            return 1
    
    else:
        logger.error("未指定命令，请使用 backup, restore, list 或 verify 命令")
        return 1

if __name__ == '__main__':
    sys.exit(main())
