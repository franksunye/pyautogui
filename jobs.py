# jobs.py
import logging
from modules.request_module import get_metabase_session, send_request, send_request_with_managed_session
from modules.data_processing_module import *
from modules.file_utils import *
from modules.notification_module import *
from modules.config import *

def service_provider_weekly_report():
    logging.info('服务商周报任务开始...')

    # 步骤1: 从两个Metabase数据源获取数据
    inspection_rate_api_url = 'http://metabase.fsgo365.cn:3000/api/card/1274/query'
    wecom_usage_api_url = 'http://metabase.fsgo365.cn:3000/api/card/1272/query'
    
    response_inspection_rate = send_request_with_managed_session(inspection_rate_api_url)
    print(response_inspection_rate)  # Add this line to print the response
    
    inspectionRateData = response_inspection_rate['data']['rows']

    response_wecom_usage = send_request_with_managed_session(wecom_usage_api_url)
    wecomUsageData = response_wecom_usage['data']['rows']

    logging.info('从Metabase数据源获取数据完成')

    # # 步骤2: 将两部分数据进行合并
    # merged_data = merge_data_sources(inspectionRateData, wecomUsageData)
    # logging.info('数据合并完成')
    
    # # 步骤3: 处理合并后的数据，批量生成周报
    # weekly_reports = generate_weekly_report_for_each_supplier(merged_data)
    # logging.info('周报生成完成')

    # 步骤4: 发送周报
    # send_status = send_reports(weekly_reports)
    # if send_status:
    #     logging.info('周报发送成功')
    # else:
    #     logging.error('周报发送失败')

    # logging.info('服务商周报任务结束')
    
# 2024年11月，北京. 幸运数字8，单合同金额1万以上和以下幸运奖励不同；节节高三档；合同累计考虑工单合同金额5万封顶
def signing_and_sales_incentive_nov_beijing():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_BJ_NOV
    performance_data_filename = PERFORMANCE_DATA_FILENAME_BJ_NOV
    status_filename = STATUS_FILENAME_BJ_NOV
    api_url = API_URL_BJ_NOV

    logging.info('BEIJING 2024 11月, Job started ...')

    response = send_request_with_managed_session(api_url)
    logging.info('BEIJING 2024 11月, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows, contract_data_filename, columns)

    logging.info(f'BEIJING 2024 11月, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)

    # 使用新的通用数据处理函数
    processed_data = process_data_generic(contract_data, existing_contract_ids, housekeeper_award_lists, 'nov_beijing')
    logging.info('BEIJING 2024 11月, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)', '活动期内第几个合同', '管家累计金额', '管家累计单数', '奖金池', '激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    notify_awards_nov_beijing(performance_data_filename, status_filename)

    archive_file(contract_data_filename)
    logging.info('BEIJING 2024 11月, Data archived')

    logging.info('BEIJING 2024 11月, Job ended')

# 2024年11月，上海. 与10月的活动规则一致
def signing_and_sales_incentive_nov_shanghai():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_SH_NOV
    performance_data_filename = PERFORMANCE_DATA_FILENAME_SH_NOV
    status_filename = STATUS_FILENAME_SH_NOV
    api_url = API_URL_SH_NOV

    logging.info('SHANGHAI 2024 11月 Conq & triumph, take 1 more city, Job started ...')
    response = send_request_with_managed_session(api_url)
    logging.info('SHANGHAI 2024 11月 Conq & triumph, take 1 more city, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'SHANGHAI 2024 11月 Conq & triumph, take 1 more city, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    # 获取管家奖励列表，升级唯一奖励列表
    housekeeper_award_lists = get_unique_housekeeper_award_list(performance_data_filename)

    # 当月的数据处理逻辑，与7月一致
    processed_data = process_data_shanghai(contract_data, existing_contract_ids,housekeeper_award_lists,'june_shanghai')

    logging.info('SHANGHAI 2024 11月 Conq & triumph, take 1 more city, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    # 当月的数据处理逻辑，与7月一致
    notify_awards_july_shanghai(performance_data_filename, status_filename, contract_data)

    archive_file(contract_data_filename)
    logging.info('SHANGHAI 2024 11月 Conq & triumph, take 1 more city, Data archived')

    logging.info('SHANGHAI 2024 11月 Conq & triumph, take 1 more city, Job ended')   

def check_technician_status():
    api_url = API_URL_TS
    status_filename = STATUS_FILENAME_TS

    logging.info('BEIJING, Job started ...')

    # session_id = get_metabase_session()
    # response = send_request(session_id, api_url)
    response = send_request_with_managed_session(api_url)
    
    status_changes = response['data']['rows']

    notify_technician_status_changes(status_changes, status_filename)

    logging.info('BEIJING, Job ended') 

def generate_daily_service_report():
    logging.info('Daily service report generation started...')
    api_url = API_URL_DAILY_SERVICE_REPORT
    status_code_filename = STATUS_FILENAME_DAILY_REPORT

    try:
        # 1. 发送请求以获取日报数据
        response = send_request_with_managed_session(api_url)
        logging.info('Daily service report request sent successfully.')

        # 2. 处理响应数据
        report_data = response['data']['rows']
        if not report_data:
            logging.warning('No data found for the daily service report.')
            # return

        # 3. 发送通知
        notify_daily_service_report(report_data, status_code_filename)
        logging.info('Daily service report notification sent successfully.')

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
    