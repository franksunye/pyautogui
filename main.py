import os
import shutil
import schedule
import time
import logging
from log_config import setup_logging
from request_module import send_request
from data_processing_module import process_data
from file_operation_module import *
from data_processing_module import process_data
# 设置日志
setup_logging()

def job():

    # logging.info('Job started')
    # response = send_request()
    # logging.info('Request sent')

    # # Extract rows from response
    # rows = response['data']['rows']

    # # Save rows to CSV file with specified column names
    # save_to_csv_with_headers(rows)

    # logging.info('Data saved to ContractData.csv')

    # logging.info('Data processed')

    contract_data_filename = 'TestData.csv'
    performance_data_filename = 'PerformanceData.csv'
    # 读取合同数据
    contract_data = read_contract_data(contract_data_filename)
    # 获取已存在的合同ID
    existing_contract_ids = read_performance_data(performance_data_filename)
    # 获取管家已经获取到的奖项
    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)
    # 处理合同数据
    processed_data = process_data(contract_data, existing_contract_ids,housekeeper_award_lists)

    logging.info('要发送的数据：')
    
    qianyue_msgs=[]
    jiangli_msgs=[]
    
    for itme in processed_data:
        msg=f'''开工大吉[庆祝][庆祝][庆祝]
恭喜{itme["管家(serviceHousekeeper)"]}签约合同{itme["合同编号(contractdocNum)"]}并完成线上收款[烟花][烟花][烟花]

本单为本月平台累计签约第{itme["活动期内第几个合同"]}单，个人累计签约第{itme["管家累计单数"]}单，累计签约金额{itme["管家累计金额"]}元，{itme["下一级奖项所需金额差"]}'''
        # logging.info(msg)
        qianyue_msgs.append(msg)

        if itme['是否发送通知']=='Y':
            jiangli_msg=f'''{itme["管家(serviceHousekeeper)"]}签约合同{itme["合同编号(contractdocNum)"]}达成{itme["奖励类型"]}  {itme["奖励名称"]}'''
            jiangli_msgs.append(jiangli_msg)
            logging.info(jiangli_msg)
            

    # 定义性能数据文件的列头
    headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '活动期内第几个合同','管家累计金额','管家累计单数','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '下一级奖项所需金额差']
    # 写入处理后的数据到性能数据文件
    write_performance_data(performance_data_filename, processed_data, headers)

    # # Archive ContractData.csv
    # archive_file('ContractData.csv')
    # logging.info('Data archived')

    logging.info('Job ended')

if __name__ == '__main__':
    logging.info('Program started')
    job() # Job starts immediately
    logging.info('Program ended')
    # schedule.every(10).minutes.do(job)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
