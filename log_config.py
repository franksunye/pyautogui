import logging

def setup_logging():
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # 移除现有的处理程序
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 配置app.log文件处理器
    app_file_handler = logging.FileHandler('app.log')
    app_file_handler.setLevel(logging.DEBUG)
    app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')
    app_file_handler.setFormatter(app_formatter)
    root_logger.addHandler(app_file_handler)
    
    # 配置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # 特定于发送消息的日志记录器
    send_logger = logging.getLogger('sendLogger')
    send_logger.setLevel(logging.INFO)  # 单独设置级别

    # 配置send_messages.log文件处理器
    send_file_handler = logging.FileHandler('send_messages.log')
    send_file_handler.setLevel(logging.INFO)
    send_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    send_file_handler.setFormatter(send_formatter)
    send_logger.addHandler(send_file_handler)

    # 为确保send_logger的消息不会被root_logger重复处理
    send_logger.propagate = False
