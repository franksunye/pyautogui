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

### 2. 数据处理模块
#### 2.1 传统数据处理 (modules/data_processing_module.py)
- **功能**: 处理合同数据，计算奖励（传统实现）
- **关键函数**:
  - `process_data_apr_beijing`: 处理北京4月数据
  - `process_data_may_beijing`: 处理北京5月数据
  - `process_data_shanghai_apr`: 处理上海4月数据
  - `process_data_may_shanghai`: 处理上海5月数据

#### 2.2 通用数据处理 (modules/data_processing_generic.py)
- **功能**: 提供通用的数据处理框架，支持所有城市和月份
- **关键函数**:
  - `process_data_generic`: 通用数据处理函数，支持文件存储和数据库存储
  - `process_data_apr_beijing_generic`: 北京4月包装函数
  - `process_data_may_beijing_generic`: 北京5月包装函数
  - `process_data_apr_shanghai_generic`: 上海4月包装函数
  - `process_data_may_shanghai_generic`: 上海5月包装函数
  - `process_beijing_data_to_db_generic`: 北京数据库处理包装函数
  - `process_shanghai_data_to_db_generic`: 上海数据库处理包装函数

### 3. 奖励计算模块 (modules/reward_calculation.py)
- **功能**: 独立的奖励计算模块，提供通用的奖励计算功能
- **关键函数**:
  - `determine_rewards_generic`: 通用奖励确定函数，基于配置确定奖励类型和名称
  - `determine_rewards_apr_beijing_generic`: 北京4月奖励确定函数
  - `determine_rewards_may_beijing_generic`: 北京5月奖励确定函数
  - `determine_rewards_apr_shanghai_generic`: 上海4月奖励确定函数
  - `determine_rewards_may_shanghai_generic`: 上海5月奖励确定函数

### 4. 配置系统 (modules/config.py)
- **功能**: 集中管理所有配置项
- **关键配置**:
  - `REWARD_CONFIGS`: 各城市各月份的奖励规则配置
  - `USE_DATABASE_FOR_PERFORMANCE_DATA`: 控制是否使用数据库存储签约台账数据
  - `USE_GENERIC_PROCESS_FUNCTION`: 控制是否使用通用数据处理函数
  - 性能上限和阈值配置

### 5. 通知模块 (modules/notification_module.py)
- **功能**: 发送奖励通知到企业微信
- **关键函数**:
  - `notify_awards_apr_beijing`: 发送北京4月奖励通知
  - `notify_awards_shanghai_generate_message_march`: 发送上海奖励通知

### 6. 任务管理系统 (task_manager.py)
- **功能**: 管理消息发送任务的创建和状态更新
- **关键组件**:
  - Task类：表示一个消息发送任务
  - 数据库交互函数：创建、更新和查询任务
  - 任务状态管理：跟踪任务的执行状态
- **关键函数**:
  - `create_task()`: 创建新的消息发送任务
  - `update_task()`: 更新任务状态
  - `get_pending_tasks()`: 获取待处理的任务

### 7. 任务调度器 (task_scheduler.py)
- **功能**: 调度和执行任务队列中的任务
- **关键组件**:
  - 任务检查循环：定期检查待处理任务
  - 任务执行线程：在后台执行任务
  - 任务锁机制：确保任务顺序执行

### 8. 请求模块 (modules/request_module.py)
- **功能**: 处理与外部系统的HTTP请求
- **关键函数**:
  - `get_metabase_session`: 获取Metabase会话
  - `send_request_with_managed_session`: 发送带会话管理的请求

### 9. 文件工具 (modules/file_utils.py)
- **功能**: 处理文件读写操作
- **关键函数**:
  - `get_all_records_from_csv`: 从CSV文件读取记录
  - `write_data_to_csv`: 将数据写入CSV文件
  - `write_performance_data_to_csv`: 将业绩数据写入CSV文件

### 10. 数据库工具 (modules/db_utils.py)
- **功能**: 处理数据库操作
- **关键函数**:
  - `init_db`: 初始化数据库和表结构
  - `save_performance_data_to_db`: 将业绩数据保存到数据库
  - `get_performance_data_from_db`: 从数据库获取业绩数据
  - `check_contract_exists`: 检查合同是否已存在于数据库

