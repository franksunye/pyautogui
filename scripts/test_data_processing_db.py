#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试数据处理模块的数据库版本
"""

import os
import sys
import logging
import csv
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from modules.performance_data_manager import (
    get_performance_data_by_campaign, get_performance_data_count, get_unique_contract_ids
)
from modules.data_processing_db_module import (
    process_beijing_data_to_db, process_shanghai_data_to_db, import_csv_to_db
)
from scripts.create_performance_data_table import create_performance_data_table

# 设置日志
setup_logging()

def create_test_contract_data(city="BJ"):
    """创建测试合同数据"""
    if city == "BJ":
        return [
            {
                '合同ID(_id)': 'test_bj_002',
                '活动城市(province)': '110000',
                '工单编号(serviceAppointmentNum)': 'GD2025045496',
                'Status': '1',
                '管家(serviceHousekeeper)': '张丁山',
                '合同编号(contractdocNum)': 'YHWX-BJ-JJSH-2025050001',
                '合同金额(adjustRefundMoney)': '5500.0',
                '支付金额(paidAmount)': '5500.0',
                '差额(difference)': '0.0',
                'State': '1',
                '创建时间(createTime)': '2025-05-02T10:01:14.253+08:00',
                '服务商(orgName)': '北京建君盛华技术服务有限公司',
                '签约时间(signedDate)': '2025-05-02T10:12:27.628+08:00',
                'Doorsill': '5500.0',
                '款项来源类型(tradeIn)': '1',
                '转化率(conversion)': '',
                '平均客单价(average)': ''
            },
            {
                '合同ID(_id)': 'test_bj_003',
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
    else:  # SH
        return [
            {
                '合同ID(_id)': 'test_sh_002',
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
                '合同ID(_id)': 'test_sh_003',
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

def create_test_csv_file(city="BJ"):
    """创建测试CSV文件"""
    filename = f"state/test_contract_data_{city}.csv"
    
    # 创建测试数据
    data = create_test_contract_data(city)
    
    # 获取字段名
    fieldnames = data[0].keys()
    
    # 写入CSV文件
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    logging.info(f"创建测试CSV文件: {filename}")
    
    return filename

def test_process_beijing_data():
    """测试处理北京数据"""
    logging.info("测试处理北京数据...")
    
    # 获取处理前的数据数量
    before_count = get_performance_data_count()
    logging.info(f"处理前数据数量: {before_count}")
    
    # 创建测试数据
    data = create_test_contract_data("BJ")
    
    # 处理数据
    processed_count = process_beijing_data_to_db(data)
    
    # 获取处理后的数据数量
    after_count = get_performance_data_count()
    logging.info(f"处理后数据数量: {after_count}")
    
    # 验证处理结果
    logging.info(f"处理的数据数量: {processed_count}")
    logging.info(f"数据数量增加: {after_count - before_count}")
    
    # 获取北京数据
    bj_data = get_performance_data_by_campaign("BJ-2025-05")
    logging.info(f"北京数据数量: {len(bj_data)}")
    
    logging.info("测试处理北京数据完成")

def test_process_shanghai_data():
    """测试处理上海数据"""
    logging.info("测试处理上海数据...")
    
    # 获取处理前的数据数量
    before_count = get_performance_data_count()
    logging.info(f"处理前数据数量: {before_count}")
    
    # 创建测试数据
    data = create_test_contract_data("SH")
    
    # 处理数据
    processed_count = process_shanghai_data_to_db(data)
    
    # 获取处理后的数据数量
    after_count = get_performance_data_count()
    logging.info(f"处理后数据数量: {after_count}")
    
    # 验证处理结果
    logging.info(f"处理的数据数量: {processed_count}")
    logging.info(f"数据数量增加: {after_count - before_count}")
    
    # 获取上海数据
    sh_data = get_performance_data_by_campaign("SH-2025-04")
    logging.info(f"上海数据数量: {len(sh_data)}")
    
    logging.info("测试处理上海数据完成")

def test_import_csv():
    """测试导入CSV文件"""
    logging.info("测试导入CSV文件...")
    
    # 创建测试CSV文件
    bj_csv = create_test_csv_file("BJ")
    sh_csv = create_test_csv_file("SH")
    
    # 获取处理前的数据数量
    before_count = get_performance_data_count()
    logging.info(f"处理前数据数量: {before_count}")
    
    # 导入北京数据
    bj_result = import_csv_to_db(bj_csv, "BJ-2025-05", "110000")
    logging.info(f"导入北京数据结果: {bj_result}")
    
    # 导入上海数据
    sh_result = import_csv_to_db(sh_csv, "SH-2025-04", "310000")
    logging.info(f"导入上海数据结果: {sh_result}")
    
    # 获取处理后的数据数量
    after_count = get_performance_data_count()
    logging.info(f"处理后数据数量: {after_count}")
    
    # 验证处理结果
    logging.info(f"数据数量增加: {after_count - before_count}")
    
    # 获取北京数据
    bj_data = get_performance_data_by_campaign("BJ-2025-05")
    logging.info(f"北京数据数量: {len(bj_data)}")
    
    # 获取上海数据
    sh_data = get_performance_data_by_campaign("SH-2025-04")
    logging.info(f"上海数据数量: {len(sh_data)}")
    
    logging.info("测试导入CSV文件完成")
    
    # 清理测试文件
    os.remove(bj_csv)
    os.remove(sh_csv)

def main():
    """主函数"""
    try:
        # 确保表已创建
        create_performance_data_table()
        
        # 测试处理北京数据
        test_process_beijing_data()
        
        # 测试处理上海数据
        test_process_shanghai_data()
        
        # 测试导入CSV文件
        test_import_csv()
        
        print("所有测试完成")
        return True
    except Exception as e:
        logging.error(f"测试过程中发生错误: {e}")
        print(f"测试过程中发生错误: {e}")
        return False

if __name__ == "__main__":
    main()
