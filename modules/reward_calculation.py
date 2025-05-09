"""
奖励计算模块

该模块包含所有与奖励计算相关的函数，用于确定合同的奖励类型和名称。
这些函数可以被文件处理模块和数据库处理模块共同使用，确保奖励计算逻辑的一致性。
"""

import logging
from modules import config

def determine_rewards_generic(
    contract_number,
    housekeeper_data,
    current_contract_amount,
    config_key
):
    """
    通用奖励确定函数，基于配置确定奖励类型和名称。

    Args:
        contract_number: 合同编号
        housekeeper_data: 管家数据，包含count、total_amount和awarded等信息
        current_contract_amount: 当前合同金额
        config_key: 配置键名，用于从REWARD_CONFIGS中获取对应配置

    Returns:
        tuple: (reward_types_str, reward_names_str, next_reward_gap)
    """
    # 输入验证
    if contract_number < 0:
        raise ValueError("合同编号不能为负数")
    if housekeeper_data.get('count', 0) < 0:
        raise ValueError("管家合同数量不能为负数")
    if current_contract_amount < 0:
        raise ValueError("合同金额不能为负数")

    # 获取配置
    if config_key not in config.REWARD_CONFIGS:
        logging.error(f"配置键 {config_key} 不存在于REWARD_CONFIGS中")
        return "", "", ""

    # 其他配置的通用实现
    reward_config = config.REWARD_CONFIGS[config_key]
    reward_types = []
    reward_names = []
    next_reward_gap = ""  # 下一级奖励所需金额差

    # 幸运数字奖励逻辑
    lucky_number = reward_config.get("lucky_number", "")
    if lucky_number and str(contract_number % 10) == lucky_number:
        reward_types.append("幸运数字")
        
        # 获取幸运奖励配置
        lucky_rewards = reward_config.get("lucky_rewards", {})
        base_reward = lucky_rewards.get("base", {})
        high_reward = lucky_rewards.get("high", {})
        
        # 根据合同金额确定具体奖励
        if high_reward and current_contract_amount >= high_reward.get("threshold", 0):
            reward_names.append(high_reward.get("name", ""))
        elif base_reward:
            reward_names.append(base_reward.get("name", ""))

    # 节节高奖励逻辑
    tiered_rewards = reward_config.get("tiered_rewards", {})
    min_contracts = tiered_rewards.get("min_contracts", 0)
    tiers = tiered_rewards.get("tiers", [])
    
    if housekeeper_data['count'] >= min_contracts:
        # 根据配置决定使用哪个金额字段
        performance_limits = reward_config.get("performance_limits", {})
        enable_cap = performance_limits.get("enable_cap", False)
        
        if enable_cap and 'performance_amount' in housekeeper_data:
            amount = housekeeper_data['performance_amount']
        else:
            amount = housekeeper_data['total_amount']
        
        logging.info(f"使用金额: {amount} (enable_cap={enable_cap})")
        
        # 确定当前达到的奖励等级
        current_tier = None
        next_reward = None
        all_tier_names = []
        
        for tier in sorted(tiers, key=lambda x: x.get("threshold", 0)):
            tier_name = tier.get("name", "")
            all_tier_names.append(tier_name)
            
            if amount >= tier.get("threshold", 0):
                current_tier = tier
            elif not next_reward:
                next_reward = tier_name
        
        # 如果达到了某个奖励等级
        if current_tier:
            tier_name = current_tier.get("name", "")
            
            # 检查是否已经获得过该奖励
            if tier_name not in housekeeper_data.get('awarded', []):
                reward_types.append("节节高")
                reward_names.append(tier_name)
            
            # 计算距离下一级奖励所需的金额差
            if next_reward:
                next_reward_threshold = next(
                    (tier["threshold"] for tier in tiers if tier["name"] == next_reward),
                    0
                )
                if next_reward_threshold > 0:
                    next_reward_gap = f"距离 {next_reward} 还需 {round(next_reward_threshold - amount, 2):,} 元"
        else:
            # 如果未达到最低合同数量要求
            if not set(all_tier_names).intersection(housekeeper_data['awarded']):
                next_reward_gap = f"距离达成节节高奖励条件还需 {min_contracts - housekeeper_data['count']} 单"

    return ', '.join(reward_types), ', '.join(reward_names), next_reward_gap

def determine_rewards_apr_beijing_generic(contract_number, housekeeper_data, current_contract_amount):
    """
    使用通用奖励确定函数计算2025年4月北京活动的奖励

    Args:
        contract_number: 合同编号
        housekeeper_data: 管家数据，包含count、total_amount和awarded等信息
        current_contract_amount: 当前合同金额

    Returns:
        tuple: (reward_types_str, reward_names_str, next_reward_gap)
    """
    return determine_rewards_generic(
        contract_number,
        housekeeper_data,
        current_contract_amount,
        "BJ-2025-04"
    )

def determine_rewards_may_beijing_generic(contract_number, housekeeper_data, current_contract_amount):
    """
    使用通用奖励确定函数计算2025年5月北京活动的奖励

    Args:
        contract_number: 合同编号
        housekeeper_data: 管家数据，包含count、total_amount和awarded等信息
        current_contract_amount: 当前合同金额

    Returns:
        tuple: (reward_types_str, reward_names_str, next_reward_gap)
    """
    return determine_rewards_generic(
        contract_number,
        housekeeper_data,
        current_contract_amount,
        "BJ-2025-05"
    )

def determine_rewards_apr_shanghai_generic(contract_number, housekeeper_data, current_contract_amount):
    """
    使用通用奖励确定函数计算2025年4月上海活动的奖励

    Args:
        contract_number: 合同编号
        housekeeper_data: 管家数据，包含count、total_amount和awarded等信息
        current_contract_amount: 当前合同金额

    Returns:
        tuple: (reward_types_str, reward_names_str, next_reward_gap)
    """
    return determine_rewards_generic(
        contract_number,
        housekeeper_data,
        current_contract_amount,
        "SH-2025-04"
    )

def determine_rewards_may_shanghai_generic(contract_number, housekeeper_data, current_contract_amount):
    """
    使用通用奖励确定函数计算2025年5月上海活动的奖励

    Args:
        contract_number: 合同编号
        housekeeper_data: 管家数据，包含count、total_amount和awarded等信息
        current_contract_amount: 当前合同金额

    Returns:
        tuple: (reward_types_str, reward_names_str, next_reward_gap)
    """
    return determine_rewards_generic(
        contract_number,
        housekeeper_data,
        current_contract_amount,
        "SH-2025-05"
    )
