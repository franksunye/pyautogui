# 通知模块设计文档

## 文档信息
**文档类型**: 设计文档  
**文档编号**: notification_module-DESIGN-001  
**版本**: 1.0.0  
**创建日期**: 2025-05-16  
**最后更新**: 2025-05-16  
**状态**: 已完成  
**负责人**: Frank  
**团队成员**: Frank, 小智  

## 1. 概述

通知模块负责向不同渠道（企业微信、微信、Webhook等）发送各种类型的通知，包括合同签约通知、奖励通知、技师状态变更通知等。本文档描述了通知模块的设计，包括统一的活动配置结构、通知工具函数和模板函数。

## 2. 设计目标

1. **解耦数据处理和通知逻辑**：将通知逻辑从数据处理中分离出来，使代码更加模块化。
2. **统一活动配置**：创建统一的活动配置结构，整合奖励计算、通知和数据源相关的配置。
3. **减少代码重复**：通过通用的工具函数和模板函数，减少代码重复。
4. **提高可维护性**：使代码更加结构化，遵循更好的设计原则，提高可维护性。
5. **保持向后兼容性**：确保与现有代码的兼容性，实现平滑过渡。

## 3. 架构设计

### 3.1 组件结构

```
modules/
├── config.py                  # 配置模块，包含统一的活动配置结构
├── notification_utils.py      # 通知工具函数模块
├── notification_templates.py  # 通知模板函数模块
├── notification_module.py     # 文件版通知函数模块
└── notification_db_module.py  # 数据库版通知函数模块
```

### 3.2 统一活动配置结构

在 `config.py` 中，我们创建了一个统一的活动配置结构 `CAMPAIGN_CONFIGS`，整合了奖励计算、通知和数据源相关的配置：

```python
CAMPAIGN_CONFIGS = {
    "BJ-2025-05": {
        # 奖励计算相关配置
        "reward": {
            "lucky_number": "6",
            "lucky_rewards": {
                "base": {"name": "接好运", "threshold": 0},
                "high": {"name": "接好运万元以上", "threshold": 10000}
            },
            "performance_limits": {
                "single_project_limit": 100000,
                "enable_cap": True,
                "single_contract_cap": 100000
            },
            "tiered_rewards": {
                "min_contracts": 6,
                "tiers": [
                    {"name": "达标奖", "threshold": 80000},
                    {"name": "优秀奖", "threshold": 120000},
                    {"name": "精英奖", "threshold": 160000}
                ]
            }
        },
        
        # 通知相关配置
        "notification": {
            "group_name": "（北京）修链服务运营",
            "contact_name": "王爽",
            "awards_mapping": {
                "接好运": "28",
                "接好运万元以上": "58",
                "达标奖": "200",
                "优秀奖": "400",
                "精英奖": "600"
            },
            "delay_seconds": 3
        },
        
        # 数据源配置
        "data_source": {
            "api_url": "http://metabase.fsgo365.cn:3000/api/card/1693/query",
            "temp_file": "state/ContractData-BJ-May.csv",
            "performance_file": "state/PerformanceData-BJ-May.csv"
        }
    },
    
    # 其他活动配置...
}
```

### 3.3 通知工具函数

在 `notification_utils.py` 中，我们创建了通用的通知发送函数：

```python
def send_contract_notification(
    channel, recipient, message, reward_status=0, 
    reward_message=None, reward_recipient=None, delay=3
):
    """发送合同通知"""
    # 实现...

def send_webhook_notification(message, webhook_url=WEBHOOK_URL_DEFAULT):
    """发送Webhook通知"""
    # 实现...

def get_campaign_config(campaign_id):
    """获取活动配置"""
    # 实现...
```

### 3.4 通知模板函数

在 `notification_templates.py` 中，我们创建了各种通知模板的函数：

```python
def format_contract_signing_message(
    housekeeper, contract_doc_num, contract_amount, 
    conversion_rate, accumulated_amount, next_reward_msg
):
    """格式化合同签约消息"""
    # 实现...

def format_award_message(
    housekeeper, contract_doc_num, org_name, 
    contract_amount, reward_type, reward_name, 
    campaign_contact, awards_mapping
):
    """格式化奖励消息"""
    # 实现...

def format_technician_status_message(technician_name, status_time, status, status_content):
    """格式化技师状态变更消息"""
    # 实现...
```

### 3.5 兼容层

为了确保与现有代码的兼容性，我们添加了兼容层函数：

```python
def get_reward_config_from_campaign_config(campaign_id):
    """从统一活动配置中获取奖励配置"""
    campaign_config = CAMPAIGN_CONFIGS.get(campaign_id)
    if not campaign_config:
        raise ValueError(f"未找到活动配置: {campaign_id}")
    
    return campaign_config["reward"]

# 为了向后兼容，保留原有的REWARD_CONFIGS结构
REWARD_CONFIGS = {
    "BJ-2025-04": get_reward_config_from_campaign_config("BJ-2025-04"),
    # 其他活动...
}
```

## 4. 详细设计

### 4.1 通知工具函数

#### 4.1.1 send_contract_notification

