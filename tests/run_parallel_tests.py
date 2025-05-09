#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
运行并行测试
在测试环境中启用功能标志并运行并行测试
"""

import os
import sys
import unittest
import logging
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
from modules.config import USE_GENERIC_PROCESS_FUNCTION

# 设置日志
setup_logging()

def main():
    """主函数"""
    # 输出测试开始信息
    logging.info("=" * 80)
    logging.info(f"开始并行测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("=" * 80)
    
    # 检查功能标志
    logging.info(f"当前功能标志 USE_GENERIC_PROCESS_FUNCTION = {USE_GENERIC_PROCESS_FUNCTION}")
    
    # 临时启用功能标志
    import modules.config
    modules.config.USE_GENERIC_PROCESS_FUNCTION = True
    logging.info(f"临时启用功能标志 USE_GENERIC_PROCESS_FUNCTION = {modules.config.USE_GENERIC_PROCESS_FUNCTION}")
    
    # 运行并行测试
    logging.info("运行并行测试...")
    test_suite = unittest.defaultTestLoader.discover('tests', pattern='test_parallel_execution.py')
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)
    
    # 输出测试结果
    logging.info("=" * 80)
    logging.info(f"并行测试完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"运行测试: {test_result.testsRun}")
    logging.info(f"成功: {test_result.testsRun - len(test_result.errors) - len(test_result.failures)}")
    logging.info(f"失败: {len(test_result.failures)}")
    logging.info(f"错误: {len(test_result.errors)}")
    
    # 输出失败和错误的测试
    if test_result.failures:
        logging.error("失败的测试:")
        for failure in test_result.failures:
            logging.error(f"- {failure[0]}")
    
    if test_result.errors:
        logging.error("错误的测试:")
        for error in test_result.errors:
            logging.error(f"- {error[0]}")
    
    logging.info("=" * 80)
    
    # 恢复功能标志
    modules.config.USE_GENERIC_PROCESS_FUNCTION = False
    logging.info(f"恢复功能标志 USE_GENERIC_PROCESS_FUNCTION = {modules.config.USE_GENERIC_PROCESS_FUNCTION}")
    
    # 返回测试结果
    return len(test_result.failures) == 0 and len(test_result.errors) == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
