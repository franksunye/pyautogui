# notification_module.py
"""
通知模块，负责发送各种通知。

该模块使用通知工具函数和模板函数来发送通知，支持多种通知渠道和模板。
"""

import logging
from modules.log_config import setup_logging
from modules.config import *
from modules.file_utils import get_all_records_from_csv, write_performance_data_to_csv
from task_manager import create_task
from modules.notification_utils import send_webhook_notification, get_campaign_config
from modules.notification_templates import format_technician_status_message
from modules.notification_templates import preprocess_amount, preprocess_rate

# 定义默认性能数据文件路径
PERFORMANCE_DATA_FILE = 'data/PerformanceData.csv'

# 配置日志
setup_logging()
# 使用专门的发送消息日志记录器
send_logger = logging.getLogger('sendLogger')

def generate_award_message(record, awards_mapping, city="BJ"):
    """
    生成奖励消息

    Args:
        record: 记录数据
        awards_mapping: 奖励金额映射
        city: 城市代码 ('BJ' 或 'SH')

    Returns:
        str: 格式化后的奖励消息
    """
    service_housekeeper = record["管家(serviceHousekeeper)"]
    contract_number = record["合同编号(contractdocNum)"]
    award_messages = []

    # 只有北京的精英管家才能获得奖励翻倍和显示徽章，上海的管家不参与奖励翻倍也不显示徽章
    if ENABLE_BADGE_MANAGEMENT and (service_housekeeper in ELITE_HOUSEKEEPER) and city == "BJ":
        # 如果是北京的精英管家，添加徽章
        service_housekeeper = f'{BADGE_NAME}{service_housekeeper}'

        # 获取奖励类型和名称列表
        reward_types = record["奖励类型"].split(', ') if record["奖励类型"] else []
        reward_names = record["奖励名称"].split(', ') if record["奖励名称"] else []

        # 创建奖励类型到奖励名称的映射
        reward_type_map = {}
        if len(reward_types) == len(reward_names):
            for i in range(len(reward_types)):
                if i < len(reward_names):
                    reward_type_map[reward_names[i]] = reward_types[i]

        for award in reward_names:
            if award in awards_mapping:
                award_info = awards_mapping[award]
                # 检查奖励类型，只有节节高奖励才翻倍
                reward_type = reward_type_map.get(award, "")

                if reward_type == "节节高":
                    # 节节高奖励翻倍
                    try:
                        award_info_double = str(int(award_info) * 2)
                        award_messages.append(f'达成 {award} 奖励条件，奖励金额 {award_info} 元，同时触发"精英连击双倍奖励"，奖励金额\U0001F680直升至 {award_info_double} 元！\U0001F9E7\U0001F9E7\U0001F9E7')
                    except ValueError:
                        award_messages.append(f'达成{award}奖励条件，获得签约奖励{award_info}元 \U0001F9E7\U0001F9E7\U0001F9E7')
                else:
                    # 幸运数字奖励不翻倍
                    award_messages.append(f'达成{award}奖励条件，获得签约奖励{award_info}元 \U0001F9E7\U0001F9E7\U0001F9E7')
    else:
        # 不启用徽章功能或非北京管家
        # 上海的管家不添加徽章，北京的普通管家也不添加徽章
        for award in record["奖励名称"].split(', '):
            if award in awards_mapping:
                award_info = awards_mapping[award]
                award_messages.append(f'达成{award}奖励条件，获得签约奖励{award_info}元 \U0001F9E7\U0001F9E7\U0001F9E7')

    return f'{service_housekeeper}签约合同{contract_number}\n\n' + '\n'.join(award_messages)

