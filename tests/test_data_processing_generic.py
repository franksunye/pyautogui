#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单元测试：通用数据处理模块
测试通用数据处理函数的功能
"""

import os
import sys
import unittest
from datetime import datetime
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from modules.data_processing_generic import (
    process_data_generic,
    process_data_apr_beijing_generic,
    process_data_may_beijing_generic,
    process_data_apr_shanghai_generic,
    process_data_may_shanghai_generic,
    process_beijing_data_to_db_generic,
    process_shanghai_data_to_db_generic
)
from modules.performance_data_manager import (
    get_performance_data_by_contract_id, get_performance_data_count, get_unique_contract_ids,
    delete_performance_data
)
from scripts.create_performance_data_table import create_performance_data_table

# 设置日志
setup_logging()

class TestDataProcessingGeneric(unittest.TestCase):
    """单元测试：通用数据处理模块"""

    @classmethod
    def setUpClass(cls):
        """测试前的准备工作"""
        # 确保数据库表存在
        create_performance_data_table()

        # 创建测试数据
        cls.test_data_beijing = [
            {
                '合同ID(_id)': 'test_generic_bj_001',
                '活动城市(province)': '北京',
                '工单编号(serviceAppointmentNum)': 'GD2025045495',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家',
                '合同编号(contractdocNum)': 'YHWX-BJ-TEST-2025050001',
                '合同金额(adjustRefundMoney)': '30000',
                '支付金额(paidAmount)': '15000',
                '差额(difference)': '15000',
                'State': '1',
                '创建时间(createTime)': '2025-05-01T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商',
                '签约时间(signedDate)': '2025-05-01T11:42:07.904+08:00',
                'Doorsill': '15000',
                '款项来源类型(tradeIn)': '1',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '30000'
            },
            {
                '合同ID(_id)': 'test_generic_bj_002',
                '活动城市(province)': '北京',
                '工单编号(serviceAppointmentNum)': 'GD2025045496',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家',
                '合同编号(contractdocNum)': 'YHWX-BJ-TEST-2025050002',
                '合同金额(adjustRefundMoney)': '20000',
                '支付金额(paidAmount)': '10000',
                '差额(difference)': '10000',
                'State': '1',
                '创建时间(createTime)': '2025-05-02T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商',
                '签约时间(signedDate)': '2025-05-02T11:42:07.904+08:00',
                'Doorsill': '10000',
                '款项来源类型(tradeIn)': '1',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            }
        ]

        cls.test_data_shanghai = [
            {
                '合同ID(_id)': 'test_generic_sh_001',
                '活动城市(province)': '上海',
                '工单编号(serviceAppointmentNum)': 'GD2025045497',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家',
                '合同编号(contractdocNum)': 'YHWX-SH-TEST-2025050001',
                '合同金额(adjustRefundMoney)': '25000',
                '支付金额(paidAmount)': '12500',
                '差额(difference)': '12500',
                'State': '1',
                '创建时间(createTime)': '2025-05-01T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商',
                '签约时间(signedDate)': '2025-05-01T11:42:07.904+08:00',
                'Doorsill': '12500',
                '款项来源类型(tradeIn)': '1',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '25000'
            }
        ]

    @classmethod
    def tearDownClass(cls):
        """测试后的清理工作"""
        # 删除测试数据
        for contract_id in ['test_generic_bj_001', 'test_generic_bj_002', 'test_generic_sh_001', 'test_generic_sh_002']:
            data = get_performance_data_by_contract_id(contract_id)
            if data:
                delete_performance_data(data.id)

    def test_01_process_data_generic_file_mode(self):
        """测试通用数据处理函数的文件存储模式"""
        # 使用通用数据处理函数处理北京数据
        result = process_data_generic(
            self.test_data_beijing,
            set(),  # 空的已存在合同ID集合
            {},  # 空的管家奖励列表
            "BJ-2025-04",  # 配置键
            False,  # 使用文件存储
            None,
            None,
            False  # 北京不使用组合键
        )

        # 验证结果
        self.assertEqual(len(result), 2, "应该处理2条数据")
        self.assertEqual(result[0]['合同ID(_id)'], 'test_generic_bj_001', "第一条数据的合同ID应该是test_generic_bj_001")
        self.assertEqual(result[1]['合同ID(_id)'], 'test_generic_bj_002', "第二条数据的合同ID应该是test_generic_bj_002")
        self.assertEqual(result[0]['管家累计单数'], 1, "第一条数据的管家累计单数应该是1")
        self.assertEqual(result[1]['管家累计单数'], 2, "第二条数据的管家累计单数应该是2")
        self.assertEqual(float(result[0]['管家累计金额']), 30000.0, "第一条数据的管家累计金额应该是30000.0")
        self.assertEqual(float(result[1]['管家累计金额']), 50000.0, "第二条数据的管家累计金额应该是50000.0")

    def test_02_process_data_generic_db_mode(self):
        """测试通用数据处理函数的数据库存储模式"""
        # 获取处理前的数据数量
        before_count = get_performance_data_count()

        # 使用通用数据处理函数处理上海数据
        result = process_data_generic(
            self.test_data_shanghai,
            get_unique_contract_ids(),  # 从数据库获取已存在的合同ID
            {},  # 空的管家奖励列表
            "SH-2025-04",  # 配置键
            True,  # 使用数据库存储
            "SH-2025-04",  # 活动ID
            "310000",  # 省份代码
            True  # 上海使用组合键
        )

        # 验证结果
        self.assertEqual(result, 1, "应该处理1条数据")

        # 获取处理后的数据数量
        after_count = get_performance_data_count()
        self.assertEqual(after_count, before_count + 1, "数据库中的数据数量应该增加1")

        # 验证数据库中的数据
        data = get_performance_data_by_contract_id('test_generic_sh_001')
        self.assertIsNotNone(data, "应该能够从数据库中获取到数据")
        self.assertEqual(data.contract_id, 'test_generic_sh_001', "合同ID应该是test_generic_sh_001")
        self.assertEqual(data.housekeeper, '测试管家', "管家应该是测试管家")
        self.assertEqual(data.contract_amount, 25000.0, "合同金额应该是25000.0")

    def test_03_process_data_apr_beijing_generic(self):
        """测试北京4月包装函数"""
        # 使用包装函数处理北京数据
        result = process_data_apr_beijing_generic(
            self.test_data_beijing,
            set(),  # 空的已存在合同ID集合
            {},  # 空的管家奖励列表
            False  # 使用文件存储
        )

        # 验证结果
        self.assertEqual(len(result), 2, "应该处理2条数据")
        self.assertEqual(result[0]['活动编号'], 'BJ-2025-04', "活动编号应该是BJ-2025-04")

    def test_04_process_data_apr_shanghai_generic(self):
        """测试上海4月包装函数"""
        # 使用包装函数处理上海数据
        result = process_data_apr_shanghai_generic(
            self.test_data_shanghai,
            set(),  # 空的已存在合同ID集合
            {},  # 空的管家奖励列表
            False  # 使用文件存储
        )

        # 验证结果
        self.assertEqual(len(result), 1, "应该处理1条数据")
        self.assertEqual(result[0]['活动编号'], 'SH-2025-04', "活动编号应该是SH-2025-04")

    def test_05_process_beijing_data_to_db_generic(self):
        """测试北京数据库处理包装函数"""
        # 获取处理前的数据数量
        before_count = get_performance_data_count()

        # 使用包装函数处理北京数据
        result = process_beijing_data_to_db_generic(
            self.test_data_beijing,
            "BJ-2025-04",  # 活动ID
            "110000"  # 省份代码
        )

        # 验证结果
        self.assertEqual(result, 2, "应该处理2条数据")

        # 获取处理后的数据数量
        after_count = get_performance_data_count()
        self.assertEqual(after_count, before_count + 2, "数据库中的数据数量应该增加2")

    def test_06_process_shanghai_data_to_db_generic(self):
        """测试上海数据库处理包装函数"""
        # 获取处理前的数据数量
        before_count = get_performance_data_count()

        # 创建一个新的测试数据，确保合同ID不重复
        test_data = self.test_data_shanghai.copy()
        test_data[0] = test_data[0].copy()
        test_data[0]['合同ID(_id)'] = 'test_generic_sh_002'

        # 使用包装函数处理上海数据
        result = process_shanghai_data_to_db_generic(
            test_data,
            "SH-2025-04",  # 活动ID
            "310000"  # 省份代码
        )

        # 验证结果
        self.assertEqual(result, 1, "应该处理1条数据")

        # 获取处理后的数据数量
        after_count = get_performance_data_count()
        self.assertEqual(after_count, before_count + 1, "数据库中的数据数量应该增加1")

        # 清理测试数据
        data = get_performance_data_by_contract_id('test_generic_sh_002')
        if data:
            delete_performance_data(data.id)


if __name__ == '__main__':
    unittest.main()
