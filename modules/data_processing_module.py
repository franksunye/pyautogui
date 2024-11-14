# data_processing_module.py
import logging
from modules.log_config import setup_logging
from datetime import date

# 设置日志
setup_logging()

# 奖励配置
Beijing_Reward_Config = {
    'nov_beijing': {
        'lucky_number': '6',
        'reward_thresholds': [100000, 60000, 40000],
        'reward_names': ['精英奖', '优秀奖', '达标奖'],
        'contract_limit': 50000,
        'min_contracts': 6
    },
    'oct_beijing': {
        'lucky_number': '8',
        'reward_thresholds': [160000, 80000, 40000],
        'reward_names': ['精英奖', '优秀奖', '达标奖'],
        'contract_limit': 50000,
        'min_contracts': 6
    },
    # Add other configurations as needed
}

def determine_rewards_beijing(contract_number, housekeeper_data, current_contract_amount, config):
    reward_types = []
    reward_names = []
    next_reward_gap = ""

    # 幸运数字奖励逻辑
    if config['lucky_number'] in str(contract_number % 10):
        reward_types.append("幸运数字")
        if current_contract_amount >= 10000:
            reward_names.append("接好运万元以上")
        else:
            reward_names.append("接好运")

    # 节节高奖励逻辑
    if housekeeper_data['count'] >= config['min_contracts']:
        amount = housekeeper_data['total_amount']
        next_reward = None
        for i, threshold in enumerate(config['reward_thresholds']):
            if amount >= threshold and config['reward_names'][i] not in housekeeper_data['awarded']:
                reward_types.append("节节高")
                reward_names.append(config['reward_names'][i])
                housekeeper_data['awarded'].append(config['reward_names'][i])
            elif not next_reward:
                next_reward = config['reward_names'][i]

        if next_reward:
            next_reward_gap = f"距离 {next_reward} 还需 {threshold - amount:,} 元"
    else:
        if not set(config['reward_names']).intersection(housekeeper_data['awarded']):
            next_reward_gap = f"距离达成节节高奖励条件还需 {config['min_contracts'] - housekeeper_data['count']} 单"

    return ', '.join(reward_types), ', '.join(reward_names), next_reward_gap

