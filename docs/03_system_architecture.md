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

### 5. 任务管理系统 (task_manager.py)
- **功能**: 管理消息发送任务的创建和状态更新
- **关键组件**:
  - Task类：表示一个消息发送任务
  - 数据库交互函数：创建、更新和查询任务
  - 任务状态管理：跟踪任务的执行状态
- **关键函数**:
  - `create_task()`: 创建新的消息发送任务
  - `update_task()`: 更新任务状态
  - `get_pending_tasks()`: 获取待处理的任务

### 6. 任务调度器 (task_scheduler.py)
- **功能**: 调度和执行任务队列中的任务
- **关键组件**:
  - 任务检查循环：定期检查待处理任务
  - 任务执行线程：在后台执行任务
  - 任务锁机制：确保任务顺序执行

### 7. 请求模块 (modules/request_module.py)
- **功能**: 处理与外部系统的HTTP请求
- **关键函数**:
  - `get_metabase_session`: 获取Metabase会话
  - `send_request_with_managed_session`: 发送带会话管理的请求

### 8. 文件工具 (modules/file_utils.py)
- **功能**: 处理文件读写操作
- **关键函数**:
  - `get_all_records_from_csv`: 从CSV文件读取记录
  - `write_data_to_csv`: 将数据写入CSV文件
  - `write_performance_data_to_csv`: 将业绩数据写入CSV文件

### 9. 消息发送模块 (modules/message_sender.py)
- **功能**: 处理实际的消息发送操作
- **关键函数**:
  - `send_wechat_message`: 发送微信消息
  - `send_wecom_message`: 发送企业微信消息

### 10. 日志配置 (modules/log_config.py)
- **功能**: 配置日志系统
- **关键功能**:
  - 设置日志级别
  - 配置日志格式
  - 设置日志输出目标

## 数据流

### 1. 数据获取流程
```
Metabase API -> request_module.py -> 临时CSV文件
```

### 2. 数据处理流程
```
临时CSV文件 -> data_processing_module.py -> 业绩数据CSV文件
```

### 3. 通知发送流程
```
业绩数据CSV文件 -> notification_module.py -> task_manager.py -> task_scheduler.py -> message_sender.py -> 企业微信API/微信
```

### 4. 任务调度流程
```
main.py -> jobs.py -> task_scheduler.py -> 各功能模块
```

## 数据存储

### 1. 文件存储
- **合同数据**: 存储在CSV文件中
- **业绩数据**: 存储在CSV文件中，包含消息发送状态标记

### 2. 数据库存储
- **SQLite数据库**: 用于存储任务和历史数据
- **表结构**:
  - `tasks`: 存储消息发送任务
    - `id`: 任务ID
    - `task_type`: 任务类型（如'send_wechat_message'或'send_wecom_message'）
    - `recipient`: 接收者
    - `message`: 消息内容
    - `status`: 任务状态（'pending'、'completed'等）
    - `created_at`: 创建时间
    - `updated_at`: 更新时间

## 外部依赖

### 1. Metabase
- **用途**: 数据源，提供合同和业绩数据
- **交互方式**: 通过HTTP API获取数据

### 2. 企业微信
- **用途**: 通知渠道，发送奖励通知
- **交互方式**: 通过Webhook发送消息

### 3. Streamlit
- **用途**: 数据可视化和仪表板
- **交互方式**: 通过Web界面展示数据

## 部署架构

### 开发环境
- **操作系统**: Windows/Linux
- **Python版本**: 3.8+
- **依赖管理**: requirements.txt

### 生产环境
- **操作系统**: Windows Server
- **部署方式**: 服务方式运行
- **监控**: 日志文件和错误报告

## 安全考虑

### 1. 敏感信息保护
- **凭据管理**: 使用环境变量存储敏感信息
- **日志脱敏**: 确保日志中不包含敏感信息

### 2. 错误处理
- **异常捕获**: 全面的异常处理机制
- **错误日志**: 详细记录错误信息
- **恢复机制**: 任务失败后的重试机制

## 扩展性设计

### 1. 新城市/活动支持
- **配置驱动**: 通过配置文件添加新城市或活动
- **通用函数**: 使用通用处理函数支持不同规则

### 2. 新功能集成
- **模块化设计**: 便于添加新功能模块
- **插件架构**: 支持功能扩展

## 性能考虑

### 1. 资源使用
- **内存管理**: 控制数据处理的内存使用
- **CPU使用**: 优化计算密集型操作

### 2. 响应时间
- **异步处理**: 使用异步方式处理耗时操作
- **批处理**: 批量处理数据减少API调用
