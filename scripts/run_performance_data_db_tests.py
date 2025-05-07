#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
运行签约台账数据库测试
"""

import os
import sys
import unittest
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging

# 设置日志
setup_logging()

def run_tests():
    """运行所有测试"""
    # 创建测试加载器
    loader = unittest.TestLoader()
    
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加单元测试
    unit_tests = loader.discover('tests', pattern='test_performance_data_db_unit.py')
    suite.addTest(unit_tests)
    
    # 添加数据处理模块测试
    data_processing_tests = loader.discover('tests', pattern='test_data_processing_db_unit.py')
    suite.addTest(data_processing_tests)
    
    # 添加集成测试
    integration_tests = loader.discover('tests', pattern='test_jobs_db_integration.py')
    suite.addTest(integration_tests)
    
    # 添加性能测试
    performance_tests = loader.discover('tests', pattern='test_performance_data_db_performance.py')
    suite.addTest(performance_tests)
    
    # 创建测试运行器
    runner = unittest.TextTestRunner(verbosity=2)
    
    # 运行测试
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()

def main():
    """主函数"""
    print("开始运行签约台账数据库测试...")
    
    # 运行测试
    success = run_tests()
    
    # 输出测试结果
    if success:
        print("所有测试通过！")
        return 0
    else:
        print("测试失败！")
        return 1

if __name__ == '__main__':
    sys.exit(main())
