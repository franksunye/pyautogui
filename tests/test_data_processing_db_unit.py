#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单元测试：数据处理模块的数据库版本
测试数据处理模块的功能
"""

import os
import sys
import unittest
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from scripts.create_performance_data_table import create_performance_data_table
from modules.performance_data_manager import (
    get_performance_data_by_contract_id, get_performance_data_count, get_unique_contract_ids
)
from modules.data_processing_db_module import (
    process_data_to_db, process_beijing_data_to_db, process_shanghai_data_to_db
)

# 设置日志
setup_logging()

class TestDataProcessingDBUnit(unittest.TestCase):
    """单元测试：数据处理模块的数据库版本"""

    @classmethod
    def setUpClass(cls):
        """测试前的准备工作"""
        # 创建数据库表
        create_performance_data_table()
        
        # 创建测试数据
        cls.test_data_bj = [
            {
                '合同ID(_id)': 'test_process_bj_001',
                '活动城市(province)': '110000',
                '工单编号(serviceAppointmentNum)': 'GD2025045495',
                'Status': '1',
                '管家(serviceHousekeeper)': '石王磊',
                '合同编号(contractdocNum)': 'YHWX-BJ-JDHS-2025050001',
                '合同金额(adjustRefundMoney)': '30548.8',
                '支付金额(paidAmount)': '15274.4',
                '差额(difference)': '15274.4',
                'State': '1',
                '创建时间(createTime)': '2025-05-01T11:36:22.444+08:00',
                '服务商(orgName)': '北京久盾宏盛建筑工程有限公司',
                '签约时间(signedDate)': '2025-05-01T11:42:07.904+08:00',
                'Doorsill': '15274.4',
                '款项来源类型(tradeIn)': '1',
                '转化率(conversion)': '',
                '平均客单价(average)': ''
            },
            {
                '合同ID(_id)': 'test_process_bj_002',
                '活动城市(province)': '110000',
                '工单编号(serviceAppointmentNum)': 'GD2025050056',
                'Status': '1',
                '管家(serviceHousekeeper)': '石王磊',
                '合同编号(contractdocNum)': 'YHWX-BJ-JDHS-2025050005',
                '合同金额(adjustRefundMoney)': '32864.1',
                '支付金额(paidAmount)': '16432.05',
                '差额(difference)': '16432.05',
                'State': '1',
                '创建时间(createTime)': '2025-05-01T22:40:51.216+08:00',
                '服务商(orgName)': '北京久盾宏盛建筑工程有限公司',
                '签约时间(signedDate)': '2025-05-02T17:16:52.872+08:00',
                'Doorsill': '16432.05',
                '款项来源类型(tradeIn)': '1',
                '转化率(conversion)': '',
                '平均客单价(average)': ''
            }
        ]
        
        cls.test_data_sh = [
            {
                '合同ID(_id)': 'test_process_sh_001',
                '活动城市(province)': '310000',
                '工单编号(serviceAppointmentNum)': 'GD2025045444',
                'Status': '1',
                '管家(serviceHousekeeper)': '魏亮',
                '合同编号(contractdocNum)': 'YHWX-SH-RJTFSGC-2025050001',
                '合同金额(adjustRefundMoney)': '2500.0',
                '支付金额(paidAmount)': '2500.0',
                '差额(difference)': '0.0',
                'State': '1',
                '创建时间(createTime)': '2025-05-01T10:19:54.707+08:00',
                '服务商(orgName)': '上海若金汤防水工程有限公司',
                '签约时间(signedDate)': '2025-05-01T10:24:23.155+08:00',
                'Doorsill': '2500.0',
                '款项来源类型(tradeIn)': '1',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '2500.0'
            },
            {
                '合同ID(_id)': 'test_process_sh_002',
                '活动城市(province)': '310000',
                '工单编号(serviceAppointmentNum)': 'GD2025032791',
                'Status': '1',
                '管家(serviceHousekeeper)': '张晓磊',
                '合同编号(contractdocNum)': 'YHWX-SH-YTJZ-2025050001',
                '合同金额(adjustRefundMoney)': '2500.0',
                '支付金额(paidAmount)': '2500.0',
                '差额(difference)': '0.0',
                'State': '1',
                '创建时间(createTime)': '2025-05-04T10:23:25.42+08:00',
                '服务商(orgName)': '上海雁棠建筑工程有限公司',
                '签约时间(signedDate)': '2025-05-04T10:33:33.165+08:00',
                'Doorsill': '2500.0',
                '款项来源类型(tradeIn)': '1',
                '转化率(conversion)': '',
                '平均客单价(average)': ''
            }
        ]

    @classmethod
    def tearDownClass(cls):
        """测试后的清理工作"""
        # 删除测试数据
        for contract_id in ['test_process_bj_001', 'test_process_bj_002', 'test_process_sh_001', 'test_process_sh_002']:
            data = get_performance_data_by_contract_id(contract_id)
            if data:
                from modules.performance_data_manager import delete_performance_data
                delete_performance_data(data.id)

    def test_01_process_data_to_db(self):
        """测试处理数据并保存到数据库"""
        # 获取处理前的数据数量
        before_count = get_performance_data_count()
        
        # 处理数据
        processed_count = process_data_to_db(
            self.test_data_bj,
            "BJ-2025-05",
            "110000"
        )
        
        # 获取处理后的数据数量
        after_count = get_performance_data_count()
        
        # 验证处理结果
        self.assertEqual(processed_count, 2, "应该处理2条数据")
        self.assertEqual(after_count, before_count + 2, "数据数量应该增加2")
        
        # 验证数据内容
        data1 = get_performance_data_by_contract_id("test_process_bj_001")
        self.assertIsNotNone(data1, "应该能够查询到数据")
        self.assertEqual(data1.campaign_id, "BJ-2025-05", "活动ID应该是BJ-2025-05")
        self.assertEqual(data1.province_code, "110000", "省份代码应该是110000")
        self.assertEqual(data1.housekeeper, "石王磊", "管家应该是石王磊")
        self.assertEqual(data1.contract_amount, 30548.8, "合同金额应该是30548.8")
        
        data2 = get_performance_data_by_contract_id("test_process_bj_002")
        self.assertIsNotNone(data2, "应该能够查询到数据")
        self.assertEqual(data2.campaign_id, "BJ-2025-05", "活动ID应该是BJ-2025-05")
        self.assertEqual(data2.province_code, "110000", "省份代码应该是110000")
        self.assertEqual(data2.housekeeper, "石王磊", "管家应该是石王磊")
        self.assertEqual(data2.contract_amount, 32864.1, "合同金额应该是32864.1")

    def test_02_process_beijing_data_to_db(self):
        """测试处理北京数据并保存到数据库"""
        # 删除之前的测试数据
        for contract_id in ['test_process_bj_001', 'test_process_bj_002']:
            data = get_performance_data_by_contract_id(contract_id)
            if data:
                from modules.performance_data_manager import delete_performance_data
                delete_performance_data(data.id)
        
        # 获取处理前的数据数量
        before_count = get_performance_data_count()
        
        # 处理数据
        processed_count = process_beijing_data_to_db(
            self.test_data_bj,
            "BJ-2025-05",
            "110000"
        )
        
        # 获取处理后的数据数量
        after_count = get_performance_data_count()
        
        # 验证处理结果
        self.assertEqual(processed_count, 2, "应该处理2条数据")
        self.assertEqual(after_count, before_count + 2, "数据数量应该增加2")
        
        # 验证数据内容
        data1 = get_performance_data_by_contract_id("test_process_bj_001")
        self.assertIsNotNone(data1, "应该能够查询到数据")
        self.assertEqual(data1.campaign_id, "BJ-2025-05", "活动ID应该是BJ-2025-05")
        
        data2 = get_performance_data_by_contract_id("test_process_bj_002")
        self.assertIsNotNone(data2, "应该能够查询到数据")
        self.assertEqual(data2.campaign_id, "BJ-2025-05", "活动ID应该是BJ-2025-05")

    def test_03_process_shanghai_data_to_db(self):
        """测试处理上海数据并保存到数据库"""
        # 获取处理前的数据数量
        before_count = get_performance_data_count()
        
        # 处理数据
        processed_count = process_shanghai_data_to_db(
            self.test_data_sh,
            "SH-2025-04",
            "310000"
        )
        
        # 获取处理后的数据数量
        after_count = get_performance_data_count()
        
        # 验证处理结果
        self.assertEqual(processed_count, 2, "应该处理2条数据")
        self.assertEqual(after_count, before_count + 2, "数据数量应该增加2")
        
        # 验证数据内容
        data1 = get_performance_data_by_contract_id("test_process_sh_001")
        self.assertIsNotNone(data1, "应该能够查询到数据")
        self.assertEqual(data1.campaign_id, "SH-2025-04", "活动ID应该是SH-2025-04")
        self.assertEqual(data1.province_code, "310000", "省份代码应该是310000")
        self.assertEqual(data1.housekeeper, "魏亮", "管家应该是魏亮")
        self.assertEqual(data1.contract_amount, 2500.0, "合同金额应该是2500.0")
        self.assertEqual(data1.conversion, 0.5, "转化率应该是0.5")
        self.assertEqual(data1.average, 2500.0, "平均客单价应该是2500.0")
        
        data2 = get_performance_data_by_contract_id("test_process_sh_002")
        self.assertIsNotNone(data2, "应该能够查询到数据")
        self.assertEqual(data2.campaign_id, "SH-2025-04", "活动ID应该是SH-2025-04")
        self.assertEqual(data2.province_code, "310000", "省份代码应该是310000")
        self.assertEqual(data2.housekeeper, "张晓磊", "管家应该是张晓磊")
        self.assertEqual(data2.contract_amount, 2500.0, "合同金额应该是2500.0")

    def test_04_process_duplicate_data(self):
        """测试处理重复数据"""
        # 获取处理前的数据数量
        before_count = get_performance_data_count()
        
        # 处理数据（重复处理）
        processed_count = process_data_to_db(
            self.test_data_bj,
            "BJ-2025-05",
            "110000"
        )
        
        # 获取处理后的数据数量
        after_count = get_performance_data_count()
        
        # 验证处理结果
        self.assertEqual(processed_count, 0, "应该处理0条数据（因为数据已存在）")
        self.assertEqual(after_count, before_count, "数据数量应该不变")

    def test_05_process_with_existing_contract_ids(self):
        """测试使用已存在的合同ID集合处理数据"""
        # 创建新的测试数据
        test_data = [
            {
                '合同ID(_id)': 'test_process_new_001',
                '活动城市(province)': '110000',
                '工单编号(serviceAppointmentNum)': 'GD2025045498',
                'Status': '1',
                '管家(serviceHousekeeper)': '王小明',
                '合同编号(contractdocNum)': 'YHWX-BJ-JDHS-2025050010',
                '合同金额(adjustRefundMoney)': '20000.0',
                '支付金额(paidAmount)': '10000.0',
                '差额(difference)': '10000.0',
                'State': '1',
                '创建时间(createTime)': '2025-05-05T11:36:22.444+08:00',
                '服务商(orgName)': '北京久盾宏盛建筑工程有限公司',
                '签约时间(signedDate)': '2025-05-05T11:42:07.904+08:00',
                'Doorsill': '10000.0',
                '款项来源类型(tradeIn)': '1',
                '转化率(conversion)': '',
                '平均客单价(average)': ''
            }
        ]
        
        # 获取已存在的合同ID集合
        existing_contract_ids = get_unique_contract_ids()
        
        # 获取处理前的数据数量
        before_count = get_performance_data_count()
        
        # 处理数据
        processed_count = process_data_to_db(
            test_data,
            "BJ-2025-05",
            "110000",
            existing_contract_ids
        )
        
        # 获取处理后的数据数量
        after_count = get_performance_data_count()
        
        # 验证处理结果
        self.assertEqual(processed_count, 1, "应该处理1条数据")
        self.assertEqual(after_count, before_count + 1, "数据数量应该增加1")
        
        # 验证数据内容
        data = get_performance_data_by_contract_id("test_process_new_001")
        self.assertIsNotNone(data, "应该能够查询到数据")
        self.assertEqual(data.campaign_id, "BJ-2025-05", "活动ID应该是BJ-2025-05")
        self.assertEqual(data.housekeeper, "王小明", "管家应该是王小明")
        
        # 清理测试数据
        if data:
            from modules.performance_data_manager import delete_performance_data
            delete_performance_data(data.id)

if __name__ == '__main__':
    unittest.main()
