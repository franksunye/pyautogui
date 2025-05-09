#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
并行运行测试
测试原始实现和新实现的功能等价性
"""

import os
import sys
import unittest
from datetime import datetime
import logging
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from modules.data_processing_module import (
    process_data_apr_beijing,
    process_data_may_beijing,
    process_data_shanghai_apr,
    process_data_may_shanghai
)
from modules.data_processing_db_module import (
    process_beijing_data_to_db,
    process_shanghai_data_to_db
)
from modules.data_processing_generic import (
    process_data_apr_beijing_generic,
    process_data_may_beijing_generic,
    process_data_apr_shanghai_generic,
    process_data_may_shanghai_generic,
    process_beijing_data_to_db_generic,
    process_shanghai_data_to_db_generic
)
from modules.performance_data_manager import (
    get_performance_data_by_contract_id, get_performance_data_count, get_unique_contract_ids,
    delete_performance_data, get_performance_data_by_campaign_id
)
from scripts.create_performance_data_table import create_performance_data_table
from tests.test_utils.result_comparison import (
    compare_results,
    compare_db_results,
    save_comparison_results
)

# 设置日志
setup_logging()

class TestParallelExecution(unittest.TestCase):
    """并行运行测试"""

    @classmethod
    def setUpClass(cls):
        """测试前的准备工作"""
        # 确保数据库表存在
        create_performance_data_table()

        # 创建测试数据目录
        os.makedirs('tests/test_data', exist_ok=True)

        # 创建测试数据
        cls.test_data_beijing = [
            {
                '合同ID(_id)': 'test_parallel_bj_001',
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
                '合同ID(_id)': 'test_parallel_bj_002',
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
                '合同ID(_id)': 'test_parallel_sh_001',
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
        contract_ids = [
            'test_parallel_bj_001', 'test_parallel_bj_002', 'test_parallel_sh_001',
            'test_parallel_bj_001_db', 'test_parallel_bj_002_db', 'test_parallel_sh_001_db'
        ]
        for contract_id in contract_ids:
            data = get_performance_data_by_contract_id(contract_id)
            if data:
                delete_performance_data(data.id)

        # 删除测试活动的数据
        campaign_ids = ['BJ-PARALLEL-TEST', 'SH-PARALLEL-TEST']
        for campaign_id in campaign_ids:
            data_list = get_performance_data_by_campaign_id(campaign_id)
            for data in data_list:
                delete_performance_data(data.id)

    def test_01_parallel_execution_file_mode_beijing(self):
        """测试并行运行文件存储模式（北京）"""
        # 运行原始实现
        original_results = process_data_apr_beijing(
            self.test_data_beijing,
            set(),  # 空的已存在合同ID集合
            {}  # 空的管家奖励列表
        )

        # 运行新实现
        new_results = process_data_apr_beijing_generic(
            self.test_data_beijing,
            set(),  # 空的已存在合同ID集合
            {},  # 空的管家奖励列表
            False  # 使用文件存储
        )

        # 比较结果
        is_equal, differences = compare_results(original_results, new_results)

        # 保存比较结果
        save_comparison_results(
            original_results,
            new_results,
            'tests/test_data/parallel_execution_file_mode_beijing.json'
        )

        # 验证结果
        self.assertTrue(is_equal, f"原始实现和新实现的结果不一致，存在 {len(differences)} 处差异")

    def test_02_parallel_execution_file_mode_shanghai(self):
        """测试并行运行文件存储模式（上海）"""
        # 运行原始实现
        original_results = process_data_shanghai_apr(
            self.test_data_shanghai,
            set(),  # 空的已存在合同ID集合
            {}  # 空的管家奖励列表
        )

        # 运行新实现
        new_results = process_data_apr_shanghai_generic(
            self.test_data_shanghai,
            set(),  # 空的已存在合同ID集合
            {},  # 空的管家奖励列表
            False  # 使用文件存储
        )

        # 比较结果
        is_equal, differences = compare_results(original_results, new_results)

        # 保存比较结果
        save_comparison_results(
            original_results,
            new_results,
            'tests/test_data/parallel_execution_file_mode_shanghai.json'
        )

        # 验证结果
        self.assertTrue(is_equal, f"原始实现和新实现的结果不一致，存在 {len(differences)} 处差异")

    def test_03_parallel_execution_db_mode_beijing(self):
        """测试并行运行数据库存储模式（北京）"""
        # 修改测试数据，确保合同ID不重复
        test_data = self.test_data_beijing.copy()
        for i, contract in enumerate(test_data):
            test_data[i] = contract.copy()
            test_data[i]['合同ID(_id)'] = f"{contract['合同ID(_id)']}_db"

        # 运行原始实现
        original_count = process_beijing_data_to_db(
            test_data,
            "BJ-PARALLEL-TEST",  # 活动ID
            "110000"  # 省份代码
        )

        # 获取原始实现的结果
        original_results = get_performance_data_by_campaign_id("BJ-PARALLEL-TEST")

        # 运行新实现
        new_count = process_beijing_data_to_db_generic(
            test_data,
            "BJ-PARALLEL-TEST",  # 活动ID
            "110000"  # 省份代码
        )

        # 获取新实现的结果
        new_results = get_performance_data_by_campaign_id("BJ-PARALLEL-TEST")

        # 比较结果数量
        self.assertEqual(original_count, new_count, "原始实现和新实现处理的合同数量不同")

        # 比较数据库结果
        is_equal, differences = compare_db_results(original_results, new_results)

        # 验证结果
        self.assertTrue(is_equal, f"原始实现和新实现的结果不一致，存在 {len(differences)} 处差异")

    def test_04_parallel_execution_db_mode_shanghai(self):
        """测试并行运行数据库存储模式（上海）"""
        # 修改测试数据，确保合同ID不重复
        test_data = self.test_data_shanghai.copy()
        for i, contract in enumerate(test_data):
            test_data[i] = contract.copy()
            test_data[i]['合同ID(_id)'] = f"{contract['合同ID(_id)']}_db"

        # 运行原始实现
        original_count = process_shanghai_data_to_db(
            test_data,
            "SH-PARALLEL-TEST",  # 活动ID
            "310000"  # 省份代码
        )

        # 获取原始实现的结果
        original_results = get_performance_data_by_campaign_id("SH-PARALLEL-TEST")

        # 运行新实现
        new_count = process_shanghai_data_to_db_generic(
            test_data,
            "SH-PARALLEL-TEST",  # 活动ID
            "310000"  # 省份代码
        )

        # 获取新实现的结果
        new_results = get_performance_data_by_campaign_id("SH-PARALLEL-TEST")

        # 比较结果数量
        self.assertEqual(original_count, new_count, "原始实现和新实现处理的合同数量不同")

        # 比较数据库结果
        is_equal, differences = compare_db_results(original_results, new_results)

        # 验证结果
        self.assertTrue(is_equal, f"原始实现和新实现的结果不一致，存在 {len(differences)} 处差异")


if __name__ == '__main__':
    unittest.main()
