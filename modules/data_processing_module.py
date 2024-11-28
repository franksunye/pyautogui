# data_processing_module.py
import logging
from modules.log_config import setup_logging
from datetime import date

# 设置日志
setup_logging()

# 2024年11月，北京. 幸运数字6，单合同金额1万以上和以下幸运奖励不同；节节高三档；合同累计考虑工单合同金额5万封顶
def determine_rewards_nov_beijing(contract_number, housekeeper_data, current_contract_amount):

    reward_types = []
    reward_names = []
    next_reward_gap = ""  # 下一级奖励所需金额差

    # 幸运数字奖励逻辑
    if '6' in str(contract_number % 10):
        reward_types.append("幸运数字")
        if current_contract_amount >= 10000:
            reward_names.append("接好运万元以上")
        else:
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
        if '精英奖' not in housekeeper_data['awarded'] and amount >= 100000:
            reward_types.append("节节高")
            reward_names.append("精英奖")
            housekeeper_data['awarded'].append('精英奖')            
            
        if not next_reward:
            if '优秀奖' in housekeeper_data['awarded'] and  amount < 100000 and  not set(["精英奖"]).intersection(housekeeper_data['awarded']):
                next_reward = "精英奖"
            elif '达标奖' in housekeeper_data['awarded'] and  amount < 60000 and  not set(["精英奖", "优秀奖"]).intersection(housekeeper_data['awarded']):
                next_reward = "优秀奖"

        # 计算距离下一级奖励所需的金额差
        if next_reward:
            if next_reward == "达标奖":
                next_reward_gap = f"距离 {next_reward} 还需 {40000 - amount:,} 元"
            elif next_reward == "优秀奖":
                next_reward_gap = f"距离 {next_reward} 还需 {60000 - amount:,} 元"
            elif next_reward == "精英奖":
                next_reward_gap = f"距离 {next_reward} 还需 {100000 - amount:,} 元"
                
    else:
        if  not set(["精英奖", "优秀奖", "达标奖"]).intersection(housekeeper_data['awarded']):
            next_reward_gap = f"距离达成节节高奖励条件还需 {6 -  housekeeper_data['count']} 单"
        
    return ', '.join(reward_types), ', '.join(reward_names), next_reward_gap

# 2024年11月，北京. 幸运数字6，单合同金额1万以上和以下幸运奖励不同；节节高三档；合同累计考虑工单合同金额5万封顶
def process_data_nov_beijing(contract_data, existing_contract_ids, housekeeper_award_lists):

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

    # 初始化工单编号累计金额字典
    service_appointment_amounts = {}

    # 遍历合同数据
    logging.info("Starting to process contract data...")
    for contract in contract_data:
        # 获取合同ID并转换为字符串
        contract_id = str(contract['合同ID(_id)'])
        # 检查合同ID是否已处理过，如果已经处理过，则跳过当前循环的剩余部分，进入下一次循环
        if contract_id in processed_contract_ids:
            logging.debug(f"Skipping duplicate contract ID: {contract_id}")
            continue
        
        # 如果是未处理过的合同，则开始本地台账的登记工作
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
        current_contract_amount = float(contract['合同金额(adjustRefundMoney)'])  
        
        # --- 新增逻辑开始：根据不同类型(sourceType)的项目，设置不同的累计合同金额上限

        # 获取工单编号(serviceAppointmentNum)
        service_appointment_num = contract['工单编号(serviceAppointmentNum)']

        # 初始化工单编号累计金额
        if service_appointment_num not in service_appointment_amounts:
            service_appointment_amounts[service_appointment_num] = 0

        # 获取当前工单编号的累计金额
        current_total_amount = service_appointment_amounts[service_appointment_num]

        # 获取类型(sourceType)字段的值
        # source_type = int(contract['类型(sourceType)'])

        # 根据sourceType确定累计金额的上限
        # if source_type in [2, 4, 5]:
        #     max_limit = 50000
        # elif source_type == 1:
        #     max_limit = 50000
        # else:
        #     max_limit = float('inf')  # 如果不是以上类型，不限制累计金额

        max_limit = 50000

        # 计算当前合同应计入的金额
        if current_total_amount < max_limit:
            remaining_quota = max_limit - current_total_amount
            amount_to_add = min(current_contract_amount, remaining_quota)
        else:
            amount_to_add = 0

        # 更新工单编号的累计金额
        service_appointment_amounts[service_appointment_num] += current_contract_amount

        # 更新管家合同总金额，保持为浮点数
        housekeeper_contracts[housekeeper]['total_amount'] += amount_to_add  # 保持为浮点数，不转换为整数

        # --- 新增逻辑结束：根据不同类型(sourceType)的项目，设置不同的累计合同金额上限。

        # 记录计算过程日志
        logging.debug(f"Housekeeper {housekeeper} count: {housekeeper_contracts[housekeeper]['count']}")
        logging.debug(f"Housekeeper {housekeeper} total amount: {housekeeper_contracts[housekeeper]['total_amount']}")

        # 添加合同ID到已处理集合
        processed_contract_ids.add(contract_id)

        # 计算奖励类型和名称
        reward_types, reward_names, next_reward_gap = determine_rewards_nov_beijing(contract_count_in_activity, housekeeper_contracts[housekeeper], current_contract_amount)
        
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
            # '类型(sourceType)': contract['类型(sourceType)'],
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
            '备注': next_reward_gap if next_reward_gap else '无',  # 添加下一级奖项所需金额差信息
            '登记时间': date.today().strftime("%Y-%m-%d"),  # 新增字段
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

