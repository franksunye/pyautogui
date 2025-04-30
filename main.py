import schedule
import time
import traceback
import logging
import threading
import argparse
import os
from dotenv import load_dotenv
from modules.log_config import setup_logging
from jobs import *
from modules.config import RUN_JOBS_SERIALLY_SCHEDULE
import datetime
import task_scheduler # 引入任务调度模块

# 解析命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description='奖励系统服务')
    parser.add_argument('--env', type=str, choices=['dev', 'test', 'prod'], default='dev',
                      help='指定运行环境 (dev: 开发环境, test: 测试环境, prod: 生产环境)')
    parser.add_argument('--run-once', action='store_true',
                      help='运行一次后退出，不进入循环')
    parser.add_argument('--task', type=str, choices=['all', 'beijing-apr', 'beijing-may', 'shanghai-apr', 'shanghai-may', 'technician', 'daily-report'],
                      help='指定要运行的任务')
    return parser.parse_args()

# 加载环境变量
def load_environment(env):
    # 配置文件目录
    config_dir = 'config'

    if env == 'dev':
        load_dotenv(f'{config_dir}/.env', override=True)
        logging.info('已加载开发环境配置')
    elif env == 'test':
        load_dotenv(f'{config_dir}/.env.test', override=True)
        logging.info('已加载测试环境配置')
    elif env == 'prod':
        load_dotenv(f'{config_dir}/.env.production', override=True)
        logging.info('已加载生产环境配置')
    else:
        load_dotenv(f'{config_dir}/.env', override=True)
        logging.info('已加载默认环境配置')

    # 验证必需的环境变量
    try:
        from modules.config import validate_required_env_vars
        validate_required_env_vars()
    except Exception as e:
        logging.error(f"环境变量验证失败: {str(e)}")
        # 在生产环境中，可能需要在这里退出程序
        # import sys
        # sys.exit(1)

# 设置日志
setup_logging()

# 创建一个锁
ui_lock = threading.Lock()

# 定义一个函数来串行执行任务
def run_jobs_serially():
    with ui_lock:  # 确保在执行 UI 操作时获得锁
        current_month = datetime.datetime.now().month
        print("Current month is:", current_month)

        if current_month == 4:
            # 上海4月份
            try:
                signing_and_sales_incentive_apr_shanghai()
                time.sleep(5)
            except Exception as e:
                logging.error(f"An error occurred while running signing_and_sales_incentive_apr_shanghai: {e}")
                logging.error(traceback.format_exc())

            # 北京4月份
            try:
                signing_and_sales_incentive_apr_beijing()
                time.sleep(5)
            except Exception as e:
                logging.error(f"An error occurred while running signing_and_sales_incentive_apr_beijing: {e}")
                logging.error(traceback.format_exc())

        elif current_month == 5:
            # 上海5月份
            try:
                signing_and_sales_incentive_may_shanghai()
                time.sleep(5)
            except Exception as e:
                logging.error(f"An error occurred while running signing_and_sales_incentive_mar_shanghai: {e}")
                logging.error(traceback.format_exc())
            # 北京5月份
            try:
                signing_and_sales_incentive_may_beijing()
                time.sleep(5)
            except Exception as e:
                logging.error(f"An error occurred while running signing_and_sales_incentive_feb_beijing: {e}")
                logging.error(traceback.format_exc())
        else:
            logging.info("No tasks scheduled for this month.")

        # 检查工程师状态
        try:
            check_technician_status()
            time.sleep(5)
        except Exception as e:
            logging.error(f"An error occurred while running check_technician_status: {e}")
            logging.error(traceback.format_exc())

# 使用schedule库调度串行执行任务的函数，定时执行一次，在config中配置
schedule.every(RUN_JOBS_SERIALLY_SCHEDULE).minutes.do(run_jobs_serially)

# 定义一个函数来执行日报任务
def daily_service_report_task():
    with ui_lock:  # 确保在执行 UI 操作时获得锁
        try:
            generate_daily_service_report()  # 调用生成日报的函数
            logging.info("Daily service report generated successfully.")
        except Exception as e:
            logging.error(f"An error occurred while generating daily service report: {e}")
            logging.error(traceback.format_exc())

# 使用schedule库调度日报任务，每天11点执行
schedule.every().day.at("11:00").do(daily_service_report_task)

# 运行指定任务
def run_specific_task(task):
    with ui_lock:  # 确保在执行 UI 操作时获得锁
        if task == 'all' or task is None:
            run_jobs_serially()
        elif task == 'beijing-apr':
            try:
                signing_and_sales_incentive_apr_beijing()
            except Exception as e:
                logging.error(f"An error occurred while running signing_and_sales_incentive_apr_beijing: {e}")
                logging.error(traceback.format_exc())
        elif task == 'beijing-may':
            try:
                signing_and_sales_incentive_may_beijing()
            except Exception as e:
                logging.error(f"An error occurred while running signing_and_sales_incentive_may_beijing: {e}")
                logging.error(traceback.format_exc())
        elif task == 'shanghai-apr':
            try:
                signing_and_sales_incentive_apr_shanghai()
            except Exception as e:
                logging.error(f"An error occurred while running signing_and_sales_incentive_apr_shanghai: {e}")
                logging.error(traceback.format_exc())
        elif task == 'shanghai-may':
            try:
                signing_and_sales_incentive_may_shanghai()
            except Exception as e:
                logging.error(f"An error occurred while running signing_and_sales_incentive_may_shanghai: {e}")
                logging.error(traceback.format_exc())
        elif task == 'technician':
            try:
                check_technician_status()
            except Exception as e:
                logging.error(f"An error occurred while running check_technician_status: {e}")
                logging.error(traceback.format_exc())
        elif task == 'daily-report':
            try:
                generate_daily_service_report()
            except Exception as e:
                logging.error(f"An error occurred while generating daily service report: {e}")
                logging.error(traceback.format_exc())

if __name__ == '__main__':
    # 解析命令行参数
    args = parse_args()

    # 加载环境变量
    load_environment(args.env)

    logging.info('Program started')
    logging.info(f'运行环境: {args.env}')

    # 如果指定了任务，则运行指定任务后退出
    if args.task:
        logging.info(f'运行指定任务: {args.task}')
        run_specific_task(args.task)
        logging.info('指定任务已完成，程序退出')
        exit(0)

    # 如果指定了只运行一次，则运行一次后退出
    if args.run_once:
        logging.info('运行一次后退出')
        run_jobs_serially()
        logging.info('任务已完成，程序退出')
        exit(0)

    # 启动任务调度器
    scheduler_thread = threading.Thread(target=task_scheduler.start)
    scheduler_thread.daemon = True  # 设置为守护线程
    # 启动任务调度器线程，注释后可单独测试任务且不会触发GUI操作
    scheduler_thread.start()

    # 启动调度循环
    logging.info('进入调度循环')
    while True:
        try:
            schedule.run_pending()  # 这里也在运行schedule的任务
            time.sleep(1)
        except Exception as e:
            logging.error(f"Job failed with exception: {e}")
            logging.error(traceback.format_exc())
            time.sleep(5)