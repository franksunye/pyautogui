#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
北京5月数据等价性验证主脚本

该脚本用于运行所有验证测试，包括：
1. 基础数据处理验证
2. 奖励计算验证
3. 通知逻辑验证

使用方法：
python scripts/run_beijing_may_verification.py
"""

import os
import sys
import logging
import time
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入项目模块
from modules.log_config import setup_logging
import modules.config
from scripts.verify_beijing_may_equivalence import main as verify_data_processing
from scripts.verify_reward_calculation_equivalence import main as verify_reward_calculation
from scripts.verify_notification_equivalence import main as verify_notification

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

def run_verification_tests():
    """运行所有验证测试"""
    logger.info("开始运行北京5月数据等价性验证测试")
    
    # 创建结果目录
    results_dir = os.path.join('tests', 'test_data')
    os.makedirs(results_dir, exist_ok=True)
    
    # 创建报告文件
    report_file = os.path.join(results_dir, 'beijing_may_verification_report.txt')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("北京5月数据等价性验证报告\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 1. 运行基础数据处理验证
        f.write("1. 基础数据处理验证\n")
        f.write("-" * 50 + "\n\n")
        
        logger.info("运行基础数据处理验证")
        start_time = time.time()
        
        # 重定向标准输出
        original_stdout = sys.stdout
        sys.stdout = f
        
        try:
            verify_data_processing()
        except Exception as e:
            f.write(f"验证过程中发生错误: {e}\n")
            logger.error(f"基础数据处理验证失败: {e}")
        
        # 恢复标准输出
        sys.stdout = original_stdout
        
        end_time = time.time()
        logger.info(f"基础数据处理验证完成，耗时: {end_time - start_time:.2f}秒")
        
        f.write(f"\n基础数据处理验证耗时: {end_time - start_time:.2f}秒\n\n")
        
        # 2. 运行奖励计算验证
        f.write("2. 奖励计算验证\n")
        f.write("-" * 50 + "\n\n")
        
        logger.info("运行奖励计算验证")
        start_time = time.time()
        
        # 重定向标准输出
        sys.stdout = f
        
        try:
            verify_reward_calculation()
        except Exception as e:
            f.write(f"验证过程中发生错误: {e}\n")
            logger.error(f"奖励计算验证失败: {e}")
        
        # 恢复标准输出
        sys.stdout = original_stdout
        
        end_time = time.time()
        logger.info(f"奖励计算验证完成，耗时: {end_time - start_time:.2f}秒")
        
        f.write(f"\n奖励计算验证耗时: {end_time - start_time:.2f}秒\n\n")
        
        # 3. 运行通知逻辑验证
        f.write("3. 通知逻辑验证\n")
        f.write("-" * 50 + "\n\n")
        
        logger.info("运行通知逻辑验证")
        start_time = time.time()
        
        # 重定向标准输出
        sys.stdout = f
        
        try:
            verify_notification()
        except Exception as e:
            f.write(f"验证过程中发生错误: {e}\n")
            logger.error(f"通知逻辑验证失败: {e}")
        
        # 恢复标准输出
        sys.stdout = original_stdout
        
        end_time = time.time()
        logger.info(f"通知逻辑验证完成，耗时: {end_time - start_time:.2f}秒")
        
        f.write(f"\n通知逻辑验证耗时: {end_time - start_time:.2f}秒\n\n")
        
        # 总结
        f.write("验证总结\n")
        f.write("=" * 50 + "\n\n")
        f.write("验证测试已完成，请查看上述详细结果。\n")
        f.write("如果所有测试都显示'通过'，则表示文件存储和数据库存储的功能完全等价。\n")
        f.write("如果存在'失败'，请查看详细输出找出差异原因。\n\n")
        f.write(f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    logger.info(f"验证报告已生成: {report_file}")
    
    # 打印报告路径
    print(f"\n验证报告已生成: {report_file}")
    print("请查看报告了解详细验证结果。")

def main():
    """主函数"""
    # 设置配置
    modules.config.USE_DATABASE_FOR_PERFORMANCE_DATA = False
    
    # 运行验证测试
    run_verification_tests()
    
    logger.info("北京5月数据等价性验证测试完成")

if __name__ == "__main__":
    main()
