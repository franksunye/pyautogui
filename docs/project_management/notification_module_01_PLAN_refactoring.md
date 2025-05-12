# 通知模块重构计划

## 文档信息
**文档类型**: 项目计划
**文档编号**: notification_module-PLAN-001
**版本**: 1.0.0
**创建日期**: 2025-05-15
**最后更新**: 2025-05-15
**状态**: 草稿
**负责人**: Frank
**团队成员**: Frank, 小智
**优先级**: 高
**预计工期**: 1个Sprint (2周)

**相关文档**:
- [项目待办事项](../00_backlog.md)
- [热修复实施报告](./completed/hotfix_reward_doubling_notification_02_IMPLEMENTATION.md)

## 1. 项目概述

### 1.1 背景

当前项目的通知功能分散在多个模块中，缺乏统一的接口和抽象。最近的热修复（修复奖励翻倍通知功能中的两个BUG）进一步凸显了通知模块重构的必要性。通过将通知功能模块化和通用化，可以提高代码的可维护性和可扩展性。

### 1.2 目标

- 将通知逻辑从数据处理中分离
- 创建统一的通知接口
- 支持多种通知渠道（企业微信、微信、Webhook等）
- 确保与现有功能完全兼容
- 简化通知相关的配置管理

### 1.3 范围

- 重构 `notification_module.py` 文件
- 创建新的通知接口和抽象类
- 修改调用通知功能的代码
- 更新相关文档和配置

### 1.4 非范围

- 不包括对系统其他部分的重构
- 不包括添加新的通知渠道
- 不包括修改通知内容的格式和样式

## 2. 当前状态分析

### 2.1 现有通知功能

当前的通知功能主要包括以下几个方面：

1. **签约喜报通知**：
   - `notify_awards_may_beijing`
   - `notify_awards_apr_beijing`
   - `notify_awards_shanghai_generate_message_march`

2. **技师状态变更通知**：
   - `notify_technician_status_changes`

3. **日报服务通知**：
   - `notify_daily_service_report`

4. **工单联络超时通知**：
   - `notify_contact_timeout_changes`
   - `notify_contact_timeout_changes_markdown`
   - `notify_contact_timeout_changes_template_card`

### 2.2 现有通知渠道

当前支持的通知渠道包括：

1. **企业微信群通知**：
   - `create_task('send_wecom_message', group_name, message)`

2. **微信个人通知**：
   - `create_task('send_wechat_message', contact_name, message)`

3. **Webhook通知**：
   - `post_text_to_webhook`
   - `post_markdown_to_webhook`
   - `post_template_card_to_webhook`

### 2.3 存在的问题

1. **代码重复**：多个通知函数中存在大量重复代码
2. **耦合度高**：通知逻辑与数据处理逻辑紧密耦合
3. **配置分散**：通知相关的配置分散在多个地方
4. **扩展性差**：添加新的通知渠道或修改现有通知逻辑需要修改多处代码
5. **测试困难**：通知功能难以单独测试

## 3. 重构方案

### 3.1 架构设计

我们将采用以下架构设计：

1. **通知接口**：定义通知的基本接口
2. **通知渠道**：实现不同的通知渠道
3. **通知模板**：定义不同类型的通知模板
4. **通知管理器**：管理通知的发送和状态跟踪

```
notification_module/
├── __init__.py
├── interfaces.py       # 通知接口定义
├── channels/           # 通知渠道实现
│   ├── __init__.py
│   ├── wecom.py        # 企业微信通知
│   ├── wechat.py       # 微信通知
│   └── webhook.py      # Webhook通知
├── templates/          # 通知模板
│   ├── __init__.py
│   ├── contract.py     # 合同通知模板
│   ├── technician.py   # 技师状态通知模板
│   └── report.py       # 报告通知模板
├── manager.py          # 通知管理器
└── utils.py            # 工具函数
```

### 3.2 接口设计

#### 3.2.1 通知接口

```python
# interfaces.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class NotificationChannel(ABC):
    """通知渠道接口"""
    
    @abstractmethod
    def send(self, recipient: str, content: str, **kwargs) -> bool:
        """
        发送通知
        
        Args:
            recipient: 接收者
            content: 通知内容
            **kwargs: 其他参数
            
        Returns:
            bool: 是否发送成功
        """
        pass

class NotificationTemplate(ABC):
    """通知模板接口"""
    
    @abstractmethod
    def render(self, data: Dict[str, Any]) -> str:
        """
        渲染通知内容
        
        Args:
            data: 通知数据
            
        Returns:
            str: 渲染后的通知内容
        """
        pass
```

