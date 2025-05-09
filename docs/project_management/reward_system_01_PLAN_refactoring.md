# 奖励系统重构计划

## 文档信息
**文档类型**: 项目计划
**文档编号**: reward_system-PLAN-001
**版本**: 1.5.0
**创建日期**: 2025-04-29
**最后更新**: 2025-05-18
**状态**: 草稿
**负责人**: Frank
**团队成员**: Frank, 小智

**相关文档**:
- [奖励系统重构任务清单](./reward_system_03_TASK_refactoring.md) (reward_system-TASK-001)
- [奖励系统重构Scrum任务板](./reward_system_02_BOARD_sprint1.md) (reward_system-BOARD-001)

## 1. 项目概述

### 1.1 背景

当前的奖励系统中，北京和上海的数据处理函数采用了不同的实现方式。北京已经使用了通用奖励确定函数，而上海仍然使用特定的奖励确定函数。这种不一致性增加了维护成本，并可能导致功能差异。

此外，系统现在支持两种存储方式：文件存储和数据库存储，通过配置项 `USE_DATABASE_FOR_PERFORMANCE_DATA` 控制。奖励计算功能需要在这两种存储方式下保持一致，确保无论数据来源是文件还是数据库，都能使用相同的奖励计算逻辑。

我们还发现，数据库处理模块直接导入了文件处理模块中的奖励计算函数，这导致了模块间的紧耦合和结构混乱。例如，在 `data_processing_db_module.py` 中有类似 `from modules.data_processing_module import determine_rewards_may_beijing_generic` 的导入语句，这使得两个模块之间产生了不必要的依赖关系，降低了代码的可维护性和可扩展性。

### 1.2 目标

1. 统一北京和上海的数据处理函数，创建一个通用的数据处理框架
2. 创建独立的奖励计算模块，解耦文件处理和数据库处理模块
3. 确保新实现与原始实现功能完全一致
4. 提高代码可维护性和可扩展性
5. 确保奖励计算功能在文件存储和数据库存储两种模式下都能正常工作
6. 在整个过程中保持系统稳定运行

### 1.3 范围

- 创建独立的奖励计算模块 `reward_calculation.py`，将所有奖励计算函数移至该模块
- 保持函数接口简单明了，避免引入不必要的复杂性
- 重构 `process_data_apr_beijing` 和 `process_data_shanghai_apr` 函数
- 创建通用数据处理函数 `process_data_generic`，支持文件和数据库两种存储方式
- 添加上海的配置到 `REWARD_CONFIGS` 字典（已完成）
- 创建上海的通用奖励确定函数包装函数（已完成）
- 确保 `determine_rewards_generic` 函数在文件和数据库处理流程中都能被正确调用
- 修改数据库处理模块，使用新的奖励计算模块而非直接导入文件处理模块
- 添加必要的测试和文档

### 1.4 非范围

- 不修改现有的业务逻辑和奖励规则
- 不修改通知模块和其他系统组件
- 不修改用户界面或API
- 不修改数据库表结构

## 2. 实施计划

### 2.1 第一阶段：准备工作（1-2周）

#### 2.1.1 添加上海的配置到 REWARD_CONFIGS

- **任务**: 在 `config.py` 中为上海添加配置项
- **详情**: 添加 "SH-2025-04" 和 "SH-2025-05" 配置，确保与现有的上海奖励规则一致
- **验收标准**: 配置项已添加并通过代码审查
- **状态**: 已完成
- **负责人**: 小智
- **截止日期**: 2025-04-29

#### 2.1.2 创建上海的通用奖励确定函数包装函数

- **任务**: 实现 `determine_rewards_apr_shanghai_generic` 和 `determine_rewards_may_shanghai_generic`
- **详情**: 这些函数调用通用函数 `determine_rewards_generic` 并传入相应的配置键
- **验收标准**: 函数已实现并通过单元测试
- **状态**: 已完成
- **负责人**: 小智
- **截止日期**: 2025-04-29

#### 2.1.3 添加单元测试

- **任务**: 为新添加的函数创建单元测试
- **详情**: 确保测试覆盖所有边界情况和特殊场景
- **验收标准**: 测试已实现并通过
- **状态**: 已完成
- **负责人**: 小智
- **截止日期**: 2025-04-29

### 2.2 第二阶段：创建独立的奖励计算模块（1-2周）

#### 2.2.1 创建奖励计算模块

