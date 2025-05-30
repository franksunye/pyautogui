# 项目文档标准规范

## 1. 文档命名规范

### 1.1 文件命名格式

所有项目管理文档应遵循以下命名格式：

```
[项目全称]_[文档类型]_[简短描述].md
```

- **项目全称**: 使用项目的完整名称，用下划线连接，举例如下：
  - reward_system: 奖励系统重构
  - sensitive_information: 敏感信息保护
  - beijing_project: 北京项目
  - shanghai_project: 上海项目

- **文档类型**: 使用以下标准类型（大写），为了表示文档的逻辑顺序，采用数字前缀
  - 01_PLAN: 项目计划
  - 02_BOARD: Scrum任务板
  - 03_TASK: 任务清单
  - 04_REVIEW: 项目回顾
  - 05_SPEC: 技术规格说明

- **简短描述**: 使用下划线连接的简短描述

### 1.2 示例

- `reward_system_01_PLAN_refactoring.md`: 奖励系统重构计划
- `sensitive_information_01_PLAN_protection.md`: 敏感信息保护计划
- `reward_system_03_TASK_phase1.md`: 奖励系统重构第一阶段任务清单
- `sensitive_information_02_BOARD_sprint1.md`: 敏感信息保护Sprint 1任务板

## 2. 文档结构规范

### 2.1 项目计划文档 (PLAN)

所有项目计划文档应包含以下标准部分，在项目规模较小的时候，项目计划中已经包含了任务清单，则无需再创建Scrum任务板文档（BOARD）文档，在项目比较复杂的时候，超过了一个Sprint，需要拆分为多个子项目的时候，我们则需要创建Scrum任务板文档（BOARD）文档。

```markdown
# [项目名称]

## 文档信息
**文档类型**: 项目计划
**文档编号**: [项目全称]-PLAN-[序号]
**版本**: [版本号]
**创建日期**: [YYYY-MM-DD]
**最后更新**: [YYYY-MM-DD]
**状态**: [草稿/已审核/已批准/已完成]
**负责人**: [负责人姓名]
**团队成员**: [团队成员列表]

## 1. 项目概述
### 1.1 背景
### 1.2 目标
### 1.3 范围
### 1.4 非范围

## 2. 实施计划
### 2.1 第一阶段: [阶段名称]
#### 2.1.1 [任务1]
#### 2.1.2 [任务2]
...

## 3. 风险与缓解措施
### 3.1 [风险1]
### 3.2 [风险2]
...

## 4. 依赖关系
### 4.1 内部依赖
### 4.2 外部依赖

## 5. 资源需求

## 6. 验收标准

## 7. 项目时间线

## 8. 附录
```
### 2.2 Scrum任务板文档 (BOARD)

Scrum任务板的本质是故事（Story）的内容，也可以包括故事点（Story Point），故事和故事点需要完全覆盖计划文档中的目标和需求，请注意在项目规模较小的时候，项目计划中已经包含了任务清单，则无需再创建Scrum任务板文档（BOARD）文档，所有Scrum任务板文档应包含以下标准部分，：

```markdown
# [项目名称] Scrum任务板

## 文档信息
**文档类型**: Scrum任务板
**文档编号**: [项目全称]-BOARD-[序号]
**版本**: [版本号]
**创建日期**: [YYYY-MM-DD]
**最后更新**: [YYYY-MM-DD]
**Sprint**: [Sprint编号] ([开始日期] 至 [结束日期])
**关联计划**: [关联的项目计划文档编号，如 reward_system-PLAN-001]

## 待办事项 (To Do)
- [ ] [任务描述] (@[负责人]) [估计工时]小时 #[优先级]

## 进行中 (In Progress)
- [ ] [任务描述] (@[负责人]) [估计工时]小时 #[优先级]

## 待审查 (Review)
- [ ] [任务描述] (@[负责人]) [估计工时]小时 #[优先级]

## 已完成 (Done)
- [x] [任务描述] (@[负责人]) [完成日期]

## 每日站会记录
### [日期]
- 完成了什么:
- 计划做什么:
- 遇到了什么障碍:

## Sprint回顾
- 完成了什么:
- 遇到了什么问题:
- 学到了什么:
- 下一步改进:
```

### 2.3 任务清单文档 (TASK)

