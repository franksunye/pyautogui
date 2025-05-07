#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单元测试：签约台账数据库功能
测试数据库表创建和数据管理模块
"""

import os
import sys
import unittest
import sqlite3
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from scripts.create_performance_data_table import create_performance_data_table
from modules.performance_data_manager import (
    PerformanceData, get_performance_data_by_id, get_performance_data_by_contract_id,
    get_performance_data_by_campaign, get_performance_data_by_housekeeper,
    get_all_performance_data, delete_performance_data, get_unique_contract_ids,
    get_performance_data_count
)

# 设置日志
setup_logging()

class TestPerformanceDataDBUnit(unittest.TestCase):
    """单元测试：签约台账数据库功能"""

    @classmethod
    def setUpClass(cls):
        """测试前的准备工作"""
        # 创建数据库表
        create_performance_data_table()
        
        # 记录初始数据数量
        cls.initial_count = get_performance_data_count()
        
        # 创建测试数据
        cls.test_data = PerformanceData(
            campaign_id="TEST-2025-05",
            contract_id="test_unit_001",
            province_code="110000",
            service_appointment_num="GD2025045495",
            status=1,
            housekeeper="测试管家",
            contract_doc_num="YHWX-TEST-2025050001",
            contract_amount=30000.0,
            paid_amount=15000.0,
            difference=15000.0,
            state=1,
            create_time="2025-05-01T11:36:22.444+08:00",
            org_name="测试服务商",
            signed_date="2025-05-01T11:42:07.904+08:00",
            doorsill=15000.0,
            trade_in=1,
            conversion=0.5,
            average=30000.0,
            contract_number_in_activity=1,
            housekeeper_total_amount=30000.0,
            housekeeper_contract_count=1,
            bonus_pool=60.0,
            performance_amount=30000.0,
            reward_status=1,
            reward_type="58",
            reward_name="接好运万元以上",
            notification_sent="N",
            remark="测试备注",
            register_time="2025-05-06"
        )
        
        # 保存测试数据
        cls.test_data_id = cls.test_data.save()
        
        # 创建第二条测试数据
        cls.test_data2 = PerformanceData(
            campaign_id="TEST-2025-05",
            contract_id="test_unit_002",
            province_code="110000",
            service_appointment_num="GD2025045496",
            status=1,
            housekeeper="测试管家",
            contract_doc_num="YHWX-TEST-2025050002",
            contract_amount=20000.0,
            paid_amount=10000.0,
            difference=10000.0,
            state=1,
            create_time="2025-05-02T11:36:22.444+08:00",
            org_name="测试服务商",
            signed_date="2025-05-02T11:42:07.904+08:00",
            doorsill=10000.0,
            trade_in=1,
            conversion=0.5,
            average=20000.0,
            contract_number_in_activity=2,
            housekeeper_total_amount=50000.0,
            housekeeper_contract_count=2,
            bonus_pool=40.0,
            performance_amount=20000.0,
            reward_status=1,
            reward_type="58",
            reward_name="接好运万元以上",
            notification_sent="N",
            remark="测试备注2",
            register_time="2025-05-06"
        )
        
        # 保存第二条测试数据
        cls.test_data2_id = cls.test_data2.save()

    @classmethod
    def tearDownClass(cls):
        """测试后的清理工作"""
        # 删除测试数据
        delete_performance_data(cls.test_data_id)
        delete_performance_data(cls.test_data2_id)

    def test_01_table_creation(self):
        """测试数据库表创建"""
        # 连接数据库
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='performance_data'")
        table_exists = cursor.fetchone() is not None
        
        # 检查索引是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_performance_data_campaign_id'")
        index1_exists = cursor.fetchone() is not None
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_performance_data_housekeeper'")
        index2_exists = cursor.fetchone() is not None
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_performance_data_signed_date'")
        index3_exists = cursor.fetchone() is not None
        
        conn.close()
        
        # 验证表和索引是否存在
        self.assertTrue(table_exists, "表 performance_data 应该存在")
        self.assertTrue(index1_exists, "索引 idx_performance_data_campaign_id 应该存在")
        self.assertTrue(index2_exists, "索引 idx_performance_data_housekeeper 应该存在")
        self.assertTrue(index3_exists, "索引 idx_performance_data_signed_date 应该存在")

    def test_02_data_insertion(self):
        """测试数据插入"""
        # 验证数据是否成功插入
        self.assertIsNotNone(self.test_data_id, "测试数据ID不应该为None")
        self.assertIsNotNone(self.test_data2_id, "测试数据2ID不应该为None")
        
        # 验证数据数量是否增加了2
        current_count = get_performance_data_count()
        self.assertEqual(current_count, self.initial_count + 2, "数据数量应该增加2")

    def test_03_data_retrieval_by_id(self):
        """测试按ID查询数据"""
        # 按ID查询数据
        data = get_performance_data_by_id(self.test_data_id)
        
        # 验证数据是否正确
        self.assertIsNotNone(data, "应该能够按ID查询到数据")
        self.assertEqual(data.contract_id, "test_unit_001", "合同ID应该是test_unit_001")
        self.assertEqual(data.campaign_id, "TEST-2025-05", "活动ID应该是TEST-2025-05")
        self.assertEqual(data.housekeeper, "测试管家", "管家应该是测试管家")
        self.assertEqual(data.contract_amount, 30000.0, "合同金额应该是30000.0")

    def test_04_data_retrieval_by_contract_id(self):
        """测试按合同ID查询数据"""
        # 按合同ID查询数据
        data = get_performance_data_by_contract_id("test_unit_001")
        
        # 验证数据是否正确
        self.assertIsNotNone(data, "应该能够按合同ID查询到数据")
        self.assertEqual(data.id, self.test_data_id, "ID应该是测试数据ID")
        self.assertEqual(data.campaign_id, "TEST-2025-05", "活动ID应该是TEST-2025-05")
        self.assertEqual(data.housekeeper, "测试管家", "管家应该是测试管家")
        self.assertEqual(data.contract_amount, 30000.0, "合同金额应该是30000.0")

    def test_05_data_retrieval_by_campaign(self):
        """测试按活动ID查询数据"""
        # 按活动ID查询数据
        data_list = get_performance_data_by_campaign("TEST-2025-05")
        
        # 验证数据是否正确
        self.assertEqual(len(data_list), 2, "应该有2条数据")
        self.assertEqual(data_list[0].campaign_id, "TEST-2025-05", "活动ID应该是TEST-2025-05")
        self.assertEqual(data_list[1].campaign_id, "TEST-2025-05", "活动ID应该是TEST-2025-05")

    def test_06_data_retrieval_by_housekeeper(self):
        """测试按管家查询数据"""
        # 按管家查询数据
        data_list = get_performance_data_by_housekeeper("测试管家")
        
        # 验证数据是否正确
        self.assertEqual(len(data_list), 2, "应该有2条数据")
        self.assertEqual(data_list[0].housekeeper, "测试管家", "管家应该是测试管家")
        self.assertEqual(data_list[1].housekeeper, "测试管家", "管家应该是测试管家")
        
        # 按管家和活动ID查询数据
        data_list = get_performance_data_by_housekeeper("测试管家", "TEST-2025-05")
        
        # 验证数据是否正确
        self.assertEqual(len(data_list), 2, "应该有2条数据")
        self.assertEqual(data_list[0].housekeeper, "测试管家", "管家应该是测试管家")
        self.assertEqual(data_list[0].campaign_id, "TEST-2025-05", "活动ID应该是TEST-2025-05")

    def test_07_data_update(self):
        """测试数据更新"""
        # 获取数据
        data = get_performance_data_by_id(self.test_data_id)
        
        # 更新数据
        data.contract_amount = 35000.0
        data.paid_amount = 17500.0
        data.difference = 17500.0
        data.remark = "已更新"
        
        # 保存更新
        data.save()
        
        # 重新获取数据
        updated_data = get_performance_data_by_id(self.test_data_id)
        
        # 验证更新是否成功
        self.assertEqual(updated_data.contract_amount, 35000.0, "合同金额应该更新为35000.0")
        self.assertEqual(updated_data.paid_amount, 17500.0, "支付金额应该更新为17500.0")
        self.assertEqual(updated_data.difference, 17500.0, "差额应该更新为17500.0")
        self.assertEqual(updated_data.remark, "已更新", "备注应该更新为'已更新'")

    def test_08_data_deletion(self):
        """测试数据删除"""
        # 创建临时测试数据
        temp_data = PerformanceData(
            campaign_id="TEST-2025-05",
            contract_id="test_unit_003",
            province_code="110000",
            service_appointment_num="GD2025045497",
            status=1,
            housekeeper="测试管家",
            contract_doc_num="YHWX-TEST-2025050003",
            contract_amount=10000.0,
            paid_amount=5000.0,
            difference=5000.0,
            state=1,
            create_time="2025-05-03T11:36:22.444+08:00",
            org_name="测试服务商",
            signed_date="2025-05-03T11:42:07.904+08:00",
            doorsill=5000.0,
            trade_in=1,
            conversion=0.5,
            average=10000.0,
            contract_number_in_activity=3,
            housekeeper_total_amount=60000.0,
            housekeeper_contract_count=3,
            bonus_pool=20.0,
            performance_amount=10000.0,
            reward_status=1,
            reward_type="28",
            reward_name="接好运",
            notification_sent="N",
            remark="测试备注3",
            register_time="2025-05-06"
        )
        
        # 保存临时测试数据
        temp_data_id = temp_data.save()
        
        # 获取删除前的数据数量
        before_count = get_performance_data_count()
        
        # 删除数据
        result = delete_performance_data(temp_data_id)
        
        # 获取删除后的数据数量
        after_count = get_performance_data_count()
        
        # 验证删除是否成功
        self.assertTrue(result, "删除应该成功")
        self.assertEqual(after_count, before_count - 1, "数据数量应该减少1")
        
        # 验证数据是否已删除
        deleted_data = get_performance_data_by_id(temp_data_id)
        self.assertIsNone(deleted_data, "已删除的数据应该为None")

    def test_09_get_unique_contract_ids(self):
        """测试获取唯一合同ID"""
        # 获取唯一合同ID
        unique_ids = get_unique_contract_ids()
        
        # 验证唯一合同ID
        self.assertIn("test_unit_001", unique_ids, "唯一合同ID应该包含test_unit_001")
        self.assertIn("test_unit_002", unique_ids, "唯一合同ID应该包含test_unit_002")

if __name__ == '__main__':
    unittest.main()
