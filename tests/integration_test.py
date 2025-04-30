import os
import sys
import unittest
import tempfile
import json
import logging
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.config import get_env, validate_required_env_vars
from modules.request_module import get_metabase_session, send_request_with_managed_session
from modules.data_processing_module import process_data_may_beijing
from modules.notification_module import notify_awards_may_beijing
from modules.file_utils import write_data_to_csv, get_all_records_from_csv

class IntegrationTest(unittest.TestCase):
    """集成测试，验证整个系统在使用环境变量和敏感信息保护措施后仍能正常运行"""

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
        os.environ['CONFIG_PERFORMANCE_AMOUNT_CAP_BJ_2025_05'] = '100000'
        os.environ['CONFIG_ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_2025_05'] = 'true'
        os.environ['CONFIG_SINGLE_PROJECT_CONTRACT_AMOUNT_LIMIT_BJ_2025_05'] = '1000000'
        
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
        
        # 设置测试日志记录器
        self.log_file = tempfile.NamedTemporaryFile(delete=False, suffix='.log')
        self.log_file.close()
        
        # 配置日志记录器
        self.logger = logging.getLogger('test_logger')
        self.logger.setLevel(logging.DEBUG)
        
        # 添加文件处理器
        self.file_handler = logging.FileHandler(self.log_file.name)
        self.file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(self.file_handler)

    def tearDown(self):
        """测试后的清理工作"""
        # 恢复原始环境变量
        os.environ.clear()
        os.environ.update(self.original_env)
        
        # 删除临时文件
        for filename in self.temp_files:
            if os.path.exists(filename):
                os.remove(filename)
        
        # 关闭和移除文件处理器
        self.file_handler.close()
        self.logger.removeHandler(self.file_handler)
        
        # 删除临时日志文件
        if os.path.exists(self.log_file.name):
            os.remove(self.log_file.name)

    @patch('modules.request_module.requests.post')
    @patch('modules.notification_module.create_task')
    def test_end_to_end_flow(self, mock_create_task, mock_post):
        """测试端到端流程"""
        # 模拟Metabase请求响应
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_response.json.return_value = {
            'data': {
                'rows': [
                    ['12345678', '张三', '北京', 'A001', 'active', 'C001', '10000', '10000', '0', 'valid', '2023-10-01', '服务商A', '2023-10-01', '10000', 'type1'],
                    ['87654321', '张三', '北京', 'A002', 'active', 'C002', '20000', '20000', '0', 'valid', '2023-10-02', '服务商A', '2023-10-02', '10000', 'type1'],
                    ['11223344', '李四', '北京', 'A003', 'active', 'C003', '30000', '30000', '0', 'valid', '2023-10-03', '服务商B', '2023-10-03', '10000', 'type1']
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
        
        # 步骤1：从Metabase获取数据
        with patch('modules.request_module.METABASE_USERNAME', 'test_username'):
            with patch('modules.request_module.METABASE_PASSWORD', 'test_password'):
                with patch('modules.request_module.logging', self.logger):
                    # 获取会话ID
                    session_id = get_metabase_session()
                    self.assertEqual(session_id, 'test_session_id')
                    
                    # 获取数据
                    api_url = os.environ['API_URL_BJ_2025_05']
                    result = send_request_with_managed_session(api_url)
                    self.assertIsNotNone(result)
                    self.assertIn('data', result)
                    self.assertEqual(len(result['data']['rows']), 3)
        
        # 步骤2：将数据写入CSV文件
        contract_data = []
        for i, row in enumerate(result['data']['rows']):
            contract = {}
            for j, col in enumerate(result['data']['cols']):
                contract[col['name']] = row[j]
            contract_data.append(contract)
        
        # 写入CSV文件
        contract_data_file = os.environ['FILE_TEMP_CONTRACT_DATA_BJ_2025_05']
        write_data_to_csv(contract_data_file, contract_data)
        
        # 验证CSV文件已创建
        self.assertTrue(os.path.exists(contract_data_file))
        
        # 步骤3：处理数据
        with patch('modules.data_processing_module.determine_rewards_may_beijing_generic') as mock_determine_rewards:
            # 模拟奖励计算结果
            mock_determine_rewards.side_effect = [
                ('lucky', '接好运', '恭喜获得接好运奖励！'),
                ('progressive', '优秀奖', '恭喜获得优秀奖奖励！'),
                ('', '', '')
            ]
            
            # 处理数据
            existing_contract_ids = set()
            housekeeper_award_lists = {}
            
            # 调用函数
            with patch('modules.data_processing_module.logging', self.logger):
                process_data_may_beijing(contract_data, existing_contract_ids, housekeeper_award_lists)
            
            # 验证结果
            self.assertEqual(len(existing_contract_ids), 3)
            self.assertIn('张三', housekeeper_award_lists)
            self.assertIn('李四', housekeeper_award_lists)
            self.assertEqual(len(housekeeper_award_lists['张三']), 2)
            self.assertEqual(len(housekeeper_award_lists['李四']), 0)
        
        # 步骤4：发送通知
        with patch('modules.notification_module.logging', self.logger):
            with patch('modules.notification_module.get_all_records_from_csv') as mock_get_records:
                with patch('modules.notification_module.load_send_status') as mock_load_status:
                    with patch('modules.notification_module.update_send_status'):
                        with patch('modules.notification_module.write_performance_data_to_csv'):
                            # 设置模拟数据
                            mock_get_records.return_value = [
                                {
                                    '合同ID(_id)': '12345678',
                                    '管家(serviceHousekeeper)': '张三',
                                    '是否发送通知': 'N',
                                    '激活奖励状态': '1',
                                    '奖励名称': '接好运',
                                    '合同编号(contractdocNum)': 'C001',
                                    '活动期内第几个合同': 1,
                                    '管家累计单数': 1,
                                    '管家累计金额': '10000',
                                    '计入业绩金额': '10000',
                                    '备注': '无'
                                },
                                {
                                    '合同ID(_id)': '87654321',
                                    '管家(serviceHousekeeper)': '张三',
                                    '是否发送通知': 'N',
                                    '激活奖励状态': '1',
                                    '奖励名称': '优秀奖',
                                    '合同编号(contractdocNum)': 'C002',
                                    '活动期内第几个合同': 2,
                                    '管家累计单数': 2,
                                    '管家累计金额': '30000',
                                    '计入业绩金额': '20000',
                                    '备注': '无'
                                },
                                {
                                    '合同ID(_id)': '11223344',
                                    '管家(serviceHousekeeper)': '李四',
                                    '是否发送通知': 'N',
                                    '激活奖励状态': '0',
                                    '奖励名称': '',
                                    '合同编号(contractdocNum)': 'C003',
                                    '活动期内第几个合同': 1,
                                    '管家累计单数': 1,
                                    '管家累计金额': '30000',
                                    '计入业绩金额': '30000',
                                    '备注': '无'
                                }
                            ]
                            mock_load_status.return_value = {}
                            
                            # 调用函数
                            performance_data_filename = os.environ['FILE_PERFORMANCE_DATA_BJ_2025_05']
                            status_filename = os.environ['FILE_STATUS_BJ_2025_05']
                            notify_awards_may_beijing(performance_data_filename, status_filename)
                            
                            # 验证结果
                            self.assertEqual(mock_create_task.call_count, 2)  # 应该调用两次create_task
        
        # 步骤5：验证日志中不包含敏感信息
        with open(self.log_file.name, 'r') as f:
            log_content = f.read()
            
            # 验证日志中不包含完整的合同ID
            self.assertNotIn('12345678', log_content)
            self.assertNotIn('87654321', log_content)
            self.assertNotIn('11223344', log_content)
            
            # 验证日志中不包含密码
            self.assertNotIn('test_password', log_content)

if __name__ == '__main__':
    unittest.main()