- **任务**: 创建 `reward_calculation.py` 模块
- **详情**:
  - 将所有奖励计算函数移至该模块
  - 包括 `determine_rewards_generic` 和所有城市/月份特定的包装函数
  - 确保函数接口保持一致
  - 添加详细的文档和注释
- **验收标准**:
  - 模块已创建并通过代码审查
  - 所有函数都有清晰的文档
  - 单元测试通过
- **状态**: 已完成
- **负责人**: 小智
- **截止日期**: 2025-05-17
- **完成日期**: 2025-05-17

#### 2.2.2 确保函数接口简单明了

- **任务**: 审查奖励计算函数接口
- **详情**:
  - 确保所有函数接口简单明了
  - 添加清晰的文档字符串
  - 避免引入不必要的抽象层
- **验收标准**:
  - 函数接口已审查并通过代码审查
  - 所有函数都有清晰的文档
  - 代码简洁易懂
- **状态**: 已完成
- **负责人**: 小智
- **截止日期**: 2025-05-17
- **完成日期**: 2025-05-17

#### 2.2.3 修改数据库处理模块

- **任务**: 更新 `data_processing_db_module.py`
- **详情**:
  - 修改导入语句，直接从奖励计算模块导入所需函数
  - 移除函数内部的导入语句
  - 使用简单条件判断选择合适的奖励计算函数
- **验收标准**:
  - 修改已完成并通过代码审查
  - 没有直接导入文件处理模块
  - 代码简洁明了
  - 功能与原始实现一致
- **状态**: 已完成
- **负责人**: 小智
- **截止日期**: 2025-05-17
- **完成日期**: 2025-05-17

#### 2.2.4 添加单元测试

- **任务**: 为新模块和修改的模块添加单元测试
- **详情**:
  - 测试奖励计算模块的所有函数
  - 测试各种场景和边界条件
  - 测试修改后的数据库处理模块
- **验收标准**:
  - 测试已实现并通过
  - 测试覆盖率高
  - 边界情况都有测试
- **状态**: 已完成
- **负责人**: 小智
- **截止日期**: 2025-05-17
- **完成日期**: 2025-05-17

### 2.3 第三阶段：实现通用数据处理函数（1-2周）

#### 2.3.1 创建通用数据处理函数

- **任务**: 实现 `process_data_generic` 函数
- **详情**:
  - 支持所有现有功能，处理北京和上海的所有差异
  - 支持文件存储和数据库存储两种模式
  - 通过参数控制输出目标（文件或数据库）
  - 确保调用 `determine_rewards_generic` 函数进行奖励计算
  - 添加详细的文档和注释
  - 从现有的 `process_data_apr_beijing` 和 `process_data_shanghai_apr` 函数中提取共同逻辑
  - 将差异部分参数化，通过配置或参数控制
- **验收标准**:
  - 函数已实现并通过代码审查
  - 函数在文件和数据库两种模式下都能正常工作
  - 奖励计算逻辑与原始实现一致
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-05-22

#### 2.3.2 添加功能标志

- **任务**: 在 `config.py` 中添加功能标志
- **详情**:
  - 添加 `USE_GENERIC_PROCESS_FUNCTION = False` 标志，允许在运行时控制是否使用新函数
  - 确保默认值为 False，以保持向后兼容性
  - 添加注释说明功能标志的用途
- **验收标准**:
  - 功能标志已添加并通过代码审查
  - 文档已更新，说明功能标志的用途
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-05-19

#### 2.3.3 创建包装函数

- **任务**: 实现 `process_data_apr_beijing_generic` 和 `process_data_shanghai_apr_generic`
- **详情**:
  - 这些函数调用通用函数并传入相应的参数
  - 支持文件存储和数据库存储两种模式
  - 通过参数 `use_database` 控制存储模式
  - 确保与数据库处理函数（如 `process_beijing_data_to_db`）功能等价
  - 为每个函数添加详细的文档字符串
  - 确保函数接口与现有函数保持一致
- **验收标准**:
  - 函数已实现并通过代码审查
  - 函数在文件和数据库两种模式下都能正常工作
  - 与原始实现功能等价
  - 文档清晰完整
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-05-24

### 2.4 第四阶段：并行运行和验证（1-2周）

#### 2.4.1 修改现有的处理函数

