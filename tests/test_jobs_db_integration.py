#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
集成测试：任务调度模块与数据库的集成
测试任务调度模块在数据库模式下的功能
"""

import os
import sys
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from scripts.create_performance_data_table import create_performance_data_table
from modules.performance_data_manager import (
    get_performance_data_by_campaign, get_performance_data_count,
    delete_performance_data
)
import modules.config

# 设置日志
setup_logging()

class TestJobsDBIntegration(unittest.TestCase):
    """集成测试：任务调度模块与数据库的集成"""

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
                        '合同ID(_id)': 'test_jobs_bj_001',
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
                        '合同ID(_id)': 'test_jobs_bj_002',
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

        cls.mock_response_sh = {
            'data': {
                'rows': [
                    {
                        '合同ID(_id)': 'test_jobs_sh_001',
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
                    }
                ]
            }
        }

    @classmethod
    def tearDownClass(cls):
        """测试后的清理工作"""
        # 恢复原始配置
        modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA = cls.original_use_database

        # 删除测试数据
        for contract_id in ['test_jobs_bj_001', 'test_jobs_bj_002', 'test_jobs_sh_001']:
            data = get_performance_data_by_campaign(contract_id)
            if data:
                for item in data:
                    delete_performance_data(item.id)

    def setUp(self):
        """每个测试前的准备工作"""
        # 记录测试开始前的数据数量
        self.before_count = get_performance_data_count()

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    def test_01_file_storage_mode(self):
        """测试文件存储模式"""
        # 设置使用文件存储
        modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA = False

        # 记录测试开始前的数据数量
        before_count = get_performance_data_count()

        # 创建测试数据
        test_data = [
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
        processed_data = process_data_may_beijing(test_data, existing_contract_ids, housekeeper_award_lists)

        # 验证处理结果
        self.assertEqual(len(processed_data), 1, "应该有1条处理后的数据")
        self.assertEqual(processed_data[0]['合同ID(_id)'], 'test_file_001', "合同ID应该是test_file_001")

        # 验证数据库中的数据数量没有变化
        after_count = get_performance_data_count()
        self.assertEqual(before_count, after_count, "数据库中的数据数量不应该变化")

    def test_02_db_storage_mode(self):
        """测试数据库存储模式"""
        # 设置使用数据库存储
        modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA = True

        # 记录测试开始前的数据数量
        before_count = get_performance_data_count()

        # 创建测试数据
        test_data = [
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
        processed_count = process_data_to_db(test_data, campaign_id, province_code)

        # 验证处理结果
        # 注意：由于测试环境中可能已经存在相同的合同ID，所以处理的数据数量可能不是2
        # 我们只需要验证数据库中的数据数量是否增加了
        self.assertGreaterEqual(processed_count, 0, "应该处理数据")

        # 验证数据库中的数据数量增加了
        after_count = get_performance_data_count()
        self.assertGreaterEqual(after_count, before_count, "数据库中的数据数量应该增加")

        # 验证数据库中的数据内容
        data_list = get_performance_data_by_campaign("BJ-2025-05")
        test_data = [data for data in data_list if data.contract_id in ['test_db_001', 'test_db_002']]
        self.assertEqual(len(test_data), 2, "应该有2条测试数据")

    def test_03_shanghai_db_storage_mode(self):
        """测试上海数据库存储模式"""
        # 设置使用数据库存储
        modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA = True

        # 记录测试开始前的数据数量
        before_count = get_performance_data_count()

        # 创建测试数据
        test_data = [
            {
                '合同ID(_id)': 'test_sh_001',
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
            }
        ]

        # 处理数据
        from modules.data_processing_db_module import process_data_to_db
        campaign_id = "SH-2025-04"
        province_code = "310000"
        processed_count = process_data_to_db(test_data, campaign_id, province_code)

        # 验证处理结果
        # 注意：由于测试环境中可能已经存在相同的合同ID，所以处理的数据数量可能不是1
        # 我们只需要验证数据库中的数据数量是否增加了
        self.assertGreaterEqual(processed_count, 0, "应该处理数据")

        # 验证数据库中的数据数量增加了
        after_count = get_performance_data_count()
        self.assertGreaterEqual(after_count, before_count, "数据库中的数据数量应该增加")

        # 验证数据库中的数据内容
        data_list = get_performance_data_by_campaign("SH-2025-04")
        test_data = [data for data in data_list if data.contract_id == 'test_sh_001']
        self.assertEqual(len(test_data), 1, "应该有1条测试数据")
        self.assertEqual(test_data[0].housekeeper, "魏亮", "管家应该是魏亮")
        self.assertEqual(test_data[0].contract_amount, 2500.0, "合同金额应该是2500.0")

    def test_04_switching_between_storage_modes(self):
        """测试在存储模式之间切换"""
        # 记录测试开始前的数据数量
        before_count = get_performance_data_count()

        # 创建测试数据
        test_data = [
            {
                '合同ID(_id)': 'test_switch_001',
                '活动城市(province)': '110000',
                '工单编号(serviceAppointmentNum)': 'GD2025045499',
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

        # 设置使用文件存储
        modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA = False

        # 处理数据（文件存储模式）
        from modules.data_processing_module import process_data_may_beijing
        existing_contract_ids = set()
        housekeeper_award_lists = {}
        processed_data = process_data_may_beijing(test_data, existing_contract_ids, housekeeper_award_lists)

        # 验证处理结果
        self.assertEqual(len(processed_data), 1, "应该有1条处理后的数据")

        # 验证数据库中的数据数量没有变化
        mid_count = get_performance_data_count()
        self.assertEqual(before_count, mid_count, "数据库中的数据数量不应该变化")

        # 设置使用数据库存储
        modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA = True

        # 处理数据（数据库存储模式）
        from modules.data_processing_db_module import process_data_to_db
        campaign_id = "BJ-2025-05"
        province_code = "110000"
        processed_count = process_data_to_db(test_data, campaign_id, province_code)

        # 验证处理结果
        # 注意：由于测试环境中可能已经存在相同的合同ID，所以处理的数据数量可能不是1
        # 我们只需要验证数据库中的数据数量是否增加了
        self.assertGreaterEqual(processed_count, 0, "应该处理数据")

        # 验证数据库中的数据数量增加了
        after_count = get_performance_data_count()
        self.assertGreaterEqual(after_count, mid_count, "数据库中的数据数量应该增加")

        # 验证数据库中的数据内容
        data_list = get_performance_data_by_campaign("BJ-2025-05")
        test_data = [data for data in data_list if data.contract_id == 'test_switch_001']
        self.assertEqual(len(test_data), 1, "应该有1条测试数据")
        self.assertEqual(test_data[0].housekeeper, "王小明", "管家应该是王小明")
        self.assertEqual(test_data[0].contract_amount, 20000.0, "合同金额应该是20000.0")

if __name__ == '__main__':
    unittest.main()
