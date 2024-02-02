# data_processing_module.py
import logging
from log_config import setup_logging

# 设置日志
setup_logging()

def determine_rewards(contract_number, housekeeper_data):
    reward_types = []
    reward_names = []
    next_reward_gap = ""  # 下一级奖励所需金额差

    # 幸运数字奖励逻辑
    if contract_number <= 10:
        reward_types.append("幸运数字")
        reward_names.append("开门红")
    elif '6' in str(contract_number % 10):
        reward_types.append("幸运数字")
        reward_names.append("接好运")

    # 节节高奖励逻辑（需要管家合同数量大于等于6）
    if housekeeper_data['count'] >= 6:
        amount = housekeeper_data['total_amount']
        next_reward = None
        if amount >= 100000 and '精英奖' not in housekeeper_data['awarded']:
            # 精英奖
            reward_types.append("节节高")
            reward_names.append("精英奖")
            housekeeper_data['awarded'].append('精英奖')
        elif amount >= 60000 and '优秀奖' not in housekeeper_data['awarded']:
            # 优秀奖
            next_reward = "精英奖"
            reward_types.append("节节高")
            reward_names.append("优秀奖")
            housekeeper_data['awarded'].append('优秀奖')
        elif amount >= 40000 and '达标奖' not in housekeeper_data['awarded']:
            # 达标奖
            next_reward = "优秀奖"
            reward_types.append("节节高")
            reward_names.append("达标奖")
            housekeeper_data['awarded'].append('达标奖')
        elif not set(["精英奖", "优秀奖", "达标奖"]).intersection(housekeeper_data['awarded']):
            next_reward = "达标奖"  # 如果没有获得任何奖项，则下一个奖项是达标奖
            
            
        # 自动发放所有低级别奖项（如果之前未获得）
        if '达标奖' not in housekeeper_data['awarded'] and amount >= 40000:
            reward_types.append("节节高")
            reward_names.append("达标奖")
            housekeeper_data['awarded'].append('达标奖')
        if '优秀奖' not in housekeeper_data['awarded'] and amount >= 60000:
            reward_types.append("节节高")
            reward_names.append("优秀奖")
            housekeeper_data['awarded'].append('优秀奖')

        if not next_reward:
            if '优秀奖' in housekeeper_data['awarded'] and  amount < 100000 and  not set(["精英奖", "达标奖"]).intersection(housekeeper_data['awarded']):
                next_reward = "精英奖"
            elif '达标奖' in housekeeper_data['awarded'] and  amount < 60000 and  not set(["精英奖", "优秀奖"]).intersection(housekeeper_data['awarded']):
                next_reward = "优秀奖"

        # 计算距离下一级奖励所需的金额差
        if next_reward:
            if next_reward == "达标奖":
                next_reward_gap = f"距离{next_reward}还需{40000 - amount}元"
            elif next_reward == "优秀奖":
                next_reward_gap = f"距离{next_reward}还需{60000 - amount}元"
            elif next_reward == "精英奖":
                next_reward_gap = f"距离{next_reward}还需{100000 - amount}元"
    else:
        if  not set(["精英奖", "优秀奖", "达标奖"]).intersection(housekeeper_data['awarded']):
            next_reward_gap = f"距离达成节节高奖励条件还需{6 -  housekeeper_data['count']}单"
        
    return ', '.join(reward_types), ', '.join(reward_names), next_reward_gap

def process_data(contract_data, existing_contract_ids, housekeeper_award_lists):

    logging.info(f"Starting data processing with {len(existing_contract_ids)} existing contract IDs.")

    logging.info(f"Existing contract IDs: {existing_contract_ids}")
    # Log individual elements of existing_contract_ids for debugging
    for id in existing_contract_ids:
        logging.info(f"Individual element in existing_contract_ids: {id}")

    performance_data = []
    contract_count_in_activity = len(existing_contract_ids) + 1
    housekeeper_contracts = {}

    for contract in contract_data:
        contract_id = str(contract['合同ID(_id)'])  # 明确转换为字符串
        logging.info(f"Processing contract ID: {contract_id}")

        housekeeper = contract['管家(serviceHousekeeper)']
        if housekeeper not in housekeeper_contracts:
            housekeeper_award=[]
            if housekeeper in housekeeper_award_lists:
                housekeeper_award=housekeeper_award_lists[housekeeper]
            housekeeper_contracts[housekeeper] = {'count': 0, 'total_amount': 0, 'awarded': housekeeper_award}

        housekeeper_contracts[housekeeper]['count'] += 1
        housekeeper_contracts[housekeeper]['total_amount'] += float(contract['合同金额(adjustRefundMoney)'])
        # Debug log for calculation process
        logging.info(f"Housekeeper {housekeeper} count: {housekeeper_contracts[housekeeper]['count']}")
        logging.info(f"Housekeeper {housekeeper} total amount: {housekeeper_contracts[housekeeper]['total_amount']}")

        reward_types, reward_names, next_reward_gap = determine_rewards(contract_count_in_activity, housekeeper_contracts[housekeeper])
        
        if contract_id in existing_contract_ids:
            logging.info(f"Skipping existing contract ID: {contract_id}")
            continue


        # Debug log for rewards calculation result
        logging.info(f"Reward types for contract {contract_id}: {reward_types}")
        logging.info(f"Reward names for contract {contract_id}: {reward_names}")

        active_status = 1 if reward_types else 0  # 激活状态基于是否有奖励类型

        # 构建返回数据记录
        performance_entry = {
            '活动编号': 'BJ-001',
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
            '管家累计金额': housekeeper_contracts[housekeeper]['total_amount'] ,
            '激活奖励状态': active_status,
            '奖励类型': reward_types,
            '奖励名称': reward_names,
            '是否发送通知': 'N',
            '下一级奖项所需金额差': next_reward_gap if next_reward_gap else '无',  # 添加下一级奖项所需金额差信息
        }

        # After processing a contract, add its ID to the existing_contract_ids set
        existing_contract_ids.add(contract_id)
        logging.info(f"Added contract ID {contract_id} to existing_contract_ids.")

        logging.info(f"Processing contract ID: {contract_id}, Rewards: {reward_types}")
        performance_data.append(performance_entry)
        contract_count_in_activity += 1

    return performance_data