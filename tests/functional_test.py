import os
import sys
import unittest
import tempfile
import json
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.config import get_env, validate_required_env_vars
from modules.request_module import get_metabase_session, send_request_with_managed_session
from modules.data_processing_module import process_data_may_beijing

class FunctionalTest(unittest.TestCase):
    """功能测试，验证系统主要功能在使用环境变量后仍能正常工作"""

    def setUp(self):
        """测试前的准备工作"""
        # 保存原始环境变量
        self.original_env = os.environ.copy()

        # 设置测试环境变量
        os.environ['METABASE_USERNAME'] = 'test_username'
        os.environ['METABASE_PASSWORD'] = 'test_password'
        os.environ['METABASE_URL'] = 'http://test.url'
        os.environ['WECOM_WEBHOOK_DEFAULT'] = 'http://webhook.url'
        os.environ['API_URL_BJ_2025_05'] = 'http://test.url/api/card/1693/query'
        os.environ['FILE_TEMP_CONTRACT_DATA_BJ_2025_05'] = 'test_contract_data.csv'
        os.environ['FILE_PERFORMANCE_DATA_BJ_2025_05'] = 'test_performance_data.csv'
        os.environ['FILE_STATUS_BJ_2025_05'] = 'test_status.json'
        os.environ['CONTACT_WECOM_GROUP_NAME_BJ_2025_05'] = 'test_group'
        os.environ['CONTACT_CAMPAIGN_CONTACT_BJ_2025_05'] = 'test_contact'
        os.environ['CONFIG_PERFORMANCE_AMOUNT_CAP_BJ_2025_02'] = '100000'
        os.environ['CONFIG_ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_2025_02'] = 'true'
        os.environ['CONFIG_SINGLE_PROJECT_CONTRACT_AMOUNT_LIMIT_BJ_2025_02'] = '1000000'

        # 创建临时文件
        self.temp_files = []
        for filename in ['test_contract_data.csv', 'test_performance_data.csv', 'test_status.json']:
            # 直接使用文件名，不使用符号链接
            self.temp_files.append(filename)

            # 初始化文件内容
            if filename.endswith('.json'):
                with open(filename, 'w') as f:
                    json.dump({}, f)
            else:
                # 创建空的CSV文件
                with open(filename, 'w') as f:
                    f.write('')

    def tearDown(self):
        """测试后的清理工作"""
        # 恢复原始环境变量
        os.environ.clear()
        os.environ.update(self.original_env)

        # 删除临时文件
        for filename in self.temp_files:
            if os.path.exists(filename):
                os.remove(filename)

    @patch('modules.request_module.requests.post')
    @patch('modules.request_module.METABASE_USERNAME', 'test_username')
    @patch('modules.request_module.METABASE_PASSWORD', 'test_password')
    def test_get_metabase_session(self, mock_post, mock_username, mock_password):
        """测试获取Metabase会话功能"""
        # 模拟请求响应
        mock_response = MagicMock()
        mock_response.json.return_value = {'id': 'test_session_id'}
        mock_post.return_value = mock_response

        # 调用函数
        session_id = get_metabase_session()

        # 验证结果
        self.assertEqual(session_id, 'test_session_id')
        mock_post.assert_called_once()

        # 验证请求参数
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json']['username'], 'test_username')
        self.assertEqual(kwargs['json']['password'], 'test_password')

    @patch('modules.request_module.requests.post')
    @patch('modules.request_module.get_valid_session')
    def test_send_request_with_managed_session(self, mock_get_valid_session, mock_post):
        """测试从Metabase获取数据功能"""
        # 模拟会话ID
        mock_get_valid_session.return_value = 'test_session_id'

        # 模拟请求响应
        mock_response = MagicMock()
        mock_response.status_code = 202  # 设置状态码为202（成功）
        mock_response.json.return_value = {
            'data': {
                'rows': [
                    ['12345678', '张三', '北京', 'A001', 'active', 'C001', '10000', '10000', '0', 'valid', '2023-10-01', '服务商A', '2023-10-01', '10000', 'type1']
                ],
                'cols': [
                    {'name': '合同ID(_id)'},
                    {'name': '管家(serviceHousekeeper)'},
                    {'name': '活动城市(province)'},
                    {'name': '工单编号(serviceAppointmentNum)'},
                    {'name': 'Status'},
                    {'name': '合同编号(contractdocNum)'},
                    {'name': '合同金额(adjustRefundMoney)'},
                    {'name': '支付金额(paidAmount)'},
                    {'name': '差额(difference)'},
                    {'name': 'State'},
                    {'name': '创建时间(createTime)'},
                    {'name': '服务商(orgName)'},
                    {'name': '签约时间(signedDate)'},
                    {'name': 'Doorsill'},
                    {'name': '款项来源类型(tradeIn)'}
                ]
            }
        }
        mock_post.return_value = mock_response

        # 调用函数
        api_url = 'http://test.url/api/card/1693/query'
        result = send_request_with_managed_session(api_url)

        # 验证结果
        self.assertIsNotNone(result)
        self.assertIn('data', result)
        self.assertIn('rows', result['data'])
        self.assertEqual(len(result['data']['rows']), 1)
        self.assertEqual(result['data']['rows'][0][0], '12345678')  # 合同ID
        self.assertEqual(result['data']['rows'][0][1], '张三')  # 管家姓名

        # 验证请求参数
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['headers']['X-Metabase-Session'], 'test_session_id')

    @patch('modules.data_processing_module.determine_rewards_may_beijing_generic')
    def test_process_data_may_beijing(self, mock_determine_rewards):
        """测试北京5月活动数据处理功能"""
        # 模拟奖励计算结果
        mock_determine_rewards.return_value = ('lucky', '接好运', '恭喜获得接好运奖励！')

        # 准备测试数据
        contract_data = [{
            '合同ID(_id)': '12345678',
            '管家(serviceHousekeeper)': '张三',
            '活动城市(province)': '北京',
            '工单编号(serviceAppointmentNum)': 'A001',
            'Status': 'active',
            '合同编号(contractdocNum)': 'C001',
            '合同金额(adjustRefundMoney)': '10000',
            '支付金额(paidAmount)': '10000',
            '差额(difference)': '0',
            'State': 'valid',
            '创建时间(createTime)': '2023-10-01',
            '服务商(orgName)': '服务商A',
            '签约时间(signedDate)': '2023-10-01',
            'Doorsill': '10000',
            '款项来源类型(tradeIn)': 'type1'
        }]
        existing_contract_ids = set()
        housekeeper_award_lists = {}  # 不预先创建张三的列表

        # 调用函数
        process_data_may_beijing(contract_data, existing_contract_ids, housekeeper_award_lists)

        # 验证结果
        self.assertIn('12345678', existing_contract_ids)
        self.assertIn('张三', housekeeper_award_lists)  # 验证张三的键已创建
        self.assertEqual(len(housekeeper_award_lists['张三']), 1)
        self.assertEqual(housekeeper_award_lists['张三'][0]['奖励类型'], 'lucky')
        self.assertEqual(housekeeper_award_lists['张三'][0]['奖励名称'], '接好运')

        # 验证奖励计算函数调用
        mock_determine_rewards.assert_called_once()
        args, kwargs = mock_determine_rewards.call_args
        self.assertEqual(args[0], '12345678')  # 合同ID
        self.assertEqual(args[1], '张三')  # 管家姓名

if __name__ == '__main__':
    unittest.main()
