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
    
# 2024年9月，北京. 幸运数字6，单合同金额1万以上和以下幸运奖励不同；节节高四节；合同累计考虑工单合同金额5万封顶
def signing_and_sales_incentive_sep_beijing():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_BJ_SEP
    performance_data_filename = PERFORMANCE_DATA_FILENAME_BJ_SEP
    status_filename = STATUS_FILENAME_BJ_SEP
    api_url = API_URL_BJ_SEP

    logging.info('BEIJING 2024 9月, Job started ...')

    response = send_request_with_managed_session(api_url)
 
    logging.info('BEIJING 2024 9月, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'BEIJING 2024 9月, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)

    processed_data = process_data_sep_beijing(contract_data, existing_contract_ids,housekeeper_award_lists)
    logging.info('BEIJING 2024 9月, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    notify_awards_sep_beijing(performance_data_filename, status_filename)

    archive_file(contract_data_filename)
    logging.info('BEIJING 2024 9月, Data archived')

    logging.info('BEIJING 2024 9月, Job ended')

# 2024年9月，上海. 与8月的活动规则一致
def signing_and_sales_incentive_sep_shanghai():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_SH_SEP
    performance_data_filename = PERFORMANCE_DATA_FILENAME_SH_SEP
    status_filename = STATUS_FILENAME_SH_SEP
    api_url = API_URL_SH_SEP

    logging.info('SHANGHAI 2024 9月 Conq & triumph, take 1 more city, Job started ...')
    response = send_request_with_managed_session(api_url)
    logging.info('SHANGHAI 2024 9月 Conq & triumph, take 1 more city, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'SHANGHAI 2024 9月 Conq & triumph, take 1 more city, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    # 获取管家奖励列表，升级唯一奖励列表
    housekeeper_award_lists = get_unique_housekeeper_award_list(performance_data_filename)

    processed_data = process_data_july_shanghai(contract_data, existing_contract_ids,housekeeper_award_lists)

    logging.info('SHANGHAI 2024 9月 Conq & triumph, take 1 more city, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    notify_awards_july_shanghai(performance_data_filename, status_filename, contract_data)

    archive_file(contract_data_filename)
    logging.info('SHANGHAI 2024 9月 Conq & triumph, take 1 more city, Data archived')

    logging.info('SHANGHAI 2024 9月 Conq & triumph, take 1 more city, Job ended')   
# 2024年8月，上海. 与7月的活动规则一致
def signing_and_sales_incentive_aug_shanghai():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_SH_AUG
    performance_data_filename = PERFORMANCE_DATA_FILENAME_SH_AUG
    status_filename = STATUS_FILENAME_SH_AUG
    api_url = API_URL_SH_AUG

    logging.info('SHANGHAI 2024 8月 Conq & triumph, take 1 more city, Job started ...')
    response = send_request_with_managed_session(api_url)
    logging.info('SHANGHAI 2024 8月 Conq & triumph, take 1 more city, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'SHANGHAI 2024 8月 Conq & triumph, take 1 more city, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    # 获取管家奖励列表，升级唯一奖励列表
    housekeeper_award_lists = get_unique_housekeeper_award_list(performance_data_filename)

    processed_data = process_data_july_shanghai(contract_data, existing_contract_ids,housekeeper_award_lists)

    logging.info('SHANGHAI 2024 8月 Conq & triumph, take 1 more city, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    notify_awards_july_shanghai(performance_data_filename, status_filename, contract_data)

    archive_file(contract_data_filename)
    logging.info('SHANGHAI 2024 8月 Conq & triumph, take 1 more city, Data archived')

    logging.info('SHANGHAI 2024 8月 Conq & triumph, take 1 more city, Job ended')    
    
# 2024年7月，上海. 与6月的活动规则一致
def signing_and_sales_incentive_july_shanghai():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_SH_JULY
    performance_data_filename = PERFORMANCE_DATA_FILENAME_SH_JULY
    status_filename = STATUS_FILENAME_SH_JULY
    api_url = API_URL_SH_JULY

    logging.info('SHANGHAI 2024 8月 Conq & triumph, take 1 more city, Job started ...')
    response = send_request_with_managed_session(api_url)
    logging.info('SHANGHAI 2024 8月 Conq & triumph, take 1 more city, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'SHANGHAI 2024 8月 Conq & triumph, take 1 more city, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    # 获取管家奖励列表，升级唯一奖励列表
    housekeeper_award_lists = get_unique_housekeeper_award_list(performance_data_filename)

    processed_data = process_data_july_shanghai(contract_data, existing_contract_ids,housekeeper_award_lists)

    logging.info('SHANGHAI 2024 8月 Conq & triumph, take 1 more city, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    notify_awards_july_shanghai(performance_data_filename, status_filename, contract_data)

    archive_file(contract_data_filename)
    logging.info('SHANGHAI 2024 8月 Conq & triumph, take 1 more city, Data archived')

    logging.info('SHANGHAI 2024 8月 Conq & triumph, take 1 more city, Job ended')
    
# 2024年8月，北京. 幸运数字8，单合同金额1万以上和以下幸运奖励不同；节节高四节；合同累计考虑工单合同金额5万封顶
def signing_and_sales_incentive_aug_beijing():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_BJ_AUG
    performance_data_filename = PERFORMANCE_DATA_FILENAME_BJ_AUG
    status_filename = STATUS_FILENAME_BJ_AUG
    api_url = API_URL_BJ_AUG

    logging.info('BEIJING 2024 8月, Job started ...')

    response = send_request_with_managed_session(api_url)
 
    logging.info('BEIJING 2024 8月, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'BEIJING 2024 8月, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)

    processed_data = process_data_aug_beijing(contract_data, existing_contract_ids,housekeeper_award_lists)
    logging.info('BEIJING 2024 8月, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    notify_awards_aug_beijing(performance_data_filename, status_filename)

    archive_file(contract_data_filename)
    logging.info('BEIJING 2024 8月, Data archived')

    logging.info('BEIJING 2024 8月, Job ended')

# 2024年7月，北京. 幸运数字8，单合同金额1万以上和以下幸运奖励不同；节节高四节；合同累计考虑工单合同金额5万封顶
def signing_and_sales_incentive_july_beijing():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_BJ_JULY
    performance_data_filename = PERFORMANCE_DATA_FILENAME_BJ_JULY
    status_filename = STATUS_FILENAME_BJ_JULY
    api_url = API_URL_BJ_JULY

    logging.info('BEIJING 2024 7月, Job started ...')

    response = send_request_with_managed_session(api_url)
 
    logging.info('BEIJING 2024 7月, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'BEIJING 2024 7月, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)

    processed_data = process_data_july_beijing(contract_data, existing_contract_ids,housekeeper_award_lists)
    logging.info('BEIJING 2024 7月, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    notify_awards_july_beijing(performance_data_filename, status_filename)

    archive_file(contract_data_filename)
    logging.info('BEIJING 2024 7月, Data archived')

    logging.info('BEIJING 2024 7月, Job ended')
    
# 2024年6月，上海.
def signing_and_sales_incentive_june_shanghai():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_SH_JUNE
    performance_data_filename = PERFORMANCE_DATA_FILENAME_SH_JUNE
    status_filename = STATUS_FILENAME_SH_JUNE
    api_url = API_URL_SH_JUNE

    logging.info('SHANGHAI 2024 June Conq & triumph, take 1 more city, Job started ...')

    # session_id = get_metabase_session()
    # response = send_request(session_id, api_url)
    response = send_request_with_managed_session(api_url)
    logging.info('SHANGHAI 2024 June Conq & triumph, take 1 more city, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'SHANGHAI 2024 June Conq & triumph, take 1 more city, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)

    processed_data = process_data_june_shanghai(contract_data, existing_contract_ids,housekeeper_award_lists)

    logging.info('SHANGHAI 2024 June Conq & triumph, take 1 more city, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    notify_awards_june_shanghai(performance_data_filename, status_filename, contract_data)

    archive_file(contract_data_filename)
    logging.info('SHANGHAI 2024 June Conq & triumph, take 1 more city, Data archived')

    logging.info('SHANGHAI 2024 June Conq & triumph, take 1 more city, Job ended')
    
# 2024年6月，北京.
def signing_and_sales_incentive_june_beijing():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_BJ_JUNE
    performance_data_filename = PERFORMANCE_DATA_FILENAME_BJ_JUNE
    status_filename = STATUS_FILENAME_BJ_JUNE
    api_url = API_URL_BJ_JUNE

    logging.info('BEIJING 2024 June Conq & triumph, take 1 more city, Job started ...')

    # session_id = get_metabase_session()
    # response = send_request(session_id, api_url)
    response = send_request_with_managed_session(api_url)

    logging.info('BEIJING 2024 June Conq & triumph, take 1 more city, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'BEIJING 2024 June Conq & triumph, take 1 more city, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)

    processed_data = process_data_june_beijing(contract_data, existing_contract_ids,housekeeper_award_lists)

    logging.info('BEIJING 2024 June Conq & triumph, take 1 more city, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注', '登记时间']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    notify_awards_june_beijing(performance_data_filename, status_filename, contract_data)

    archive_file(contract_data_filename)
    logging.info('BEIJING 2024 June Conq & triumph, take 1 more city, Data archived')

    logging.info('BEIJING 2024 June Conq & triumph, take 1 more city, Job ended')
    
# 2024年五月，过关斩将·再下一城活动 Conq & triumph, take 1 more city.
def signing_and_sales_incentive_ctt1mc_shanghai():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_SH_MAY
    performance_data_filename = PERFORMANCE_DATA_FILENAME_SH_MAY
    status_filename = STATUS_FILENAME_SH_MAY
    api_url = API_URL_SH_MAY

    logging.info('SHANGHAI 2024 May Conq & triumph, take 1 more city, Job started ...')

    # session_id = get_metabase_session()
    # response = send_request(session_id, api_url)
    response = send_request_with_managed_session(api_url)
    logging.info('SHANGHAI 2024 May Conq & triumph, take 1 more city, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'SHANGHAI 2024 May Conq & triumph, take 1 more city, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)

    processed_data = process_data_ctt1mc_shanghai(contract_data, existing_contract_ids,housekeeper_award_lists)

    logging.info('SHANGHAI 2024 May Conq & triumph, take 1 more city, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    notify_awards_ctt1mc_shanghai(performance_data_filename, status_filename, contract_data)

    archive_file(contract_data_filename)
    logging.info('SHANGHAI 2024 May Conq & triumph, take 1 more city, Data archived')

    logging.info('SHANGHAI 2024 May Conq & triumph, take 1 more city, Job ended')
    
# 2024年五月，过关斩将·再下一城活动 Conq & triumph, take 1 more city.
def signing_and_sales_incentive_ctt1mc_beijing():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_BJ_MAY
    performance_data_filename = PERFORMANCE_DATA_FILENAME_BJ_MAY
    status_filename = STATUS_FILENAME_BJ_MAY
    api_url = API_URL_BJ_MAY

    logging.info('BEIJING 2024 May Conq & triumph, take 1 more city, Job started ...')

    # session_id = get_metabase_session()
    # response = send_request(session_id, api_url)
    response = send_request_with_managed_session(api_url)

    logging.info('BEIJING 2024 May Conq & triumph, take 1 more city, Request sent')

    rows = response['data']['rows']

    columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)", "转化率(conversion)", "平均客单价(average)"]
    save_to_csv_with_headers(rows,contract_data_filename,columns)

    logging.info(f'BEIJING 2024 May Conq & triumph, take 1 more city, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)

    processed_data = process_data_ctt1mc_beijing(contract_data, existing_contract_ids,housekeeper_award_lists)

    logging.info('BEIJING 2024 May Conq & triumph, take 1 more city, Data processed')

    performance_data_headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '转化率(conversion)', '平均客单价(average)','活动期内第几个合同','管家累计金额','管家累计单数','奖金池','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注']

    write_performance_data(performance_data_filename, processed_data, performance_data_headers)

    notify_awards_ctt1mc_beijing(performance_data_filename, status_filename, contract_data)

    archive_file(contract_data_filename)
    logging.info('BEIJING 2024 May Conq & triumph, take 1 more city, Data archived')

    logging.info('BEIJING 2024 May Conq & triumph, take 1 more city, Job ended')
    
def check_signing_and_award_sales_incentive():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE
    performance_data_filename = PERFORMANCE_DATA_FILENAME
    status_filename = STATUS_FILENAME

    logging.info('BEIJING, Job started ...')

    session_id = get_metabase_session()
    response = send_request(session_id)
    logging.info('BEIJING, Request sent')

    rows = response['data']['rows']

    save_to_csv_with_headers(rows,contract_data_filename)

    logging.info(f'BEIJING, Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)

    processed_data = process_data(contract_data, existing_contract_ids,housekeeper_award_lists)
    logging.info('BEIJING, Data processed')

    headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '活动期内第几个合同','管家累计金额','管家累计单数','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '下一级奖项所需金额差']

    write_performance_data(performance_data_filename, processed_data, headers)

    notify_awards(performance_data_filename, status_filename)

    archive_file(contract_data_filename)
    logging.info('BEIJING, Data archived')

    logging.info('BEIJING, Job ended')

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
    
def check_signing_and_award_sales_incentive_shanghai():
    contract_data_filename = TEMP_CONTRACT_DATA_FILE_SHANGHAI
    performance_data_filename = PERFORMANCE_DATA_FILENAME_SHANGHAI
    status_filename = STATUS_FILENAME_SHANGHAI

    api_url = API_URL_SHANGHAI
    
    logging.info('SHANGHAI, Job started')

    session_id = get_metabase_session()
    response = send_request(session_id, api_url)

    rows = response['data']['rows']

    save_to_csv_with_headers(rows,contract_data_filename)

    logging.info(f'SHANGHAI: Data saved to {contract_data_filename}')

    contract_data = read_contract_data(contract_data_filename)

    # 业务台账中已经登记过的合同ID
    existing_contract_ids = collect_unique_contract_ids_from_file(performance_data_filename)

    # 业务台账中已经获奖的管家列表
    housekeeper_award_lists = get_housekeeper_award_list(performance_data_filename)
    
    # 统计业务台账中已经发放的不同类型的奖励数量
    reward_type_counts = count_reward_types(performance_data_filename)
    logging.info(f"SHANGHAI: Reward type counts: {reward_type_counts}")

    # 根据上海活动的逻辑来处理数据，需要的是单独进行“计算奖励类型和名称”的确认。
    processed_data = process_data_shanghai(contract_data, existing_contract_ids, housekeeper_award_lists, reward_type_counts)
    logging.info('SHANGHAI: Data processed')

    headers = ['活动编号', '合同ID(_id)', '活动城市(province)', '工单编号(serviceAppointmentNum)', 'Status', '管家(serviceHousekeeper)', '合同编号(contractdocNum)', '合同金额(adjustRefundMoney)', '支付金额(paidAmount)', '差额(difference)', 'State', '创建时间(createTime)', '服务商(orgName)', '签约时间(signedDate)', 'Doorsill', '款项来源类型(tradeIn)', '活动期内第几个合同','管家累计金额','管家累计单数','激活奖励状态', '奖励类型', '奖励名称', '是否发送通知', '备注']

    write_performance_data(performance_data_filename, processed_data, headers)

    # 根据上海活动的逻辑来进行通知
    notify_awards_shanghai(performance_data_filename, status_filename)

    archive_file(contract_data_filename)
    logging.info('SHANGHAI: Data archived')

    logging.info('SHANGHAI: Job ended')