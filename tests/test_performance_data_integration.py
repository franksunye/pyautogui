#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试签约台账数据库集成
"""

import os
import sys
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
import modules.config
import jobs
from scripts.create_performance_data_table import create_performance_data_table
from modules.performance_data_manager import get_performance_data_count, get_all_performance_data

# 设置日志
setup_logging()

class TestPerformanceDataIntegration(unittest.TestCase):
    """测试签约台账数据库集成"""

    @classmethod
    def setUpClass(cls):
        """测试前的准备工作"""
        # 创建数据库表
        create_performance_data_table()

        # 保存原始配置
        cls.original_use_database = modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA

        # 模拟API响应
        cls.mock_response = {
            'data': {
                'rows': [
                    {
                        '合同ID(_id)': 'test_integration_001',
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
                        '合同ID(_id)': 'test_integration_002',
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
            }
        }

    @classmethod
    def tearDownClass(cls):
        """测试后的清理工作"""
        # 恢复原始配置
        jobs.USE_DATABASE_FOR_PERFORMANCE_DATA = cls.original_use_database

    def setUp(self):
        """每个测试前的准备工作"""
        # 记录测试开始前的数据数量
        self.before_count = get_performance_data_count()

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    def test_signing_and_sales_incentive_may_beijing_file_storage(self):
        """测试北京5月签约和奖励播报（文件存储）"""
        # 设置使用文件存储
        modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA = False

        # 记录测试开始前的数据数量
        before_count = get_performance_data_count()

        # 创建测试数据
        contract_data = [
            {
                '合同ID(_id)': 'test_file_001',
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
            }
        ]

        # 处理数据
        from modules.data_processing_module import process_data_may_beijing
        existing_contract_ids = set()
        housekeeper_award_lists = {}
        processed_data = process_data_may_beijing(contract_data, existing_contract_ids, housekeeper_award_lists)

        # 验证处理结果
        self.assertEqual(len(processed_data), 1, "应该有1条处理后的数据")
        self.assertEqual(processed_data[0]['合同ID(_id)'], 'test_file_001', "合同ID应该是test_file_001")

        # 验证数据库中的数据数量没有变化
        after_count = get_performance_data_count()
        self.assertEqual(before_count, after_count, "数据库中的数据数量不应该变化")

    def test_signing_and_sales_incentive_may_beijing_db_storage(self):
        """测试北京5月签约和奖励播报（数据库存储）"""
        # 设置使用数据库存储
        modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA = True

        # 记录测试开始前的数据数量
        before_count = get_performance_data_count()

        # 创建测试数据
        contract_data = [
            {
                '合同ID(_id)': 'test_db_001',
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
                '合同ID(_id)': 'test_db_002',
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

        # 处理数据
        from modules.data_processing_db_module import process_data_to_db
        campaign_id = "BJ-2025-05"
        province_code = "110000"
        processed_count = process_data_to_db(contract_data, campaign_id, province_code)

        # 验证处理结果
        self.assertEqual(processed_count, 2, "应该处理2条数据")

        # 验证数据库中的数据数量增加了
        after_count = get_performance_data_count()
        self.assertEqual(before_count + 2, after_count, "数据库中的数据数量应该增加2")

        # 验证数据库中的数据内容
        all_data = get_all_performance_data()
        test_data = [data for data in all_data if data.contract_id in ['test_db_001', 'test_db_002']]
        self.assertEqual(len(test_data), 2, "应该有2条测试数据")

        # 验证第一条数据
        data1 = [data for data in test_data if data.contract_id == 'test_db_001'][0]
        self.assertEqual(data1.campaign_id, "BJ-2025-05", "活动ID应该是BJ-2025-05")
        self.assertEqual(data1.province_code, "110000", "省份代码应该是110000")
        self.assertEqual(data1.housekeeper, "石王磊", "管家应该是石王磊")
        self.assertEqual(data1.contract_amount, 30548.8, "合同金额应该是30548.8")

        # 验证第二条数据
        data2 = [data for data in test_data if data.contract_id == 'test_db_002'][0]
        self.assertEqual(data2.campaign_id, "BJ-2025-05", "活动ID应该是BJ-2025-05")
        self.assertEqual(data2.province_code, "110000", "省份代码应该是110000")
        self.assertEqual(data2.housekeeper, "石王磊", "管家应该是石王磊")
        self.assertEqual(data2.contract_amount, 32864.1, "合同金额应该是32864.1")

if __name__ == '__main__':
    unittest.main()
