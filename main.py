import schedule
import time
import traceback
import logging
from modules.log_config import setup_logging
from jobs import check_signing_and_award_sales_incentive, check_technician_status
from modules.config import JOBS

# 设置日志
setup_logging()

def run_job_with_exception_handling():

    # schedule.every(15).minutes.do(check_signing_and_award_sales_incentive)
    # schedule.every(1).minutes.do(check_technician_status)
    
    for job_name, job_config in JOBS.items():
        # 解析函数名为实际的函数引用
        job_function = globals()[job_config['function']]
        # 使用解析后的函数引用调度任务
        schedule.every(job_config['schedule']).minutes.do(job_function)
            
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.error(f"Job failed with exception: {e}")
            logging.error(traceback.format_exc())
            time.sleep(5)  #  等待x秒后重试

if __name__ == '__main__':
    logging.info('Program started')

    # check_signing_and_award_sales_incentive() # Job starts immediately
    # check_technician_status()
    run_job_with_exception_handling()