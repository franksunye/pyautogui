#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试签约台账数据库功能
"""

import os
import sys
import logging
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from modules.performance_data_manager import (
    PerformanceData, get_performance_data_by_id, get_performance_data_by_contract_id,
    get_performance_data_by_campaign, get_performance_data_by_housekeeper,
    get_all_performance_data, delete_performance_data, get_unique_contract_ids,
    get_performance_data_count
)
from scripts.create_performance_data_table import create_performance_data_table

# 设置日志
setup_logging()

def test_create_table():
    """测试创建表"""
    logging.info("测试创建表...")
    create_performance_data_table()
    logging.info("测试创建表完成")

def test_insert_data():
    """测试插入数据"""
    logging.info("测试插入数据...")
    
    # 创建北京数据
    bj_data = PerformanceData(
        campaign_id="BJ-2025-05",
        contract_id="test_bj_001",
        province_code="110000",
        service_appointment_num="GD2025045495",
        status=1,
        housekeeper="石王磊",
        contract_doc_num="YHWX-BJ-JDHS-2025050001",
        contract_amount=30548.8,
        paid_amount=15274.4,
        difference=15274.4,
        state=1,
        create_time="2025-05-01T11:36:22.444+08:00",
        org_name="北京久盾宏盛建筑工程有限公司",
        signed_date="2025-05-01T11:42:07.904+08:00",
        doorsill=15274.4,
        trade_in=1,
        conversion=0.0,
        average=0.0,
        contract_number_in_activity=1,
        housekeeper_total_amount=30548.8,
        housekeeper_contract_count=1,
        bonus_pool=0.0,
        performance_amount=30548.8,
        reward_status=0,
        reward_type="",
        reward_name="",
        notification_sent="Y",
        remark="距离达成节节高奖励条件还需 5 单",
        register_time="2025-05-06"
    )
    
    # 保存北京数据
    bj_id = bj_data.save()
    logging.info(f"北京数据保存成功，ID: {bj_id}")
    
    # 创建上海数据
    sh_data = PerformanceData(
        campaign_id="SH-2025-04",
        contract_id="test_sh_001",
        province_code="310000",
        service_appointment_num="GD2025050096",
        status=1,
        housekeeper="李涛",
        contract_doc_num="YHWX-SH-QQFS-2025050001",
        contract_amount=3023.0,
        paid_amount=3023.0,
        difference=0.0,
        state=1,
        create_time="2025-05-02T15:05:38.083+08:00",
        org_name="上海荃璆实业有限公司",
        signed_date="2025-05-02T16:57:29.449+08:00",
        doorsill=3023.0,
        trade_in=1,
        conversion=0.3333333333333333,
        average=3023.0,
        contract_number_in_activity=1,
        housekeeper_total_amount=3023.0,
        housekeeper_contract_count=1,
        bonus_pool=6.046,
        performance_amount=3023.0,
        reward_status=0,
        reward_type="",
        reward_name="",
        notification_sent="Y",
        remark="距离达成节节高奖励条件还需 4 单",
        register_time="2025-05-06"
    )
    
    # 保存上海数据
    sh_id = sh_data.save()
    logging.info(f"上海数据保存成功，ID: {sh_id}")
    
    logging.info("测试插入数据完成")
    
    return bj_id, sh_id

def test_query_data(bj_id, sh_id):
    """测试查询数据"""
    logging.info("测试查询数据...")
    
    # 根据ID查询
    bj_data = get_performance_data_by_id(bj_id)
    logging.info(f"根据ID查询北京数据: {bj_data.contract_doc_num}")
    
    sh_data = get_performance_data_by_id(sh_id)
    logging.info(f"根据ID查询上海数据: {sh_data.contract_doc_num}")
    
    # 根据合同ID查询
    bj_data = get_performance_data_by_contract_id("test_bj_001")
    logging.info(f"根据合同ID查询北京数据: {bj_data.contract_doc_num}")
    
    sh_data = get_performance_data_by_contract_id("test_sh_001")
    logging.info(f"根据合同ID查询上海数据: {sh_data.contract_doc_num}")
    
    # 根据活动ID查询
    bj_list = get_performance_data_by_campaign("BJ-2025-05")
    logging.info(f"根据活动ID查询北京数据，数量: {len(bj_list)}")
    
    sh_list = get_performance_data_by_campaign("SH-2025-04")
    logging.info(f"根据活动ID查询上海数据，数量: {len(sh_list)}")
    
    # 根据管家查询
    bj_housekeeper_list = get_performance_data_by_housekeeper("石王磊")
    logging.info(f"根据管家查询北京数据，数量: {len(bj_housekeeper_list)}")
    
    sh_housekeeper_list = get_performance_data_by_housekeeper("李涛")
    logging.info(f"根据管家查询上海数据，数量: {len(sh_housekeeper_list)}")
    
    # 查询所有数据
    all_data = get_all_performance_data()
    logging.info(f"查询所有数据，数量: {len(all_data)}")
    
    # 获取唯一合同ID
    unique_contract_ids = get_unique_contract_ids()
    logging.info(f"唯一合同ID数量: {len(unique_contract_ids)}")
    
    # 获取数据总数
    count = get_performance_data_count()
    logging.info(f"数据总数: {count}")
    
    logging.info("测试查询数据完成")

def test_update_data(bj_id):
    """测试更新数据"""
    logging.info("测试更新数据...")
    
    # 获取数据
    bj_data = get_performance_data_by_id(bj_id)
    
    # 更新数据
    bj_data.contract_amount = 35000.0
    bj_data.paid_amount = 17500.0
    bj_data.difference = 17500.0
    bj_data.housekeeper_total_amount = 35000.0
    bj_data.performance_amount = 35000.0
    bj_data.remark = "已更新"
    
    # 保存更新
    bj_data.save()
    
    # 重新获取数据
    updated_data = get_performance_data_by_id(bj_id)
    
    # 验证更新
    logging.info(f"更新前合同金额: 30548.8, 更新后: {updated_data.contract_amount}")
    logging.info(f"更新前支付金额: 15274.4, 更新后: {updated_data.paid_amount}")
    logging.info(f"更新前差额: 15274.4, 更新后: {updated_data.difference}")
    logging.info(f"更新前管家累计金额: 30548.8, 更新后: {updated_data.housekeeper_total_amount}")
    logging.info(f"更新前计入业绩金额: 30548.8, 更新后: {updated_data.performance_amount}")
    logging.info(f"更新前备注: 距离达成节节高奖励条件还需 5 单, 更新后: {updated_data.remark}")
    
    logging.info("测试更新数据完成")

def test_delete_data(sh_id):
    """测试删除数据"""
    logging.info("测试删除数据...")
    
    # 删除前数据总数
    before_count = get_performance_data_count()
    logging.info(f"删除前数据总数: {before_count}")
    
    # 删除数据
    result = delete_performance_data(sh_id)
    logging.info(f"删除结果: {result}")
    
    # 删除后数据总数
    after_count = get_performance_data_count()
    logging.info(f"删除后数据总数: {after_count}")
    
    # 验证删除
    logging.info(f"删除前后差异: {before_count - after_count}")
    
    logging.info("测试删除数据完成")

def main():
    """主函数"""
    try:
        # 测试创建表
        test_create_table()
        
        # 测试插入数据
        bj_id, sh_id = test_insert_data()
        
        # 测试查询数据
        test_query_data(bj_id, sh_id)
        
        # 测试更新数据
        test_update_data(bj_id)
        
        # 测试删除数据
        test_delete_data(sh_id)
        
        print("所有测试完成")
        return True
    except Exception as e:
        logging.error(f"测试过程中发生错误: {e}")
        print(f"测试过程中发生错误: {e}")
        return False

if __name__ == "__main__":
    main()
