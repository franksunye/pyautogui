# 项目管理文档

本目录包含与项目管理相关的文档，用于跟踪和管理各个项目的进度、计划和任务。

## 文档组织

### 活动项目

活动项目的文档直接存放在本目录中。

### 已完成项目

已完成项目的文档存放在`completed`子目录中，并且状态已更新为"已完成"。这样可以保持文档的完整性和可追溯性，同时也方便查阅历史项目的信息，并将活动项目与已完成项目清晰分开。

## 已完成项目处理指南

当一个项目完成时，应按照以下步骤处理相关文档：

1. **更新文档状态**：
   - 将所有相关文档的状态字段从"草稿"、"活动"等更新为"已完成"
   - 更新最后更新日期
   - 添加版本记录，说明状态更新

2. **创建项目完成总结文档**：
   - 创建一个名为`[项目全称]_10_COMPLETE_summary.md`的文档
   - 总结项目的目标、成果、挑战和经验教训
   - 记录任何后续工作或维护要求

3. **移动文档到completed目录**：
   - 将所有相关文档移动到`completed`子目录中
   - 确保文档之间的相对路径引用仍然有效

4. **更新相关引用**：
   - 如果其他文档引用了该项目的文档，确保更新这些引用，说明项目已完成并已移动到`completed`目录

## 当前已完成项目

以下项目已经完成：

### 奖励系统重构计划 (reward_system)

**完成日期**: 2025-05-19
**主要文档**:
- [奖励系统重构计划](./completed/reward_system_01_PLAN_refactoring.md)
- [奖励系统重构任务清单](./completed/reward_system_03_TASK_refactoring.md)
- [奖励系统重构Scrum任务板](./completed/reward_system_02_BOARD_sprint1.md)
- [奖励系统重构项目完成总结](./completed/reward_system_10_COMPLETE_summary.md)

**主要成果**:
- 创建了独立的奖励计算模块 `reward_calculation.py`
- 实现了通用数据处理函数 `process_data_generic`
- 统一了北京和上海的数据处理函数
- 确保了新实现与原始实现功能完全一致
- 提高了代码可维护性和可扩展性
- 确保了奖励计算功能在文件存储和数据库存储两种模式下都能正常工作

### 敏感信息保护计划 (sensitive_information)

**完成日期**: 2025-05-07
**主要文档**:
- [敏感信息保护计划](./completed/sensitive_information_01_PLAN_protection.md)
- [敏感信息清单](./completed/sensitive_information_00_DOC_inventory.md)
- [环境变量结构设计](./completed/sensitive_information_02_DOC_env_var_structure.md)
- [敏感信息保护任务清单](./completed/sensitive_information_03_TASK_protection.md)
- [敏感信息保护计划 - Sprint回顾](./completed/sensitive_information_04_REVIEW_protection.md)
- [敏感信息保护计划 - 部署计划](./completed/sensitive_information_05_DEPLOY_plan.md)
- [敏感信息保护计划 - 项目完成总结](./completed/sensitive_information_10_COMPLETE_summary.md)

**主要成果**:
- 识别并移除了代码中所有硬编码的敏感信息
- 实施了安全的配置管理机制
- 确保了代码功能在修改后保持不变
- 建立了敏感信息管理的最佳实践

## 文档命名规范

所有项目管理文档应遵循以下命名格式：

```
[项目全称]_[文档类型]_[简短描述].md
```

- **项目全称**: 使用项目的完整名称，用下划线连接
- **文档类型**: 使用以下标准类型（大写），为了表示文档的逻辑顺序，采用数字前缀
  - 00_DOC: 技术文档
  - 01_PLAN: 项目计划
  - 02_BOARD: Scrum任务板
  - 03_TASK: 任务清单
  - 04_REVIEW: 项目回顾
  - 05_DEPLOY: 部署计划
  - 10_COMPLETE: 项目完成总结
- **简短描述**: 使用下划线连接的简短描述

## 文档状态

- **草稿**: 初始创建，尚未完成
- **活动**: 正在进行中
- **已审核**: 已完成并经过审核
- **已批准**: 已获得批准可以执行
- **已完成**: 项目已完成，文档归档

## 更新记录

| 版本 | 日期 | 更新者 | 更新内容 |
|------|------|--------|----------|
| 1.0.0 | 2025-05-07 | Frank | 初始版本 |
| 1.1.0 | 2025-05-07 | Frank | 更新已完成项目处理指南，添加completed目录说明 |
