import schedule
import time
import traceback
import logging
from modules.log_config import setup_logging
from jobs import *
from modules.config import RUN_JOBS_SERIALLY_SCHEDULE

# 设置日志
setup_logging()

# 定义一个函数来串行执行任务
def run_jobs_serially():
    
    # 北京7月份
    try:
        signing_and_sales_incentive_july_beijing()
        time.sleep(5)
    except Exception as e:
        logging.error(f"An error occurred while running signing_and_sales_incentive_ctt1mc_beijing: {e}")
        logging.error(traceback.format_exc())
   
    # 上海7月份
    try:
        signing_and_sales_incentive_july_shanghai()
        time.sleep(5)
    except Exception as e:
        logging.error(f"An error occurred while running signing_and_sales_incentive_ctt1mc_shanghai: {e}")
        logging.error(traceback.format_exc())
    
    # 上海6月份    
    try:
        signing_and_sales_incentive_june_shanghai()
        time.sleep(5)
    except Exception as e:
        logging.error(f"An error occurred while running signing_and_sales_incentive_ctt1mc_shanghai: {e}")
        logging.error(traceback.format_exc())
    
    # 北京6月份    
    try:
        signing_and_sales_incentive_june_beijing()
        time.sleep(5)
    except Exception as e:
        logging.error(f"An error occurred while running signing_and_sales_incentive_ctt1mc_shanghai: {e}")
        logging.error(traceback.format_exc())                
    
    # 检查工程师状态
    try:
        check_technician_status()
        time.sleep(5)
    except Exception as e:
        logging.error(f"An error occurred while running check_technician_status: {e}")
        logging.error(traceback.format_exc())

# 使用schedule库调度串行执行任务的函数，定时执行一次，在config中配置
schedule.every(RUN_JOBS_SERIALLY_SCHEDULE).minutes.do(run_jobs_serially)

if __name__ == '__main__':
    logging.info('Program started')

    # signing_and_sales_incentive_july_beijing() 
    # signing_and_sales_incentive_june_shanghai()
    # check_contact_timeout()     
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.error(f"Job failed with exception: {e}")
            logging.error(traceback.format_exc())
            time.sleep(5)