def determine_rewards_june_shanghai(contract_number, housekeeper_data):
    reward_types = []
    reward_names = []
    next_reward_gap = ""  # 下一级奖励所需金额差

    # 节节高奖励逻辑（需要管家合同数量大于等于3）
    if housekeeper_data['count'] >= 3:
        amount = housekeeper_data['total_amount']
        next_reward = None
        if amount >= 160000 and '卓越奖' not in housekeeper_data['awarded']:
            # 卓越奖
            reward_types.append("节节高")
            reward_names.append("卓越奖")
            housekeeper_data['awarded'].append('卓越奖')
        elif amount >= 120000 and '精英奖' not in housekeeper_data['awarded']:
            # 精英奖
            next_reward = "卓越奖"
            reward_types.append("节节高")
            reward_names.append("精英奖")
            housekeeper_data['awarded'].append('精英奖')
        elif amount >= 80000 and '优秀奖' not in housekeeper_data['awarded']:
            # 优秀奖
            next_reward = "精英奖"
            reward_types.append("节节高")
            reward_names.append("优秀奖")
            housekeeper_data['awarded'].append('优秀奖')
        elif amount >= 60000 and '达标奖' not in housekeeper_data['awarded']:
            # 达标奖
            next_reward = "优秀奖"
            reward_types.append("节节高")
            reward_names.append("达标奖")
            housekeeper_data['awarded'].append('达标奖')
        elif amount >= 40000 and '基础奖' not in housekeeper_data['awarded']:
            # 达标奖
            next_reward = "达标奖"
            reward_types.append("节节高")
            reward_names.append("基础奖")
            housekeeper_data['awarded'].append('基础奖')            
        elif not set(["精英奖", "优秀奖", "达标奖", "基础奖"]).intersection(housekeeper_data['awarded']):
            next_reward = "基础奖"  # 如果没有获得任何奖项，则下一个奖项是基础奖
            
        # 自动发放所有低级别奖项（如果之前未获得）
        if '基础奖' not in housekeeper_data['awarded'] and amount >= 40000:
            reward_types.append("节节高")
            reward_names.append("基础奖")
            housekeeper_data['awarded'].append('基础奖')
        if '达标奖' not in housekeeper_data['awarded'] and amount >= 60000:
            reward_types.append("节节高")
            reward_names.append("达标奖")
            housekeeper_data['awarded'].append('达标奖')
        if '优秀奖' not in housekeeper_data['awarded'] and amount >= 80000:
            reward_types.append("节节高")
            reward_names.append("优秀奖")
            housekeeper_data['awarded'].append('优秀奖')
        if '精英奖' not in housekeeper_data['awarded'] and amount >= 120000:
            reward_types.append("节节高")
            reward_names.append("精英奖")
            housekeeper_data['awarded'].append('精英奖')            
            
        if not next_reward:
            if '精英奖' in housekeeper_data['awarded'] and  amount < 160000 and  not set(["卓越奖"]).intersection(housekeeper_data['awarded']):
                next_reward = "卓越奖"
            elif '优秀奖' in housekeeper_data['awarded'] and  amount < 120000 and  not set(["卓越奖", "精英奖"]).intersection(housekeeper_data['awarded']):
                next_reward = "精英奖"
            elif '达标奖' in housekeeper_data['awarded'] and  amount < 80000 and  not set(["卓越奖", "精英奖", "优秀奖"]).intersection(housekeeper_data['awarded']):
                next_reward = "优秀奖"
            elif '基础奖' in housekeeper_data['awarded'] and  amount < 60000 and  not set(["卓越奖", "精英奖", "优秀奖", "达标奖"]).intersection(housekeeper_data['awarded']):
                next_reward = "达标奖"

        # 计算距离下一级奖励所需的金额差
        if next_reward:
            if next_reward == "基础奖":
                next_reward_gap = f"距离 {next_reward} 还需 {40000 - amount:,} 元"
            elif next_reward == "达标奖":
                next_reward_gap = f"距离 {next_reward} 还需 {60000 - amount:,} 元"
            elif next_reward == "优秀奖":
                next_reward_gap = f"距离 {next_reward} 还需 {80000 - amount:,} 元"
            elif next_reward == "精英奖":
                next_reward_gap = f"距离 {next_reward} 还需 {120000 - amount:,} 元"
            elif next_reward == "卓越奖":
                next_reward_gap = f"距离 {next_reward} 还需 {160000 - amount:,} 元"                
    else:
        if  not set(["卓越奖", "精英奖", "优秀奖", "达标奖"]).intersection(housekeeper_data['awarded']):
            next_reward_gap = f"距离达成节节高奖励条件还需 {3 -  housekeeper_data['count']} 单"
        
    return ', '.join(reward_types), ', '.join(reward_names), next_reward_gap

