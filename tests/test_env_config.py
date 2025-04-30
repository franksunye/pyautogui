import unittest
import os
import sys
import tempfile
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.config import get_env, validate_required_env_vars

class TestEnvConfig(unittest.TestCase):
    """测试环境变量加载和验证机制"""

    def setUp(self):
        """测试前的准备工作"""
        # 保存原始环境变量
        self.original_env = os.environ.copy()
        
        # 清除可能影响测试的环境变量
        if 'TEST_ENV_VAR' in os.environ:
            del os.environ['TEST_ENV_VAR']
        if 'TEST_BOOL_VAR' in os.environ:
            del os.environ['TEST_BOOL_VAR']
        if 'TEST_INT_VAR' in os.environ:
            del os.environ['TEST_INT_VAR']
        if 'TEST_FLOAT_VAR' in os.environ:
            del os.environ['TEST_FLOAT_VAR']
        if 'METABASE_USERNAME' in os.environ:
            del os.environ['METABASE_USERNAME']
        if 'METABASE_PASSWORD' in os.environ:
            del os.environ['METABASE_PASSWORD']
        if 'METABASE_URL' in os.environ:
            del os.environ['METABASE_URL']
        if 'WECOM_WEBHOOK_DEFAULT' in os.environ:
            del os.environ['WECOM_WEBHOOK_DEFAULT']

    def tearDown(self):
        """测试后的清理工作"""
        # 恢复原始环境变量
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_get_env_with_default(self):
        """测试get_env函数使用默认值"""
        # 环境变量不存在，应该返回默认值
        self.assertEqual(get_env('TEST_ENV_VAR', 'default_value'), 'default_value')
        
        # 设置环境变量
        os.environ['TEST_ENV_VAR'] = 'test_value'
        
        # 环境变量存在，应该返回环境变量的值
        self.assertEqual(get_env('TEST_ENV_VAR', 'default_value'), 'test_value')

    def test_get_env_with_cast(self):
        """测试get_env函数的类型转换功能"""
        # 测试布尔值转换
        os.environ['TEST_BOOL_VAR'] = 'true'
        self.assertEqual(get_env('TEST_BOOL_VAR', 'false', bool), True)
        
        os.environ['TEST_BOOL_VAR'] = 'yes'
        self.assertEqual(get_env('TEST_BOOL_VAR', 'false', bool), True)
        
        os.environ['TEST_BOOL_VAR'] = '1'
        self.assertEqual(get_env('TEST_BOOL_VAR', 'false', bool), True)
        
        os.environ['TEST_BOOL_VAR'] = 'y'
        self.assertEqual(get_env('TEST_BOOL_VAR', 'false', bool), True)
        
        os.environ['TEST_BOOL_VAR'] = 'false'
        self.assertEqual(get_env('TEST_BOOL_VAR', 'true', bool), False)
        
        # 测试整数转换
        os.environ['TEST_INT_VAR'] = '123'
        self.assertEqual(get_env('TEST_INT_VAR', '0', int), 123)
        
        # 测试浮点数转换
        os.environ['TEST_FLOAT_VAR'] = '123.45'
        self.assertEqual(get_env('TEST_FLOAT_VAR', '0.0', float), 123.45)

    def test_get_env_with_none_default(self):
        """测试get_env函数使用None作为默认值"""
        # 环境变量不存在，应该返回None
        self.assertIsNone(get_env('TEST_ENV_VAR'))
        
        # 设置环境变量
        os.environ['TEST_ENV_VAR'] = 'test_value'
        
        # 环境变量存在，应该返回环境变量的值
        self.assertEqual(get_env('TEST_ENV_VAR'), 'test_value')

    def test_validate_required_env_vars_success(self):
        """测试validate_required_env_vars函数在所有必需的环境变量都存在时不抛出异常"""
        # 设置所有必需的环境变量
        os.environ['METABASE_USERNAME'] = 'test_username'
        os.environ['METABASE_PASSWORD'] = 'test_password'
        os.environ['METABASE_URL'] = 'http://test.url'
        os.environ['WECOM_WEBHOOK_DEFAULT'] = 'http://webhook.url'
        
        # 不应该抛出异常
        try:
            validate_required_env_vars()
        except Exception as e:
            self.fail(f"validate_required_env_vars() raised {type(e).__name__} unexpectedly!")

    def test_validate_required_env_vars_missing(self):
        """测试validate_required_env_vars函数在缺少必需的环境变量时抛出异常"""
        # 只设置部分必需的环境变量
        os.environ['METABASE_USERNAME'] = 'test_username'
        os.environ['METABASE_PASSWORD'] = 'test_password'
        # 缺少 METABASE_URL 和 WECOM_WEBHOOK_DEFAULT
        
        # 应该抛出异常
        with self.assertRaises(EnvironmentError) as context:
            validate_required_env_vars()
        
        # 验证异常消息包含缺失的环境变量
        self.assertIn('METABASE_URL', str(context.exception))
        self.assertIn('WECOM_WEBHOOK_DEFAULT', str(context.exception))

    @patch('modules.config.logging.error')
    def test_validate_required_env_vars_in_config(self, mock_logging_error):
        """测试config.py中对validate_required_env_vars的调用"""
        # 导入config模块，这将触发validate_required_env_vars的调用
        import modules.config
        
        # 重新加载模块以确保执行验证
        import importlib
        importlib.reload(modules.config)
        
        # 验证logging.error被调用
        mock_logging_error.assert_called()
        # 验证错误消息包含"环境变量验证失败"
        self.assertIn('环境变量验证失败', mock_logging_error.call_args[0][0])

if __name__ == '__main__':
    unittest.main()
