#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试奖励翻倍通知功能修复
"""

import unittest
from modules.notification_module import generate_award_message
from modules.config import ENABLE_BADGE_MANAGEMENT, ELITE_HOUSEKEEPER, BADGE_NAME

class TestNotificationFix(unittest.TestCase):
    """测试奖励翻倍通知功能修复"""

    def setUp(self):
        """设置测试环境"""
        # 确保徽章功能启用
        self.original_enable_badge = ENABLE_BADGE_MANAGEMENT

        # 测试数据
        self.awards_mapping = {
            '接好运': '36',
            '接好运万元以上': '66',
            '达标奖': '200',
            '优秀奖': '400',
            '精英奖': '600'
        }

        # 精英管家记录 - 北京
        self.elite_record_bj = {
            "管家(serviceHousekeeper)": ELITE_HOUSEKEEPER[0],  # 使用配置中的第一个精英管家
            "合同编号(contractdocNum)": "BJ-2025-04-001",
            "奖励类型": "幸运数字, 节节高",
            "奖励名称": "接好运万元以上, 达标奖"
        }

        # 普通管家记录 - 北京
        self.normal_record_bj = {
            "管家(serviceHousekeeper)": "普通管家",
            "合同编号(contractdocNum)": "BJ-2025-04-002",
            "奖励类型": "幸运数字, 节节高",
            "奖励名称": "接好运万元以上, 达标奖"
        }

        # 精英管家记录 - 上海
        self.elite_record_sh = {
            "管家(serviceHousekeeper)": ELITE_HOUSEKEEPER[0],  # 使用配置中的第一个精英管家
            "合同编号(contractdocNum)": "SH-2025-04-001",
            "奖励类型": "幸运数字, 节节高",
            "奖励名称": "接好运万元以上, 达标奖"
        }

    def test_elite_bj_reward_doubling(self):
        """测试北京精英管家的节节高奖励是否正确翻倍"""
        message = generate_award_message(self.elite_record_bj, self.awards_mapping, "BJ")

        # 验证消息中包含徽章
        self.assertIn(BADGE_NAME, message)

        # 验证节节高奖励被翻倍
        self.assertIn("达标奖", message)
        self.assertIn("奖励金额 200 元", message)
        self.assertIn("直升至 400 元", message)

        # 验证幸运数字奖励没有被翻倍
        self.assertIn("接好运万元以上", message)
        self.assertIn("获得签约奖励66元", message)
        self.assertNotIn("直升至 132 元", message)

    def test_normal_bj_no_doubling(self):
        """测试北京普通管家的奖励不会翻倍"""
        message = generate_award_message(self.normal_record_bj, self.awards_mapping, "BJ")

        # 验证消息中不包含徽章
        self.assertNotIn(BADGE_NAME, message)

        # 验证节节高奖励没有被翻倍
        self.assertIn("达标奖", message)
        self.assertIn("获得签约奖励200元", message)
        self.assertNotIn("直升至", message)

        # 验证幸运数字奖励没有被翻倍
        self.assertIn("接好运万元以上", message)
        self.assertIn("获得签约奖励66元", message)
        self.assertNotIn("直升至", message)

    def test_elite_sh_no_doubling(self):
        """测试上海精英管家的奖励不会翻倍且不显示徽章"""
        message = generate_award_message(self.elite_record_sh, self.awards_mapping, "SH")

        # 验证消息中不包含徽章（上海管家不显示徽章）
        self.assertNotIn(BADGE_NAME, message)

        # 验证节节高奖励没有被翻倍
        self.assertIn("达标奖", message)
        self.assertIn("获得签约奖励200元", message)
        self.assertNotIn("直升至", message)

        # 验证幸运数字奖励没有被翻倍
        self.assertIn("接好运万元以上", message)
        self.assertIn("获得签约奖励66元", message)
        self.assertNotIn("直升至", message)

if __name__ == "__main__":
    unittest.main()