- **任务**: 在 `process_data_apr_beijing` 和 `process_data_shanghai_apr` 中添加并行运行逻辑
- **详情**:
  - 同时调用原始逻辑和新逻辑，但只返回原始结果
  - 添加日志记录比较两种方法的结果
  - 根据功能标志 `USE_GENERIC_PROCESS_FUNCTION` 决定是否执行并行运行
  - 确保原始功能不受影响
- **验收标准**:
  - 修改已完成并通过代码审查
  - 并行运行逻辑正确工作
  - 原始功能不受影响
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-05-26

#### 2.4.2 添加结果比较函数

- **任务**: 实现 `compare_results` 和 `convert_db_result_to_file_format` 函数
- **详情**:
  - `compare_results` 函数详细比较两种方法的结果，记录任何差异
  - `convert_db_result_to_file_format` 函数将数据库结果转换为与文件格式相同的格式
  - 添加详细的日志记录，方便分析差异
  - 确保比较逻辑全面覆盖所有关键字段
- **验收标准**:
  - 函数已实现并通过代码审查
  - 比较逻辑全面准确
  - 转换逻辑正确
  - 日志记录清晰详细
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-05-28

#### 2.4.3 在测试环境中启用功能标志

- **任务**: 在测试环境中设置 `USE_GENERIC_PROCESS_FUNCTION = True`
- **详情**:
  - 收集并分析比较结果，确保新实现与原始实现一致
  - 测试不同城市和月份的数据处理
  - 测试文件存储和数据库存储两种模式
  - 记录并解决发现的任何差异
- **验收标准**:
  - 测试完成，结果一致或差异已解决
  - 测试覆盖所有主要场景
  - 测试结果有详细记录
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-05-31

### 2.5 第五阶段：切换到新实现（1周）

#### 2.5.1 修改包装函数

- **任务**: 更新 `process_data_apr_beijing` 和 `process_data_shanghai_apr` 以使用新逻辑
- **详情**:
  - 根据功能标志选择使用新逻辑或原始逻辑
  - 确保平滑过渡，不影响现有功能
  - 添加详细的日志记录，方便排查问题
- **验收标准**:
  - 修改已完成并通过代码审查
  - 功能标志控制正常工作
  - 现有功能不受影响
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-06-02

#### 2.5.2 在生产环境中启用功能标志

- **任务**: 在生产环境中设置 `USE_GENERIC_PROCESS_FUNCTION = True`
- **详情**:
  - 监控系统，确保一切正常运行
  - 观察日志，确保没有异常
  - 准备回滚方案，以防出现问题
- **验收标准**:
  - 功能标志已启用
  - 系统运行正常
  - 没有新的错误或警告
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-06-05

#### 2.5.3 简化日志记录

- **任务**: 简化并行运行期间的日志记录
- **详情**:
  - 移除详细的比较日志，只保留必要的日志
  - 确保日志级别适当，不会产生过多的日志
  - 保持关键信息的记录
- **验收标准**:
  - 日志记录已简化
  - 关键信息仍然被记录
  - 日志级别适当
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-06-07

### 2.6 第六阶段：清理和完成（1周）

#### 2.6.1 移除原始实现

- **任务**: 一旦确认新实现稳定可靠，移除原始逻辑
- **详情**:
  - 保留包装函数，以维持向后兼容性
  - 移除并行运行逻辑
  - 移除不再需要的比较函数
  - 简化代码结构
- **验收标准**:
  - 原始逻辑已移除
  - 系统运行正常
  - 代码结构更加清晰
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-06-10

#### 2.6.2 移除功能标志

- **任务**: 移除 `USE_GENERIC_PROCESS_FUNCTION` 标志
- **详情**:
  - 直接使用新实现
  - 移除所有与功能标志相关的条件判断
  - 确保代码简洁明了
- **验收标准**:
  - 功能标志已移除
  - 系统运行正常
  - 代码简洁明了
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-06-12

#### 2.6.3 更新文档

- **任务**: 更新所有相关文档
- **详情**:
  - 反映新的实现
  - 更新函数说明和用法
  - 确保文档与代码一致
- **验收标准**:
  - 文档已更新并通过审查
  - 文档与代码一致
  - 文档清晰易懂
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-06-14

#### 2.6.4 代码审查和最终测试

- **任务**: 进行全面的代码审查和测试
- **详情**:
  - 运行完整的测试套件
  - 确保所有功能正常工作
  - 确保代码质量符合标准
  - 确保没有引入新的问题
