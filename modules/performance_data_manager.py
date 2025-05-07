#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
签约台账数据管理模块
提供对签约台账数据的CRUD操作
"""

import sqlite3
import logging
from datetime import datetime
import pandas as pd
from modules.log_config import setup_logging

# 设置日志
setup_logging()

# 数据库文件路径
DB_FILE = 'tasks.db'

class PerformanceData:
    """签约台账数据类"""
    
    def __init__(self, **kwargs):
        """初始化签约台账数据对象"""
        self.id = kwargs.get('id')
        self.campaign_id = kwargs.get('campaign_id')
        self.contract_id = kwargs.get('contract_id')
        self.province_code = kwargs.get('province_code')
        self.service_appointment_num = kwargs.get('service_appointment_num')
        self.status = kwargs.get('status')
        self.housekeeper = kwargs.get('housekeeper')
        self.contract_doc_num = kwargs.get('contract_doc_num')
        self.contract_amount = kwargs.get('contract_amount')
        self.paid_amount = kwargs.get('paid_amount')
        self.difference = kwargs.get('difference')
        self.state = kwargs.get('state')
        self.create_time = kwargs.get('create_time')
        self.org_name = kwargs.get('org_name')
        self.signed_date = kwargs.get('signed_date')
        self.doorsill = kwargs.get('doorsill')
        self.trade_in = kwargs.get('trade_in')
        self.conversion = kwargs.get('conversion')
        self.average = kwargs.get('average')
        self.contract_number_in_activity = kwargs.get('contract_number_in_activity')
        self.housekeeper_total_amount = kwargs.get('housekeeper_total_amount')
        self.housekeeper_contract_count = kwargs.get('housekeeper_contract_count')
        self.bonus_pool = kwargs.get('bonus_pool')
        self.performance_amount = kwargs.get('performance_amount')
        self.reward_status = kwargs.get('reward_status')
        self.reward_type = kwargs.get('reward_type')
        self.reward_name = kwargs.get('reward_name')
        self.notification_sent = kwargs.get('notification_sent')
        self.remark = kwargs.get('remark')
        self.register_time = kwargs.get('register_time')
        self.created_at = kwargs.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.updated_at = kwargs.get('updated_at', self.created_at)
    
    def save(self):
        """保存签约台账数据到数据库"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        if self.id:
            # 更新现有记录
            self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = '''
            UPDATE performance_data SET
                campaign_id = ?, contract_id = ?, province_code = ?, service_appointment_num = ?,
                status = ?, housekeeper = ?, contract_doc_num = ?, contract_amount = ?,
                paid_amount = ?, difference = ?, state = ?, create_time = ?,
                org_name = ?, signed_date = ?, doorsill = ?, trade_in = ?,
                conversion = ?, average = ?, contract_number_in_activity = ?, housekeeper_total_amount = ?,
                housekeeper_contract_count = ?, bonus_pool = ?, performance_amount = ?, reward_status = ?,
                reward_type = ?, reward_name = ?, notification_sent = ?, remark = ?,
                register_time = ?, updated_at = ?
            WHERE id = ?
            '''
            cursor.execute(sql, (
                self.campaign_id, self.contract_id, self.province_code, self.service_appointment_num,
                self.status, self.housekeeper, self.contract_doc_num, self.contract_amount,
                self.paid_amount, self.difference, self.state, self.create_time,
                self.org_name, self.signed_date, self.doorsill, self.trade_in,
                self.conversion, self.average, self.contract_number_in_activity, self.housekeeper_total_amount,
                self.housekeeper_contract_count, self.bonus_pool, self.performance_amount, self.reward_status,
                self.reward_type, self.reward_name, self.notification_sent, self.remark,
                self.register_time, self.updated_at, self.id
            ))
        else:
            # 插入新记录
            sql = '''
            INSERT INTO performance_data (
                campaign_id, contract_id, province_code, service_appointment_num,
                status, housekeeper, contract_doc_num, contract_amount,
                paid_amount, difference, state, create_time,
                org_name, signed_date, doorsill, trade_in,
                conversion, average, contract_number_in_activity, housekeeper_total_amount,
                housekeeper_contract_count, bonus_pool, performance_amount, reward_status,
                reward_type, reward_name, notification_sent, remark,
                register_time, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(sql, (
                self.campaign_id, self.contract_id, self.province_code, self.service_appointment_num,
                self.status, self.housekeeper, self.contract_doc_num, self.contract_amount,
                self.paid_amount, self.difference, self.state, self.create_time,
                self.org_name, self.signed_date, self.doorsill, self.trade_in,
                self.conversion, self.average, self.contract_number_in_activity, self.housekeeper_total_amount,
                self.housekeeper_contract_count, self.bonus_pool, self.performance_amount, self.reward_status,
                self.reward_type, self.reward_name, self.notification_sent, self.remark,
                self.register_time, self.created_at, self.updated_at
            ))
            self.id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return self.id

def get_performance_data_by_id(data_id):
    """根据ID获取签约台账数据"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM performance_data WHERE id = ?', (data_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return PerformanceData(**dict(row))
    return None

def get_performance_data_by_contract_id(contract_id):
    """根据合同ID获取签约台账数据"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM performance_data WHERE contract_id = ?', (contract_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return PerformanceData(**dict(row))
    return None

def get_performance_data_by_campaign(campaign_id):
    """根据活动ID获取签约台账数据列表"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM performance_data WHERE campaign_id = ? ORDER BY signed_date', (campaign_id,))
    rows = cursor.fetchall()
    
    conn.close()
    
    return [PerformanceData(**dict(row)) for row in rows]

def get_performance_data_by_housekeeper(housekeeper, campaign_id=None):
    """根据管家获取签约台账数据列表"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if campaign_id:
        cursor.execute(
            'SELECT * FROM performance_data WHERE housekeeper = ? AND campaign_id = ? ORDER BY signed_date',
            (housekeeper, campaign_id)
        )
    else:
        cursor.execute(
            'SELECT * FROM performance_data WHERE housekeeper = ? ORDER BY signed_date',
            (housekeeper,)
        )
    
    rows = cursor.fetchall()
    
    conn.close()
    
    return [PerformanceData(**dict(row)) for row in rows]

def get_all_performance_data():
    """获取所有签约台账数据"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM performance_data ORDER BY signed_date')
    rows = cursor.fetchall()
    
    conn.close()
    
    return [PerformanceData(**dict(row)) for row in rows]

def delete_performance_data(data_id):
    """删除签约台账数据"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM performance_data WHERE id = ?', (data_id,))
    
    conn.commit()
    conn.close()
    
    return cursor.rowcount > 0

def get_unique_contract_ids():
    """获取所有唯一的合同ID"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT contract_id FROM performance_data')
    rows = cursor.fetchall()
    
    conn.close()
    
    return set(row[0] for row in rows)

def get_performance_data_count():
    """获取签约台账数据总数"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM performance_data')
    count = cursor.fetchone()[0]
    
    conn.close()
    
    return count
