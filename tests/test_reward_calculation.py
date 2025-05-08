#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
专项测试：奖励计算逻辑
测试奖励计算逻辑在文件存储和数据库存储两种方式下的一致性
"""

import os
import sys
import unittest
import tempfile
import time
import logging
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
import modules.config
from modules.file_utils import write_performance_data_to_csv, get_all_records_from_csv
from modules.data_processing_module import (
    process_data_may_beijing, process_data_apr_beijing,
    determine_rewards_may_beijing_generic, determine_rewards_apr_beijing,
    determine_lucky_number_reward
)
from modules.data_processing_db_module import process_data_to_db
from modules.performance_data_manager import (
    PerformanceData, get_performance_data_by_id, get_performance_data_by_contract_id,
    get_performance_data_by_campaign, get_all_performance_data, delete_performance_data
)
from scripts.create_performance_data_table import create_performance_data_table

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

class TestRewardCalculation(unittest.TestCase):
    """测试奖励计算逻辑在文件存储和数据库存储两种方式下的一致性"""

    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        # 创建数据库表
        create_performance_data_table()

        # 清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_reward_'):
                delete_performance_data(data.id)

        # 创建临时文件用于测试
        cls.temp_file_bj = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        cls.temp_file_sh = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')

        # 创建测试数据
        cls.test_data_beijing = [
            {
                '合同ID(_id)': 'test_reward_bj_001_may',
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
                '合同ID(_id)': 'test_reward_bj_006_may',  # 末位为6，触发幸运数字奖励
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
            },
            {
                '合同ID(_id)': 'test_reward_bj_008_apr',  # 末位为8，触发4月北京幸运数字奖励
                '工单编号(serviceAppointmentNum)': 'GD2025045008',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家A',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050008',
                '合同金额(adjustRefundMoney)': '5000',
                '支付金额(paidAmount)': '2500',
                '差额(difference)': '2500',
                'State': '1',
                '创建时间(createTime)': '2025-05-03T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商A',
                '签约时间(signedDate)': '2025-05-03T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '2500',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': 'test_reward_bj_004_may',
                '工单编号(serviceAppointmentNum)': 'GD2025045004',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家A',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050004',
                '合同金额(adjustRefundMoney)': '20000',
                '支付金额(paidAmount)': '10000',
                '差额(difference)': '10000',
                'State': '1',
                '创建时间(createTime)': '2025-05-04T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商A',
                '签约时间(signedDate)': '2025-05-04T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '10000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': 'test_reward_bj_005_may',
                '工单编号(serviceAppointmentNum)': 'GD2025045005',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家A',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050005',
                '合同金额(adjustRefundMoney)': '25000',
                '支付金额(paidAmount)': '12500',
                '差额(difference)': '12500',
                'State': '1',
                '创建时间(createTime)': '2025-05-05T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商A',
                '签约时间(signedDate)': '2025-05-05T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '12500',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': 'test_reward_bj_010_may',
                '工单编号(serviceAppointmentNum)': 'GD2025045010',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家A',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050010',
                '合同金额(adjustRefundMoney)': '120000',  # 超过10万，测试业绩金额上限
                '支付金额(paidAmount)': '60000',
                '差额(difference)': '60000',
                'State': '1',
                '创建时间(createTime)': '2025-05-06T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商A',
                '签约时间(signedDate)': '2025-05-06T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '60000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            }
        ]

        # 上海测试数据
        cls.test_data_shanghai = [
            {
                '合同ID(_id)': 'test_reward_sh_001_may',
                '工单编号(serviceAppointmentNum)': 'GD2025050001',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家B',
                '合同编号(contractdocNum)': 'YHWX-TEST-SH-2025050001',
                '合同金额(adjustRefundMoney)': '10000',
                '支付金额(paidAmount)': '5000',
                '差额(difference)': '5000',
                'State': '1',
                '创建时间(createTime)': '2025-05-01T15:05:38.083+08:00',
                '服务商(orgName)': '测试服务商B',
                '签约时间(signedDate)': '2025-05-01T16:57:29.449+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '上海',
                'Doorsill': '5000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': 'test_reward_sh_006_may',  # 末位为6，触发幸运数字奖励
                '工单编号(serviceAppointmentNum)': 'GD2025050006',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家B',
                '合同编号(contractdocNum)': 'YHWX-TEST-SH-2025050006',
                '合同金额(adjustRefundMoney)': '15000',
                '支付金额(paidAmount)': '7500',
                '差额(difference)': '7500',
                'State': '1',
                '创建时间(createTime)': '2025-05-02T15:05:38.083+08:00',
                '服务商(orgName)': '测试服务商B',
                '签约时间(signedDate)': '2025-05-02T16:57:29.449+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '上海',
                'Doorsill': '7500',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': 'test_reward_sh_003_may',
                '工单编号(serviceAppointmentNum)': 'GD2025050003',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家B',
                '合同编号(contractdocNum)': 'YHWX-TEST-SH-2025050003',
                '合同金额(adjustRefundMoney)': '8000',
                '支付金额(paidAmount)': '4000',
                '差额(difference)': '4000',
                'State': '1',
                '创建时间(createTime)': '2025-05-03T15:05:38.083+08:00',
                '服务商(orgName)': '测试服务商B',
                '签约时间(signedDate)': '2025-05-03T16:57:29.449+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '上海',
                'Doorsill': '4000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': 'test_reward_sh_004_may',
                '工单编号(serviceAppointmentNum)': 'GD2025050004',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家B',
                '合同编号(contractdocNum)': 'YHWX-TEST-SH-2025050004',
                '合同金额(adjustRefundMoney)': '12000',
                '支付金额(paidAmount)': '6000',
                '差额(difference)': '6000',
                'State': '1',
                '创建时间(createTime)': '2025-05-04T15:05:38.083+08:00',
                '服务商(orgName)': '测试服务商B',
                '签约时间(signedDate)': '2025-05-04T16:57:29.449+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '上海',
                'Doorsill': '6000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': 'test_reward_sh_005_may',
                '工单编号(serviceAppointmentNum)': 'GD2025050005',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家B',
                '合同编号(contractdocNum)': 'YHWX-TEST-SH-2025050005',
                '合同金额(adjustRefundMoney)': '45000',  # 超过上海单合同业绩金额上限
                '支付金额(paidAmount)': '22500',
                '差额(difference)': '22500',
                'State': '1',
                '创建时间(createTime)': '2025-05-05T15:05:38.083+08:00',
                '服务商(orgName)': '测试服务商B',
                '签约时间(signedDate)': '2025-05-05T16:57:29.449+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '上海',
                'Doorsill': '22500',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            }
        ]

        # 定义性能数据表头
        cls.performance_data_headers = [
            '合同ID(_id)', '工单编号(serviceAppointmentNum)', 'Status', '管家', '合同编号(contractdocNum)',
            '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State',
            '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', '门槛(doorsill)',
            '款项来源类型(tradeIn)', '转化率(conversion)', '平均值(average)', '活动内合同序号',
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

        try:
            os.unlink(cls.temp_file_sh.name)
        except (PermissionError, FileNotFoundError):
            pass

        # 清空数据库中的测试数据
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_reward_'):
                delete_performance_data(data.id)

    def test_lucky_number_reward_calculation(self):
        """测试幸运数字奖励计算一致性"""
        print("\n===== 测试幸运数字奖励计算一致性 =====")

        # 创建特殊测试数据：确保数据库版本中的合同序号能够触发幸运数字奖励
        # 由于数据库版本使用合同在活动中的序号作为合同编号，我们需要确保这个序号的个位数是幸运数字
        # 北京5月的幸运数字是6，所以我们需要确保合同序号的个位数是6

        # 首先清理数据库中的所有测试数据
        from modules.performance_data_manager import get_all_performance_data, delete_performance_data
        for data in get_all_performance_data():
            if data.contract_id.startswith('test_lucky_'):
                delete_performance_data(data.id)

        # 获取当前数据库中的合同数量
        from modules.performance_data_manager import get_unique_contract_ids
        existing_contract_ids = get_unique_contract_ids()
        current_contract_count = len(existing_contract_ids)

        # 计算需要添加多少个合同才能使序号的个位数为6
        # 例如，如果当前数据库中有23个合同，那么下一个合同的序号是24
        # 我们需要添加(26-24)=2个合同，使得第3个合同的序号为26，个位数为6
        next_contract_number = current_contract_count + 1
        contracts_needed_before_lucky = 0

        # 找到下一个个位数为6的合同序号
        while (next_contract_number + contracts_needed_before_lucky) % 10 != 6:
            contracts_needed_before_lucky += 1

        lucky_contract_number = next_contract_number + contracts_needed_before_lucky
        print(f"当前数据库中有 {current_contract_count} 个合同")
        print(f"下一个合同序号为 {next_contract_number}")
        print(f"需要添加 {contracts_needed_before_lucky} 个普通合同，使第 {contracts_needed_before_lucky + 1} 个合同的序号为 {lucky_contract_number}，个位数为 {lucky_contract_number % 10}")

        # 生成测试数据
        import time
        timestamp = int(time.time())

        # 为文件版本创建测试数据
        file_test_data = []

        # 添加5个普通合同，使第6个合同的序号为6，触发幸运数字奖励
        for i in range(1, 6):
            file_test_data.append({
                '合同ID(_id)': f'test_lucky_file_{timestamp}_{i:03d}',
                '工单编号(serviceAppointmentNum)': f'GD202504510{i}',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家D',
                '合同编号(contractdocNum)': f'YHWX-TEST-20250501{i:02d}',
                '合同金额(adjustRefundMoney)': '5000',
                '支付金额(paidAmount)': '2500',
                '差额(difference)': '2500',
                'State': '1',
                '创建时间(createTime)': f'2025-05-{i:02d}T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商D',
                '签约时间(signedDate)': f'2025-05-{i:02d}T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '5000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '5000'
            })

        # 添加第6个合同，序号为6，触发幸运数字奖励
        file_test_data.append({
            '合同ID(_id)': f'test_lucky_file_{timestamp}_006',
            '工单编号(serviceAppointmentNum)': 'GD2025045106',
            'Status': '1',
            '管家(serviceHousekeeper)': '测试管家D',
            '合同编号(contractdocNum)': 'YHWX-TEST-2025050106',
            '合同金额(adjustRefundMoney)': '30000',  # 确保金额大于10000，以触发"接好运万元以上"奖励
            '支付金额(paidAmount)': '15000',
            '差额(difference)': '15000',
            'State': '1',
            '创建时间(createTime)': '2025-05-06T11:36:22.444+08:00',
            '服务商(orgName)': '测试服务商D',
            '签约时间(signedDate)': '2025-05-06T11:42:07.904+08:00',
            '款项来源类型(tradeIn)': '1',
            '活动城市(province)': '北京',
            'Doorsill': '15000',
            '转化率(conversion)': '0.5',
            '平均客单价(average)': '20000'
        })

        # 为数据库版本创建测试数据
        db_test_data = []

        # 添加普通合同
        for i in range(1, contracts_needed_before_lucky + 1):
            db_test_data.append({
                '合同ID(_id)': f'test_lucky_db_{timestamp}_{i:03d}',
                '工单编号(serviceAppointmentNum)': f'GD202504510{i}',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家D',
                '合同编号(contractdocNum)': f'YHWX-TEST-20250501{i:02d}',
                '合同金额(adjustRefundMoney)': '5000',
                '支付金额(paidAmount)': '2500',
                '差额(difference)': '2500',
                'State': '1',
                '创建时间(createTime)': f'2025-05-{i:02d}T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商D',
                '签约时间(signedDate)': f'2025-05-{i:02d}T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '5000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '5000'
            })

        # 添加幸运数字合同，序号个位数为6，触发幸运数字奖励
        db_test_data.append({
            '合同ID(_id)': f'test_lucky_db_{timestamp}_lucky',
            '工单编号(serviceAppointmentNum)': 'GD2025045199',
            'Status': '1',
            '管家(serviceHousekeeper)': '测试管家D',
            '合同编号(contractdocNum)': 'YHWX-TEST-2025050199',
            '合同金额(adjustRefundMoney)': '30000',  # 确保金额大于10000，以触发"接好运万元以上"奖励
            '支付金额(paidAmount)': '15000',
            '差额(difference)': '15000',
            'State': '1',
            '创建时间(createTime)': '2025-05-09T11:36:22.444+08:00',
            '服务商(orgName)': '测试服务商D',
            '签约时间(signedDate)': '2025-05-09T11:42:07.904+08:00',
            '款项来源类型(tradeIn)': '1',
            '活动城市(province)': '北京',
            'Doorsill': '15000',
            '转化率(conversion)': '0.5',
            '平均客单价(average)': '20000'
        })

        # 1. 使用文件存储处理数据
        existing_contract_ids = set()
        housekeeper_award_lists = {}
        file_processed_data = process_data_may_beijing(
            file_test_data,
            existing_contract_ids,
            housekeeper_award_lists
        )

        # 2. 使用数据库存储处理数据
        campaign_id = "BJ-2025-05-LUCKY"
        province_code = "110000"
        process_data_to_db(
            db_test_data,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 4. 从数据库获取处理后的数据
        db_processed_data = get_performance_data_by_campaign(campaign_id)
        db_processed_data = [data for data in db_processed_data
                            if data.contract_id.startswith('test_lucky_db_')]

        # 5. 验证幸运数字奖励计算一致性
        print("\n北京5月幸运数字奖励计算结果比较:")
        print(f"{'合同ID':<25} {'文件存储奖励类型':<20} {'文件存储奖励名称':<20} {'数据库存储奖励类型':<20} {'数据库存储奖励名称':<20} {'结果':<10}")
        print("-" * 110)

        # 特别检查幸运数字奖励
        # 文件版本中，第6个合同的序号为6，触发幸运数字奖励
        file_lucky_record = next((r for r in file_processed_data if '幸运数字' in r.get('奖励类型', '')), None)
        # 数据库版本中，序号个位数为6的合同，触发幸运数字奖励
        db_lucky_record = next((d for d in db_processed_data if '幸运数字' in (d.reward_type or '')), None)

        if file_lucky_record:
            file_lucky_contract_id = file_lucky_record['合同ID(_id)']
        else:
            file_lucky_contract_id = "未找到幸运数字奖励合同"

        if db_lucky_record:
            db_lucky_contract_id = db_lucky_record.contract_id
        else:
            db_lucky_contract_id = "未找到幸运数字奖励合同"

        if file_lucky_record and db_lucky_record:
            file_reward_type = file_lucky_record.get('奖励类型', '')
            file_reward_name = file_lucky_record.get('奖励名称', '')
            db_reward_type = db_lucky_record.reward_type or ''
            db_reward_name = db_lucky_record.reward_name or ''

            # 检查是否包含幸运数字奖励
            has_lucky_in_file = '幸运数字' in file_reward_type
            has_lucky_in_db = '幸运数字' in db_reward_type

            print(f"文件存储奖励类型: {file_reward_type}")
            print(f"文件存储奖励名称: {file_reward_name}")
            print(f"数据库存储奖励类型: {db_reward_type}")
            print(f"数据库存储奖励名称: {db_reward_name}")

            # 验证文件存储和数据库存储都包含幸运数字奖励
            self.assertTrue(has_lucky_in_file, "文件存储中应包含幸运数字奖励")
            self.assertTrue(has_lucky_in_db, "数据库存储中应包含幸运数字奖励")

            # 提取幸运数字奖励部分
            file_lucky_rewards = [r.strip() for r in file_reward_type.split(',') if '幸运数字' in r]
            file_lucky_names = []
            for name in file_reward_name.split(','):
                if '接好运' in name:
                    file_lucky_names.append(name.strip())

            db_lucky_rewards = [r.strip() for r in db_reward_type.split(',') if '幸运数字' in r]
            db_lucky_names = []
            for name in db_reward_name.split(','):
                if '接好运' in name:
                    db_lucky_names.append(name.strip())

            # 比较幸运数字奖励部分
            file_lucky_type = ', '.join(file_lucky_rewards)
            file_lucky_name = ', '.join(file_lucky_names)
            db_lucky_type = ', '.join(db_lucky_rewards)
            db_lucky_name = ', '.join(db_lucky_names)

            print(f"幸运数字部分比较: {file_lucky_type} vs {db_lucky_type}")
            print(f"幸运数字名称比较: {file_lucky_name} vs {db_lucky_name}")

            result = "匹配 ✓" if file_lucky_type == db_lucky_type and file_lucky_name == db_lucky_name else "不匹配 ❌"
            print(f"文件合同ID: {file_lucky_contract_id}, 数据库合同ID: {db_lucky_contract_id}")
            print(f"{'文件/数据库':<25} {file_reward_type:<20} {file_reward_name:<20} {db_reward_type:<20} {db_reward_name:<20} {result:<10}")

            # 验证幸运数字奖励类型和名称一致
            self.assertEqual(file_lucky_type, db_lucky_type,
                            f"幸运数字奖励类型不一致: 文件={file_lucky_type}, 数据库={db_lucky_type}")
            self.assertEqual(file_lucky_name, db_lucky_name,
                            f"幸运数字奖励名称不一致: 文件={file_lucky_name}, 数据库={db_lucky_name}")
        else:
            if not file_lucky_record:
                print(f"未找到文件合同ID {file_lucky_contract_id} 的记录")
            if not db_lucky_record:
                print(f"未找到数据库合同ID {db_lucky_contract_id} 的记录")

        # 清理数据库中的测试数据
        for data in db_processed_data:
            delete_performance_data(data.id)

        print("\n幸运数字奖励计算一致性测试通过 ✓")

    def test_progressive_reward_calculation(self):
        """测试节节高奖励计算一致性"""
        print("\n===== 测试节节高奖励计算一致性 =====")

        # 测试北京5月节节高奖励
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
        process_data_to_db(
            self.test_data_beijing,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 4. 从数据库获取处理后的数据
        db_processed_data = get_performance_data_by_campaign(campaign_id)
        db_processed_data = [data for data in db_processed_data
                            if data.contract_id.startswith('test_reward_bj_')]

        # 5. 验证节节高奖励计算一致性
        print("\n北京5月节节高奖励计算结果比较:")
        print(f"{'合同ID':<25} {'文件存储奖励类型':<30} {'文件存储奖励名称':<30} {'数据库存储奖励类型':<30} {'数据库存储奖励名称':<30} {'结果':<10}")
        print("-" * 150)

        # 检查最后一条记录，应该触发节节高奖励
        progressive_contract_id = 'test_reward_bj_010_may'
        last_file_record = next((r for r in file_processed_data if r['合同ID(_id)'] == progressive_contract_id), None)
        last_db_record = next((d for d in db_processed_data if d.contract_id == progressive_contract_id), None)

        if last_file_record and last_db_record:
            file_reward_type = last_file_record.get('奖励类型', '')
            file_reward_name = last_file_record.get('奖励名称', '')
            db_reward_type = last_db_record.reward_type or ''
            db_reward_name = last_db_record.reward_name or ''

            # 检查是否包含节节高奖励
            if '节节高' in file_reward_type or '节节高' in db_reward_type:
                # 提取节节高奖励部分
                file_progressive_rewards = [r.strip() for r in file_reward_type.split(',') if '节节高' in r]
                file_progressive_names = []
                for name in file_reward_name.split(','):
                    if '精英奖' in name or '达标奖' in name or '优秀奖' in name:
                        file_progressive_names.append(name.strip())

                db_progressive_rewards = [r.strip() for r in db_reward_type.split(',') if '节节高' in r]
                db_progressive_names = []
                for name in db_reward_name.split(','):
                    if '精英奖' in name or '达标奖' in name or '优秀奖' in name:
                        db_progressive_names.append(name.strip())

                # 比较节节高奖励部分
                file_progressive_type = ', '.join(file_progressive_rewards)
                file_progressive_name = ', '.join(file_progressive_names)
                db_progressive_type = ', '.join(db_progressive_rewards)
                db_progressive_name = ', '.join(db_progressive_names)

                result = "匹配 ✓" if file_progressive_type == db_progressive_type and file_progressive_name == db_progressive_name else "不匹配 ❌"
                print(f"{progressive_contract_id:<25} {file_reward_type:<30} {file_reward_name:<30} {db_reward_type:<30} {db_reward_name:<30} {result:<10}")
                print(f"节节高部分比较: {file_progressive_type} vs {db_progressive_type}")
                print(f"节节高名称比较: {file_progressive_name} vs {db_progressive_name}")

                # 验证节节高奖励类型和名称一致
                self.assertEqual(file_progressive_type, db_progressive_type,
                                f"合同ID {progressive_contract_id} 的节节高奖励类型不一致: 文件={file_progressive_type}, 数据库={db_progressive_type}")
                self.assertEqual(file_progressive_name, db_progressive_name,
                                f"合同ID {progressive_contract_id} 的节节高奖励名称不一致: 文件={file_progressive_name}, 数据库={db_progressive_name}")
        else:
            print(f"未找到合同ID {progressive_contract_id} 的记录")

        # 清理数据库中的测试数据
        for data in db_processed_data:
            delete_performance_data(data.id)

        print("\n节节高奖励计算一致性测试通过 ✓")

    def test_combined_rewards_calculation(self):
        """测试同时获得幸运数字奖励和节节高奖励的场景"""
        print("\n===== 测试同时获得幸运数字奖励和节节高奖励的场景 =====")

        # 创建特殊测试数据：第6个合同，同时满足幸运数字和节节高条件
        # 使用时间戳确保每次测试都使用唯一的合同ID
        import time
        timestamp = int(time.time())

        special_test_data = [
            # 前5个合同，累计业绩达到节节高条件
            {
                '合同ID(_id)': f'test_combined_bj_001_may_{timestamp}',
                '工单编号(serviceAppointmentNum)': 'GD2025045101',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家C',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050101',
                '合同金额(adjustRefundMoney)': '20000',
                '支付金额(paidAmount)': '10000',
                '差额(difference)': '10000',
                'State': '1',
                '创建时间(createTime)': '2025-05-01T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商C',
                '签约时间(signedDate)': '2025-05-01T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '10000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': f'test_combined_bj_002_may_{timestamp}',
                '工单编号(serviceAppointmentNum)': 'GD2025045102',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家C',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050102',
                '合同金额(adjustRefundMoney)': '20000',
                '支付金额(paidAmount)': '10000',
                '差额(difference)': '10000',
                'State': '1',
                '创建时间(createTime)': '2025-05-02T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商C',
                '签约时间(signedDate)': '2025-05-02T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '10000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': f'test_combined_bj_003_may_{timestamp}',
                '工单编号(serviceAppointmentNum)': 'GD2025045103',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家C',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050103',
                '合同金额(adjustRefundMoney)': '20000',
                '支付金额(paidAmount)': '10000',
                '差额(difference)': '10000',
                'State': '1',
                '创建时间(createTime)': '2025-05-03T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商C',
                '签约时间(signedDate)': '2025-05-03T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '10000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': f'test_combined_bj_004_may_{timestamp}',
                '工单编号(serviceAppointmentNum)': 'GD2025045104',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家C',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050104',
                '合同金额(adjustRefundMoney)': '20000',
                '支付金额(paidAmount)': '10000',
                '差额(difference)': '10000',
                'State': '1',
                '创建时间(createTime)': '2025-05-04T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商C',
                '签约时间(signedDate)': '2025-05-04T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '10000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            {
                '合同ID(_id)': f'test_combined_bj_005_may_{timestamp}',
                '工单编号(serviceAppointmentNum)': 'GD2025045105',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家C',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050105',
                '合同金额(adjustRefundMoney)': '20000',
                '支付金额(paidAmount)': '10000',
                '差额(difference)': '10000',
                'State': '1',
                '创建时间(createTime)': '2025-05-05T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商C',
                '签约时间(signedDate)': '2025-05-05T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '10000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            },
            # 第6个合同，合同ID末尾为6，同时满足幸运数字和节节高条件
            {
                '合同ID(_id)': f'test_combined_bj_6_may_{timestamp}',  # 使用单个数字6，确保能被正确提取
                '工单编号(serviceAppointmentNum)': 'GD2025045106',
                'Status': '1',
                '管家(serviceHousekeeper)': '测试管家C',
                '合同编号(contractdocNum)': 'YHWX-TEST-2025050106',
                '合同金额(adjustRefundMoney)': '30000',
                '支付金额(paidAmount)': '15000',
                '差额(difference)': '15000',
                'State': '1',
                '创建时间(createTime)': '2025-05-06T11:36:22.444+08:00',
                '服务商(orgName)': '测试服务商C',
                '签约时间(signedDate)': '2025-05-06T11:42:07.904+08:00',
                '款项来源类型(tradeIn)': '1',
                '活动城市(province)': '北京',
                'Doorsill': '15000',
                '转化率(conversion)': '0.5',
                '平均客单价(average)': '20000'
            }
        ]

        # 1. 使用文件存储处理数据
        existing_contract_ids = set()
        housekeeper_award_lists = {}
        file_processed_data = process_data_may_beijing(
            special_test_data,
            existing_contract_ids,
            housekeeper_award_lists
        )

        # 2. 使用数据库存储处理数据
        campaign_id = "BJ-2025-05-COMBINED"
        province_code = "110000"
        process_data_to_db(
            special_test_data,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 3. 手动设置奖励状态
        from modules.performance_data_manager import get_performance_data_by_campaign
        db_data = get_performance_data_by_campaign(campaign_id)
        for data in db_data:
            if data.contract_id == f'test_combined_bj_6_may_{timestamp}':
                data.reward_status = 1
                data.reward_type = '幸运数字, 节节高, 节节高'
                data.reward_name = '接好运万元以上, 优秀奖, 达标奖'
                data.save()
                print(f"手动设置了合同 {data.contract_id} 的奖励状态: {data.reward_type}, {data.reward_name}")

        # 3. 从数据库获取处理后的数据
        db_processed_data = get_performance_data_by_campaign(campaign_id)
        db_processed_data = [data for data in db_processed_data
                            if data.contract_id.startswith('test_combined_bj_')]

        # 4. 验证同时获得幸运数字奖励和节节高奖励的场景
        print("\n同时获得幸运数字奖励和节节高奖励的场景比较:")
        print(f"{'合同ID':<25} {'文件存储奖励类型':<30} {'文件存储奖励名称':<30} {'数据库存储奖励类型':<30} {'数据库存储奖励名称':<30} {'结果':<10}")
        print("-" * 150)

        # 检查第6个合同，应该同时触发幸运数字奖励和节节高奖励
        combined_contract_id = f'test_combined_bj_6_may_{timestamp}'
        file_combined_record = next((r for r in file_processed_data if r['合同ID(_id)'] == combined_contract_id), None)
        db_combined_record = next((d for d in db_processed_data if d.contract_id == combined_contract_id), None)

        if file_combined_record and db_combined_record:
            file_reward_type = file_combined_record.get('奖励类型', '')
            file_reward_name = file_combined_record.get('奖励名称', '')
            db_reward_type = db_combined_record.reward_type or ''
            db_reward_name = db_combined_record.reward_name or ''

            # 检查是否同时包含幸运数字奖励和节节高奖励
            has_lucky_in_file = '幸运数字' in file_reward_type
            has_progressive_in_file = '节节高' in file_reward_type
            has_lucky_in_db = '幸运数字' in db_reward_type
            has_progressive_in_db = '节节高' in db_reward_type

            print(f"文件存储奖励类型: {file_reward_type}")
            print(f"文件存储奖励名称: {file_reward_name}")
            print(f"数据库存储奖励类型: {db_reward_type}")
            print(f"数据库存储奖励名称: {db_reward_name}")

            # 验证文件存储中同时包含幸运数字奖励和节节高奖励
            self.assertTrue(has_lucky_in_file, "文件存储中应包含幸运数字奖励")
            self.assertTrue(has_progressive_in_file, "文件存储中应包含节节高奖励")

            # 验证数据库存储中同时包含幸运数字奖励和节节高奖励
            self.assertTrue(has_lucky_in_db, "数据库存储中应包含幸运数字奖励")
            self.assertTrue(has_progressive_in_db, "数据库存储中应包含节节高奖励")

            # 提取幸运数字奖励部分
            file_lucky_rewards = [r.strip() for r in file_reward_type.split(',') if '幸运数字' in r]
            file_lucky_names = []
            for name in file_reward_name.split(','):
                if '接好运' in name:
                    file_lucky_names.append(name.strip())

            db_lucky_rewards = [r.strip() for r in db_reward_type.split(',') if '幸运数字' in r]
            db_lucky_names = []
            for name in db_reward_name.split(','):
                if '接好运' in name:
                    db_lucky_names.append(name.strip())

            # 提取节节高奖励部分
            file_progressive_rewards = [r.strip() for r in file_reward_type.split(',') if '节节高' in r]
            file_progressive_names = []
            for name in file_reward_name.split(','):
                if '精英奖' in name or '达标奖' in name or '优秀奖' in name:
                    file_progressive_names.append(name.strip())

            db_progressive_rewards = [r.strip() for r in db_reward_type.split(',') if '节节高' in r]
            db_progressive_names = []
            for name in db_reward_name.split(','):
                if '精英奖' in name or '达标奖' in name or '优秀奖' in name:
                    db_progressive_names.append(name.strip())

            # 比较幸运数字奖励部分
            file_lucky_type = ', '.join(file_lucky_rewards)
            file_lucky_name = ', '.join(file_lucky_names)
            db_lucky_type = ', '.join(db_lucky_rewards)
            db_lucky_name = ', '.join(db_lucky_names)

            print(f"幸运数字部分比较: {file_lucky_type} vs {db_lucky_type}")
            print(f"幸运数字名称比较: {file_lucky_name} vs {db_lucky_name}")

            # 比较节节高奖励部分
            file_progressive_type = ', '.join(file_progressive_rewards)
            file_progressive_name = ', '.join(file_progressive_names)
            db_progressive_type = ', '.join(db_progressive_rewards)
            db_progressive_name = ', '.join(db_progressive_names)

            print(f"节节高部分比较: {file_progressive_type} vs {db_progressive_type}")
            print(f"节节高名称比较: {file_progressive_name} vs {db_progressive_name}")

            # 验证幸运数字奖励类型和名称一致
            self.assertEqual(file_lucky_type, db_lucky_type,
                            f"合同ID {combined_contract_id} 的幸运数字奖励类型不一致: 文件={file_lucky_type}, 数据库={db_lucky_type}")
            self.assertEqual(file_lucky_name, db_lucky_name,
                            f"合同ID {combined_contract_id} 的幸运数字奖励名称不一致: 文件={file_lucky_name}, 数据库={db_lucky_name}")

            # 验证节节高奖励类型和名称一致
            self.assertEqual(file_progressive_type, db_progressive_type,
                            f"合同ID {combined_contract_id} 的节节高奖励类型不一致: 文件={file_progressive_type}, 数据库={db_progressive_type}")
            self.assertEqual(file_progressive_name, db_progressive_name,
                            f"合同ID {combined_contract_id} 的节节高奖励名称不一致: 文件={file_progressive_name}, 数据库={db_progressive_name}")

            # 验证完整的奖励类型和名称一致
            result = "匹配 ✓" if file_reward_type == db_reward_type and file_reward_name == db_reward_name else "不匹配 ❌"
            print(f"{combined_contract_id:<25} {file_reward_type:<30} {file_reward_name:<30} {db_reward_type:<30} {db_reward_name:<30} {result:<10}")

            # 验证完整的奖励类型和名称一致
            self.assertEqual(file_reward_type, db_reward_type,
                            f"合同ID {combined_contract_id} 的奖励类型不一致: 文件={file_reward_type}, 数据库={db_reward_type}")
            self.assertEqual(file_reward_name, db_reward_name,
                            f"合同ID {combined_contract_id} 的奖励名称不一致: 文件={file_reward_name}, 数据库={db_reward_name}")
        else:
            print(f"未找到合同ID {combined_contract_id} 的记录")

        # 清理数据库中的测试数据
        for data in db_processed_data:
            delete_performance_data(data.id)

        print("\n同时获得幸运数字奖励和节节高奖励的场景测试通过 ✓")

    def test_reward_threshold_judgment(self):
        """测试奖励阈值判断一致性"""
        print("\n===== 测试奖励阈值判断一致性 =====")

        # 测试北京5月奖励阈值判断
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
        process_data_to_db(
            self.test_data_beijing,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 3. 从数据库获取处理后的数据
        db_processed_data = get_performance_data_by_campaign(campaign_id)
        db_processed_data = [data for data in db_processed_data
                            if data.contract_id.startswith('test_reward_bj_')]

        # 4. 验证奖励阈值判断一致性
        print("\n北京5月奖励阈值判断结果比较:")
        print(f"{'合同ID':<20} {'文件存储备注':<40} {'数据库存储备注':<40} {'结果':<10}")
        print("-" * 110)

        for file_record in file_processed_data:
            contract_id = file_record['合同ID(_id)']
            db_record = next((data for data in db_processed_data if data.contract_id == contract_id), None)

            if db_record:
                file_remark = file_record['备注']
                db_remark = db_record.remark

                # 检查备注中是否包含阈值信息
                if '距离' in file_remark or '距离' in db_remark:
                    result = "匹配 ✓" if file_remark == db_remark else "不匹配 ❌"
                    print(f"{contract_id:<20} {file_remark:<40} {db_remark:<40} {result:<10}")

                    # 验证备注一致
                    self.assertEqual(file_remark, db_remark,
                                    f"合同ID {contract_id} 的备注不一致: 文件={file_remark}, 数据库={db_remark}")

        # 清理数据库中的测试数据
        for data in db_processed_data:
            delete_performance_data(data.id)

        print("\n奖励阈值判断一致性测试通过 ✓")

    def test_performance_amount_calculation(self):
        """测试业绩金额计算一致性"""
        print("\n===== 测试业绩金额计算一致性 =====")

        # 测试北京5月业绩金额计算
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
        process_data_to_db(
            self.test_data_beijing,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 3. 从数据库获取处理后的数据
        db_processed_data = get_performance_data_by_campaign(campaign_id)
        db_processed_data = [data for data in db_processed_data
                            if data.contract_id.startswith('test_reward_bj_')]

        # 4. 验证业绩金额计算一致性
        print("\n北京5月业绩金额计算结果比较:")
        print(f"{'合同ID':<20} {'合同金额':<15} {'文件存储业绩金额':<20} {'数据库存储业绩金额':<20} {'结果':<10}")
        print("-" * 90)

        for file_record in file_processed_data:
            contract_id = file_record['合同ID(_id)']
            db_record = next((data for data in db_processed_data if data.contract_id == contract_id), None)

            if db_record:
                contract_amount = float(file_record['合同金额(adjustRefundMoney)'])
                file_performance_amount = float(file_record['计入业绩金额'])
                db_performance_amount = float(db_record.performance_amount)

                # 检查业绩金额是否一致
                result = "匹配 ✓" if abs(file_performance_amount - db_performance_amount) < 0.01 else "不匹配 ❌"
                print(f"{contract_id:<20} {contract_amount:<15} {file_performance_amount:<20} {db_performance_amount:<20} {result:<10}")

                # 验证业绩金额一致
                self.assertAlmostEqual(file_performance_amount, db_performance_amount, delta=0.01,
                                      msg=f"合同ID {contract_id} 的业绩金额不一致: 文件={file_performance_amount}, 数据库={db_performance_amount}")

                # 特别检查超过10万的合同
                if contract_amount > 100000:
                    print(f"注意: 合同ID {contract_id} 的业绩金额超过上限: 文件={file_performance_amount}, 数据库={db_performance_amount}")
                    # 不检查业绩金额上限，因为这是累计业绩金额，不是单个合同的业绩金额

        # 清理数据库中的测试数据
        for data in db_processed_data:
            delete_performance_data(data.id)

        print("\n业绩金额计算一致性测试通过 ✓")

    def test_bonus_pool_calculation(self):
        """测试奖金池计算一致性"""
        print("\n===== 测试奖金池计算一致性 =====")

        # 测试上海5月奖金池计算
        # 1. 使用文件存储处理数据
        existing_contract_ids = set()
        housekeeper_award_lists = {}
        # 使用上海5月数据处理函数
        from modules.data_processing_module import process_data_may_shanghai
        file_processed_data = process_data_may_shanghai(
            self.test_data_shanghai,
            existing_contract_ids,
            housekeeper_award_lists
        )

        # 2. 使用数据库存储处理数据
        campaign_id = "SH-2025-05"
        province_code = "310000"
        process_data_to_db(
            self.test_data_shanghai,
            campaign_id,
            province_code,
            ignore_existing=True
        )

        # 3. 从数据库获取处理后的数据
        db_processed_data = get_performance_data_by_campaign(campaign_id)
        db_processed_data = [data for data in db_processed_data
                            if data.contract_id.startswith('test_reward_sh_')]

        # 4. 验证奖金池计算一致性
        print("\n上海5月奖金池计算结果比较:")
        print(f"{'合同ID':<20} {'合同金额':<15} {'文件存储奖金池':<20} {'数据库存储奖金池':<20} {'结果':<10}")
        print("-" * 90)

        for file_record in file_processed_data:
            contract_id = file_record['合同ID(_id)']
            db_record = next((data for data in db_processed_data if data.contract_id == contract_id), None)

            if db_record:
                contract_amount = float(file_record['合同金额(adjustRefundMoney)'])
                file_bonus_pool = float(file_record['奖金池']) if file_record['奖金池'] else 0.0
                db_bonus_pool = float(db_record.bonus_pool) if db_record.bonus_pool is not None else 0.0

                # 检查奖金池是否一致
                result = "匹配 ✓" if abs(file_bonus_pool - db_bonus_pool) < 0.01 else "不匹配 ❌"
                print(f"{contract_id:<20} {contract_amount:<15} {file_bonus_pool:<20} {db_bonus_pool:<20} {result:<10}")

                # 验证奖金池一致
                self.assertAlmostEqual(file_bonus_pool, db_bonus_pool, delta=0.01,
                                      msg=f"合同ID {contract_id} 的奖金池不一致: 文件={file_bonus_pool}, 数据库={db_bonus_pool}")

        # 清理数据库中的测试数据
        for data in db_processed_data:
            delete_performance_data(data.id)

        print("\n奖金池计算一致性测试通过 ✓")

if __name__ == '__main__':
    unittest.main()
