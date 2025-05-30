# 业务规则参考

## 奖励计算规则

### 幸运数字奖励
- **触发条件**: 合同编号末位包含指定的幸运数字
- **奖励等级**:
  - **基础幸运奖**: 合同金额 < 10,000元
  - **高额幸运奖**: 合同金额 ≥ 10,000元
- **城市差异**:
  - **北京4月**: 幸运数字为"8"
  - **北京5月**: 幸运数字为"6"
  - **上海4月**: 幸运数字为"6"
  - **上海5月**: 幸运数字为"6"

### 节节高奖励
- **基本条件**: 管家累计合同数量达到最低要求
- **奖励等级**: 根据管家累计业绩金额确定
- **城市差异**:
  - **北京**: 最低需要6个合同，三档奖励(达标奖、优秀奖、精英奖)
  - **上海**: 最低需要5个合同，四档奖励(基础奖、达标奖、优秀奖、精英奖)

### 奖励阈值
- **北京4月和5月**:
  - 达标奖: 40,000元
  - 优秀奖: 60,000元
  - 精英奖: 100,000元
- **上海4月和5月**:
  - 基础奖: 40,000元
  - 达标奖: 60,000元
  - 优秀奖: 80,000元
  - 精英奖: 120,000元

### 自动发放规则
- 当管家累计业绩达到高级别奖励阈值时，自动发放所有低级别奖励
- 例如: 达到精英奖标准时，自动发放达标奖和优秀奖

### 业绩金额计算
- **性能上限**:
  - **北京**: 单个合同计入业绩金额上限为100,000元
  - **上海**: 单个合同计入业绩金额上限为40,000元
- **工单金额上限**:
  - **北京**: 单个工单累计合同金额上限为100,000元
  - **上海**: 无工单金额上限

### 奖金池计算
- 奖金池 = 合同金额 × 奖金池计算比例
- 奖金池计算比例为0.2% (0.002)

## 业务术语定义

### 核心术语
- **管家**: 负责客户服务和合同签约的服务人员
- **节节高**: 基于累计业绩的阶梯式奖励机制
- **幸运数字**: 触发特殊奖励的合同编号末位数字
- **工单**: 服务请求单，一个工单可能对应多个合同
- **合同**: 客户签约的服务协议，包含金额和服务内容
- **业绩金额**: 计入奖励计算的合同金额，可能有上限限制
- **奖金池**: 用于发放奖励的资金池，基于合同金额计算

### 奖励类型
- **接好运**: 基础幸运数字奖励，合同金额小于1万元
- **接好运万元以上**: 高额幸运数字奖励，合同金额1万元以上
- **基础奖**: 上海节节高第一级奖励
- **达标奖**: 节节高第一级奖励(北京)/第二级奖励(上海)
- **优秀奖**: 节节高第二级奖励(北京)/第三级奖励(上海)
- **精英奖**: 节节高最高级奖励

## 特殊情况处理

### 重复合同处理
- 系统会检测并跳过重复的合同ID
- 重复合同不计入管家业绩和合同数量

### 已存在合同处理
- 已存在于历史记录中的合同ID会被跳过
- 已存在合同不会触发新的奖励通知

### 管家奖励记录
- 系统维护每个管家已获得的奖励记录
- 已获得的奖励不会重复发放

### 精英管家标识
- 特定管家(如胡林波、余金凤等)被标记为精英管家
- 精英管家在通知中会显示特殊徽章

### 服务商映射
- 系统维护服务商名称到接收人名称的映射
- 通知会发送给映射表中指定的接收人

## 当前业务重点

当前重构工作中，需要特别关注:

1. 确保通用数据处理函数正确处理北京和上海的所有业务规则差异
2. 保持奖励计算逻辑的一致性，特别是在处理边界情况时
3. 正确应用性能上限和工单金额上限规则
4. 确保自动发放低级别奖励的逻辑在所有场景下正确工作
