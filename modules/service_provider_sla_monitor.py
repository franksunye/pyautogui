import json
import os
from datetime import datetime, timedelta
import logging
from modules.config import SERVICE_PROVIDER_MAPPING, SLA_VIOLATIONS_RECORDS_FILE, SLA_CONFIG  # 引入配置中的服务商映射和文件路径
from modules.notification_module import send_wecom_message as original_send_wecom_message  # 导入已有的发送消息函数并重命名

# 假设SLA违规记录存储在这个文件中
# SLA_VIOLATIONS_RECORDS_FILE = 'sla_violations.json'

def monitor_sla_compliance_and_report(sla_violation_data):
    # 1. 检查前一天的SLA违规情况
    if has_sla_violations_yesterday(sla_violation_data):
        # 发送SLA违规通知
        send_sla_violation_notifications(sla_violation_data)
        logging.info("已发送昨日SLA违规通知，违规数量: %d", len(sla_violation_data))
    else:
        logging.debug("昨日无SLA违规记录，无需发送通知")

    # 2. 检查过去一周的SLA达标情况
    sla_violating_providers = get_weekly_sla_violations()  # 获取过去一周违反SLA的服务商
    if is_monday():  # 每周一进行周报
        compliant_providers = get_sla_compliant_providers(sla_violating_providers)
        
        # 发送表扬消息给达标的服务商
        if compliant_providers:
            compliance_msg = "上周无超时工单，请继续保持。👍"
            for provider_name in compliant_providers:
                receiver_name = SERVICE_PROVIDER_MAPPING.get(provider_name, "sunye")
                try:
                    send_wecom_message_wrapper(receiver_name, compliance_msg)
                    logging.debug(f"已向服务商 {provider_name}({receiver_name}) 发送SLA达标通知")
                except Exception as e:
                    logging.error(f"发送SLA达标通知给 {receiver_name} 时出错: {e}")

        # 为每个违反SLA的服务商发送详细的周报
        for provider_name in sla_violating_providers:
            sla_performance_report = generate_sla_performance_report(provider_name)
            logging.debug(f"生成{provider_name}的SLA表现周报:\n{sla_performance_report}")
            receiver_name = SERVICE_PROVIDER_MAPPING.get(provider_name, "sunye")
            try:
                send_wecom_message_wrapper(receiver_name, sla_performance_report)
                logging.info(f"已完成服务商 {provider_name} 的SLA周报发送")
            except Exception as e:
                logging.error(f"发送SLA周报给 {receiver_name} 时出错: {e}")

def has_sla_violations_yesterday(sla_data):
    return len(sla_data) > 0

def get_weekly_sla_violations():
    timeout_records = load_sla_violation_records()
    if not timeout_records:
        logging.warning("没有找到超时记录文件或文件为空")
        return []

    today = datetime.now().date()
    last_week_services = set()
    
    for i in range(1, 8):  # 从1到7，确保不包括今天
        date_str = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        logging.debug(f"检查 {date_str} 的超时记录")
        
        if date_str not in timeout_records:
            logging.debug(f"{date_str} 没有任何记录")
            continue
            
        if not timeout_records[date_str]:  # 空列表的情况
            logging.debug(f"{date_str} 没有超时记录")
            continue
            
        # 找到有记录的情况
        current_day_timeouts = set(record['orgName'] for record in timeout_records[date_str])
        if current_day_timeouts:
            last_week_services.update(current_day_timeouts)
            logging.debug(f"{date_str} 发现 {len(current_day_timeouts)} 个超时服务商")

    if last_week_services:
        logging.info(f"过去一周总计发现 {len(last_week_services)} 个不同的超时服务商")
    else:
        logging.info("过去一周没有发现任何超时服务商")
        
    return list(last_week_services)

def get_sla_compliant_providers(non_compliant_providers):
    all_providers = set(SERVICE_PROVIDER_MAPPING.keys())
    logging.debug("正在统计符合SLA要求的服务商")
    compliant_providers = all_providers - set(non_compliant_providers)

    return list(compliant_providers)

