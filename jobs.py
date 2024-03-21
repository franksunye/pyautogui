# jobs.py
import logging
from modules.request_module import get_metabase_session, send_request
from modules.data_processing_module import process_data
from modules.file_utils import *
from modules.notification_module import notify_awards, notify_technician_status_changes
from modules.config import *

def check_signing_and_award_sales_incentive():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE
    performance_data_filename = PERFORMANCE_DATA_FILENAME
    status_filename = STATUS_FILENAME

    logging.info('Job started')

    session_id = get_metabase_session()
    response = send_request(session_id)
    logging.info('Request sent')

    rows = response['data']['rows']

    save_to_csv_with_headers(rows,contract_data_filename)

    logging.info('Data saved to ContractData.csv')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = read_performance_data(performance_data_filename)

    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)

    processed_data = process_data(contract_data, existing_contract_ids,housekeeper_award_lists)
    logging.info('Data processed')

    headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '活动期内第几个合同','管家累计金额','管家累计单数','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '下一级奖项所需金额差']

    write_performance_data(performance_data_filename, processed_data, headers)

    notify_awards(performance_data_filename, status_filename)

    archive_file(contract_data_filename)
    logging.info('Data archived')

    logging.info('Job ended')

def check_technician_status():
    api_url = API_URL_TS
    status_filename = STATUS_FILENAME_TS

    logging.info('Checking technician status...')

    session_id = get_metabase_session()
    logging.info(f'Metabase session ID: {session_id}')

    response = send_request(session_id, api_url) # 请替换为实际的API端点
    logging.info('Request sent to get technician status updates.')

    status_changes = response['data']['rows']

    notify_technician_status_changes(status_changes, status_filename)

    logging.info('Technician status check completed.') 