```python
def send_contract_notification(
    channel, recipient, message, reward_status=0, 
    reward_message=None, reward_recipient=None, delay=3
):
    """
    发送合同通知
    
    Args:
        channel: 通知渠道 ('wecom' 或 'wechat')
        recipient: 接收者 (群名称或联系人)
        message: 通知消息
        reward_status: 奖励状态 (0=无奖励, 1=有奖励)
        reward_message: 奖励消息 (如果有)
        reward_recipient: 奖励消息接收者 (如果有)
        delay: 发送后延迟时间(秒)
    
    Returns:
        bool: 是否成功发送
    """
```

#### 4.1.2 send_webhook_notification

```python
def send_webhook_notification(message, webhook_url=WEBHOOK_URL_DEFAULT):
    """
    发送Webhook通知
    
    Args:
        message: 通知消息
        webhook_url: Webhook URL
    
    Returns:
        bool: 是否成功发送
    """
```

#### 4.1.3 get_campaign_config

```python
def get_campaign_config(campaign_id):
    """
    获取活动配置
    
    Args:
        campaign_id: 活动ID (例如 'BJ-2025-05')
    
    Returns:
        dict: 活动配置
    """
```

### 4.2 通知模板函数

#### 4.2.1 format_contract_signing_message

```python
def format_contract_signing_message(
    housekeeper, contract_doc_num, contract_amount, 
    conversion_rate, accumulated_amount, next_reward_msg
):
    """
    格式化合同签约消息
    
    Args:
        housekeeper: 管家姓名
        contract_doc_num: 合同编号
        contract_amount: 合同金额
        conversion_rate: 转化率
        accumulated_amount: 累计金额
        next_reward_msg: 下一个奖励提示
    
    Returns:
        str: 格式化后的消息
    """
```

#### 4.2.2 format_award_message

```python
def format_award_message(
    housekeeper, contract_doc_num, org_name, 
    contract_amount, reward_type, reward_name, 
    campaign_contact, awards_mapping
):
    """
    格式化奖励消息
    
    Args:
        housekeeper: 管家姓名
        contract_doc_num: 合同编号
        org_name: 服务商名称
        contract_amount: 合同金额
        reward_type: 奖励类型
        reward_name: 奖励名称
        campaign_contact: 活动联系人
        awards_mapping: 奖励金额映射
    
    Returns:
        str: 格式化后的消息
    """
```

#### 4.2.3 format_technician_status_message

```python
def format_technician_status_message(technician_name, status_time, status, status_content):
    """
    格式化技师状态变更消息
    
    Args:
        technician_name: 技师姓名
        status_time: 状态变更时间
        status: 状态 ('上线' 或 '下线')
        status_content: 状态内容
    
    Returns:
        str: 格式化后的消息
    """
```

## 5. 使用示例

### 5.1 获取活动配置

```python
# 获取活动配置
campaign_id = 'BJ-2025-05'
config = get_campaign_config(campaign_id)
notification_config = config.get('notification', {})

# 获取通知相关配置
group_name = notification_config.get('group_name')
contact_name = notification_config.get('contact_name')
awards_mapping = notification_config.get('awards_mapping', {})
delay_seconds = notification_config.get('delay_seconds', 3)
```

### 5.2 发送合同签约通知

```python
# 格式化签约消息
msg = format_contract_signing_message(
    housekeeper=housekeeper, 
    contract_doc_num=contract_doc_num, 
    contract_amount=contract_amount, 
    conversion_rate=conversion_rate, 
    accumulated_amount=accumulated_amount, 
    next_reward_msg=next_msg
)

# 发送通知
send_contract_notification(
    channel='wecom', 
    recipient=group_name, 
    message=msg, 
    reward_status=reward_status, 
    reward_message=reward_message, 
    reward_recipient=contact_name,
    delay=delay_seconds
)
```

### 5.3 发送技师状态变更通知

```python
# 格式化技师状态变更消息
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
```

## 6. 测试策略

### 6.1 单元测试

为通知工具函数和模板函数创建单元测试，确保它们在各种情况下都能正常工作。

### 6.2 集成测试

创建集成测试，验证通知模块与其他模块的集成，确保整个系统能够正常工作。

### 6.3 功能等价性测试

验证新实现与原始实现的功能等价性，确保重构不会改变系统的行为。

## 7. 迁移策略

### 7.1 阶段1：准备工作

1. 创建统一活动配置结构
2. 创建通知工具函数和模板函数
3. 添加兼容层函数

### 7.2 阶段2：更新通知函数

1. 更新文件版通知函数
2. 更新数据库版通知函数
3. 更新技师状态通知函数
4. 更新其他通知函数

### 7.3 阶段3：测试和验证

1. 创建单元测试和集成测试
2. 验证功能等价性
3. 进行回归测试

### 7.4 阶段4：完全迁移

1. 逐步迁移所有代码到新的统一配置结构
2. 移除兼容层函数
3. 更新文档

## 8. 结论

通过这次重构，我们成功地解决了通知模块中的代码重复、耦合和硬编码问题。新的设计更加模块化、可维护，并且遵循了更好的设计原则。统一的活动配置结构提供了面向业务的视图，使配置和维护更加容易。

## 9. 参考资料

1. 原始代码库
2. 项目需求文档
3. 设计模式参考
4. Python最佳实践指南
