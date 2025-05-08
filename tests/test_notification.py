#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
专项测试：通知逻辑
测试通知逻辑在文件存储和数据库存储两种方式下的一致性
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
from modules.file_utils import write_performance_data_to_csv, get_all_records_from_csv
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

class TestNotification(unittest.TestCase):
    """测试通知逻辑在文件存储和数据库存储两种方式下的一致性"""

    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        # 创建数据库表
        create_performance_data_table()

        # 清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_notify_') or data.contract_id.startswith('test_reward_'):
                delete_performance_data(data.id)

        # 创建临时文件用于测试
        cls.temp_file_bj = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')

        # 创建测试数据
        cls.test_data_beijing = [
            {
                '合同ID(_id)': 'test_notify_bj_001_may',
                '奖励类型': '节节高',
                '奖励名称': '达标奖',
                '激活奖励状态': '1',
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
                '合同ID(_id)': 'test_notify_bj_006_may',  # 末位为6，触发幸运数字奖励
                '奖励类型': '幸运数字',
                '奖励名称': '接好运',
                '激活奖励状态': '1',
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

        # 定义性能数据表头
        cls.performance_data_headers = [
            '合同ID(_id)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)',
            '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State',
            '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', '门槛(doorsill)',
            '款项来源类型(tradeIn)', '活动城市(province)', 'Doorsill', '转化率(conversion)', '平均客单价(average)',
            '活动编号', '活动期内第几个合同', '管家累计单数', '登记时间',
            '管家累计金额', '管家合同数量', '奖金池', '计入业绩金额', '激活奖励状态', '奖励类型', '奖励名称',
            '是否发送通知', '备注'
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
            if data.contract_id.startswith('test_notify_') or data.contract_id.startswith('test_reward_'):
                delete_performance_data(data.id)

    @patch('task_manager.create_task')
    def test_notification_trigger_condition(self, mock_create_task):
        """测试通知触发条件一致性"""
        print("\n===== 测试通知触发条件一致性 =====")

        # 1. 使用文件存储处理数据
        existing_contract_ids = set()
        housekeeper_award_lists = {}
        file_processed_data = process_data_may_beijing(
            self.test_data_beijing,
            existing_contract_ids,
            housekeeper_award_lists
        )

        # 写入临时文件
        write_performance_data_to_csv(self.temp_file_bj.name, file_processed_data, self.performance_data_headers)

        # 2. 使用数据库存储处理数据
        campaign_id = "BJ-2025-05"
        province_code = "110000"

        # 先清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_notify_'):
                delete_performance_data(data.id)

        process_data_to_db(
            self.test_data_beijing,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 3. 测试文件存储通知触发条件
        # 模拟通知函数
        with patch('modules.notification_module.PERFORMANCE_DATA_FILE', self.temp_file_bj.name):
            # 重置mock
            mock_create_task.reset_mock()

            # 调用通知函数
            notify_awards_may_beijing()

            # 获取调用次数
            file_call_count = mock_create_task.call_count

            # 获取调用参数
            file_call_args = [call[0] for call in mock_create_task.call_args_list]

            print(f"\n文件存储通知触发次数: {file_call_count}")
            if file_call_count > 0:
                print("文件存储通知触发参数:")
                for args in file_call_args:
                    print(f"  - {args}")

        # 4. 测试数据库存储通知触发条件
        # 重置mock
        mock_create_task.reset_mock()

        # 获取数据库中的性能数据
        db_data = get_performance_data_by_campaign("BJ-2025-05")

        # 手动设置奖励状态
        for data in db_data:
            if data.contract_id.startswith('test_notify_bj_'):
                data.reward_status = 1
                data.reward_type = '幸运数字'
                data.reward_name = '接好运'
                data.notification_sent = 'N'
                data.save()

        # 重新获取数据库中的性能数据
        db_data = get_performance_data_by_campaign("BJ-2025-05")

        # 调用数据库版本的通知函数
        notify_awards_may_beijing_db(db_data)

        # 获取调用次数
        db_call_count = mock_create_task.call_count

        # 获取调用参数
        db_call_args = [call[0] for call in mock_create_task.call_args_list]

        print(f"\n数据库存储通知触发次数: {db_call_count}")
        if db_call_count > 0:
            print("数据库存储通知触发参数:")
            for args in db_call_args:
                print(f"  - {args}")

        # 5. 验证通知触发条件一致性
        self.assertEqual(file_call_count, db_call_count,
                        f"通知触发次数不一致: 文件={file_call_count}, 数据库={db_call_count}")

        print("\n通知触发条件一致性测试通过 ✓")

    @patch('task_manager.create_task')
    def test_notification_content_generation(self, mock_create_task):
        """测试通知内容生成一致性"""
        print("\n===== 测试通知内容生成一致性 =====")

        # 1. 使用文件存储处理数据
        existing_contract_ids = set()
        housekeeper_award_lists = {}
        file_processed_data = process_data_may_beijing(
            self.test_data_beijing,
            existing_contract_ids,
            housekeeper_award_lists
        )

        # 写入临时文件
        write_performance_data_to_csv(self.temp_file_bj.name, file_processed_data, self.performance_data_headers)

        # 2. 使用数据库存储处理数据
        campaign_id = "BJ-2025-05"
        province_code = "110000"

        # 先清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_notify_'):
                delete_performance_data(data.id)

        process_data_to_db(
            self.test_data_beijing,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 3. 测试文件存储通知内容生成
        # 模拟通知函数
        with patch('modules.notification_module.PERFORMANCE_DATA_FILE', self.temp_file_bj.name):
            # 重置mock
            mock_create_task.reset_mock()

            # 调用通知函数
            notify_awards_may_beijing()

            # 获取通知内容
            file_notification_contents = []
            for call in mock_create_task.call_args_list:
                if call[0][0] == 'send_wecom_message':
                    file_notification_contents.append(call[0][2])  # 消息内容是第三个参数

            print("\n文件存储通知内容:")
            for content in file_notification_contents:
                print(f"  - {content[:100]}...")  # 只打印前100个字符

        # 4. 测试数据库存储通知内容生成
        # 重置mock
        mock_create_task.reset_mock()

        # 获取数据库中的性能数据
        db_data = get_performance_data_by_campaign("BJ-2025-05")

        # 手动设置奖励状态
        for data in db_data:
            if data.contract_id.startswith('test_notify_bj_'):
                data.reward_status = 1
                data.reward_type = '幸运数字'
                data.reward_name = '接好运'
                data.notification_sent = 'N'
                data.save()

        # 重新获取数据库中的性能数据
        db_data = get_performance_data_by_campaign("BJ-2025-05")

        # 调用数据库版本的通知函数
        notify_awards_may_beijing_db(db_data)

        # 获取通知内容
        db_notification_contents = []
        for call in mock_create_task.call_args_list:
            if call[0][0] == 'send_wecom_message':
                db_notification_contents.append(call[0][2])  # 消息内容是第三个参数

        print("\n数据库存储通知内容:")
        for content in db_notification_contents:
            print(f"  - {content[:100]}...")  # 只打印前100个字符

        # 5. 验证通知内容生成一致性
        self.assertEqual(len(file_notification_contents), len(db_notification_contents),
                        f"通知内容数量不一致: 文件={len(file_notification_contents)}, 数据库={len(db_notification_contents)}")

        # 比较通知内容
        for i, (file_content, db_content) in enumerate(zip(file_notification_contents, db_notification_contents)):
            # 由于时间戳和其他动态内容可能不同，我们只比较关键部分
            file_key_parts = [part for part in file_content.split('\n') if '管家' in part or '合同编号' in part or '服务商' in part]
            db_key_parts = [part for part in db_content.split('\n') if '管家' in part or '合同编号' in part or '服务商' in part]

            print(f"\n通知 {i+1} 关键内容比较:")
            print(f"文件存储: {file_key_parts}")
            print(f"数据库存储: {db_key_parts}")

            # 验证关键部分一致
            self.assertEqual(file_key_parts, db_key_parts,
                            f"通知 {i+1} 的关键内容不一致")

        print("\n通知内容生成一致性测试通过 ✓")

    @patch('task_manager.create_task')
    def test_notification_recipient_determination(self, mock_create_task):
        """测试通知接收人确定一致性"""
        print("\n===== 测试通知接收人确定一致性 =====")

        # 1. 使用文件存储处理数据
        existing_contract_ids = set()
        housekeeper_award_lists = {}
        file_processed_data = process_data_may_beijing(
            self.test_data_beijing,
            existing_contract_ids,
            housekeeper_award_lists
        )

        # 写入临时文件
        write_performance_data_to_csv(self.temp_file_bj.name, file_processed_data, self.performance_data_headers)

        # 2. 使用数据库存储处理数据
        campaign_id = "BJ-2025-05"
        province_code = "110000"

        # 先清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_notify_'):
                delete_performance_data(data.id)

        process_data_to_db(
            self.test_data_beijing,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 3. 测试文件存储通知接收人确定
        # 模拟通知函数
        with patch('modules.notification_module.PERFORMANCE_DATA_FILE', self.temp_file_bj.name):
            # 重置mock
            mock_create_task.reset_mock()

            # 调用通知函数
            notify_awards_may_beijing()

            # 获取接收人
            file_recipients = []
            for call in mock_create_task.call_args_list:
                if call[0][0] == 'send_wecom_message':
                    file_recipients.append(call[0][1])  # 接收人是第二个参数

            print("\n文件存储通知接收人:")
            for recipient in file_recipients:
                print(f"  - {recipient}")

        # 4. 测试数据库存储通知接收人确定
        # 重置mock
        mock_create_task.reset_mock()

        # 获取数据库中的性能数据
        db_data = get_performance_data_by_campaign("BJ-2025-05")

        # 手动设置奖励状态
        for data in db_data:
            if data.contract_id.startswith('test_notify_bj_'):
                data.reward_status = 1
                data.reward_type = '幸运数字'
                data.reward_name = '接好运'
                data.notification_sent = 'N'
                data.save()

        # 重新获取数据库中的性能数据
        db_data = get_performance_data_by_campaign("BJ-2025-05")

        # 调用数据库版本的通知函数
        notify_awards_may_beijing_db(db_data)

        # 获取接收人
        db_recipients = []
        for call in mock_create_task.call_args_list:
            if call[0][0] == 'send_wecom_message':
                db_recipients.append(call[0][1])  # 接收人是第二个参数

        print("\n数据库存储通知接收人:")
        for recipient in db_recipients:
            print(f"  - {recipient}")

        # 5. 验证通知接收人确定一致性
        self.assertEqual(len(file_recipients), len(db_recipients),
                        f"通知接收人数量不一致: 文件={len(file_recipients)}, 数据库={len(db_recipients)}")

        # 比较接收人
        for i, (file_recipient, db_recipient) in enumerate(zip(file_recipients, db_recipients)):
            print(f"\n通知 {i+1} 接收人比较:")
            print(f"文件存储: {file_recipient}")
            print(f"数据库存储: {db_recipient}")

            # 验证接收人一致
            self.assertEqual(file_recipient, db_recipient,
                            f"通知 {i+1} 的接收人不一致: 文件={file_recipient}, 数据库={db_recipient}")

        print("\n通知接收人确定一致性测试通过 ✓")

    @patch('task_manager.create_task')
    def test_notification_status_tracking(self, mock_create_task):
        """测试通知状态跟踪一致性"""
        print("\n===== 测试通知状态跟踪一致性 =====")

        # 1. 使用文件存储处理数据
        existing_contract_ids = set()
        housekeeper_award_lists = {}
        file_processed_data = process_data_may_beijing(
            self.test_data_beijing,
            existing_contract_ids,
            housekeeper_award_lists
        )

        # 写入临时文件
        write_performance_data_to_csv(self.temp_file_bj.name, file_processed_data, self.performance_data_headers)

        # 2. 使用数据库存储处理数据
        campaign_id = "BJ-2025-05"
        province_code = "110000"

        # 先清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_notify_'):
                delete_performance_data(data.id)

        process_data_to_db(
            self.test_data_beijing,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 3. 测试文件存储通知状态跟踪
        # 模拟通知函数
        with patch('modules.notification_module.PERFORMANCE_DATA_FILE', self.temp_file_bj.name):
            # 重置mock
            mock_create_task.reset_mock()

            # 调用通知函数
            notify_awards_may_beijing()

            # 读取更新后的文件数据
            file_data_after = get_all_records_from_csv(self.temp_file_bj.name)

            # 检查通知状态
            file_notification_statuses = {record['合同ID(_id)']: record['是否发送通知'] for record in file_data_after}

            print("\n文件存储通知状态:")
            for contract_id, status in file_notification_statuses.items():
                print(f"  - {contract_id}: {status}")

        # 4. 测试数据库存储通知状态跟踪
        # 重置mock
        mock_create_task.reset_mock()

        # 获取数据库中的性能数据
        db_data = get_performance_data_by_campaign("BJ-2025-05")

        # 手动设置奖励状态
        for data in db_data:
            if data.contract_id.startswith('test_notify_bj_'):
                data.reward_status = 1
                data.reward_type = '幸运数字'
                data.reward_name = '接好运'
                data.notification_sent = 'N'
                data.save()

        # 重新获取数据库中的性能数据
        db_data = get_performance_data_by_campaign("BJ-2025-05")

        # 调用数据库版本的通知函数
        notify_awards_may_beijing_db(db_data)

        # 读取更新后的数据库数据
        db_data_after = get_performance_data_by_campaign(campaign_id)
        db_data_after = [data for data in db_data_after
                        if data.contract_id.startswith('test_notify_bj_')]

        # 检查通知状态
        db_notification_statuses = {data.contract_id: data.notification_sent for data in db_data_after}

        print("\n数据库存储通知状态:")
        for contract_id, status in db_notification_statuses.items():
            print(f"  - {contract_id}: {status}")

        # 5. 验证通知状态跟踪一致性
        self.assertEqual(len(file_notification_statuses), len(db_notification_statuses),
                        f"通知状态数量不一致: 文件={len(file_notification_statuses)}, 数据库={len(db_notification_statuses)}")

        # 比较通知状态
        for contract_id in file_notification_statuses:
            if contract_id in db_notification_statuses:
                file_status = file_notification_statuses[contract_id]
                db_status = db_notification_statuses[contract_id]

                print(f"\n合同 {contract_id} 通知状态比较:")
                print(f"文件存储: {file_status}")
                print(f"数据库存储: {db_status}")

                # 验证通知状态一致
                self.assertEqual(file_status, db_status,
                                f"合同 {contract_id} 的通知状态不一致: 文件={file_status}, 数据库={db_status}")

        print("\n通知状态跟踪一致性测试通过 ✓")

if __name__ == '__main__':
    unittest.main()