- **验收标准**:
  - 代码审查已完成
  - 所有测试通过
  - 没有新的错误或警告
  - 代码质量符合标准
- **状态**: 未开始
- **负责人**: 小智
- **截止日期**: 2025-06-15

## 3. 风险和缓解措施

### 3.1 功能差异风险

- **风险**: 新实现可能与原始实现有细微差异
- **影响**: 高
- **可能性**: 中
- **缓解措施**: 详细的比较逻辑和全面的测试
- **触发条件**: 发现任何功能差异
- **应急计划**: 回滚到原始实现，修复差异后重新部署

### 3.2 性能风险

- **风险**: 通用函数可能比专用函数慢
- **影响**: 中
- **可能性**: 低
- **缓解措施**: 性能测试和优化
- **触发条件**: 性能下降超过10%
- **应急计划**: 优化通用函数，必要时回滚

### 3.3 回滚风险

- **风险**: 如果新实现有问题，可能难以回滚
- **影响**: 高
- **可能性**: 低
- **缓解措施**: 功能标志和保留原始逻辑作为后备
- **触发条件**: 需要回滚但遇到困难
- **应急计划**: 使用功能标志立即切换回原始实现

### 3.4 团队协作风险

- **风险**: 团队成员可能不熟悉新实现
- **影响**: 中
- **可能性**: 中
- **缓解措施**: 详细文档和知识分享会议
- **触发条件**: 团队成员反馈理解困难
- **应急计划**: 增加培训和文档，安排一对一辅导

## 4. 依赖关系

### 4.1 内部依赖

- 完成第一阶段后才能开始第二阶段
- 完成第二阶段后才能开始第三阶段
- 完成第三阶段后才能开始第四阶段
- 完成第四阶段后才能开始第五阶段

### 4.2 外部依赖

- 需要测试环境可用性
- 需要团队成员的时间和资源
- 需要代码审查和测试资源

## 5. 资源需求

### 5.1 人力资源

- 开发人员: 1-2人
- 测试人员: 1人
- 代码审查人员: 1-2人
- 项目管理: 1人

### 5.2 环境资源

- 开发环境
- 测试环境
- 生产环境

## 6. 沟通计划

### 6.1 定期会议

- 每周进度会议
- 每阶段结束后的评审会议
- 需要时的临时会议

### 6.2 报告和文档

- 每周进度报告
- 每阶段结束报告
- 最终项目总结报告

## 7. 验收标准

### 7.1 功能验收

- 新实现与原始实现功能完全一致
- 所有测试用例通过
- 没有新的错误或警告

### 7.2 性能验收

- 性能不低于原始实现
- 响应时间在可接受范围内
- 资源使用在可接受范围内

### 7.3 代码质量验收

- 代码符合项目编码标准
- 代码审查通过
- 文档完整且准确

## 8. 项目时间线

| 阶段 | 开始日期 | 结束日期 | 持续时间 | 状态 |
|------|----------|----------|----------|------|
| 第一阶段：准备工作 | 2025-04-29 | 2025-04-29 | 1天 | 已完成 |
| 第二阶段：创建独立的奖励计算模块 | 2025-05-15 | 2025-05-17 | 3天 | 已完成 |
| 第三阶段：实现通用数据处理函数 | 2025-05-18 | 2025-05-24 | 1周 | 未开始 |
| 第四阶段：并行运行和验证 | 2025-05-25 | 2025-05-31 | 1周 | 未开始 |
| 第五阶段：切换到新实现 | 2025-06-01 | 2025-06-07 | 1周 | 未开始 |
| 第六阶段：清理和完成 | 2025-06-08 | 2025-06-15 | 1周 | 未开始 |
| 总计 | 2025-04-29 | 2025-06-15 | 7周 | 进行中 |

## 9. 进度跟踪

