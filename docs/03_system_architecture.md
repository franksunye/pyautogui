# 系统架构概览

## 程序入口

### 主程序入口 (main.py)
- **功能**: 系统的主要执行入口，初始化和启动所有组件
- **关键职责**:
  - 初始化日志系统
  - 定义并调度定时任务
  - 启动任务调度器线程
  - 维护主循环，确保程序持续运行
- **执行方式**: 通过 `python main.py` 或 `start.bat` 启动

### 可视化仪表板入口 (streamlit_app/app.py)
- **功能**: Streamlit数据可视化仪表板的入口
- **关键职责**:
  - 展示业绩数据和奖励统计
  - 提供数据筛选和分析功能
- **执行方式**: 通过 `streamlit run streamlit_app/app.py` 或 `run_streamlit.bat` 启动

## 核心组件

### 1. 作业系统 (jobs.py)
- **功能**: 定义并执行定时任务，如签约奖励计算和通知发送
- **关键任务**:
  - `signing_and_sales_incentive_apr_beijing`: 北京4月签约奖励活动
  - `signing_and_sales_incentive_may_beijing`: 北京5月签约奖励活动
  - `signing_and_sales_incentive_may_shanghai`: 上海5月签约奖励活动
  - `check_technician_status`: 技师状态检查
  - `generate_daily_service_report`: 生成日常服务报告

### 2. 数据处理模块 (modules/data_processing_module.py)
- **功能**: 处理合同数据，计算奖励
- **关键函数**:
  - `determine_rewards_generic`: 通用奖励确定函数
  - `process_data_apr_beijing`: 处理北京4月数据
  - `process_data_shanghai_apr`: 处理上海4月数据

### 3. 配置系统 (modules/config.py)
- **功能**: 集中管理所有配置项
- **关键配置**:
  - `REWARD_CONFIGS`: 各城市各月份的奖励规则配置
  - 性能上限和阈值配置

### 4. 通知模块 (modules/notification_module.py)
- **功能**: 发送奖励通知到企业微信
- **关键函数**:
  - `notify_awards_apr_beijing`: 发送北京4月奖励通知
  - `notify_awards_shanghai_generate_message_march`: 发送上海奖励通知

### 5. 任务调度器 (task_scheduler.py)
- **功能**: 管理和执行任务队列
- **关键组件**:
  - 任务检查循环
  - 任务执行函数

### 6. 任务管理系统 (task_manager.py)
- **功能**: 管理任务的创建、更新和查询
- **关键函数**:
  - `create_task`: 创建新任务
  - `update_task`: 更新任务状态
  - `get_pending_tasks`: 获取待处理任务

### 7. 日志系统 (modules/log_config.py)
- **功能**: 配置和管理系统日志
- **关键特性**:
  - 分级日志记录 (DEBUG, INFO, ERROR)
  - 日志轮转 (RotatingFileHandler)
  - 环境感知 (开发/生产环境不同日志级别)
  - 专用日志通道 (应用日志、消息发送日志)

### 8. SLA监控系统 (modules/service_provider_sla_monitor.py)
- **功能**: 监控服务商SLA违规情况并发送通知
- **关键功能**:
  - 违规记录管理
  - 每日违规通知
  - 每周SLA报告
  - 合规服务商表扬

## 执行流程

### 主程序执行流程

```
初始化日志系统 → 创建定时任务 → 启动任务调度器线程 → 进入主循环 → 执行待处理任务
```

1. **初始化**: main.py启动时初始化日志系统和锁机制
2. **任务定义**: 定义run_jobs_serially和daily_service_report_task等定时任务
3. **任务调度**: 使用schedule库设置任务执行时间和频率
4. **线程启动**: 启动任务调度器线程，处理数据库中的任务
5. **主循环**: 进入无限循环，定期检查和执行schedule中的任务

### 数据处理流程

```
外部API → 数据获取 → 数据处理 → 结果存储 → 任务创建 → 通知发送
```

1. **数据获取**: 从Metabase API获取合同数据
2. **数据处理**: 应用奖励规则计算奖励
3. **结果存储**: 将处理结果保存到CSV文件
4. **任务创建**: 将通知任务存储到SQLite数据库
5. **通知发送**: 任务调度器执行任务，向相关人员发送通知

## 关键技术

- **Python**: 核心开发语言
- **SQLite**: 任务管理数据库，存储通知任务
- **Streamlit**: 用于数据可视化仪表板
- **Schedule**: 任务调度库，用于定时任务调度
- **Threading**: 多线程处理，用于并行执行任务调度器
- **CSV文件**: 合同和业绩数据存储方式
- **Pandas**: 数据处理和分析
- **企业微信API**: 通知发送渠道
- **PyAutoGUI**: 自动化操作，用于某些通知发送场景
- **Logging**: 分级日志系统，用于监控和调试
- **Requests**: HTTP客户端，用于API调用
- **JSON/CSV处理**: 数据序列化和存储

## 数据存储架构

系统使用混合数据存储策略:

1. **SQLite数据库**:
   - 存储任务队列数据
   - 表结构: `tasks` 表包含 id, task_type, recipient, message, status, created_at, updated_at 字段
   - 用于任务的持久化和状态跟踪

2. **CSV文件**:
   - 存储合同数据和业绩数据
   - 用于数据分析和报表生成
   - 支持历史数据归档

3. **JSON文件**:
   - 存储状态记录和配置数据
   - 用于跟踪通知发送状态和SLA违规记录

## 错误处理与监控

系统采用多层次的错误处理和监控策略:

1. **异常捕获与日志记录**:
   - 所有关键操作都包含在try-except块中
   - 异常详细信息记录到日志文件
   - 使用traceback模块记录完整的错误堆栈

2. **任务隔离**:
   - 每个任务在独立的try-except块中执行
   - 单个任务失败不影响其他任务执行
   - 使用锁机制防止任务并发执行导致的冲突

3. **状态跟踪**:
   - 任务执行状态持久化到数据库
   - 通知发送状态记录到JSON文件
   - SLA违规记录持久化存储和定期报告

4. **自动恢复机制**:
   - 会话过期自动重新获取
   - 任务执行失败后延时重试
   - 主循环异常捕获确保程序持续运行

## 当前重构重点

当前正在进行奖励系统重构，主要目标是:
1. 统一北京和上海的数据处理函数
2. 创建通用数据处理框架
3. 提高代码可维护性和可扩展性
4. 优化数据库使用，考虑扩展SQLite的应用范围
5. 增强错误处理和监控能力

重构采用渐进式方法，先实现通用奖励确定函数，再实现通用数据处理函数，确保系统稳定运行。
