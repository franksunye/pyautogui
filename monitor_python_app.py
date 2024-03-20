import psutil
import requests
import schedule
import time
import logging
import sys

#  配置日志
#  配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor_log.txt'),  #  文件日志处理器
        logging.StreamHandler(sys.stdout)  #  控制台日志处理器
    ]
)

# 企业微信Webhook地址
WEBHOOK_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=59cf22c5-0623-4b34-b207-0f404f13eeeb'

# Python应用程序的进程名
APP_PROCESS_NAME = 'python.exe'

#  你的Python应用程序的命令行参数
APP_CMD_LINE_ARG = 'main.py'

# 检查Python应用程序的运行状态
def check_app_status():
    try:
        for proc in psutil.process_iter(['pid', 'cmdline', 'name']):
            try:
                if proc.info['name'] == APP_PROCESS_NAME and APP_CMD_LINE_ARG in ' '.join(proc.info['cmdline']):
                    logging.info(f"{APP_PROCESS_NAME} with argument {APP_CMD_LINE_ARG} is running.")
                    return True
            except KeyError:
                logging.warning(f"Could not access 'name' attribute for process {proc.pid}.")
    except Exception as e:
        logging.error(f"Error checking app status: {e}")
    logging.info(f"{APP_PROCESS_NAME} with argument {APP_CMD_LINE_ARG} is not running.")
    return False

#  发送企业微信Webhook通知
def send_wechat_notification():
    try:
        data = {
            "msgtype": "text",
            "text": {
                "content": f"{APP_PROCESS_NAME} with argument {APP_CMD_LINE_ARG} is not running. Please check the application（开门红活动统计机器人）."
            }
        }
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code ==  200:
            logging.info(f"WeChat notification sent successfully.")
        else:
            logging.error(f"Failed to send WeChat notification: {response.text}")
    except Exception as e:
        logging.error(f"Error sending WeChat notification: {e}")

#  定期执行检查
def job():
    if not check_app_status():
        send_wechat_notification()
        logging.info(f"Sending WeChat notification.")

#  每1分钟执行一次检查
schedule.every(5).minutes.do(job)

#  主循环
while True:
    schedule.run_pending()
    time.sleep(1)
