# modules\log_config.py
import logging
import logging.handlers
import os
from dotenv import load_dotenv

def get_log_level():
    """根据环境变量设置日志级别"""
    load_dotenv()  # 加载环境变量
    env = os.getenv('ENVIRONMENT', 'production').lower()
    if env == 'development':
        return logging.DEBUG
    else:
        return logging.INFO

def setup_logging():
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(get_log_level())

    # 移除现有的处理程序
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 确保logs目录存在
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 配置logs/app.log文件处理器
    app_file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'app.log'), 
        maxBytes=5000000, 
        backupCount=5,
        encoding="utf-8"  # 设置编码为 UTF-8
    )
    env = os.getenv('ENVIRONMENT', 'production').lower()
    if env == 'production':
        app_file_handler.setLevel(logging.ERROR)
    else:
        app_file_handler.setLevel(logging.DEBUG)
    
    # 修改格式化器，去掉记录器名称，并用方括号括起文件名和函数名
    app_formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s] - [%(funcName)s] - %(message)s')
    app_file_handler.setFormatter(app_formatter)
    root_logger.addHandler(app_file_handler)
    
    # 配置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(get_log_level())
    
    # 修改控制台格式化器，去掉记录器名称，并用方括号括起文件名和函数名
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s] - [%(funcName)s] - %(message)s')
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # 特定于发送消息的日志记录器
    send_logger = logging.getLogger('sendLogger')
    send_logger.setLevel(logging.INFO)  # 单独设置级别

    # 配置send_messages.log文件处理器
    send_file_handler = logging.FileHandler(os.path.join(log_dir, 'send_messages.log'))
    send_file_handler.setLevel(logging.INFO)
    
    # 修改发送日志格式化器，去掉记录器名称，并用方括号括起文件名
    send_formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(message)s]')
    send_file_handler.setFormatter(send_formatter)
    send_logger.addHandler(send_file_handler)

    # 为确保send_logger的消息不会被root_logger重复处理
    send_logger.propagate = False
