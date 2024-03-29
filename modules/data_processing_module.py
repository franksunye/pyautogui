# data_processing_module.py
import logging
from modules.log_config import setup_logging

# 设置日志
setup_logging()

def determine_rewards(contract_number, housekeeper_data):
    """
    根据合同序号和管家数据计算奖励类型和名称。
    参数：
    contract_number - 合同序号
    housekeeper_data - 管家相关数据，包括合同数量、总金额和已获得的奖励

    整体逻辑：
    1. 初始化奖励类型和名称列表
    2. 根据合同序号计算“幸运数字”奖励
    3. 如果管家合同数量满足条件，计算“节节高”奖励
    4. 根据管家合同数量和总金额计算下一级奖励所需的金额差
    5. 返回奖励类型、奖励名称和下一级奖励所需的金额差
    """
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
            if '优秀奖' in housekeeper_data['awarded'] and  amount < 100000 and  not set(["精英奖"]).intersection(housekeeper_data['awarded']):
                next_reward = "精英奖"
            elif '达标奖' in housekeeper_data['awarded'] and  amount < 60000 and  not set(["精英奖", "优秀奖"]).intersection(housekeeper_data['awarded']):
                next_reward = "优秀奖"
            elif '精英奖' in housekeeper_data['awarded'] and  amount < 60000 and  not set(["精英奖"]).intersection(housekeeper_data['awarded']):
                next_reward = "精英奖"

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
    """
    处理合同数据的主要函数。
    参数：
    contract_data - 待处理的合同数据列表，这是全量的合同数据
    existing_contract_ids - 本地获奖统计表中已存在的合同ID集合，用于检测重复合同，重复的合同不进行获奖统计
    housekeeper_award_lists - 本地获奖统计表彰管家获奖情况数据，用于奖励核对

    整体逻辑：
    1. 初始化获奖统计数据列表和合同计数器
    2. 遍历合同数据，对每个合同进行处理
    3. 检查合同ID是否已经经过获奖统计过，如果重复则跳过处理
    4. 根据合同序号和管家数据计算奖励
    5. 构建获奖统计数据记录并添加到获奖统计数据列表中
    6. 更新已存在的合同ID集合
    7. 返回处理后的性能数据列表
    """
    logging.info(f"Starting data processing with {len(existing_contract_ids)} existing contract IDs.")

    logging.debug(f"Existing contract IDs: {existing_contract_ids}")

    # 初始化性能数据列表
    performance_data = []
    # 初始化合同计数器，从已存在的合同ID数量开始
    contract_count_in_activity = len(existing_contract_ids) + 1
    # 初始化管家合同数据字典
    housekeeper_contracts = {}

    # 初始化已处理的合同ID集合
    processed_contract_ids = set()

    # 遍历合同数据
    logging.info("Starting to process contract data...")
    for contract in contract_data:
        # 获取合同ID并转换为字符串
        contract_id = str(contract['合同ID(_id)'])
        # 检查合同ID是否已处理过
        if contract_id in processed_contract_ids:
            logging.debug(f"Skipping duplicate contract ID: {contract_id}")
            continue
        logging.debug(f"Processing contract ID: {contract_id}")

        # 获取管家信息
        housekeeper = contract['管家(serviceHousekeeper)']
        # 如果管家信息不存在，则初始化管家数据
        if housekeeper not in housekeeper_contracts:
            housekeeper_award = []
            if housekeeper in housekeeper_award_lists:
                housekeeper_award = housekeeper_award_lists[housekeeper]
            housekeeper_contracts[housekeeper] = {'count': 0, 'total_amount': 0, 'awarded': housekeeper_award}

        # 更新管家合同数量和总金额
        housekeeper_contracts[housekeeper]['count'] += 1
        housekeeper_contracts[housekeeper]['total_amount'] += float(contract['合同金额(adjustRefundMoney)'])
        # 记录计算过程日志
        logging.debug(f"Housekeeper {housekeeper} count: {housekeeper_contracts[housekeeper]['count']}")
        logging.debug(f"Housekeeper {housekeeper} total amount: {housekeeper_contracts[housekeeper]['total_amount']}")

        # 添加合同ID到已处理集合
        processed_contract_ids.add(contract_id)

        # 计算奖励类型和名称
        reward_types, reward_names, next_reward_gap = determine_rewards(contract_count_in_activity, housekeeper_contracts[housekeeper])
        
        if contract_id in existing_contract_ids:
            # 如果合同ID已经存在于已处理的合同ID集合中，则跳过此合同的处理
            logging.debug(f"Skipping existing contract ID: {contract_id}")
            continue

        # Debug log for rewards calculation result
        logging.info(f"Reward types for contract {contract_id}: {reward_types}")
        logging.info(f"Reward names for contract {contract_id}: {reward_names}")

        active_status = 1 if reward_types else 0  # 激活状态基于是否有奖励类型

        # 构建性能数据记录
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
        # 添加性能数据记录到列表中
        performance_data.append(performance_entry)
        logging.info(f"Added performance entry for contract ID {contract_id}.")

        # 更新合同计数器
        contract_count_in_activity += 1

    # 返回处理后的性能数据列表
    return performance_data