#### 3.2.2 通知管理器

```python
# manager.py
from typing import Dict, Any, Optional, List
from .interfaces import NotificationChannel, NotificationTemplate

class NotificationManager:
    """通知管理器"""
    
    def __init__(self):
        self.channels: Dict[str, NotificationChannel] = {}
        self.templates: Dict[str, NotificationTemplate] = {}
        
    def register_channel(self, name: str, channel: NotificationChannel) -> None:
        """注册通知渠道"""
        self.channels[name] = channel
        
    def register_template(self, name: str, template: NotificationTemplate) -> None:
        """注册通知模板"""
        self.templates[name] = template
        
    def send(self, channel_name: str, recipient: str, template_name: str, data: Dict[str, Any], **kwargs) -> bool:
        """
        发送通知
        
        Args:
            channel_name: 通知渠道名称
            recipient: 接收者
            template_name: 通知模板名称
            data: 通知数据
            **kwargs: 其他参数
            
        Returns:
            bool: 是否发送成功
        """
        if channel_name not in self.channels:
            raise ValueError(f"Unknown channel: {channel_name}")
            
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
            
        channel = self.channels[channel_name]
        template = self.templates[template_name]
        
        content = template.render(data)
        return channel.send(recipient, content, **kwargs)
```

### 3.3 实现示例

#### 3.3.1 企业微信通知渠道

```python
# channels/wecom.py
from ..interfaces import NotificationChannel
from task_manager import create_task

class WecomChannel(NotificationChannel):
    """企业微信通知渠道"""
    
    def send(self, recipient: str, content: str, **kwargs) -> bool:
        """
        发送企业微信通知
        
        Args:
            recipient: 企业微信群名称
            content: 通知内容
            **kwargs: 其他参数
            
        Returns:
            bool: 是否发送成功
        """
        try:
            create_task('send_wecom_message', recipient, content)
            return True
        except Exception as e:
            import logging
            logging.error(f"Failed to send Wecom message: {e}")
            return False
```

#### 3.3.2 合同通知模板

```python
# templates/contract.py
from typing import Dict, Any
from ..interfaces import NotificationTemplate

class ContractNotificationTemplate(NotificationTemplate):
    """合同通知模板"""
    
    def render(self, data: Dict[str, Any]) -> str:
        """
        渲染合同通知内容
        
        Args:
            data: 通知数据，包括：
                - service_housekeeper: 管家姓名
                - contract_number: 合同编号
                - contract_rank: 活动期内第几个合同
                - personal_rank: 个人累计第几个合同
                - accumulated_amount: 累计金额
                - next_message: 下一步提示
                
        Returns:
            str: 渲染后的通知内容
        """
        service_housekeeper = data.get('service_housekeeper', '')
        contract_number = data.get('contract_number', '')
        contract_rank = data.get('contract_rank', '')
        personal_rank = data.get('personal_rank', '')
        accumulated_amount = data.get('accumulated_amount', '')
        next_message = data.get('next_message', '')
        
        return f'''\U0001F9E8\U0001F9E8\U0001F9E8 签约喜报 \U0001F9E8\U0001F9E8\U0001F9E8
恭喜 {service_housekeeper} 签约合同 {contract_number} 并完成线上收款\U0001F389\U0001F389\U0001F389

\U0001F33B 本单为活动期间平台累计签约第 {contract_rank} 单，个人累计签约第 {personal_rank} 单。

\U0001F33B {service_housekeeper}累计签约 {accumulated_amount} 元

\U0001F44A {next_message}。
'''
```

## 4. 实施计划

### 4.1 第一阶段：准备工作（第1-2天）

- [ ] **任务1.1**: 创建详细的通知功能清单
  - 优先级: 高
  - 估计工时: 2小时
  - 描述: 全面审查代码，创建包含所有通知功能的详细清单。

- [ ] **任务1.2**: 设计通知接口和类结构
  - 优先级: 高
  - 估计工时: 4小时
  - 描述: 设计通知接口和类结构，确保满足所有需求。

- [ ] **任务1.3**: 创建单元测试框架
  - 优先级: 高
  - 估计工时: 3小时
  - 描述: 创建单元测试框架，为重构后的通知模块提供测试覆盖。

### 4.2 第二阶段：核心实现（第3-7天）