任务清单是具体的研发的工作项（Work Item），所有任务清单文档应包含以下标准部分：

```markdown
# [项目名称] 任务清单

## 文档信息
**文档类型**: 任务清单
**文档编号**: [项目全称]-TASK-[序号]
**版本**: [版本号]
**创建日期**: [YYYY-MM-DD]
**最后更新**: [YYYY-MM-DD]
**状态**: [活动/已完成]
**关联计划**: [关联的项目计划文档编号]

## [阶段1名称]

### 任务1: [任务名称]
- **描述**: [详细描述]
- **验收标准**: [验收标准列表]
- **估计工时**: [小时数]
- **优先级**: [高/中/低]
- **状态**: [待办/进行中/已完成]
- **负责人**: [负责人姓名]
- **团队成员**: [团队成员列表]
- **笔记**: [任务相关笔记]

### 任务2: [任务名称]
...

## [阶段2名称]
...
```

## 3. 内容格式规范

### 3.1 通用格式规则

- 使用Markdown格式
- 标题使用层级结构 (#, ##, ###, ####)
- 列表项使用 - 或 1. 格式
- 代码块使用 ```语言名称 格式
- 表格使用标准Markdown表格格式

### 3.2 任务状态标记

- **待办**: [ ] 任务描述
- **进行中**: [~] 任务描述
- **已完成**: [x] 任务描述

### 3.3 优先级标记

- **高优先级**: #高
- **中优先级**: #中
- **低优先级**: #低

### 3.4 日期格式

所有日期应使用ISO 8601格式: YYYY-MM-DD

## 4. 文档管理规范

### 4.1 版本控制

- 主版本号: 重大变更
- 次版本号: 功能添加
- 修订版本号: 错误修复和小调整

例如: 1.0.0, 1.1.0, 1.1.1

### 4.2 文档状态

- **草稿**: 初始创建，尚未完成
- **已审核**: 已完成并经过审核
- **已批准**: 已获得批准可以执行
- **已完成**: 项目已完成，文档归档

### 4.3 文档更新记录

每个文档应在文档末尾包含更新记录部分:

```markdown
## 更新记录

| 版本 | 日期 | 更新者 | 更新内容 |
|------|------|--------|----------|
| 1.0.0 | 2025-04-29 | Frank | 初始版本 |
| 1.0.1 | 2025-04-30 | 小智 | 修正任务估计 |
```

### 4.4 Git 版本管理规则

#### 4.4.1 分支管理策略

- **main 分支**: 生产环境稳定版本，始终保持可部署状态
- **refactor 分支**: 用于复杂重构工作，完成后合并回 main 分支
- **feature 分支**: 用于开发新功能，命名格式: `feature/[功能名称]`
- **bugfix 分支**: 用于修复 bug，命名格式: `bugfix/[问题简述]`
- **hotfix 分支**: 用于紧急修复生产环境问题，命名格式: `hotfix/[问题简述]`

#### 4.4.2 标签管理

- **版本标签**: 用于标记重要的发布版本，命名格式: `v[主版本号].[次版本号].[修订版本号]`
  - 例如: `v1.0.0`, `v1.1.0`, `v1.2.3`
- **里程碑标签**: 用于标记重要的项目里程碑，命名格式: `milestone-[名称]`
  - 例如: `milestone-phase1-complete`
- **稳定版标签**: 用于标记稳定的生产环境版本，命名格式: `v[版本号]-stable`
  - 例如: `v1.0.0-stable`

#### 4.4.3 提交信息规范

提交信息应遵循以下格式:

```
[类型]: [简短描述]

[详细描述]
```

类型包括:
- **Feature**: 新功能
- **Fix**: 修复 bug
- **Docs**: 文档更新
- **Style**: 代码风格调整，不影响功能
- **Refactor**: 代码重构，不添加新功能或修复 bug
- **Test**: 添加或修改测试
- **Chore**: 构建过程或辅助工具变动

例如:
```
Feature: 添加上海5月奖励配置

- 在 config.py 中添加 SH-2025-05 配置
- 添加相关单元测试
- 更新文档
```

#### 4.4.4 代码审查流程

1. 创建 Pull Request (PR) 前，确保:
   - 所有测试通过
   - 代码符合项目编码标准
   - 提交信息符合规范
2. PR 应包含清晰的描述，说明变更内容和目的
3. 至少需要一名团队成员审查并批准
4. 解决所有审查意见后才能合并

#### 4.4.5 发布流程

1. 在合并到 main 分支前，确保:
   - 所有功能完整实现
   - 所有测试通过
   - 文档已更新
2. 合并到 main 分支后:
   - 创建版本标签
   - 更新版本号
   - 生成发布说明
3. 重大版本发布前，应进行全面的回归测试

## 5. 文档相互引用规范

### 5.1 引用格式

引用其他文档时，应使用以下格式:

```markdown
参见 [文档标题](文档路径) (文档编号)
```

例如:

```markdown
参见 [奖励系统重构计划](./reward_system_01_PLAN_refactoring.md) (reward_system-PLAN-001)
```

### 5.2 相关文档列表

每个文档应在文档信息部分后包含相关文档列表:

```markdown
**相关文档**:
- [文档标题1](文档路径1) (文档编号1)
- [文档标题2](文档路径2) (文档编号2)
```

## 6. 文档转换规范

### 6.1 现有文档转换

对于现有文档，应按照以下步骤进行转换:

1. 重命名文件，符合命名规范
2. 添加文档信息部分
3. 调整文档结构，符合结构规范
4. 添加更新记录
5. 更新相关文档的引用

### 6.2 转换优先级

1. 项目计划文档
2. 任务清单文档
3. Scrum任务板文档
4. 其他文档

## 7. 示例文档

### 7.1 项目计划文档示例

```markdown
# 奖励系统重构计划

## 文档信息
**文档类型**: 项目计划
**文档编号**: reward_system-PLAN-001
**版本**: 1.0.0
**创建日期**: 2025-04-29
**最后更新**: 2025-04-29
**状态**: 已审核
**负责人**: Frank
**团队成员**: Frank, 小智

**相关文档**:
- [奖励系统重构任务清单](./reward_system_03_TASK_refactoring.md) (reward_system-TASK-001)
- [奖励系统重构Scrum任务板](./reward_system_02_BOARD_sprint1.md) (reward_system-BOARD-001)

## 1. 项目概述
### 1.1 背景
当前的奖励系统中，北京和上海的数据处理函数采用了不同的实现方式...
```

### 7.2 任务清单文档示例

```markdown
# 奖励系统重构任务清单

## 文档信息
**文档类型**: 任务清单
**文档编号**: reward_system-TASK-001
**版本**: 1.0.0
**创建日期**: 2025-04-29
**最后更新**: 2025-04-29
**状态**: 活动
**关联计划**: reward_system-PLAN-001

**相关文档**:
- [奖励系统重构计划](./reward_system_01_PLAN_refactoring.md) (reward_system-PLAN-001)
- [奖励系统重构Scrum任务板](./reward_system_02_BOARD_sprint1.md) (reward_system-BOARD-001)

## 第一阶段: 准备工作

### 任务1: 在config.py中添加上海的配置到REWARD_CONFIGS
- **描述**: 分析现有上海奖励规则，在config.py的REWARD_CONFIGS字典中添加SH-2025-04和SH-2025-05配置
- **验收标准**:
  - 配置项已添加
  - 配置与现有上海奖励规则一致
  - 单元测试通过
- **估计工时**: 2小时
- **优先级**: 高
- **状态**: 已完成
- **负责人**: 小智
- **团队成员**: Frank, 小智
- **笔记**: 添加了SH-2025-04和SH-2025-05配置
```

## 8. 文档审查清单

在提交或更新文档前，请检查以下项目:

- [ ] 文件名符合命名规范
- [ ] 文档包含完整的文档信息部分
- [ ] 文档结构符合相应文档类型的结构规范
- [ ] 内容格式符合格式规范
- [ ] 任务状态和优先级标记正确
- [ ] 日期使用正确的格式
- [ ] 包含更新记录
- [ ] 相关文档引用正确
- [ ] 文档内容清晰、准确、完整

## 更新记录

| 版本 | 日期 | 更新者 | 更新内容 |
|------|------|--------|----------|
| 1.0.0 | 2025-04-29 | 小智 | 初始版本 |
| 1.1.0 | 2025-04-29 | Frank | 添加Git版本管理规则 |