### 11. 消息发送模块 (modules/message_sender.py)
- **功能**: 处理实际的消息发送操作
- **关键函数**:
  - `send_wechat_message`: 发送微信消息
  - `send_wecom_message`: 发送企业微信消息

### 12. 日志配置 (modules/log_config.py)
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

### 2. 数据处理流程（传统文件存储模式）
```
临时CSV文件 -> data_processing_module.py -> 业绩数据CSV文件
```

### 3. 数据处理流程（传统数据库存储模式）
```
临时CSV文件 -> data_processing_module.py -> SQLite数据库(performance_data表)
```

### 4. 数据处理流程（通用文件存储模式）
```
临时CSV文件 -> data_processing_generic.py -> reward_calculation.py -> 业绩数据CSV文件
```

### 5. 数据处理流程（通用数据库存储模式）
```
临时CSV文件 -> data_processing_generic.py -> reward_calculation.py -> SQLite数据库(performance_data表)
```

### 6. 通知发送流程（文件存储模式）
```
业绩数据CSV文件 -> notification_module.py -> task_manager.py -> task_scheduler.py -> message_sender.py -> 企业微信API/微信
```

### 7. 通知发送流程（数据库存储模式）
```
SQLite数据库(performance_data表) -> notification_module.py -> task_manager.py -> task_scheduler.py -> message_sender.py -> 企业微信API/微信
```

### 8. 任务调度流程
```
main.py -> jobs.py -> task_scheduler.py -> 各功能模块
```

## 数据存储

### 1. 文件存储
- **合同数据**: 存储在CSV文件中（传统方式）
- **业绩数据**: 存储在CSV文件中，包含消息发送状态标记（传统方式）

### 2. 数据库存储
- **SQLite数据库**: 用于存储任务和历史数据以及签约台账数据
- **表结构**:
  - `tasks`: 存储消息发送任务
    - `id`: 任务ID
    - `task_type`: 任务类型（如'send_wechat_message'或'send_wecom_message'）
    - `recipient`: 接收者
    - `message`: 消息内容
    - `status`: 任务状态（'pending'、'completed'等）
    - `created_at`: 创建时间
    - `updated_at`: 更新时间
  - `performance_data`: 存储签约台账数据
    - `id`: 记录ID
    - `contract_id`: 合同ID
    - `city`: 城市（如'北京'、'上海'）
    - `month`: 月份（如'2025-04'、'2025-05'）
    - `housekeeper`: 管家姓名
    - `contract_amount`: 合同金额
    - `performance_amount`: 计入业绩的金额
    - `contract_number`: 合同编号
    - `service_appointment`: 工单编号
    - `service_provider`: 服务商
    - `lucky_reward`: 幸运数字奖励
    - `progressive_reward`: 节节高奖励
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
- **配置驱动**: 通过在 `REWARD_CONFIGS` 中添加新城市或活动的配置
- **通用函数**: 使用 `determine_rewards_generic` 和 `process_data_generic` 支持不同规则
- **包装函数**: 创建新的包装函数，如 `process_data_jun_beijing_generic`，调用通用函数并传入特定参数

### 2. 存储方式选择
- **配置驱动**: 通过配置项 `USE_DATABASE_FOR_PERFORMANCE_DATA` 选择文件存储或数据库存储
- **功能等价**: 通过 `process_data_generic` 确保两种存储方式功能完全等价
- **平滑过渡**: 支持在不同存储方式间平滑切换
- **并行验证**: 通过并行测试验证两种存储方式的功能等价性

### 3. 新功能集成
- **模块化设计**: 便于添加新功能模块
- **插件架构**: 支持功能扩展
- **功能标志**: 通过配置项 `USE_GENERIC_PROCESS_FUNCTION` 控制是否使用新实现
- **独立模块**: 奖励计算和数据处理功能分离，便于单独升级和测试

## 性能考虑

### 1. 资源使用
- **内存管理**: 控制数据处理的内存使用
- **CPU使用**: 优化计算密集型操作
- **存储效率**: 数据库存储比文件存储更节省空间

### 2. 响应时间
- **异步处理**: 使用异步方式处理耗时操作
- **批处理**: 批量处理数据减少API调用
- **查询优化**: 数据库索引提高查询性能

### 3. 数据库性能
- **索引优化**: 为常用查询字段创建索引
- **批量操作**: 使用事务和批量插入提高性能
- **连接池**: 管理数据库连接减少开销