| 日期 | 完成的任务 | 遇到的问题 | 解决方案 | 下一步计划 |
|------|------------|------------|----------|------------|
| 2025-04-29 | 创建项目计划文档；完成第一阶段所有任务 | 无 | 无 | 开始第二阶段 |
| 2025-05-15 | 更新项目计划，添加奖励计算模块重构 | 发现数据库处理模块直接导入文件处理模块中的奖励计算函数，导致模块间紧耦合 | 计划创建独立的奖励计算模块，解耦文件处理和数据库处理模块 | 开始实现奖励计算模块 |
| 2025-05-16 | 更新项目计划和任务清单，简化设计，移除工厂模式 | 工厂模式可能引入不必要的复杂性 | 使用简单条件判断替代工厂模式，遵循"保持简洁，保持敏捷，避免过度工程化"的原则 | 开始创建独立的奖励计算模块 |
| 2025-05-17 | 完成第二阶段所有任务：创建奖励计算模块，确保函数接口简单明了，修改数据库处理模块，添加单元测试 | 奖励计算模块与原始实现有一些差异 | 修复差异，确保新模块与原始实现完全一致 | 开始第三阶段：实现通用数据处理函数 |
| 2025-05-18 | 更新项目计划和任务清单，详细规划第三阶段至第六阶段的工作 | 需要明确各阶段的工作内容和时间安排 | 详细规划各阶段的任务，设定明确的截止日期，简化性能和边界条件的考虑 | 开始实现通用数据处理函数 |

## 10. 附录

### 10.1 参考文档

- 现有系统文档
- 代码库链接
- 相关技术文档

### 10.2 术语表

- **通用奖励确定函数**: `determine_rewards_generic` 函数，基于配置确定奖励类型和名称
- **通用数据处理函数**: `process_data_generic` 函数，支持所有城市和存储方式的通用数据处理逻辑
- **功能标志**: 用于控制是否使用新实现的配置项，如 `USE_GENERIC_PROCESS_FUNCTION`
- **包装函数**: 调用通用函数并传入特定参数的函数，如 `process_data_apr_beijing_generic`
- **存储模式**: 系统支持的数据存储方式，包括文件存储和数据库存储
- **REWARD_CONFIGS**: 配置字典，包含不同城市和月份的奖励规则配置
- **奖励计算模块**: 独立的模块 `reward_calculation.py`，包含所有奖励计算函数，设计简洁明了

### 10.3 代码示例

#### 10.3.1 通用数据处理函数示例

```python
def process_data_generic(
    contract_data,
    existing_contract_ids,
    housekeeper_award_lists,
    config_key,  # 例如 "BJ-2025-04", "SH-2025-04"
    use_database=False,  # 是否使用数据库存储
    campaign_id=None,  # 活动ID，用于数据库存储
    province_code=None,  # 省份代码，用于数据库存储
    use_combined_key=False  # 是否使用组合键（上海特有）
):
    """
    通用数据处理函数，处理合同数据并返回结果。

    Args:
        contract_data: 合同数据列表
        existing_contract_ids: 已存在的合同ID集合
        housekeeper_award_lists: 管家奖励列表
        config_key: 配置键名，用于从REWARD_CONFIGS中获取对应配置
        use_database: 是否使用数据库存储
        campaign_id: 活动ID，用于数据库存储
        province_code: 省份代码，用于数据库存储
        use_combined_key: 是否使用组合键（上海特有）

    Returns:
        如果use_database为False，返回处理后的性能数据列表
        如果use_database为True，返回处理的合同数量
    """
    # 从配置中获取相关参数
    city_code = config_key.split("-")[0]  # 例如 "BJ", "SH"

    # 根据城市代码选择相应的配置
    if city_code == "BJ":
        performance_cap = config.PERFORMANCE_AMOUNT_CAP_BJ_FEB
        project_limit = config.SINGLE_PROJECT_CONTRACT_AMOUNT_LIMIT_BJ_FEB
        enable_cap = config.ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_FEB
    else:  # "SH"
        performance_cap = config.PERFORMANCE_AMOUNT_CAP
        project_limit = None  # 上海没有工单金额上限
        enable_cap = config.ENABLE_PERFORMANCE_AMOUNT_CAP

    # 初始化数据结构
    performance_data = []
    contract_count_in_activity = len(existing_contract_ids) + 1
    housekeeper_contracts = {}
    processed_contract_ids = set()
    service_appointment_amounts = {}

    # 遍历合同数据
    for contract in contract_data:
        # 处理逻辑...

        # 计算奖励类型和名称
        reward_types, reward_names, next_reward_gap = determine_rewards_generic(
            contract_number,
            housekeeper_data,
            current_contract_amount,
            config_key
        )

        # 根据存储方式选择不同的处理逻辑
        if use_database:
            # 数据库存储逻辑
            db_utils.save_performance_data_to_db(
                contract_id,
                city_code,
                month,
                housekeeper_name,
                contract_amount,
                performance_amount,
                contract_number,
                service_appointment,
                service_provider,
                reward_types,
                reward_names
            )
            processed_count += 1
        else:
            # 文件存储逻辑
            performance_data.append({
                'contract_id': contract_id,
                'housekeeper': housekeeper_name,
                'contract_amount': contract_amount,
                'performance_amount': performance_amount,
                'contract_number': contract_number,
                'service_appointment': service_appointment,
                'service_provider': service_provider,
                'lucky_reward': reward_types[0] if reward_types else '',
                'progressive_reward': reward_types[1] if len(reward_types) > 1 else ''
            })

    # 根据存储方式返回不同的结果
    if use_database:
        return processed_count
    else:
        return performance_data
```