# 2025年5月，北京. 幸运数字6，单合同金额1万以上和以下幸运奖励不同；节节高三档；合同累计考虑工单合同金额10万封顶
def notify_awards_may_beijing(performance_data_filename=None):
    """通知奖励并更新性能数据文件"""
    if performance_data_filename is None:
        performance_data_filename = PERFORMANCE_DATA_FILE
    records = get_all_records_from_csv(performance_data_filename)
    updated = False

    # 获取活动配置
    campaign_id = 'BJ-2025-05'
    config = get_campaign_config(campaign_id)
    notification_config = config.get('notification', {})

    # 获取通知相关配置
    group_name = notification_config.get('group_name')
    contact_name = notification_config.get('contact_name')
    awards_mapping = notification_config.get('awards_mapping', {})
    for record in records:
        if record['是否发送通知'] == 'N':
            # 准备数据
            contract_id = record['合同ID(_id)']
            housekeeper = record["管家(serviceHousekeeper)"]
            contract_doc_num = record["合同编号(contractdocNum)"]
            accumulated_amount = record["管家累计金额"]
            conversion_rate = record.get("转化率(conversion)", "")

            # 添加是否启用徽章管理的判断，如果启用则在北京的精英管家名称前添加徽章名称
            service_housekeeper = housekeeper
            if ENABLE_BADGE_MANAGEMENT and housekeeper in ELITE_HOUSEKEEPER:
                service_housekeeper = f'{BADGE_NAME}{housekeeper}'

            # 准备附加信息
            processed_accumulated_amount = preprocess_amount(accumulated_amount)
            processed_enter_performance_amount = preprocess_amount(record.get("计入业绩金额", "0"))
            next_msg = '恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩 \U0001F389\U0001F389\U0001F389' if '无' in record.get("备注", "") else f'{record.get("备注", "")}'

            # 构建消息
            msg = f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8
恭喜 {service_housekeeper} 签约合同 {contract_doc_num} 并完成线上收款\U0001F389\U0001F389\U0001F389

\U0001F33B 本单为活动期间平台累计签约第 {record.get("活动期内第几个合同", "N/A")} 单，个人累计签约第 {record.get("管家累计单数", "N/A")} 单。

\U0001F33B {housekeeper}累计签约 {processed_accumulated_amount} 元{f', 累计计入业绩 {processed_enter_performance_amount} 元' if ENABLE_PERFORMANCE_AMOUNT_CAP_BJ else ''}

\U0001F44A {next_msg}。
'''
            # 发送主通知
            create_task('send_wecom_message', group_name, msg)

            # 如果有奖励，发送奖励通知
            if record.get('激活奖励状态', '0') == '1':
                jiangli_msg = generate_award_message(record, awards_mapping, "BJ")
                create_task('send_wechat_message', contact_name, jiangli_msg)

            # 更新状态
            record['是否发送通知'] = 'Y'
            updated = True

            # 确保合同ID至少有4个字符，否则使用完整ID
            contract_id_display = contract_id[-4:] if len(contract_id) >= 4 else contract_id
            logging.info(f"Notification sent for contract ID: {contract_id_display}")

    if updated:
        write_performance_data_to_csv(performance_data_filename, records, list(records[0].keys()))
        logging.info("PerformanceData.csv updated with notification status.")

# 2025年4月，北京. 幸运数字8，单合同金额1万以上和以下幸运奖励不同；节节高三档；合同累计考虑工单合同金额10万封顶
def notify_awards_apr_beijing(performance_data_filename=None):
    """通知奖励并更新性能数据文件"""
    if performance_data_filename is None:
        performance_data_filename = PERFORMANCE_DATA_FILE
    records = get_all_records_from_csv(performance_data_filename)
    updated = False

    # 获取活动配置
    campaign_id = 'BJ-2025-04'
    config = get_campaign_config(campaign_id)
    notification_config = config.get('notification', {})

    # 获取通知相关配置
    group_name = notification_config.get('group_name')
    contact_name = notification_config.get('contact_name')
    awards_mapping = notification_config.get('awards_mapping', {})
    for record in records:
        if record['是否发送通知'] == 'N':
            # 准备数据
            contract_id = record['合同ID(_id)']
            housekeeper = record["管家(serviceHousekeeper)"]
            contract_doc_num = record["合同编号(contractdocNum)"]
            accumulated_amount = record["管家累计金额"]

            # 添加是否启用徽章管理的判断，如果启用则在北京的精英管家名称前添加徽章名称
            service_housekeeper = housekeeper
            if ENABLE_BADGE_MANAGEMENT and housekeeper in ELITE_HOUSEKEEPER:
                service_housekeeper = f'{BADGE_NAME}{housekeeper}'

            # 准备附加信息
            processed_accumulated_amount = preprocess_amount(accumulated_amount)
            processed_enter_performance_amount = preprocess_amount(record.get("计入业绩金额", "0"))
            next_msg = '恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩 \U0001F389\U0001F389\U0001F389' if '无' in record.get("备注", "") else f'{record.get("备注", "")}'

            # 构建消息
            msg = f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8
恭喜 {service_housekeeper} 签约合同 {contract_doc_num} 并完成线上收款\U0001F389\U0001F389\U0001F389

\U0001F33B 本单为活动期间平台累计签约第 {record.get("活动期内第几个合同", "N/A")} 单，个人累计签约第 {record.get("管家累计单数", "N/A")} 单。

\U0001F33B {housekeeper}累计签约 {processed_accumulated_amount} 元{f', 累计计入业绩 {processed_enter_performance_amount} 元' if ENABLE_PERFORMANCE_AMOUNT_CAP_BJ else ''}

\U0001F44A {next_msg}。
'''
            # 发送主通知
            create_task('send_wecom_message', group_name, msg)

            # 如果有奖励，发送奖励通知
            if record.get('激活奖励状态', '0') == '1':
                jiangli_msg = generate_award_message(record, awards_mapping, "BJ")
                create_task('send_wechat_message', contact_name, jiangli_msg)

            # 更新状态
            record['是否发送通知'] = 'Y'
            updated = True

            # 确保合同ID至少有4个字符，否则使用完整ID
            contract_id_display = contract_id[-4:] if len(contract_id) >= 4 else contract_id
            logging.info(f"Notification sent for contract ID: {contract_id_display}")

    if updated:
        write_performance_data_to_csv(performance_data_filename, records, list(records[0].keys()))
        logging.info("PerformanceData.csv updated with notification status.")