def process_data_july_shanghai(contract_data, existing_contract_ids, housekeeper_award_lists):

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
            housekeeper_award = []
            if unique_housekeeper_key in housekeeper_award_lists:
                housekeeper_award = housekeeper_award_lists[unique_housekeeper_key]
            housekeeper_contracts[unique_housekeeper_key] = {'count': 0, 'total_amount': 0, 'awarded': housekeeper_award}

        housekeeper_contracts[unique_housekeeper_key]['count'] += 1
        housekeeper_contracts[unique_housekeeper_key]['total_amount'] += float(contract['合同金额(adjustRefundMoney)'])

        housekeeper_contracts[unique_housekeeper_key]['total_amount'] = int(housekeeper_contracts[unique_housekeeper_key]['total_amount'])

        logging.debug(f"Housekeeper {unique_housekeeper_key} count: {housekeeper_contracts[unique_housekeeper_key]['count']}")
        logging.debug(f"Housekeeper {unique_housekeeper_key} total amount: {housekeeper_contracts[unique_housekeeper_key]['total_amount']}")

        processed_contract_ids.add(contract_id)

        reward_types, reward_names, next_reward_gap = determine_rewards_june_shanghai(contract_count_in_activity, housekeeper_contracts[unique_housekeeper_key])

        if contract_id in existing_contract_ids:
            logging.debug(f"Skipping existing contract ID: {contract_id}")
            continue

        active_status = 1 if reward_types else 0  # 激活状态基于是否有奖励类型

        performance_entry = {
            '活动编号': 'BJ-002',
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
            '转化率(conversion)': contract['转化率(conversion)'], # 新增字段
            '平均客单价(average)': contract['平均客单价(average)'], # 新增字段            
            '活动期内第几个合同': contract_count_in_activity,
            '管家累计单数': housekeeper_contracts[unique_housekeeper_key]['count'],
            '管家累计金额': housekeeper_contracts[unique_housekeeper_key]['total_amount'],
            '奖金池': float(contract['合同金额(adjustRefundMoney)']) * 0.002, # 新增字段，计算奖金池           
            '激活奖励状态': active_status,
            '奖励类型': reward_types,
            '奖励名称': reward_names,
            '是否发送通知': 'N',
            '备注': next_reward_gap if next_reward_gap else '无',  # 添加下一级奖项所需金额差信息
            '登记时间': date.today().strftime("%Y-%m-%d"),  # 新增字段
        }

        existing_contract_ids.add(contract_id)
        logging.info(f"Added contract ID {contract_id} to existing_contract_ids.")
        logging.info(f"Processing contract ID: {contract_id}, Rewards: {reward_types}")
        performance_data.append(performance_entry)
        logging.info(f"Added performance entry for contract ID {contract_id}.")

        contract_count_in_activity += 1

    return performance_data