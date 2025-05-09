"""
奖励计算模块

该模块包含所有与奖励计算相关的函数，用于确定合同的奖励类型和名称。
这些函数可以被文件处理模块和数据库处理模块共同使用，确保奖励计算逻辑的一致性。

模块结构:
1. determine_rewards_generic: 通用奖励确定函数，基于配置确定奖励类型和名称
2. 城市/月份特定的包装函数:
   - determine_rewards_apr_beijing_generic: 2025年4月北京活动
   - determine_rewards_may_beijing_generic: 2025年5月北京活动
   - determine_rewards_apr_shanghai_generic: 2025年4月上海活动
   - determine_rewards_may_shanghai_generic: 2025年5月上海活动

使用方法:
1. 直接使用城市/月份特定的函数，如:
   ```python
   reward_types, reward_names, next_reward_gap = determine_rewards_apr_beijing_generic(
       contract_number=123,
       housekeeper_data={'count': 6, 'total_amount': 85000, 'performance_amount': 85000, 'awarded': []},
       current_contract_amount=15000
   )
   ```

2. 或者使用通用函数，指定配置键:
   ```python
   reward_types, reward_names, next_reward_gap = determine_rewards_generic(
       contract_number=123,
       housekeeper_data={'count': 6, 'total_amount': 85000, 'performance_amount': 85000, 'awarded': []},
       current_contract_amount=15000,
       config_key="BJ-2025-04"
   )
   ```
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
        contract_number (int): 合同编号，用于判断是否触发幸运数字奖励。
            通常使用合同在活动中的序号，而不是合同ID。

        housekeeper_data (dict): 管家数据字典，必须包含以下字段:
            - count (int): 管家的合同数量
            - total_amount (float): 管家的合同总金额
            - performance_amount (float, 可选): 计入业绩的金额，如果启用了业绩金额上限
            - awarded (list): 已获得的奖励名称列表，用于避免重复发放奖励

        current_contract_amount (float): 当前合同金额，用于判断触发哪种幸运奖励

        config_key (str): 配置键名，用于从REWARD_CONFIGS中获取对应配置。
            格式为"城市代码-年份-月份"，如"BJ-2025-04"表示2025年4月北京活动。

    Returns:
        tuple: 包含三个元素的元组:
            - reward_types_str (str): 奖励类型字符串，多个类型用逗号分隔，如"幸运数字, 节节高"
            - reward_names_str (str): 奖励名称字符串，多个名称用逗号分隔，如"接好运万元以上, 达标奖"
            - next_reward_gap (str): 下一级奖励提示，如"距离 优秀奖 还需 35,000 元"

    Raises:
        ValueError: 当输入参数无效时抛出，如合同编号为负数
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
    if lucky_number:
        lucky_rewards = reward_config.get("lucky_rewards", {})

        # 检查幸运数字
        if lucky_number in str(contract_number % 10):
            reward_types.append("幸运数字")

            # 根据合同金额确定奖励名称
            high_threshold = lucky_rewards.get("high", {}).get("threshold", 10000)
            if current_contract_amount >= high_threshold:
                reward_name = lucky_rewards.get("high", {}).get("name", "接好运万元以上")
                reward_names.append(reward_name)
            else:
                reward_name = lucky_rewards.get("base", {}).get("name", "接好运")
                reward_names.append(reward_name)

    # 节节高奖励逻辑
    tiered_rewards = reward_config.get("tiered_rewards", {})
    min_contracts = tiered_rewards.get("min_contracts", 0)
    tiers = tiered_rewards.get("tiers", [])

    # 记录所有奖励名称，用于后续检查
    all_tier_names = [tier.get("name", "") for tier in tiers]

    if housekeeper_data['count'] >= min_contracts:
        # 根据配置决定使用哪个金额字段
        performance_limits = reward_config.get("performance_limits", {})
        enable_cap = performance_limits.get("enable_cap", False)

        if enable_cap and 'performance_amount' in housekeeper_data:
            amount = housekeeper_data['performance_amount']
        else:
            amount = housekeeper_data['total_amount']

        logging.info(f"使用金额: {amount} (enable_cap={enable_cap})")

        next_reward = None

        # 按照阈值从高到低排序奖励等级
        sorted_tiers = sorted(tiers, key=lambda x: x.get("threshold", 0), reverse=True)

        # 第一阶段：检查是否达到奖励条件，并添加奖励
        for i, tier in enumerate(sorted_tiers):
            tier_name = tier.get("name", "")
            tier_threshold = tier.get("threshold", 0)

            if amount >= tier_threshold and tier_name not in housekeeper_data.get('awarded', []):
                reward_types.append("节节高")
                reward_names.append(tier_name)
                housekeeper_data.setdefault('awarded', []).append(tier_name)

                # 如果不是最高级别的奖励，设置下一个奖励
                if i > 0:
                    next_reward = sorted_tiers[i-1].get("name", "")
                break

        # 如果未达到任何奖励阈值，设置下一个奖励为最低等级
        if not set(all_tier_names).intersection(housekeeper_data.get('awarded', [])):
            if sorted_tiers:
                next_reward = sorted_tiers[-1].get("name", "")

        # 第二阶段：自动发放所有低级别奖项（如果之前未获得）
        for tier in sorted(tiers, key=lambda x: x.get("threshold", 0)):
            tier_name = tier.get("name", "")
            tier_threshold = tier.get("threshold", 0)

            if tier_name not in housekeeper_data.get('awarded', []) and amount >= tier_threshold:
                reward_types.append("节节高")
                reward_names.append(tier_name)
                housekeeper_data.setdefault('awarded', []).append(tier_name)

        # 第三阶段：确定下一个奖励
        if not next_reward:
            for i in range(len(sorted_tiers) - 1):
                if i + 1 < len(sorted_tiers):
                    current_tier = sorted_tiers[i+1]
                    next_tier = sorted_tiers[i]

                    if (current_tier.get("name", "") in housekeeper_data.get('awarded', []) and
                        amount < next_tier.get("threshold", 0) and
                        next_tier.get("name", "") not in housekeeper_data.get('awarded', [])):
                        next_reward = next_tier.get("name", "")
                        break

        # 计算距离下一级奖励所需的金额差
        if next_reward:
            next_reward_threshold = next(
                (tier.get("threshold", 0) for tier in tiers if tier.get("name", "") == next_reward),
                0
            )
            if next_reward_threshold > 0:
                next_reward_gap = f"距离 {next_reward} 还需 {round(next_reward_threshold - amount, 2):,} 元"
    else:
        # 如果未达到最低合同数量要求
        if not set(all_tier_names).intersection(housekeeper_data.get('awarded', [])):
            next_reward_gap = f"距离达成节节高奖励条件还需 {min_contracts - housekeeper_data['count']} 单"

    return ', '.join(reward_types), ', '.join(reward_names), next_reward_gap

def determine_rewards_apr_beijing_generic(contract_number, housekeeper_data, current_contract_amount):
    """
    计算2025年4月北京活动的奖励。

    这是一个包装函数，调用通用奖励确定函数并传入"BJ-2025-04"配置键。
    北京4月活动的幸运数字是8，节节高奖励有三档（达标奖、优秀奖、精英奖）。

    Args:
        contract_number (int): 合同编号，用于判断是否触发幸运数字奖励。
            通常使用合同在活动中的序号，而不是合同ID。

        housekeeper_data (dict): 管家数据字典，必须包含以下字段:
            - count (int): 管家的合同数量
            - total_amount (float): 管家的合同总金额
            - performance_amount (float, 可选): 计入业绩的金额
            - awarded (list): 已获得的奖励名称列表

        current_contract_amount (float): 当前合同金额，用于判断触发哪种幸运奖励

    Returns:
        tuple: 包含三个元素的元组:
            - reward_types_str (str): 奖励类型字符串，如"幸运数字, 节节高"
            - reward_names_str (str): 奖励名称字符串，如"接好运万元以上, 达标奖"
            - next_reward_gap (str): 下一级奖励提示
    """
    return determine_rewards_generic(
        contract_number,
        housekeeper_data,
        current_contract_amount,
        "BJ-2025-04"
    )

def determine_rewards_may_beijing_generic(contract_number, housekeeper_data, current_contract_amount):
    """
    计算2025年5月北京活动的奖励。

    这是一个包装函数，调用通用奖励确定函数并传入"BJ-2025-05"配置键。
    北京5月活动的幸运数字是6，节节高奖励有三档（达标奖、优秀奖、精英奖）。

    Args:
        contract_number (int): 合同编号，用于判断是否触发幸运数字奖励。
            通常使用合同在活动中的序号，而不是合同ID。

        housekeeper_data (dict): 管家数据字典，必须包含以下字段:
            - count (int): 管家的合同数量
            - total_amount (float): 管家的合同总金额
            - performance_amount (float, 可选): 计入业绩的金额
            - awarded (list): 已获得的奖励名称列表

        current_contract_amount (float): 当前合同金额，用于判断触发哪种幸运奖励

    Returns:
        tuple: 包含三个元素的元组:
            - reward_types_str (str): 奖励类型字符串，如"幸运数字, 节节高"
            - reward_names_str (str): 奖励名称字符串，如"接好运万元以上, 达标奖"
            - next_reward_gap (str): 下一级奖励提示
    """
    return determine_rewards_generic(
        contract_number,
        housekeeper_data,
        current_contract_amount,
        "BJ-2025-05"
    )

def determine_rewards_apr_shanghai_generic(contract_number, housekeeper_data, current_contract_amount):
    """
    计算2025年4月上海活动的奖励。

    这是一个包装函数，调用通用奖励确定函数并传入"SH-2025-04"配置键。
    上海4月活动的幸运数字是6，节节高奖励有四档（基础奖、达标奖、优秀奖、精英奖）。

    Args:
        contract_number (int): 合同编号，用于判断是否触发幸运数字奖励。
            通常使用合同在活动中的序号，而不是合同ID。

        housekeeper_data (dict): 管家数据字典，必须包含以下字段:
            - count (int): 管家的合同数量
            - total_amount (float): 管家的合同总金额
            - performance_amount (float, 可选): 计入业绩的金额
            - awarded (list): 已获得的奖励名称列表

        current_contract_amount (float): 当前合同金额，用于判断触发哪种幸运奖励

    Returns:
        tuple: 包含三个元素的元组:
            - reward_types_str (str): 奖励类型字符串，如"幸运数字, 节节高"
            - reward_names_str (str): 奖励名称字符串，如"接好运万元以上, 达标奖"
            - next_reward_gap (str): 下一级奖励提示
    """
    return determine_rewards_generic(
        contract_number,
        housekeeper_data,
        current_contract_amount,
        "SH-2025-04"
    )

def determine_rewards_may_shanghai_generic(contract_number, housekeeper_data, current_contract_amount):
    """
    计算2025年5月上海活动的奖励。

    这是一个包装函数，调用通用奖励确定函数并传入"SH-2025-05"配置键。
    上海5月活动的幸运数字是6，节节高奖励有四档（基础奖、达标奖、优秀奖、精英奖）。

    Args:
        contract_number (int): 合同编号，用于判断是否触发幸运数字奖励。
            通常使用合同在活动中的序号，而不是合同ID。

        housekeeper_data (dict): 管家数据字典，必须包含以下字段:
            - count (int): 管家的合同数量
            - total_amount (float): 管家的合同总金额
            - performance_amount (float, 可选): 计入业绩的金额
            - awarded (list): 已获得的奖励名称列表

        current_contract_amount (float): 当前合同金额，用于判断触发哪种幸运奖励

    Returns:
        tuple: 包含三个元素的元组:
            - reward_types_str (str): 奖励类型字符串，如"幸运数字, 节节高"
            - reward_names_str (str): 奖励名称字符串，如"接好运万元以上, 达标奖"
            - next_reward_gap (str): 下一级奖励提示
    """
    return determine_rewards_generic(
        contract_number,
        housekeeper_data,
        current_contract_amount,
        "SH-2025-05"
    )
