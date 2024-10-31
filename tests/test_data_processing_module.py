import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules')))
from datetime import date
from modules.data_processing_module import determine_rewards_nov_beijing, process_data_nov_beijing

class TestDataProcessingModule(unittest.TestCase):

    def test_determine_rewards_nov_beijing(self):
        print("开始测试 determine_rewards_nov_beijing")
        # 测试数据
        contract_number = 16
        housekeeper_data = {
            'count': 6,
            'total_amount': 50000,
            'awarded': []
        }
        current_contract_amount = 15000

        # 调用函数
        reward_types, reward_names, next_reward_gap = determine_rewards_nov_beijing(
            contract_number, housekeeper_data, current_contract_amount
        )

        # 断言
        print("断言结果")
        self.assertIn("幸运数字", reward_types)
        self.assertIn("接好运万元以上", reward_names)
        self.assertIn("节节高", reward_types)
        self.assertIn("达标奖", reward_names)
        self.assertEqual(next_reward_gap, "距离 优秀奖 还需 10,000 元")
        print("determine_rewards_nov_beijing 测试通过")

    def test_process_data_nov_beijing(self):
        print("开始测试 process_data_nov_beijing")
        
        # 模拟数据：创建5个合同，所有合同都与同一个管家（张三）相关联
        contract_data = [
            {
                '合同ID(_id)': str(i),  # 合同ID
                '活动城市(province)': '北京',
                '工单编号(serviceAppointmentNum)': f'A00{i}',  # 工单编号
                'Status': 'active',
                '管家(serviceHousekeeper)': '张三',  # 管家姓名
                '合同编号(contractdocNum)': f'C00{i}',  # 合同编号
                '合同金额(adjustRefundMoney)': '15000',  # 合同金额
                '支付金额(paidAmount)': '15000',  # 支付金额
                '差额(difference)': '0',  # 差额
                'State': 'valid',
                '创建时间(createTime)': '2023-10-01',
                '服务商(orgName)': '服务商A',
                '签约时间(signedDate)': '2023-10-01',
                'Doorsill': '10000',
                '款项来源类型(tradeIn)': 'type1'
            }
            for i in range(1, 6)  # 创建5个合同
        ]
        
        # 添加第六个合同，确保触发幸运奖和节节高
        contract_data.append({
            '合同ID(_id)': '6',
            '活动城市(province)': '北京',
            '工单编号(serviceAppointmentNum)': 'A006',  # 工单编号
            'Status': 'active',
            '管家(serviceHousekeeper)': '张三',  # 管家姓名
            '合同编号(contractdocNum)': 'C006',  # 合同编号
            '合同金额(adjustRefundMoney)': '15000',  # 合同金额
            '支付金额(paidAmount)': '15000',  # 支付金额
            '差额(difference)': '0',  # 差额
            'State': 'valid',
            '创建时间(createTime)': '2023-10-06',
            '服务商(orgName)': '服务商A',
            '签约时间(signedDate)': '2023-10-06',
            'Doorsill': '10000',
            '款项来源类型(tradeIn)': 'type1'
        })

        existing_contract_ids = set()
        housekeeper_award_lists = {
            '张三': []  # 假设张三还没有获得任何奖励
        }

        # 调用函数
        performance_data = process_data_nov_beijing(
            contract_data, existing_contract_ids, housekeeper_award_lists
        )

        # 打印实际结果
        # print("实际的 performance_data:", performance_data)

        # 断言
        print("断言结果")
        self.assertEqual(len(performance_data), 6)  # 现在应该有六个合同
        for i in range(6):
            self.assertEqual(performance_data[i]['合同ID(_id)'], str(i + 1))  # 确保合同ID正确

        # 检查第六个合同的奖励类型和名称
        self.assertIn("幸运数字", performance_data[5]['奖励类型'])  # 第六个合同应该触发幸运数字
        self.assertIn("接好运万元以上", performance_data[5]['奖励名称'])  # 第六个合同应该触发接好运万元以上
        self.assertIn("节节高", performance_data[5]['奖励类型'])  # 第六个合同应该触发节节高
        self.assertIn("优秀奖", performance_data[5]['奖励名称'])  # 第六个合同应该触发精英奖

        print("process_data_nov_beijing 测试通过")

if __name__ == '__main__':
    unittest.main() 