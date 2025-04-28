# jobs.py
import logging
from modules.request_module import get_metabase_session, send_request, send_request_with_managed_session
from modules.data_processing_module import *
from modules.file_utils import *
from modules.notification_module import *
from modules.config import *
from modules.service_provider_sla_monitor import process_sla_violations

# 2025年4月，北京. 
# 幸运数字8，单合同金额1万以上和以下幸运奖励不同；节节高三档；
# 单个项目（工单）签约合同金额大于10万时，参与累计合同金额计算时均按10万计入。
def signing_and_sales_incentive_apr_beijing():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_BJ_APR
    performance_data_filename = PERFORMANCE_DATA_FILENAME_BJ_APR
    status_filename = STATUS_FILENAME_BJ_APR
    api_url = API_URL_BJ_APR

    logging.info('BEIJING 2025 4月, Job started ...')

    response = send_request_with_managed_session(api_url)
 
    logging.info('BEIJING 2025 4月, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'BEIJING 2025 4月, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)

    # 当月的数据处理逻辑
    processed_data = process_data_apr_beijing(contract_data, existing_contract_ids,housekeeper_award_lists,use_generic=True)
    logging.info('BEIJING 2025 4月, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池','计入业绩金额','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    # 当月的数据处理逻辑
    notify_awards_apr_beijing(performance_data_filename, status_filename)

    archive_file(contract_data_filename)
    logging.info('BEIJING 2025 4月, Data archived')

    logging.info('BEIJING 2025 4月, Job ended')

# 2025年4月，上海. 签约和奖励播报
def signing_and_sales_incentive_apr_shanghai():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_SH_APR
    performance_data_filename = PERFORMANCE_DATA_FILENAME_SH_APR
    status_filename = STATUS_FILENAME_SH_APR
    api_url = API_URL_SH_APR

    logging.info('SHANGHAI 2025 4月 Conq & triumph, take 1 more city, Job started ...')
    response = send_request_with_managed_session(api_url)
    logging.info('SHANGHAI 2025 4月 Conq & triumph, take 1 more city, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'SHANGHAI 2025 4月 Conq & triumph, take 1 more city, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    # 获取管家奖励列表，升级唯一奖励列表
    housekeeper_award_lists = get_unique_housekeeper_award_list(performance_data_filename)

    # 当月的数据处理逻辑，奖励规则按照3月份的
    processed_data = process_data_shanghai_apr(contract_data, existing_contract_ids, housekeeper_award_lists)

    logging.info('SHANGHAI 2025 4月 Conq & triumph, take 1 more city, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池', '计入业绩金额','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    # 当月的通知数据处理逻辑（与三月一致）
    notify_awards_shanghai_generate_message_march(performance_data_filename, status_filename, contract_data)

    archive_file(contract_data_filename)
    logging.info('SHANGHAI 2025 4月 Conq & triumph, take 1 more city, Data archived')

    logging.info('SHANGHAI 2025 4月 Conq & triumph, take 1 more city, Job ended')   

def check_technician_status():
    api_url = API_URL_TS
    status_filename = STATUS_FILENAME_TS

    logging.info('BEIJING, Technician Status Check Job started')

    response = send_request_with_managed_session(api_url)    
    status_changes = response['data']['rows']

    notify_technician_status_changes(status_changes, status_filename)

    logging.info('BEIJING, Technician Status Check Job ended') 

def generate_daily_service_report():
    logging.info('Daily service report generation started...')
    api_url = API_URL_DAILY_SERVICE_REPORT
    temp_daily_service_report_file = TEMP_DAILY_SERVICE_REPORT_FILE
    status_code_filename = DAILY_SERVICE_REPORT_RECORD_FILE

    try:
        # 1. 发送请求以获取日报数据
        response = send_request_with_managed_session(api_url)
        logging.info('Daily service report request sent successfully.')

        # 2. 处理响应数据
        report_data = response['data']['rows']
        if not report_data:
            logging.warning('No data found for the daily service report.')
            # return

        # 3. 保存数据到CSV文件
        columns = ["_id", "sid", "saCreateTime", "orderNum", "province", "orgName", "supervisorName", "sourceType", "status", "msg", "memo", "workType", "createTime"]
        save_to_csv_with_headers(report_data, temp_daily_service_report_file, columns)

        # 4. 读取数据
        report_data = read_daily_service_report(temp_daily_service_report_file)
        logging.info(f"Report data: {report_data}")

        # 新的SLA违规检查并发送通知服务
        process_sla_violations(report_data)
        logging.info('SLA violations processed successfully.')

        # # 当前适用的发送日常服务报告
        # notify_daily_service_report(report_data, status_code_filename)
        # logging.info('Daily service report notification sent successfully.')

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    logging.info('Daily service report generation completed.')

def check_contact_timeout():
    api_url = API_URL_CONTACT_TIMEOUT
    # notify_status_filename = STATUS_FILENAME_CONTACT_TIMEOUT

    logging.info('Contact Timeout Check, Job started ...')

    response = send_request_with_managed_session(api_url)
    
    if response is None:
        logging.error('Failed to get response for contact timeout check')
        return

    contact_timeout_data = response['data']['rows']
    print(contact_timeout_data)  # 打印 status_changes

    notify_contact_timeout_changes_template_card(contact_timeout_data)

    logging.info('Contact Timeout Check, Job ended')
    