#### 10.3.2 包装函数示例

```python
def process_data_apr_beijing_generic(contract_data, existing_contract_ids, housekeeper_award_lists, use_database=False):
    """
    使用通用数据处理函数处理2025年4月北京活动的数据。

    Args:
        contract_data: 合同数据列表
        existing_contract_ids: 已存在的合同ID集合
        housekeeper_award_lists: 管家奖励列表
        use_database: 是否使用数据库存储

    Returns:
        如果use_database为False，返回处理后的性能数据列表
        如果use_database为True，返回处理的合同数量
    """
    return process_data_generic(
        contract_data,
        existing_contract_ids,
        housekeeper_award_lists,
        "BJ-2025-04",
        use_database,
        "BJ-2025-04" if use_database else None,
        "110000" if use_database else None,
        False  # 北京不使用组合键
    )
```

#### 10.3.3 奖励计算模块示例

```python
# modules/reward_calculation.py

def determine_rewards_generic(contract_number, housekeeper_data, contract_amount, config_key):
    """
    通用奖励确定函数，基于配置确定奖励类型和名称。

    Args:
        contract_number: 合同编号
        housekeeper_data: 管家数据
        contract_amount: 合同金额
        config_key: 配置键名，用于从REWARD_CONFIGS中获取对应配置

    Returns:
        tuple: (奖励类型列表, 奖励名称列表, 下一级奖励差距)
    """
    # 通用奖励计算逻辑...
    pass

def determine_rewards_apr_beijing_generic(contract_number, housekeeper_data, contract_amount):
    """
    北京4月奖励确定函数。

    Args:
        contract_number: 合同编号
        housekeeper_data: 管家数据
        contract_amount: 合同金额

    Returns:
        tuple: (奖励类型列表, 奖励名称列表, 下一级奖励差距)
    """
    return determine_rewards_generic(contract_number, housekeeper_data, contract_amount, "BJ-2025-04")

def determine_rewards_may_beijing_generic(contract_number, housekeeper_data, contract_amount):
    """
    北京5月奖励确定函数。

    Args:
        contract_number: 合同编号
        housekeeper_data: 管家数据
        contract_amount: 合同金额

    Returns:
        tuple: (奖励类型列表, 奖励名称列表, 下一级奖励差距)
    """
    return determine_rewards_generic(contract_number, housekeeper_data, contract_amount, "BJ-2025-05")

def determine_rewards_apr_shanghai_generic(contract_number, housekeeper_data, contract_amount):
    """
    上海4月奖励确定函数。

    Args:
        contract_number: 合同编号
        housekeeper_data: 管家数据
        contract_amount: 合同金额

    Returns:
        tuple: (奖励类型列表, 奖励名称列表, 下一级奖励差距)
    """
    return determine_rewards_generic(contract_number, housekeeper_data, contract_amount, "SH-2025-04")

def determine_rewards_may_shanghai_generic(contract_number, housekeeper_data, contract_amount):
    """
    上海5月奖励确定函数。

    Args:
        contract_number: 合同编号
        housekeeper_data: 管家数据
        contract_amount: 合同金额

    Returns:
        tuple: (奖励类型列表, 奖励名称列表, 下一级奖励差距)
    """
    return determine_rewards_generic(contract_number, housekeeper_data, contract_amount, "SH-2025-05")
```

#### 10.3.4 数据库处理模块示例

