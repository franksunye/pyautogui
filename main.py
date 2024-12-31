import schedule
import time
import traceback
import logging
import threading
from modules.log_config import setup_logging
from jobs import *
from modules.config import RUN_JOBS_SERIALLY_SCHEDULE
import datetime
import task_scheduler # 引入任务调度模块

# 设置日志
setup_logging()

# 创建一个锁
ui_lock = threading.Lock()

# 定义一个函数来串行执行任务
def run_jobs_serially():
    with ui_lock:  # 确保在执行 UI 操作时获得锁
        current_month = datetime.datetime.now().month
        print("Current month is:", current_month)

        if current_month == 12:
            # 上海12月份
            try:
                signing_and_sales_incentive_dec_shanghai()
                time.sleep(5)
            except Exception as e:
                logging.error(f"An error occurred while running signing_and_sales_incentive_dec_shanghai: {e}")
                logging.error(traceback.format_exc())
                
        elif current_month == 1:
            # 上海1月份
            try:
                signing_and_sales_incentive_jan_shanghai()
                time.sleep(5)
            except Exception as e:
                logging.error(f"An error occurred while running signing_and_sales_incentive_jan_shanghai: {e}")
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

if __name__ == '__main__':
    logging.info('Program started')

    # 启动任务调度器
    scheduler_thread = threading.Thread(target=task_scheduler.start)
    scheduler_thread.daemon = True  # 设置为守护线程
    scheduler_thread.start()

    # generate_daily_service_report()
    # signing_and_sales_incentive_nov_beijing()
    # signing_and_sales_incentive_dec_shanghai()
    # 启动调度循环
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.error(f"Job failed with exception: {e}")
            logging.error(traceback.format_exc())
            time.sleep(5)