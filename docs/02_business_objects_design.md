# 业务对象设计

## 概述

本文档通过业务分析，从现有代码中提炼出隐含的业务对象设计。虽然当前项目采用函数式编程方法实现，但面向对象的设计思路对项目升级和重构具有重要指导意义。

## 核心业务对象

### 1. 活动(Campaign)

**描述**: 表示一个销售激励活动，具有特定的时间范围、地区和奖励规则。

**属性**:
- 活动ID: 如 "BJ-2025-04"（北京2025年4月活动）
- 活动城市: 如 "北京"、"上海"
- 活动时间: 开始日期和结束日期
- 幸运数字: 触发幸运数字奖励的数字
- 奖励规则: 包括幸运数字奖励和节节高奖励的规则
- 性能上限配置: 单个合同计入业绩金额的上限

**行为**:
- 初始化活动
- 获取活动数据
- 处理活动数据
- 发送活动通知

**代码体现**:
```python
# 在config.py中的REWARD_CONFIGS字典中定义
"BJ-2025-04": {
    "lucky_number": "8",
    "lucky_rewards": {...},
    "performance_limits": {...},
    "tiered_rewards": {...}
}

# 在jobs.py中的函数体现
def signing_and_sales_incentive_apr_beijing():
    # 活动初始化和执行
```

### 2. 合同(Contract)

**描述**: 表示客户签约的服务协议，是奖励计算的基础单位。

**属性**:
- 合同ID: 唯一标识符
- 工单编号: 关联的服务工单
- 合同编号: 业务编号
- 合同金额: 签约金额
- 支付金额: 已支付金额
- 创建时间: 合同创建时间
- 签约时间: 合同签约时间
- 管家: 负责该合同的服务人员
- 服务商: 提供服务的公司
- 活动城市: 合同所属城市

**行为**:
- 计算计入业绩金额
- 检查是否触发幸运数字奖励
- 更新合同状态

**代码体现**:
```python
# 在数据处理中作为字典处理
contract = {
    '合同ID(_id)': '123456',
    '工单编号(serviceAppointmentNum)': 'GD123456',
    '合同编号(contractdocNum)': 'HT123456',
    '合同金额(adjustRefundMoney)': '10000',
    '管家(serviceHousekeeper)': '张三',
    '服务商(orgName)': '服务商A'
    # 其他属性...
}

# 在process_data_apr_beijing等函数中处理
performance_amount = min(contract_amount, performance_cap)
```

### 3. 管家(Housekeeper)

**描述**: 负责客户服务和合同签约的服务人员，是奖励发放的对象。

**属性**:
- 姓名: 管家姓名
- 服务商: 所属服务商
- 累计合同数: 活动期内累计签约合同数
- 累计金额: 活动期内累计签约金额
- 计入业绩金额: 考虑上限后的累计业绩金额
- 已获奖励: 已经获得的奖励列表
- 是否精英管家: 是否具有精英管家标识

**行为**:
- 累计合同
- 计算业绩
- 获取奖励
- 接收通知

**代码体现**:
```python
# 在数据处理中作为字典处理
housekeeper_contracts[housekeeper] = {
    'count': 0, 
    'total_amount': 0, 
    'awarded': [], 
    'performance_amount': 0
}

# 精英管家列表
ELITE_HOUSEKEEPER = ["胡林波", "余金凤", "文刘飞", "李卓", "吕世军"]
```

### 4. 奖励(Reward)

**描述**: 表示根据业绩规则发放给管家的奖励。

**属性**:
- 奖励类型: 如 "幸运数字"、"节节高"
- 奖励名称: 如 "接好运"、"达标奖"、"优秀奖"、"精英奖"
- 奖励阈值: 触发奖励的金额阈值
- 关联合同: 触发奖励的合同
- 关联管家: 获得奖励的管家

**行为**:
- 检查是否满足奖励条件
- 生成奖励通知
- 记录奖励状态

**代码体现**:
```python
# 在determine_rewards_generic等函数中
reward_types = []
reward_names = []

# 在REWARD_CONFIGS中定义奖励规则
"tiered_rewards": {
    "min_contracts": 6,
    "tiers": [
        {"name": "达标奖", "threshold": 40000},
        {"name": "优秀奖", "threshold": 60000},
        {"name": "精英奖", "threshold": 100000}
    ]
}
```

### 5. 通知(Notification)

**描述**: 表示发送给相关人员的消息通知。

**属性**:
- 通知类型: 如 "奖励通知"、"状态变更通知"、"SLA违规通知"
- 接收人: 通知接收人
- 消息内容: 通知内容
- 发送状态: 如 "待发送"、"已发送"
- 创建时间: 通知创建时间

**行为**:
- 生成通知内容
- 发送通知
- 更新发送状态

**代码体现**:
```python
# 在task_manager.py中作为Task对象
class Task:
    def __init__(self, task_type, recipient, message):
        self.task_type = task_type
        self.recipient = recipient
        self.message = message
        self.status = 'pending'
        # 其他属性...

# 在notification_module.py中
create_task('send_wecom_message', WECOM_GROUP_NAME_BJ_APR, msg)
```

### 6. 服务商(ServiceProvider)