def process_data_beijing(contract_data, existing_contract_ids, housekeeper_award_lists, config_key):
    config = Beijing_Reward_Config[config_key] # 获取北京活动的奖励配置
    logging.info(f"Starting data processing with {len(existing_contract_ids)} existing contract IDs.")
    logging.debug(f"Existing contract IDs: {existing_contract_ids}")

    performance_data = []
    contract_count_in_activity = len(existing_contract_ids) + 1
    housekeeper_contracts = {}
    processed_contract_ids = set()
    service_appointment_amounts = {}

    logging.info("Starting to process contract data...")
    for contract in contract_data:
        contract_id = str(contract['合同ID(_id)'])
        if contract_id in processed_contract_ids:
            logging.debug(f"Skipping duplicate contract ID: {contract_id}")
            continue

        logging.debug(f"Processing contract ID: {contract_id}")
        housekeeper = contract['管家(serviceHousekeeper)']
        if housekeeper not in housekeeper_contracts:
            housekeeper_award = housekeeper_award_lists.get(housekeeper, [])
            housekeeper_contracts[housekeeper] = {'count': 0, 'total_amount': 0, 'awarded': housekeeper_award}

        housekeeper_contracts[housekeeper]['count'] += 1
        current_contract_amount = float(contract['合同金额(adjustRefundMoney)'])

        service_appointment_num = contract['工单编号(serviceAppointmentNum)']
        if service_appointment_num not in service_appointment_amounts:
            service_appointment_amounts[service_appointment_num] = 0

        current_total_amount = service_appointment_amounts[service_appointment_num]
        max_limit = config['contract_limit']
        if current_total_amount < max_limit:
            remaining_quota = max_limit - current_total_amount
            amount_to_add = min(current_contract_amount, remaining_quota)
        else:
            amount_to_add = 0

        service_appointment_amounts[service_appointment_num] += current_contract_amount
        housekeeper_contracts[housekeeper]['total_amount'] += amount_to_add

        logging.debug(f"Housekeeper {housekeeper} count: {housekeeper_contracts[housekeeper]['count']}")
        logging.debug(f"Housekeeper {housekeeper} total amount: {housekeeper_contracts[housekeeper]['total_amount']}")

        processed_contract_ids.add(contract_id)

        reward_types, reward_names, next_reward_gap = determine_rewards_beijing(contract_count_in_activity, housekeeper_contracts[housekeeper], current_contract_amount, config)

        if contract_id in existing_contract_ids:
            logging.debug(f"Skipping existing contract ID: {contract_id}")
            continue

        active_status = 1 if reward_types else 0

        performance_entry = {
            '活动编号': 'BJ-08',
            '合同ID(_id)': contract_id,
            '活动城市(province)': contract['活动城市(province)'],
            '工单编号(serviceAppointmentNum)': contract['工单编号(serviceAppointmentNum)'],
            'Status': contract['Status'],
            '管家(serviceHousekeeper)': housekeeper,
            '合同编号(contractdocNum)': contract['合同编号(contractdocNum)'],
            '合同金额(adjustRefundMoney)': contract['合同金额(adjustRefundMoney)'],
            '支付金额(paidAmount)': contract['支付金额(paidAmount)'],
            '差额(difference)': contract['差额(difference)'],
            'State': contract['State'],
            '创建时间(createTime)': contract['创建时间(createTime)'],
            '服务商(orgName)': contract['服务商(orgName)'],
            '签约时间(signedDate)': contract['签约时间(signedDate)'],
            'Doorsill': contract['Doorsill'],
            '款项来源类型(tradeIn)': contract['款项来源类型(tradeIn)'],
            '活动期内第几个合同': contract_count_in_activity,
            '管家累计单数': housekeeper_contracts[housekeeper]['count'],
            '管家累计金额': housekeeper_contracts[housekeeper]['total_amount'],
            '激活奖励状态': active_status,
            '奖励类型': reward_types,
            '奖励名称': reward_names,
            '是否发送通知': 'N',
            '备注': next_reward_gap if next_reward_gap else '无',
            '登记时间': date.today().strftime("%Y-%m-%d"),
        }

        existing_contract_ids.add(contract_id)
        logging.info(f"Added contract ID {contract_id} to existing_contract_ids.")
        logging.info(f"Processing contract ID: {contract_id}, Rewards: {reward_types}")
        performance_data.append(performance_entry)
        logging.info(f"Added performance entry for contract ID {contract_id}.")

        contract_count_in_activity += 1

    return performance_data

# ... existing code ...

# 奖励配置
Shanghai_Reward_Config = {
    'june_shanghai': {
        'reward_thresholds': [160000, 120000, 80000, 60000, 40000],
        'reward_names': ['卓越奖', '精英奖', '优秀奖', '达标奖', '基础奖'],
        'min_contracts': 3
    },
    # Add other configurations as needed
}

def determine_rewards_shanghai(contract_number, housekeeper_data, config):
    reward_types = []
    reward_names = []
    next_reward_gap = ""

    # 判断是否达到最小合同数量
    if housekeeper_data['count'] >= config['min_contracts']:
        amount = housekeeper_data['total_amount']
        
        for i, threshold in enumerate(config['reward_thresholds']):
            reward_name = config['reward_names'][i]
            # 如果达到该奖励的金额且该奖励未获得
            if amount >= threshold and reward_name not in housekeeper_data['awarded']:
                reward_types.append("节节高")
                reward_names.append(reward_name)
                housekeeper_data['awarded'].append(reward_name)
            # 计算第一个不达成的奖励差距
            elif amount < threshold:
                next_reward_gap = f"距离 {reward_name} 还需 {threshold - amount:,} 元"
                break  # 一旦找到第一个不达成条件的奖励后，立即退出循环

    else:
        # 合同数不达标时计算差距
        if not set(config['reward_names']).intersection(housekeeper_data['awarded']):
            next_reward_gap = f"距离达成节节高奖励条件还需 {config['min_contracts'] - housekeeper_data['count']} 单"

    return ', '.join(reward_types), ', '.join(reward_names), next_reward_gap

