#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
创建签约台账数据表的脚本
"""

import sqlite3
import logging
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging

# 设置日志
setup_logging()

# 数据库文件路径
DB_FILE = 'tasks.db'

def create_performance_data_table():
    """创建签约台账数据表"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 创建表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id TEXT NOT NULL,
            contract_id TEXT NOT NULL UNIQUE,
            province_code TEXT,
            service_appointment_num TEXT,
            status INTEGER,
            housekeeper TEXT,
            contract_doc_num TEXT,
            contract_amount REAL,
            paid_amount REAL,
            difference REAL,
            state INTEGER,
            create_time TIMESTAMP,
            org_name TEXT,
            signed_date TIMESTAMP,
            doorsill REAL,
            trade_in INTEGER,
            conversion REAL,
            average REAL,
            contract_number_in_activity INTEGER,
            housekeeper_total_amount REAL,
            housekeeper_contract_count INTEGER,
            bonus_pool REAL,
            performance_amount REAL,
            reward_status INTEGER,
            reward_type TEXT,
            reward_name TEXT,
            notification_sent TEXT,
            remark TEXT,
            register_time TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_data_campaign_id ON performance_data(campaign_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_data_housekeeper ON performance_data(housekeeper)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_data_signed_date ON performance_data(signed_date)')
    
    conn.commit()
    conn.close()
    
    logging.info("签约台账数据表创建成功")

def main():
    """主函数"""
    try:
        create_performance_data_table()
        print("签约台账数据表创建成功")
    except Exception as e:
        logging.error(f"创建签约台账数据表时发生错误: {e}")
        print(f"创建签约台账数据表时发生错误: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
