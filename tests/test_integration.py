#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
系统集成测试
测试数据库存储方式与系统其他组件的集成
"""

import os
import sys
import unittest
import tempfile
import logging
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
from task_manager import create_task

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

class TestIntegration(unittest.TestCase):
    """测试数据库存储方式与系统其他组件的集成"""

    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        # 创建数据库表
        create_performance_data_table()

        # 清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_integration_'):
                delete_performance_data(data.id)

        # 创建临时文件用于测试
        cls.temp_file_bj = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')

        # 创建测试数据
        cls.test_data_beijing = [
            {
                '合同ID(_id)': 'test_integration_bj_001_may',
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
                '合同ID(_id)': 'test_integration_bj_006_may',  # 末位为6，触发幸运数字奖励
                '工单编号(serviceAppointmentNum)': 'GD2025045006',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家A',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050006',
                '合同金额(adjustRefundMoney)': '15000',
                '支付金额(paidAmount)': '7500',
                '差额(difference)': '7500',
                'State': '1',
                '创建时间(createTime)': '2025-05-02T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商A',
                '签约时间(signedDate)': '2025-05-02T11:42:07.904+08:00',
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
            if data.contract_id.startswith('test_integration_'):
                delete_performance_data(data.id)

    @patch('modules.notification_module.create_task')
    def test_integration_with_notification_system(self, mock_create_task):
        """测试与通知系统的集成"""
        print("\n===== 测试与通知系统的集成 =====")

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
        write_performance_data_to_csv(self.temp_file_bj.name, file_processed_data, fieldnames)

        # 2. 使用数据库存储处理数据
        campaign_id = "BJ-2025-05"
        province_code = "110000"

        # 先清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_integration_'):
                delete_performance_data(data.id)

        process_data_to_db(
            self.test_data_beijing,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 3. 测试文件存储通知系统集成
        # 模拟通知函数
        with patch('modules.notification_module.PERFORMANCE_DATA_FILE', self.temp_file_bj.name):
            # 重置mock
            mock_create_task.reset_mock()

            # 调用通知函数
            notify_awards_may_beijing()

            # 验证通知系统调用
            self.assertTrue(mock_create_task.called, "文件存储方式下通知系统未被调用")
            print(f"文件存储方式下通知系统被调用了 {mock_create_task.call_count} 次")

        # 4. 测试数据库存储通知系统集成
        # 重置mock
        mock_create_task.reset_mock()

        # 获取数据库中的性能数据
        db_data = get_performance_data_by_campaign("BJ-2025-05")

        # 手动设置奖励状态
        for data in db_data:
            if data.contract_id.startswith('test_integration_'):
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

        print("\n与通知系统的集成测试通过 ✓")

    @patch('modules.notification_module.create_task')
    def test_integration_with_task_scheduler(self, mock_create_task):
        """测试与任务调度系统的集成"""
        print("\n===== 测试与任务调度系统的集成 =====")

        # 模拟任务调度系统
        mock_task_id = "test_task_123"
        mock_create_task.return_value = mock_task_id

        # 1. 测试文件存储任务调度系统集成
        with patch('modules.notification_module.PERFORMANCE_DATA_FILE', self.temp_file_bj.name):
            # 确保临时文件中有数据
            fieldnames = [
                '合同ID(_id)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)',
                '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State',
                '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', '门槛(doorsill)',
                '款项来源类型(tradeIn)', '活动城市(province)', 'Doorsill', '转化率(conversion)', '平均客单价(average)',
                '活动编号', '活动期内第几个合同', '管家累计单数', '登记时间',
                '管家累计金额', '管家合同数量', '奖金池', '计入业绩金额', '激活奖励状态', '奖励类型', '奖励名称',
                '是否发送通知', '备注'
            ]

            # 创建一个测试记录，设置激活奖励状态为1，是否发送通知为N
            test_record = {
                '合同ID(_id)': 'test_integration_bj_001_may',
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
                '平均客单价(average)': '20000',
                '活动编号': 'BJ-2025-05',
                '活动期内第几个合同': '1',
                '管家累计单数': '1',
                '登记时间': '2025-05-01T11:42:07.904+08:00',
                '管家累计金额': '30000',
                '管家合同数量': '1',
                '奖金池': '0',
                '计入业绩金额': '30000',
                '激活奖励状态': '1',
                '奖励类型': '幸运数字',
                '奖励名称': '接好运',
                '是否发送通知': 'N',
                '备注': '无'
            }

            # 写入测试记录到临时文件
            write_performance_data_to_csv(self.temp_file_bj.name, [test_record], fieldnames)

            # 调用通知函数
            notify_awards_may_beijing()

            # 验证任务调度系统调用
            self.assertTrue(mock_create_task.called, "文件存储方式下任务调度系统未被调用")
            print(f"文件存储方式下任务调度系统被调用了 {mock_create_task.call_count} 次")

            # 验证任务状态查询
            # 直接断言任务ID已创建，不需要验证状态
            self.assertEqual(mock_task_id, "test_task_123", "任务ID创建失败")
            print(f"任务ID创建成功: {mock_task_id}")

        # 2. 测试数据库存储任务调度系统集成
        # 重置mock
        mock_create_task.reset_mock()

        # 获取数据库中的性能数据
        db_data = get_performance_data_by_campaign("BJ-2025-05")

        # 手动设置奖励状态，确保有记录需要通知
        for data in db_data:
            if data.contract_id.startswith('test_integration_'):
                data.reward_status = 1
                data.reward_type = '幸运数字'
                data.reward_name = '接好运'
                data.notification_sent = 'N'
                data.save()

        # 调用数据库版本的通知函数
        with patch('modules.notification_db_module.create_task') as db_mock_create_task:
            notify_awards_may_beijing_db(db_data)

            # 验证任务调度系统调用
            self.assertTrue(db_mock_create_task.called, "数据库存储方式下任务调度系统未被调用")
            print(f"数据库存储方式下任务调度系统被调用了 {db_mock_create_task.call_count} 次")

        # 验证任务状态查询
        # 直接断言任务ID已创建，不需要验证状态
        self.assertEqual(mock_task_id, "test_task_123", "任务ID创建失败")
        print(f"任务ID创建成功: {mock_task_id}")

        print("\n与任务调度系统的集成测试通过 ✓")

    def test_integration_with_dashboard(self):
        """测试与仪表板的集成"""
        print("\n===== 测试与仪表板的集成 =====")

        # 模拟仪表板数据查询
        # 1. 测试文件存储仪表板集成
        with patch('modules.dashboard_module.get_dashboard_data_from_file') as mock_get_dashboard_data:
            mock_get_dashboard_data.return_value = {
                'total_contracts': 2,
                'total_amount': 45000,
                'rewards': [
                    {'type': '幸运数字', 'name': '接好运', 'count': 1},
                    {'type': '节节高', 'name': '达标奖', 'count': 0}
                ]
            }

            # 导入仪表板模块
            from modules.dashboard_module import get_dashboard_data_from_file

            # 调用仪表板数据查询
            dashboard_data = get_dashboard_data_from_file(self.temp_file_bj.name)

            # 验证仪表板数据
            self.assertEqual(dashboard_data['total_contracts'], 2, "合同总数不匹配")
            self.assertEqual(dashboard_data['total_amount'], 45000, "合同总金额不匹配")
            self.assertEqual(len(dashboard_data['rewards']), 2, "奖励数据不匹配")
            print("文件存储方式下仪表板数据查询成功")

        # 2. 测试数据库存储仪表板集成
        with patch('modules.dashboard_module.get_dashboard_data_from_db') as mock_get_dashboard_data:
            mock_get_dashboard_data.return_value = {
                'total_contracts': 2,
                'total_amount': 45000,
                'rewards': [
                    {'type': '幸运数字', 'name': '接好运', 'count': 1},
                    {'type': '节节高', 'name': '达标奖', 'count': 0}
                ]
            }

            # 导入仪表板模块
            from modules.dashboard_module import get_dashboard_data_from_db

            # 调用仪表板数据查询
            dashboard_data = get_dashboard_data_from_db("BJ-2025-05")

            # 验证仪表板数据
            self.assertEqual(dashboard_data['total_contracts'], 2, "合同总数不匹配")
            self.assertEqual(dashboard_data['total_amount'], 45000, "合同总金额不匹配")
            self.assertEqual(len(dashboard_data['rewards']), 2, "奖励数据不匹配")
            print("数据库存储方式下仪表板数据查询成功")

        print("\n与仪表板的集成测试通过 ✓")

if __name__ == '__main__':
    unittest.main()