def notify_awards_shanghai_generate_message_march(performance_data_filename, status_filename=None, contract_data=None):
    """
    通知奖励并更新性能数据文件，同时跟踪发送状态

    Args:
        performance_data_filename: 性能数据文件路径
        status_filename: 状态文件名（可选，用于兼容旧接口）
        contract_data: 合同数据（可选，用于兼容旧接口）
    """
    records = get_all_records_from_csv(performance_data_filename)
    updated = False

    # 获取活动配置
    campaign_id = 'SH-2025-04'
    config = get_campaign_config(campaign_id)
    notification_config = config.get('notification', {})

    # 获取通知相关配置
    group_name = notification_config.get('group_name')
    contact_name = notification_config.get('contact_name')
    awards_mapping = notification_config.get('awards_mapping', {})
    for record in records:
        if record['是否发送通知'] == 'N':
            # 准备数据
            contract_id = record['合同ID(_id)']
            housekeeper = record["管家(serviceHousekeeper)"]
            contract_doc_num = record["合同编号(contractdocNum)"]
            accumulated_amount = record["管家累计金额"]
            conversion_rate = record.get("转化率(conversion)", "")

            # 确保合同ID至少有4个字符，否则使用完整ID
            contract_id_display = contract_id[-4:] if len(contract_id) >= 4 else contract_id
            logging.info(f"Processing contract ID: {contract_id_display}")

            # 准备附加信息
            processed_accumulated_amount = preprocess_amount(accumulated_amount)
            processed_conversion_rate = preprocess_rate(conversion_rate)
            next_msg = '恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩 \U0001F389\U0001F389\U0001F389' if '无' in record.get("备注", "") else f'{record.get("备注", "")}'

            # 构建消息
            msg = f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8

恭喜 {housekeeper} 签约合同 {contract_doc_num} 并完成线上收款\U0001F389\U0001F389\U0001F389

\U0001F33B 本单为本月平台累计签约第 {record.get("活动期内第几个合同", "N/A")} 单，

\U0001F33B 个人累计签约第 {record.get("管家累计单数", "N/A")} 单，

\U0001F33B 个人累计签约 {processed_accumulated_amount} 元，

\U0001F33B 个人转化率 {processed_conversion_rate}，

