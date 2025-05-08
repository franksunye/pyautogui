#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库工具模块
提供数据库相关的工具函数
"""

import os
import sqlite3
import logging
from modules.log_config import setup_logging

# 设置日志
setup_logging()

# 数据库文件路径
DB_FILE = 'tasks.db'

def get_db_path():
    """获取数据库文件的绝对路径"""
    # 获取当前工作目录
    current_dir = os.getcwd()
    # 构建数据库文件的绝对路径
    db_path = os.path.join(current_dir, DB_FILE)
    return db_path

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_FILE)
    return conn

def execute_query(query, params=None):
    """执行SQL查询"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        conn.commit()
        return cursor.fetchall()
    except Exception as e:
        logging.error(f"执行SQL查询失败: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def execute_update(query, params=None):
    """执行SQL更新"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        logging.error(f"执行SQL更新失败: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
