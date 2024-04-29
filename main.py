import schedule
import time
import traceback
import logging
from modules.log_config import setup_logging
from jobs import check_signing_and_award_sales_incentive, check_technician_status, check_signing_and_award_sales_incentive_shanghai, signing_and_sales_incentive_ctt1mc_beijing, signing_and_sales_incentive_ctt1mc_shanghai
from modules.config import RUN_JOBS_SERIALLY_SCHEDULE

# 设置日志
setup_logging()

# 定义一个函数来串行执行任务
def run_jobs_serially():
    try:
        # signing_and_sales_incentive_ctt1mc_beijing()
        # time.sleep(5)
        check_signing_and_award_sales_incentive()
        time.sleep(5)
        check_technician_status()
        time.sleep(5)
        check_signing_and_award_sales_incentive_shanghai()
        time.sleep(5)
        # signing_and_sales_incentive_ctt1mc_shanghai()
        # time.sleep(5)
    except Exception as e:
        logging.error(f"An error occurred while running jobs: {e}")
        logging.error(traceback.format_exc())

# 使用schedule库调度串行执行任务的函数，定时执行一次，在config中配置
schedule.every(RUN_JOBS_SERIALLY_SCHEDULE).minutes.do(run_jobs_serially)

if __name__ == '__main__':
    logging.info('Program started')

    signing_and_sales_incentive_ctt1mc_shanghai()
    signing_and_sales_incentive_ctt1mc_beijing()
    
    # while True:
    #     try:
    #         schedule.run_pending()
    #         time.sleep(1)
    #     except Exception as e:
    #         logging.error(f"Job failed with exception: {e}")
    #         logging.error(traceback.format_exc())
    #         time.sleep(5) #  等待x秒后重试