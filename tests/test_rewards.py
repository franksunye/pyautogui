import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.data_processing_module import determine_rewards_nov_beijing

class TestRewards(unittest.TestCase):
    def setUp(self):
        """每个测试用例前的初始化"""
        self.base_housekeeper_data = {
            'count': 0,
            'total_amount': 0,
            'awarded': []
        }

    def test_lucky_number_basic(self):
        """测试基本的幸运数字奖励（合同金额小于1万）"""
        housekeeper_data = self.base_housekeeper_data.copy()
        reward_types, reward_names, gap = determine_rewards_nov_beijing(
            contract_number=16,
            housekeeper_data=housekeeper_data,
            current_contract_amount=5000
        )
        self.assertEqual(reward_types, "幸运数字")
        self.assertEqual(reward_names, "接好运")

    def test_lucky_number_high_amount(self):
        """测试高金额的幸运数字奖励（合同金额大于等于1万）"""
        housekeeper_data = self.base_housekeeper_data.copy()
        reward_types, reward_names, gap = determine_rewards_nov_beijing(
            contract_number=26,
            housekeeper_data=housekeeper_data,
            current_contract_amount=15000
        )
        self.assertEqual(reward_types, "幸运数字")
        self.assertEqual(reward_names, "接好运万元以上")

    def test_no_rewards(self):
        """测试无奖励情况"""
        housekeeper_data = self.base_housekeeper_data.copy()
        reward_types, reward_names, gap = determine_rewards_nov_beijing(
            contract_number=11,
            housekeeper_data=housekeeper_data,
            current_contract_amount=5000
        )
        self.assertEqual(reward_types, "")
        self.assertEqual(reward_names, "")
        self.assertTrue("距离达成节节高奖励条件还需 6 单" in gap)

    def test_tiered_rewards_first_level(self):
        """测试节节高第一档奖励"""
        housekeeper_data = {
            'count': 6,
            'total_amount': 45000,
            'awarded': []
        }
        reward_types, reward_names, gap = determine_rewards_nov_beijing(
            contract_number=11,
            housekeeper_data=housekeeper_data,
            current_contract_amount=5000
        )
        self.assertEqual(reward_types, "节节高")
        self.assertEqual(reward_names, "达标奖")
        self.assertTrue("距离 优秀奖 还需" in gap)

    def test_tiered_rewards_second_level(self):
        """测试节节高第二档奖励"""
        housekeeper_data = {
            'count': 6,
            'total_amount': 65000,
            'awarded': ['达标奖']
        }
        reward_types, reward_names, gap = determine_rewards_nov_beijing(
            contract_number=11,
            housekeeper_data=housekeeper_data,
            current_contract_amount=5000
        )
        self.assertEqual(reward_types, "节节高")
        self.assertEqual(reward_names, "优秀奖")
        self.assertTrue("距离 精英奖 还需" in gap)

    def test_tiered_rewards_all_levels(self):
        """测试节节高全部档位奖励"""
        housekeeper_data = {
            'count': 6,
            'total_amount': 110000,
            'awarded': ['达标奖', '优秀奖']
        }
        reward_types, reward_names, gap = determine_rewards_nov_beijing(
            contract_number=11,
            housekeeper_data=housekeeper_data,
            current_contract_amount=5000
        )
        self.assertEqual(reward_types, "节节高")
        self.assertEqual(reward_names, "精英奖")
        self.assertEqual(gap, "")

    def test_combined_rewards(self):
        """测试同时获得幸运数字和节节高奖励"""
        housekeeper_data = {
            'count': 6,
            'total_amount': 45000,
            'awarded': []
        }
        reward_types, reward_names, gap = determine_rewards_nov_beijing(
            contract_number=16,
            housekeeper_data=housekeeper_data,
            current_contract_amount=15000
        )
        self.assertEqual(reward_types, "幸运数字, 节节高")
        self.assertEqual(reward_names, "接好运万元以上, 达标奖")
        self.assertTrue("距离 优秀奖 还需" in gap)

    def test_invalid_input(self):
        """测试无效输入"""
        housekeeper_data = self.base_housekeeper_data.copy()
        with self.assertRaises(ValueError):
            determine_rewards_nov_beijing(-1, housekeeper_data, 5000)
        
        with self.assertRaises(ValueError):
            determine_rewards_nov_beijing(1, {'count': -1}, 5000)

        with self.assertRaises(ValueError):
            determine_rewards_nov_beijing(1, {'count': 1}, -5000)

if __name__ == '__main__':
    unittest.main()