def process_data_shanghai(contract_data, existing_contract_ids, housekeeper_award_lists, config_key):
    config = Shanghai_Reward_Config[config_key]
    logging.info(f"Starting data processing with {len(existing_contract_ids)} existing contract IDs.")
    logging.debug(f"Existing contract IDs: {existing_contract_ids}")

    performance_data = []
    contract_count_in_activity = len(existing_contract_ids) + 1
    housekeeper_contracts = {}
    processed_contract_ids = set()

    logging.info("Starting to process contract data...")
    for contract in contract_data:
        contract_id = str(contract['合同ID(_id)'])
        if contract_id in processed_contract_ids:
            logging.debug(f"Skipping duplicate contract ID: {contract_id}")
            continue

        logging.debug(f"Processing contract ID: {contract_id}")
        housekeeper = contract['管家(serviceHousekeeper)']
        service_provider = contract['服务商(orgName)']
        unique_housekeeper_key = f"{housekeeper}_{service_provider}"

        if unique_housekeeper_key not in housekeeper_contracts:
            housekeeper_award = housekeeper_award_lists.get(unique_housekeeper_key, [])
            housekeeper_contracts[unique_housekeeper_key] = {'count': 0, 'total_amount': 0, 'awarded': housekeeper_award}

        housekeeper_contracts[unique_housekeeper_key]['count'] += 1
        housekeeper_contracts[unique_housekeeper_key]['total_amount'] += float(contract['合同金额(adjustRefundMoney)'])

        logging.debug(f"Housekeeper {unique_housekeeper_key} count: {housekeeper_contracts[unique_housekeeper_key]['count']}")
        logging.debug(f"Housekeeper {unique_housekeeper_key} total amount: {housekeeper_contracts[unique_housekeeper_key]['total_amount']}")

        processed_contract_ids.add(contract_id)

        reward_types, reward_names, next_reward_gap = determine_rewards_shanghai(contract_count_in_activity, housekeeper_contracts[unique_housekeeper_key], config)

        if contract_id in existing_contract_ids:
            logging.debug(f"Skipping existing contract ID: {contract_id}")
            continue

        active_status = 1 if reward_types else 0

        performance_entry = {
            '活动编号': 'SH-001',
            '合同ID(_id)': contract_id,
            '活动城市(province)': contract['活动城市(province)'],
            '工单编号(serviceAppointmentNum)': contract['工单编号(serviceAppointmentNum)'],
            'Status': contract['Status'],
            '管家(serviceHousekeeper)': housekeeper,
            '合同编号(contractdocNum)': contract['合同编号(contractdocNum)'],
            '合同金额(adjustRefundMoney)': contract['合同金额(adjustRefundMoney)'],
            '支付金额(paidAmount)': contract['支付金额(paidAmount)'],
            '差额(difference)': contract['差额(difference)'],
            'State': contract['State'],
            '创建时间(createTime)': contract['创建时间(createTime)'],
            '服务商(orgName)': service_provider,
            '签约时间(signedDate)': contract['签约时间(signedDate)'],
            'Doorsill': contract['Doorsill'],
            '款项来源类型(tradeIn)': contract['款项来源类型(tradeIn)'],
            '转化率(conversion)': contract.get('转化率(conversion)', ''),
            '平均客单价(average)': contract.get('平均客单价(average)', ''),
            '活动期内第几个合同': contract_count_in_activity,
            '管家累计单数': housekeeper_contracts[unique_housekeeper_key]['count'],
            '管家累计金额': housekeeper_contracts[unique_housekeeper_key]['total_amount'],
            '奖金池': float(contract['合同金额(adjustRefundMoney)']) * 0.002,
            '激活奖励状态': active_status,
            '奖励类型': reward_types,
            '奖励名称': reward_names,
            '是否发送通知': 'N',
            '备注': next_reward_gap if next_reward_gap else '无',
            '登记时间': date.today().strftime("%Y-%m-%d"),
        }

        existing_contract_ids.add(contract_id)
        logging.info(f"Added contract ID {contract_id} to existing_contract_ids.")
        logging.info(f"Processing contract ID: {contract_id}, Rewards: {reward_types}")
        performance_data.append(performance_entry)
        logging.info(f"Added performance entry for contract ID {contract_id}.")

        contract_count_in_activity += 1

    return performance_data