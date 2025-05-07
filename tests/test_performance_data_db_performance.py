#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
性能测试：签约台账数据库性能
测试数据库操作性能，与文件操作性能比较
"""

import os
import sys
import time
import unittest
import csv
import tempfile
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
from modules.file_utils import (
    get_all_records_from_csv, write_performance_data_to_csv,
    collect_unique_contract_ids_from_file
)

# 设置日志
setup_logging()

class TestPerformanceDataDBPerformance(unittest.TestCase):
    """性能测试：签约台账数据库性能"""

    @classmethod
    def setUpClass(cls):
        """测试前的准备工作"""
        # 创建数据库表
        create_performance_data_table()
        
        # 创建测试数据
        cls.test_data = []
        for i in range(100):
            cls.test_data.append({
                'campaign_id': "PERF-2025-05",
                'contract_id': f"test_perf_{i:03d}",
                'province_code': "110000",
                'service_appointment_num': f"GD2025045{i:03d}",
                'status': 1,
                'housekeeper': "性能测试管家",
                'contract_doc_num': f"YHWX-PERF-2025050{i:03d}",
                'contract_amount': 30000.0 + i * 100,
                'paid_amount': 15000.0 + i * 50,
                'difference': 15000.0 + i * 50,
                'state': 1,
                'create_time': "2025-05-01T11:36:22.444+08:00",
                'org_name': "性能测试服务商",
                'signed_date': "2025-05-01T11:42:07.904+08:00",
                'doorsill': 15000.0 + i * 50,
                'trade_in': 1,
                'conversion': 0.5,
                'average': 30000.0 + i * 100,
                'contract_number_in_activity': i + 1,
                'housekeeper_total_amount': 30000.0 * (i + 1),
                'housekeeper_contract_count': i + 1,
                'bonus_pool': 60.0 + i,
                'performance_amount': 30000.0 + i * 100,
                'reward_status': 1,
                'reward_type': "58",
                'reward_name': "接好运万元以上",
                'notification_sent': "N",
                'remark': f"性能测试备注{i}",
                'register_time': "2025-05-06"
            })
        
        # 创建临时CSV文件
        cls.temp_csv_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        cls.temp_csv_file.close()
        
        # 写入CSV文件
        with open(cls.temp_csv_file.name, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[
                '活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)',
                'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)',
                '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)',
                '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)',
                '转化率(conversion)', '平均客单价(average)', '活动期内第几个合同', '管家累计金额',
                '管家累计单数', '奖金池', '计入业绩金额', '激活奖励状态', '奖励类型', '奖励名称',
                '是否发送通知', '备注', '登记时间'
            ])
            writer.writeheader()
            
            for i in range(100):
                writer.writerow({
                    '活动编号': "PERF-2025-05",
                    '合同ID(_id)': f"test_perf_{i:03d}",
                    '活动城市(province)': "110000",
                    '工单编号(serviceAppointmentNum)': f"GD2025045{i:03d}",
                    'Status': "1",
                    '管家(serviceHousekeeper)': "性能测试管家",
                    '合同编号(contractdocNum)': f"YHWX-PERF-2025050{i:03d}",
                    '合同金额(adjustRefundMoney)': str(30000.0 + i * 100),
                    '支付金额(paidAmount)': str(15000.0 + i * 50),
                    '差额(difference)': str(15000.0 + i * 50),
                    'State': "1",
                    '创建时间(createTime)': "2025-05-01T11:36:22.444+08:00",
                    '服务商(orgName)': "性能测试服务商",
                    '签约时间(signedDate)': "2025-05-01T11:42:07.904+08:00",
                    'Doorsill': str(15000.0 + i * 50),
                    '款项来源类型(tradeIn)': "1",
                    '转化率(conversion)': "0.5",
                    '平均客单价(average)': str(30000.0 + i * 100),
                    '活动期内第几个合同': str(i + 1),
                    '管家累计金额': str(30000.0 * (i + 1)),
                    '管家累计单数': str(i + 1),
                    '奖金池': str(60.0 + i),
                    '计入业绩金额': str(30000.0 + i * 100),
                    '激活奖励状态': "1",
                    '奖励类型': "58",
                    '奖励名称': "接好运万元以上",
                    '是否发送通知': "N",
                    '备注': f"性能测试备注{i}",
                    '登记时间': "2025-05-06"
                })

    @classmethod
    def tearDownClass(cls):
        """测试后的清理工作"""
        # 删除测试数据
        for i in range(100):
            data = get_performance_data_by_contract_id(f"test_perf_{i:03d}")
            if data:
                delete_performance_data(data.id)
        
        # 删除临时CSV文件
        os.unlink(cls.temp_csv_file.name)

    def test_01_db_insertion_performance(self):
        """测试数据库插入性能"""
        # 记录开始时间
        start_time = time.time()
        
        # 插入数据
        for data in self.test_data:
            perf_data = PerformanceData(**data)
            perf_data.save()
        
        # 记录结束时间
        end_time = time.time()
        
        # 计算耗时
        elapsed_time = end_time - start_time
        
        print(f"\n数据库插入100条记录耗时: {elapsed_time:.6f}秒")
        
        # 验证数据是否成功插入
        count = get_performance_data_count()
        self.assertGreaterEqual(count, 100, "数据库中应该至少有100条记录")

    def test_02_db_query_performance(self):
        """测试数据库查询性能"""
        # 记录开始时间
        start_time = time.time()
        
        # 查询数据
        data_list = get_performance_data_by_campaign("PERF-2025-05")
        
        # 记录结束时间
        end_time = time.time()
        
        # 计算耗时
        elapsed_time = end_time - start_time
        
        print(f"数据库查询所有记录耗时: {elapsed_time:.6f}秒")
        
        # 验证查询结果
        self.assertEqual(len(data_list), 100, "应该查询到100条记录")

    def test_03_db_update_performance(self):
        """测试数据库更新性能"""
        # 记录开始时间
        start_time = time.time()
        
        # 更新数据
        for i in range(100):
            data = get_performance_data_by_contract_id(f"test_perf_{i:03d}")
            if data:
                data.remark = f"已更新的性能测试备注{i}"
                data.save()
        
        # 记录结束时间
        end_time = time.time()
        
        # 计算耗时
        elapsed_time = end_time - start_time
        
        print(f"数据库更新100条记录耗时: {elapsed_time:.6f}秒")
        
        # 验证更新结果
        data = get_performance_data_by_contract_id("test_perf_050")
        self.assertEqual(data.remark, "已更新的性能测试备注50", "备注应该已更新")

    def test_04_file_read_performance(self):
        """测试文件读取性能"""
        # 记录开始时间
        start_time = time.time()
        
        # 读取CSV文件
        records = get_all_records_from_csv(self.temp_csv_file.name)
        
        # 记录结束时间
        end_time = time.time()
        
        # 计算耗时
        elapsed_time = end_time - start_time
        
        print(f"文件读取100条记录耗时: {elapsed_time:.6f}秒")
        
        # 验证读取结果
        self.assertEqual(len(records), 100, "应该读取到100条记录")

    def test_05_file_write_performance(self):
        """测试文件写入性能"""
        # 读取CSV文件
        records = get_all_records_from_csv(self.temp_csv_file.name)
        
        # 修改记录
        for record in records:
            record['备注'] = f"已更新的文件性能测试备注{records.index(record)}"
        
        # 记录开始时间
        start_time = time.time()
        
        # 写入CSV文件
        write_performance_data_to_csv(self.temp_csv_file.name, records, list(records[0].keys()))
        
        # 记录结束时间
        end_time = time.time()
        
        # 计算耗时
        elapsed_time = end_time - start_time
        
        print(f"文件写入100条记录耗时: {elapsed_time:.6f}秒")
        
        # 验证写入结果
        new_records = get_all_records_from_csv(self.temp_csv_file.name)
        self.assertEqual(len(new_records), 100, "应该写入100条记录")
        self.assertEqual(new_records[50]['备注'], "已更新的文件性能测试备注50", "备注应该已更新")

    def test_06_collect_unique_contract_ids_performance(self):
        """测试收集唯一合同ID性能"""
        # 记录开始时间
        start_time = time.time()
        
        # 收集唯一合同ID
        unique_ids = collect_unique_contract_ids_from_file(self.temp_csv_file.name)
        
        # 记录结束时间
        end_time = time.time()
        
        # 计算耗时
        elapsed_time = end_time - start_time
        
        print(f"文件收集唯一合同ID耗时: {elapsed_time:.6f}秒")
        
        # 验证结果
        self.assertEqual(len(unique_ids), 100, "应该有100个唯一合同ID")

    def test_07_get_unique_contract_ids_performance(self):
        """测试获取唯一合同ID性能"""
        # 记录开始时间
        start_time = time.time()
        
        # 获取唯一合同ID
        unique_ids = get_unique_contract_ids()
        
        # 记录结束时间
        end_time = time.time()
        
        # 计算耗时
        elapsed_time = end_time - start_time
        
        print(f"数据库获取唯一合同ID耗时: {elapsed_time:.6f}秒")
        
        # 验证结果
        self.assertGreaterEqual(len(unique_ids), 100, "应该至少有100个唯一合同ID")

if __name__ == '__main__':
    unittest.main()