\U0001F44A {next_msg}。
'''
            # 发送主通知
            create_task('send_wecom_message', group_name, msg)

            # 如果有奖励，发送奖励通知
            if record.get('激活奖励状态', '0') == '1':
                jiangli_msg = generate_award_message(record, awards_mapping, "SH")
                create_task('send_wechat_message', contact_name, jiangli_msg)


            # 更新状态
            record['是否发送通知'] = 'Y'
            updated = True
            logging.info(f"Notification sent for contract ID: {contract_id_display}")

    if updated:
        write_performance_data_to_csv(performance_data_filename, records, list(records[0].keys()))
        logging.info("PerformanceData.csv updated with notification status.")

def notify_awards_may_shanghai(performance_data_filename=None):
    """通知奖励并更新性能数据文件"""
    if performance_data_filename is None:
        performance_data_filename = PERFORMANCE_DATA_FILE
    records = get_all_records_from_csv(performance_data_filename)
    updated = False

    # 获取活动配置
    campaign_id = 'SH-2025-05'
    config = get_campaign_config(campaign_id)
    notification_config = config.get('notification', {})

    # 获取通知相关配置
    group_name = notification_config.get('group_name')
    contact_name = notification_config.get('contact_name')
    awards_mapping = notification_config.get('awards_mapping', {})
    for record in records:
        if record['是否发送通知'] == 'N':
            # 准备数据
            contract_id = record['合同ID(_id)']
            housekeeper = record["管家(serviceHousekeeper)"]
            contract_doc_num = record["合同编号(contractdocNum)"]
            accumulated_amount = record["管家累计金额"]
            conversion_rate = record.get("转化率(conversion)", "")

            # 确保合同ID至少有4个字符，否则使用完整ID
            contract_id_display = contract_id[-4:] if len(contract_id) >= 4 else contract_id
            logging.info(f"Processing contract ID: {contract_id_display}")

            # 准备附加信息
            processed_accumulated_amount = preprocess_amount(accumulated_amount)
            processed_conversion_rate = preprocess_rate(conversion_rate)
            next_msg = '恭喜已经达成所有奖励，祝愿再接再厉，再创佳绩 \U0001F389\U0001F389\U0001F389' if '无' in record.get("备注", "") else f'{record.get("备注", "")}'

            # 构建消息
            msg = f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8
恭喜 {housekeeper} 签约合同 {contract_doc_num} 并完成线上收款\U0001F389\U0001F389\U0001F389

\U0001F33B 本单为本月平台累计签约第 {record.get("活动期内第几个合同", "N/A")} 单，个人累计签约第 {record.get("管家累计单数", "N/A")} 单，

\U0001F33B {housekeeper}累计签约 {processed_accumulated_amount} 元，

\U0001F33B 转化率 {processed_conversion_rate}。

\U0001F44A {next_msg}。
'''
            # 发送主通知
            create_task('send_wecom_message', group_name, msg)

            # 如果有奖励，发送奖励通知
            if record.get('激活奖励状态', '0') == '1':
                jiangli_msg = generate_award_message(record, awards_mapping, "SH")
                create_task('send_wechat_message', contact_name, jiangli_msg)



            # 更新状态
            record['是否发送通知'] = 'Y'
            updated = True
            logging.info(f"Notification sent for contract ID: {contract_id_display}")

    if updated:
        write_performance_data_to_csv(performance_data_filename, records, list(records[0].keys()))
        logging.info("PerformanceData.csv updated with notification status.")

def notify_technician_status_changes(status_changes, status_filename=None):
    """
    通知技师的状态变更信息。

    Args:
        status_changes: 状态变更数组
        status_filename: 状态文件名（可选，用于兼容旧接口）
    """
    for change in status_changes:
        change_id = change[0]
        change_time = change[1]
        technician_name = change[2]
        company_name = change[3]
        update_content = change[5]

        # 提取状态（上线或下线）
        status = update_content[0] if update_content else ""

        # 使用模板函数格式化消息
        message = format_technician_status_message(
            technician_name=technician_name,
            status_time=change_time,
            status=status,
            status_content=update_content
        )

        # 发送微信消息
        create_task('send_wechat_message', company_name, message)

        # 发送Webhook消息
        send_webhook_notification(message)

        logging.info(f"Notification sent for technician status change: {change_id}")

# 使用新的工具函数替代原来的函数
def post_text_to_webhook(message, webhook_url=WEBHOOK_URL_DEFAULT):
    """
    发送文本消息到Webhook

    Args:
        message: 消息内容
        webhook_url: Webhook URL

    Returns:
        bool: 是否成功发送
    """
    return send_webhook_notification(message, webhook_url)