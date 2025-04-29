# 测试策略简述

## 测试重点

### 奖励确定函数测试
- **幸运数字奖励**: 测试不同合同编号和金额下的幸运数字奖励判定
- **节节高奖励**: 测试不同累计金额和合同数量下的节节高奖励判定
- **多重奖励**: 测试同时获得幸运数字和节节高奖励的情况
- **自动发放低级奖励**: 测试高金额合同自动发放低级别奖励的逻辑
- **边界条件**: 测试合同数量和金额在边界值附近的情况

### 数据处理函数测试
- **数据转换**: 测试合同数据到性能数据的转换
- **重复合同处理**: 测试对重复合同ID的处理
- **性能上限应用**: 测试性能金额上限的正确应用
- **工单金额累计**: 测试工单编号累计金额的计算
- **奖励状态更新**: 测试奖励状态的正确更新

### 通用函数测试
- **配置一致性**: 测试通用函数与特定函数的结果一致性
- **城市差异处理**: 测试对北京和上海差异的正确处理
- **错误处理**: 测试对无效输入的处理

## 测试数据管理

### 测试数据准备
- **模拟合同数据**: 创建包含各种场景的模拟合同数据
- **预设管家数据**: 准备不同状态的管家数据，覆盖各种奖励场景
- **边界值数据**: 特别准备边界条件的测试数据

### 测试数据存储
- **测试CSV文件**: 在tests目录下保存测试用CSV文件
- **测试数据版本控制**: 确保测试数据与代码版本匹配
- **测试数据隔离**: 测试数据与生产数据严格分离

## 常见测试案例

### 案例1: 幸运数字和节节高奖励同时获得
```python
def test_may_beijing_lucky_and_progressive_rewards(self):
    """测试5月北京活动同时获得幸运数字和节节高奖励"""
    # 设置管家数据，满足节节高奖励条件
    housekeeper_data = {
        'count': 6,  # 满足最低合同数量要求
        'total_amount': 85000,  # 达到达标奖阈值
        'performance_amount': 85000,  # 使用相同的绩效金额
        'awarded': []  # 尚未获得任何奖励
    }
    
    # 使用带有幸运数字6的合同编号和高于1万的合同金额
    reward_types, reward_names, gap = determine_rewards_may_beijing_generic(
        contract_number=16,  # 合同编号末位为6，触发幸运数字奖励
        housekeeper_data=housekeeper_data,
        current_contract_amount=15000  # 高于1万，触发高额幸运奖励
    )
    
    # 验证结果
    self.assertIn("幸运数字", reward_types)
    self.assertIn("接好运万元以上", reward_names)
    self.assertIn("节节高", reward_types)
    self.assertIn("达标奖", reward_names)
```

### 案例2: 高金额合同自动发放低级别奖励
```python
def test_may_beijing_auto_award_lower_tiers(self):
    """测试高金额合同自动发放低级别奖励"""
    # 设置管家数据，初始金额已经达到优秀奖阈值
    housekeeper_data = {
        'count': 6,  # 满足最低合同数量要求
        'total_amount': 130000,  # 已经达到优秀奖阈值(120000)
        'performance_amount': 130000,  # 使用相同的绩效金额
        'awarded': []  # 尚未获得任何奖励
    }
    
    # 使用不触发幸运数字的合同编号和普通合同金额
    reward_types, reward_names, gap = determine_rewards_may_beijing_generic(
        contract_number=11,  # 合同编号不触发幸运数字奖励
        housekeeper_data=housekeeper_data,
        current_contract_amount=5000  # 普通合同金额
    )
    
    # 验证结果
    self.assertIn("节节高", reward_types)
    self.assertIn("达标奖", reward_names)
    self.assertIn("优秀奖", reward_names)
```

### 案例3: 上海四档奖励测试
```python
def test_shanghai_four_tier_rewards(self):
    """测试上海活动四档奖励（基础奖、达标奖、优秀奖、精英奖）"""
    # 设置管家数据，满足基础奖条件
    housekeeper_data = {
        'count': 5,  # 满足最低合同数量要求（上海需要5个合同）
        'total_amount': 45000,  # 达到基础奖阈值
        'performance_amount': 45000,  # 使用相同的绩效金额
        'awarded': []  # 尚未获得任何奖励
    }
    
    # 调用奖励函数
    reward_types, reward_names, gap = determine_rewards_apr_shanghai_generic(
        contract_number=11,  # 合同编号不触发幸运数字奖励
        housekeeper_data=housekeeper_data,
        current_contract_amount=5000  # 普通合同金额
    )
    
    # 验证获得了基础奖
    self.assertEqual(reward_types, "节节高")
    self.assertEqual(reward_names, "基础奖")
    self.assertTrue("距离 达标奖 还需" in gap)
```

## 当前测试重点

当前重构工作中，测试重点是:

1. 为通用数据处理函数 (process_data_generic) 编写全面测试
2. 测试包装函数与原始函数的结果一致性
3. 测试功能标志的正确工作
4. 测试边界条件和特殊情况处理

所有新实现的函数必须通过现有测试，并且需要添加新测试覆盖新增功能和边界情况。