- [ ] **任务2.1**: 实现通知接口和抽象类
  - 优先级: 高
  - 估计工时: 4小时
  - 描述: 实现通知接口和抽象类，为不同的通知渠道和模板提供基础。

- [ ] **任务2.2**: 实现通知渠道
  - 优先级: 高
  - 估计工时: 6小时
  - 描述: 实现企业微信、微信和Webhook等通知渠道。

- [ ] **任务2.3**: 实现通知模板
  - 优先级: 高
  - 估计工时: 8小时
  - 描述: 实现合同通知、技师状态通知和报告通知等模板。

- [ ] **任务2.4**: 实现通知管理器
  - 优先级: 高
  - 估计工时: 4小时
  - 描述: 实现通知管理器，管理通知的发送和状态跟踪。

### 4.3 第三阶段：集成与测试（第8-12天）

- [ ] **任务3.1**: 修改现有代码，使用新的通知模块
  - 优先级: 高
  - 估计工时: 8小时
  - 描述: 修改现有代码，使用新的通知模块替代原有的通知功能。

- [ ] **任务3.2**: 编写单元测试
  - 优先级: 高
  - 估计工时: 6小时
  - 描述: 为新的通知模块编写单元测试，确保功能正确。

- [ ] **任务3.3**: 执行集成测试
  - 优先级: 高
  - 估计工时: 4小时
  - 描述: 执行集成测试，验证新的通知模块与系统其他部分的集成。

- [ ] **任务3.4**: 修复发现的问题
  - 优先级: 高
  - 估计工时: 6小时
  - 描述: 修复测试过程中发现的问题。

### 4.4 第四阶段：文档与部署（第13-14天）

- [ ] **任务4.1**: 更新文档
  - 优先级: 中
  - 估计工时: 4小时
  - 描述: 更新文档，包括通知模块的使用说明和配置指南。

- [ ] **任务4.2**: 准备部署
  - 优先级: 中
  - 估计工时: 2小时
  - 描述: 准备部署，包括创建部署脚本和配置文件。

- [ ] **任务4.3**: Sprint回顾与总结
  - 优先级: 中
  - 估计工时: 1小时
  - 描述: 进行Sprint回顾，总结经验和教训。

## 5. 测试计划

### 5.1 单元测试

为通知模块的各个组件编写单元测试，包括：

1. **通知渠道测试**：
   - 测试企业微信通知渠道
   - 测试微信通知渠道
   - 测试Webhook通知渠道

2. **通知模板测试**：
   - 测试合同通知模板
   - 测试技师状态通知模板
   - 测试报告通知模板

3. **通知管理器测试**：
   - 测试通知管理器的注册功能
   - 测试通知管理器的发送功能

### 5.2 集成测试

执行集成测试，验证通知模块与系统其他部分的集成，包括：

1. **数据处理与通知集成测试**：
   - 测试数据处理后的通知发送
   - 测试通知状态的跟踪和更新

2. **配置与通知集成测试**：
   - 测试不同配置下的通知行为
   - 测试配置变更对通知的影响

### 5.3 回归测试

执行回归测试，确保重构后的通知模块与原有功能完全兼容，包括：

1. **功能等价性测试**：
   - 测试重构前后的通知内容一致性
   - 测试重构前后的通知行为一致性

2. **性能测试**：
   - 测试重构前后的通知性能
   - 测试大量通知的处理能力

## 6. 风险与缓解措施

### 6.1 已识别风险

1. **功能中断风险**：
   - **风险**：重构可能导致现有通知功能中断
   - **缓解**：全面的测试计划和回滚机制

2. **性能下降风险**：
   - **风险**：新的通知模块可能导致性能下降
   - **缓解**：性能测试和优化

3. **集成复杂性风险**：
   - **风险**：与现有代码的集成可能比预期更复杂
   - **缓解**：分阶段实施，先处理最简单的部分

### 6.2 应急计划

1. 保留原始代码的备份
2. 准备回滚脚本
3. 设置监控和警报机制

## 7. 交付物

1. 重构后的通知模块代码
2. 单元测试和集成测试
3. 更新的文档，包括使用说明和配置指南
4. 部署脚本和配置文件

## 8. 验收标准

1. 所有单元测试和集成测试通过
2. 重构后的通知模块与原有功能完全兼容
3. 代码质量符合项目标准
4. 文档完整且准确

## 更新记录

| 版本 | 日期 | 更新者 | 更新内容 |
|------|------|--------|----------|
| 1.0.0 | 2025-05-15 | 小智 | 初始版本 |