def send_sla_violation_notifications(violation_data):
    for record in violation_data:
        msg = construct_sla_violation_message(record)
        receiver_name = SERVICE_PROVIDER_MAPPING.get(record['orgName'], "sunye")
        try:
            send_wecom_message_wrapper(receiver_name, msg)  # 发送消息
            logging.info(f"已向 {record['orgName']} 发送超时通知")
            logging.info(f"消息内容: {msg}")
        except Exception as e:
            logging.error(f"发送消息给 {receiver_name} 时出错: {e}")

def construct_sla_violation_message(violation_record):
    try:
        # 解析建单时间并格式化
        create_time = datetime.fromisoformat(violation_record['saCreateTime'].replace("Z", ""))  # 处理时区
        # formatted_time = create_time.strftime("%Y年%m月%d日 %H:%M")  # 格式化为 YYYY年MM月DD日 HH:MM
        
        # 使用 str.format() 构建消息内容
        msg = (
            f"超时通知:\n"
            f"工单编号：{violation_record['orderNum']}\n"
            f"建单时间：{create_time}\n"
            f"管家：{violation_record['supervisorName']}\n"
            f"违规类型：{violation_record['msg']}\n"
            f"违规描述：{violation_record['memo']}\n"
            f"说明：以上数据为服务商昨日工单超时统计，如有异议请于下周一十二点前联系运营人员王金申诉。"
        )
        return msg
    except Exception as e:
        logging.error(f"Error constructing message for record {violation_record}: {e}")
        return "消息构建失败"