```python
# modules/data_processing_db_module.py

from modules.reward_calculation import (
    determine_rewards_apr_beijing_generic,
    determine_rewards_may_beijing_generic,
    determine_rewards_apr_shanghai_generic,
    determine_rewards_may_shanghai_generic
)

def process_beijing_data_to_db(contract_data, campaign_id="BJ-2025-05", province_code="110000"):
    """
    处理北京合同数据并将结果保存到数据库。

    Args:
        contract_data: 合同数据列表
        campaign_id: 活动ID，默认为"BJ-2025-05"
        province_code: 省份代码，默认为"110000"

    Returns:
        int: 处理的合同数量
    """
    # 解析城市和月份
    parts = campaign_id.split("-")
    city_code = parts[0]
    year_month = parts[1] + "-" + parts[2]
    month_code = parts[2]

    # 选择合适的奖励计算函数
    if city_code == "BJ" and month_code == "04":
        reward_calculator = determine_rewards_apr_beijing_generic
    elif city_code == "BJ" and month_code == "05":
        reward_calculator = determine_rewards_may_beijing_generic
    elif city_code == "SH" and month_code == "04":
        reward_calculator = determine_rewards_apr_shanghai_generic
    elif city_code == "SH" and month_code == "05":
        reward_calculator = determine_rewards_may_shanghai_generic
    else:
        raise ValueError(f"不支持的城市和月份组合: {city_code}-{month_code}")

    # 处理合同数据
    for contract in contract_data:
        # 处理逻辑...

        # 使用奖励计算函数
        reward_types, reward_names, next_reward_gap = reward_calculator(
            contract_number, housekeeper_data, contract_amount
        )

        # 保存到数据库...

    return processed_count
```

#### 10.3.5 数据库处理函数简化示例

```python
def process_beijing_data_to_db(contract_data, campaign_id="BJ-2025-05", province_code="110000"):
    """
    处理北京合同数据并将结果保存到数据库中。

    Args:
        contract_data: 合同数据列表
        campaign_id: 活动ID，默认为"BJ-2025-05"
        province_code: 省份代码，默认为"110000"

    Returns:
        处理的合同数量
    """
    config_key = campaign_id  # 使用活动ID作为配置键
    return process_data_generic(
        contract_data,
        get_unique_contract_ids(),  # 从数据库获取已存在的合同ID
        {},  # 空的管家奖励列表，将在函数内部初始化
        config_key,
        True,  # 使用数据库存储
        campaign_id,
        province_code
    )
```

#### 10.3.4 并行运行逻辑示例

```python
def process_data_apr_beijing(contract_data, existing_contract_ids, housekeeper_award_lists):
    """
    处理2025年4月北京活动的数据。

    Args:
        contract_data: 合同数据列表
        existing_contract_ids: 已存在的合同ID集合
        housekeeper_award_lists: 管家奖励列表

    Returns:
        处理后的性能数据列表
    """
    # 原始逻辑
    original_result = original_process_logic(...)

    if config.USE_GENERIC_PROCESS_FUNCTION:
        # 新逻辑
        use_database = config.USE_DATABASE_FOR_PERFORMANCE_DATA
        new_result = process_data_apr_beijing_generic(
            contract_data,
            existing_contract_ids.copy(),  # 使用副本避免影响原始逻辑
            housekeeper_award_lists,
            use_database
        )

        # 如果使用数据库，需要将结果转换为与原始结果相同的格式进行比较
        if use_database:
            new_result_converted = convert_db_result_to_file_format(new_result)
            compare_results(original_result, new_result_converted, "BJ-2025-04")
        else:
            compare_results(original_result, new_result, "BJ-2025-04")

    return original_result
```



## 更新记录

| 版本 | 日期 | 更新者 | 更新内容 |
|------|------|--------|----------|
| 1.0.0 | 2025-04-29 | Frank | 初始版本 |
| 1.1.0 | 2025-05-15 | Frank | 更新计划以反映数据库存储支持需求；添加更详细的通用数据处理函数设计；更新代码示例 |
| 1.2.0 | 2025-05-16 | Frank | 添加奖励计算模块重构计划；增加新的第二阶段；更新项目时间线；添加奖励计算模块和工厂函数的代码示例 |
| 1.3.0 | 2025-05-16 | Frank | 简化设计，移除工厂模式；更新代码示例以使用简单条件判断；遵循"保持简洁，保持敏捷，避免过度工程化"的原则 |
| 1.4.0 | 2025-05-17 | 小智 | 更新第二阶段任务状态为已完成；更新项目时间线和进度跟踪；添加2025-05-17完成的任务记录 |
| 1.5.0 | 2025-05-18 | 小智 | 详细规划第三阶段至第六阶段的工作；更新任务详情和验收标准；设定明确的截止日期；更新项目时间线；添加2025-05-18进度记录 |