**描述**: 提供服务的公司，管理多个管家。

**属性**:
- 名称: 服务商名称
- 城市: 所在城市
- 管家列表: 所属管家列表
- 接收人: 通知接收人
- SLA记录: 服务水平协议违规记录

**行为**:
- 接收通知
- 管理管家
- 监控SLA

**代码体现**:
```python
# 在config.py中的SERVICE_PROVIDER_MAPPING
SERVICE_PROVIDER_MAPPING = {
    "北京博远恒泰装饰装修有限公司": "博远恒泰（沟通群）",
    "北京德客声商贸有限公司": "德客声（沟通群）",
    # 其他映射...
}

# 在service_provider_sla_monitor.py中
def process_sla_violations(violation_data):
    # 处理服务商SLA违规
```

### 7. 工单(ServiceAppointment)

**描述**: 服务请求单，可能对应多个合同。

**属性**:
- 工单编号: 唯一标识符
- 创建时间: 工单创建时间
- 状态: 工单状态
- 服务商: 负责的服务商
- 管家: 负责的管家
- 关联合同: 关联的合同列表

**行为**:
- 创建工单
- 更新状态
- 关联合同

**代码体现**:
```python
# 在数据处理中通过工单编号关联
service_appointment_num = contract['工单编号(serviceAppointmentNum)']
service_appointment_amounts[service_appointment_num] = service_appointment_amounts.get(service_appointment_num, 0)
```

### 8. SLA违规记录(SLAViolation)

**描述**: 服务水平协议违规记录。

**属性**:
- 违规ID: 唯一标识符
- 工单编号: 关联的工单
- 服务商: 违规的服务商
- 管家: 相关管家
- 违规类型: 违规的类型
- 违规描述: 详细描述
- 创建时间: 记录创建时间

**行为**:
- 记录违规
- 生成通知
- 生成周报

**代码体现**:
```python
# 在service_provider_sla_monitor.py中
def _update_violation_records(violation_data):
    # 更新违规记录

def send_sla_violation_notifications(violation_data):
    # 发送违规通知
```

## 业务对象关系

### 主要关系

1. **活动(Campaign) 1:N 合同(Contract)**
   - 一个活动包含多个合同
   - 合同属于特定活动

2. **管家(Housekeeper) 1:N 合同(Contract)**
   - 一个管家负责多个合同
   - 合同由一个管家负责

3. **服务商(ServiceProvider) 1:N 管家(Housekeeper)**
   - 一个服务商包含多个管家
   - 管家属于一个服务商

4. **工单(ServiceAppointment) 1:N 合同(Contract)**
   - 一个工单可能关联多个合同
   - 合同属于一个工单

5. **管家(Housekeeper) 1:N 奖励(Reward)**
   - 一个管家可以获得多个奖励
   - 奖励发放给特定管家

6. **合同(Contract) 1:N 奖励(Reward)**
   - 一个合同可能触发多个奖励
   - 奖励与特定合同关联

7. **服务商(ServiceProvider) 1:N SLA违规记录(SLAViolation)**
   - 一个服务商可能有多个SLA违规记录
   - SLA违规记录属于特定服务商

8. **奖励(Reward) 1:N 通知(Notification)**
   - 一个奖励可能产生多个通知
   - 通知可能关联特定奖励

### 关系图

```
Campaign (活动)
    |
    +--> Contract (合同) <---- ServiceAppointment (工单)
            |                       |
            v                       |
    Housekeeper (管家) <------------|
            |                       |
            +--> Reward (奖励)      |
            |       |               |
            |       +--> Notification (通知)
            |                       |
            v                       v
    ServiceProvider (服务商) ----> SLAViolation (SLA违规记录)
```

## 业务流程

1. **活动初始化**:
   - 在config.py中定义活动配置
   - 在jobs.py中创建活动处理函数

2. **数据获取**:
   - 从Metabase API获取合同数据
   - 加载已存在的合同ID和管家奖励记录

3. **数据处理**:
   - 遍历合同数据
   - 更新管家累计合同数和金额
   - 应用业绩金额上限规则
   - 检查是否触发奖励

4. **奖励确定**:
   - 检查幸运数字奖励条件
   - 检查节节高奖励条件
   - 生成奖励记录

5. **通知发送**:
   - 创建通知任务
   - 任务调度器执行任务
   - 更新通知发送状态

6. **SLA监控**:
   - 检查SLA违规情况
   - 记录违规数据
   - 发送违规通知和周报

## 设计建议

1. **显式定义业务对象**:
   - 考虑将隐含的业务对象显式定义为类
   - 将相关功能封装到对应类中

2. **统一数据结构**:
   - 标准化合同、管家等数据结构
   - 使用类型提示增强代码可读性

3. **抽象通用功能**:
   - 进一步抽象通用的数据处理逻辑
   - 创建通用的奖励计算框架

4. **增强业务规则配置**:
   - 扩展配置系统，支持更复杂的业务规则
   - 考虑使用规则引擎处理复杂条件

5. **改进对象关系**:
   - 明确定义对象间的关系
   - 考虑使用ORM管理数据关系

这些业务对象和关系的清晰定义将有助于未来的系统扩展和重构，使代码更加模块化和可维护。