def update_sla_violation_records(violation_data):
    logging.info("开始更新SLA违规记录，数据条数: %d", len(violation_data))
    # 更新超时记录
    if not os.path.exists(SLA_VIOLATIONS_RECORDS_FILE):
        logging.debug("SLA违规记录文件不存在，创建新的记录字典")
        timeout_records = {}
    else:
        logging.debug("从文件加载已有的SLA违规记录")
        with open(SLA_VIOLATIONS_RECORDS_FILE, 'r', encoding='utf-8') as f:
            timeout_records = json.load(f)

    today = datetime.now().date()
    last_week = today - timedelta(days=7)
    logging.debug(f"开始清理{last_week}之前的过期记录")

    # 清理过期记录
    old_records_count = len(timeout_records)
    timeout_records = {date: records for date, records in timeout_records.items() if datetime.strptime(date, '%Y-%m-%d').date() >= last_week and datetime.strptime(date, '%Y-%m-%d').date() < today}
    logging.info(f"清理完成，删除了 {old_records_count - len(timeout_records)} 条过期记录")

    # 记录今天的超时情况，记录详细信息
    today_str = today.strftime('%Y-%m-%d')
    timeout_records[today_str] = violation_data  # 直接记录所有详细信息
    logging.info(f"更新{today_str}的违规记录完成，共{len(violation_data)}条")

    # 保存更新后的记录，确保中文字符不被转义
    logging.debug("开始保存更新后的记录到文件")
    with open(SLA_VIOLATIONS_RECORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(timeout_records, f, ensure_ascii=False, indent=4)
    logging.info("SLA违规记录更新完成")

def get_last_week_sla_violations():
    # 获取过去一周的超时记录，不包括今天
    if not os.path.exists(SLA_VIOLATIONS_RECORDS_FILE):
        return []

    with open(SLA_VIOLATIONS_RECORDS_FILE, 'r') as f:
        timeout_records = json.load(f)

    last_week_records = set()
    today = datetime.now().date()
    for i in range(1, 8):  # 从1到7，确保不包括今天
        date_str = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        if date_str in timeout_records:
            last_week_records.update(timeout_records[date_str])

    return list(last_week_records)

def is_monday():
    """
    检查今天是否是星期一
    如果配置FORCE_MONDAY为True，则始终返回True（用于测试）
    否则检查实际日期
    """
    if SLA_CONFIG["FORCE_MONDAY"]:
        return True
    return datetime.now().weekday() == 0

def send_wecom_message_wrapper(receiver_name, msg):
    # 调用已存在的 send_wecom_message 函数
    try:
        original_send_wecom_message(receiver_name, msg)  # 使用导入的函数发送消息
    except Exception as e:
        logging.error(f"发送消息给 {receiver_name} 时出错: {e}")

def generate_sla_performance_report(provider):
    # 构建指定服务商的一周内超时记录的汇总消息
    # 获取当前周一日期作为发送日期
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    # 计算数据周期
    period_start = (monday - timedelta(days=7)).strftime('%Y.%m.%d')
    period_end = (monday - timedelta(days=1)).strftime('%Y.%m.%d')
    appeal_deadline = monday.strftime('%Y 年%m月%d日')
    
    report = f"数据周期: {period_start}-{period_end}\n"
    report += f"服务商: {provider}\n\n"
    records = get_provider_sla_violations(provider)  # 获取该服务商的超时记录
    for record in records:
        report += f"- 工单编号：{record['orderNum']} 管家：{record['supervisorName']} 违规类型：{record['msg']}\n"
    
    report += f"\n如有异议，请于 {appeal_deadline} 24 时前，联系运营人员王金申诉"
    return report

def get_provider_sla_violations(provider_name):
    # 获取指定服务商的超时记录，并将日期信息包含在每个记录中
    if not os.path.exists(SLA_VIOLATIONS_RECORDS_FILE):
        return []

    with open(SLA_VIOLATIONS_RECORDS_FILE, 'r', encoding='utf-8') as f:
        timeout_records = json.load(f)

    records = []
    today = datetime.now().date()
    for i in range(1, 8):  # 从1到7，确保不包括今天
        date_str = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        if date_str in timeout_records:
            for record in timeout_records[date_str]:
                # 只获取指定服务商的记录
                if record['orgName'] == provider_name:
                    # 将日期信息添加到每个记录中
                    record_with_date = record.copy()  # 复制原始记录
                    record_with_date['date'] = date_str  # 添加日期字段
                    records.append(record_with_date)

    return records

def load_sla_violation_records():
    if not os.path.exists(SLA_VIOLATIONS_RECORDS_FILE):
        return {}
    with open(SLA_VIOLATIONS_RECORDS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# 示例调用
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # 测试数据
    report_data = [
        # 2024-11-19: 无超时记录
        {
            "_id": "3341236962944102",
            "sid": "814846055670172227",
            "saCreateTime": "2024-10-21T09:38:53+08:00",
            "orderNum": "GD20241000646",
            "province": "110000",
            "orgName": "北京博远恒泰装饰装修有限公司",
            "supervisorName": "马明超",
            "sourceType": 5,
            "status": 201,  #超时
            "msg": "超时",
            "memo": "超时详情",
            "workType": 1,
            "createTime": "2024-11-11T03:02:00.17+08:00"
        },
        # 其他服务商的正常记录
        {
            "_id": "5845381274122222",
            "sid": "1344991201244527380",
            "saCreateTime": "2024-10-16T09:57:30+08:00",
            "orderNum": "GD2024102682",
            "province": "110000",
            "orgName": "北京众德森建材有限责任公司",
            "supervisorName": "李四",
            "sourceType": 2,
            "status": 201, 
            "msg": "正常",
            "memo": "无超时",
            "workType": 1,
            "createTime": "2024-11-11T03:00:59.554+08:00"
        },
        # 其他服务商的正常记录
        {
            "_id": "5845381274122222",
            "sid": "1344991201244527380",
            "saCreateTime": "2024-10-16T09:57:30+08:00",
            "orderNum": "GD2024102682",
            "province": "110000",
            "orgName": "北京众德森建材有限责任公司",
            "supervisorName": "李四",
            "sourceType": 2,
            "status": 201, 
            "msg": "正常",
            "memo": "无超时",
            "workType": 1,
            "createTime": "2024-11-11T03:00:59.554+08:00"
        }
    ]

    # 更新超时记录
    update_sla_violation_records(report_data)

    # 发送日报通知
    monitor_sla_compliance_and_report(report_data)

    # 额外的测试数据，模拟一周内无超时情况
    # 这里可以手动修改 timeout_records.json 文件，确保过去一周没有超时记录
    # 例如，手动清空 timeout_records.json 文件或确保其中的记录为 []
