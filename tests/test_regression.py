#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
系统回归测试
确保数据库迁移不影响现有功能
"""

import os
import sys
import unittest
import tempfile
import logging
# 不再需要json和csv导入
from unittest.mock import patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from modules.file_utils import write_performance_data_to_csv
from modules.data_processing_module import process_data_may_beijing
from modules.data_processing_db_module import process_data_to_db
from modules.performance_data_manager import (
    get_performance_data_by_campaign, get_all_performance_data, delete_performance_data
)
from modules.notification_module import notify_awards_may_beijing
from modules.notification_db_module import notify_awards_may_beijing_db
from scripts.create_performance_data_table import create_performance_data_table

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

class TestRegression(unittest.TestCase):
    """系统回归测试，确保数据库迁移不影响现有功能"""

    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        # 创建数据库表
        create_performance_data_table()

        # 清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_regression_'):
                delete_performance_data(data.id)

        # 创建临时文件用于测试
        cls.temp_file_bj = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')

        # 创建测试数据
        cls.test_data_beijing = [
            {
                '合同ID(_id)': 'test_regression_bj_001_may',
                '工单编号(serviceAppointmentNum)': 'GD2025045001',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家A',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050001',
                '合同金额(adjustRefundMoney)': '30000',
                '支付金额(paidAmount)': '15000',
                '差额(difference)': '15000',
                'State': '1',
                '创建时间(createTime)': '2025-05-01T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商A',
                '签约时间(signedDate)': '2025-05-01T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '15000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': 'test_regression_bj_002_may',
                '工单编号(serviceAppointmentNum)': 'GD2025045002',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家A',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050002',
                '合同金额(adjustRefundMoney)': '20000',
                '支付金额(paidAmount)': '10000',
                '差额(difference)': '10000',
                'State': '1',
                '创建时间(createTime)': '2025-05-02T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商A',
                '签约时间(signedDate)': '2025-05-02T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '10000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': 'test_regression_bj_003_may',
                '工单编号(serviceAppointmentNum)': 'GD2025045003',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家A',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050003',
                '合同金额(adjustRefundMoney)': '25000',
                '支付金额(paidAmount)': '12500',
                '差额(difference)': '12500',
                'State': '1',
                '创建时间(createTime)': '2025-05-03T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商A',
                '签约时间(signedDate)': '2025-05-03T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '12500',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': 'test_regression_bj_006_may',  # 末位为6，触发幸运数字奖励
                '工单编号(serviceAppointmentNum)': 'GD2025045006',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家A',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050006',
                '合同金额(adjustRefundMoney)': '15000',
                '支付金额(paidAmount)': '7500',
                '差额(difference)': '7500',
                'State': '1',
                '创建时间(createTime)': '2025-05-06T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商A',
                '签约时间(signedDate)': '2025-05-06T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '7500',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            }
        ]

    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        # 删除临时文件
        try:
            os.unlink(cls.temp_file_bj.name)
        except (PermissionError, FileNotFoundError):
            pass

        # 清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_regression_'):
                delete_performance_data(data.id)

    def test_data_processing_consistency(self):
        """测试数据处理一致性"""
        print("\n===== 测试数据处理一致性 =====")

        # 1. 使用数据库存储处理数据
        campaign_id = "BJ-2025-05"
        province_code = "110000"

        # 先清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_regression_'):
                delete_performance_data(data.id)

        # 处理数据到数据库
        process_data_to_db(
            self.test_data_beijing,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 从数据库中读取处理后的数据
        db_data = get_performance_data_by_campaign(campaign_id)
        db_data = [data for data in db_data if data.contract_id.startswith('test_regression_')]

        # 验证数据条数
        self.assertEqual(len(self.test_data_beijing), len(db_data), "输入数据和数据库中的数据条数不一致")
        print(f"输入数据和数据库中的数据条数一致: {len(db_data)}")

        # 验证关键字段
        for input_record in self.test_data_beijing:
            contract_id = input_record['合同ID(_id)']
            db_record = None
            for record in db_data:
                if record.contract_id == contract_id:
                    db_record = record
                    break

            self.assertIsNotNone(db_record, f"在数据库中找不到合同ID为 {contract_id} 的记录")

            # 比较合同金额
            self.assertEqual(
                float(input_record['合同金额(adjustRefundMoney)']),
                float(db_record.contract_amount),
                f"合同 {contract_id} 的合同金额不一致"
            )

            # 比较合同编号
            self.assertEqual(
                input_record['合同编号(contractdocNum)'],
                db_record.contract_doc_num,
                f"合同 {contract_id} 的合同编号不一致"
            )

            print(f"合同 {contract_id} 的数据一致性验证通过")

        print("\n数据处理一致性测试通过 ✓")

    @patch('modules.notification_module.create_task')
    def test_notification_functionality(self, mock_create_task):
        """测试通知功能"""
        print("\n===== 测试通知功能 =====")

        # 1. 使用文件存储处理数据
        existing_contract_ids = set()
        housekeeper_award_lists = {}
        file_processed_data = process_data_may_beijing(
            self.test_data_beijing,
            existing_contract_ids,
            housekeeper_award_lists
        )

        # 写入临时文件
        fieldnames = [
            '合同ID(_id)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)',
            '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State',
            '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', '门槛(doorsill)',
            '款项来源类型(tradeIn)', '活动城市(province)', 'Doorsill', '转化率(conversion)', '平均客单价(average)',
            '活动编号', '活动期内第几个合同', '管家累计单数', '登记时间',
            '管家累计金额', '管家合同数量', '奖金池', '计入业绩金额', '激活奖励状态', '奖励类型', '奖励名称',
            '是否发送通知', '备注'
        ]

        # 设置一些记录的奖励状态为1，以触发通知
        for record in file_processed_data:
            if record['合同ID(_id)'] == 'test_regression_bj_006_may':
                record['激活奖励状态'] = '1'
                record['奖励类型'] = '幸运数字'
                record['奖励名称'] = '接好运'
                record['是否发送通知'] = 'N'

        write_performance_data_to_csv(self.temp_file_bj.name, file_processed_data, fieldnames)

        # 2. 测试文件存储通知功能
        with patch('modules.notification_module.PERFORMANCE_DATA_FILE', self.temp_file_bj.name):
            # 重置mock
            mock_create_task.reset_mock()

            # 调用通知函数
            notify_awards_may_beijing()

            # 验证通知系统调用
            self.assertTrue(mock_create_task.called, "文件存储方式下通知系统未被调用")
            print(f"文件存储方式下通知系统被调用了 {mock_create_task.call_count} 次")

        # 3. 测试数据库存储通知功能
        # 获取数据库中的性能数据
        campaign_id = "BJ-2025-05"
        db_data = get_performance_data_by_campaign(campaign_id)
        db_data = [data for data in db_data if data.contract_id.startswith('test_regression_')]

        # 设置一些记录的奖励状态为1，以触发通知
        for data in db_data:
            if data.contract_id == 'test_regression_bj_006_may':
                data.reward_status = 1
                data.reward_type = '幸运数字'
                data.reward_name = '接好运'
                data.notification_sent = 'N'
                data.save()

        # 调用数据库版本的通知函数
        with patch('modules.notification_db_module.create_task') as db_mock_create_task:
            notify_awards_may_beijing_db(db_data)

            # 验证通知系统调用
            self.assertTrue(db_mock_create_task.called, "数据库存储方式下通知系统未被调用")
            print(f"数据库存储方式下通知系统被调用了 {db_mock_create_task.call_count} 次")

        print("\n通知功能测试通过 ✓")

    def test_reward_calculation(self):
        """测试奖励计算"""
        print("\n===== 测试奖励计算 =====")

        # 1. 使用文件存储处理数据
        existing_contract_ids = set()
        housekeeper_award_lists = {}
        file_processed_data = process_data_may_beijing(
            self.test_data_beijing,
            existing_contract_ids,
            housekeeper_award_lists
        )

        # 2. 使用数据库存储处理数据
        campaign_id = "BJ-2025-05"
        province_code = "110000"

        # 先清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_regression_'):
                delete_performance_data(data.id)

        process_data_to_db(
            self.test_data_beijing,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 3. 比较奖励计算结果
        # 从数据库中读取处理后的数据
        db_data = get_performance_data_by_campaign(campaign_id)
        db_data = [data for data in db_data if data.contract_id.startswith('test_regression_')]

        # 检查幸运数字奖励
        file_lucky_rewards = [record for record in file_processed_data if record['奖励类型'] == '幸运数字']
        db_lucky_rewards = [record for record in db_data if record.reward_type == '幸运数字']

        self.assertEqual(len(file_lucky_rewards), len(db_lucky_rewards), "幸运数字奖励数量不一致")
        print(f"幸运数字奖励数量一致: {len(file_lucky_rewards)}")

        # 检查节节高奖励
        file_progressive_rewards = [record for record in file_processed_data if record['奖励类型'] == '节节高']
        db_progressive_rewards = [record for record in db_data if record.reward_type == '节节高']

        self.assertEqual(len(file_progressive_rewards), len(db_progressive_rewards), "节节高奖励数量不一致")
        print(f"节节高奖励数量一致: {len(file_progressive_rewards)}")

        # 检查业绩金额计算
        for file_record in file_processed_data:
            db_record = None
            for record in db_data:
                if record.contract_id == file_record['合同ID(_id)']:
                    db_record = record
                    break

            self.assertIsNotNone(db_record, f"在数据库中找不到合同ID为 {file_record['合同ID(_id)']} 的记录")

            # 比较计入业绩金额
            if '计入业绩金额' in file_record and file_record['计入业绩金额']:
                self.assertEqual(
                    float(file_record['计入业绩金额']),
                    float(db_record.performance_amount),
                    f"合同 {file_record['合同ID(_id)']} 的计入业绩金额不一致"
                )

            print(f"合同 {file_record['合同ID(_id)']} 的奖励计算验证通过")

        print("\n奖励计算测试通过 ✓")

if __name__ == '__main__':
    unittest.main()
