# 签约台账数据库化系统操作手册

## 文档信息
**文档类型**: 操作手册
**文档编号**: performance_data_db-MANUAL-001
**版本**: 1.0.0
**创建日期**: 2025-05-07
**最后更新**: 2025-05-07
**状态**: 草稿
**负责人**: Frank
**团队成员**: Frank & AI助手

**相关文档**:
- [项目计划](./performance_data_db_01_PLAN_migration.md)
- [技术总结](./performance_data_db_04_TECHNICAL_summary.md)
- [部署计划](./performance_data_db_05_DEPLOYMENT_plan.md)

## 1. 系统概述

签约台账数据库化系统是一个用于管理签约台账数据的应用程序。系统支持两种存储模式：文件存储和数据库存储。本手册主要介绍数据库存储模式下的操作方法。

## 2. 系统要求

- **操作系统**: Windows
- **Python版本**: 3.8+
- **数据库**: SQLite 3
- **依赖库**: 见requirements.txt

## 3. 系统安装

### 3.1 安装步骤

1. **克隆代码库**
   ```bash
   git clone https://github.com/franksunye/pyautogui.git
   cd pyautogui
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **创建数据库表**
   ```bash
   python scripts/create_performance_data_table.py
   ```

4. **配置系统**
   编辑`modules/config.py`文件，设置`USE_DATABASE_FOR_PERFORMANCE_DATA = True`启用数据库存储模式。

## 4. 系统配置

### 4.1 存储模式配置

在`modules/config.py`文件中，可以通过以下配置项控制存储模式：

```python
# 使用数据库存储
USE_DATABASE_FOR_PERFORMANCE_DATA = True

# 使用文件存储
USE_DATABASE_FOR_PERFORMANCE_DATA = False
```

### 4.2 数据库配置

数据库配置在`modules/db_config.py`文件中：

```python
# 数据库文件路径
DATABASE_PATH = 'tasks.db'

# 数据库连接超时时间
DATABASE_TIMEOUT = 30
```

### 4.3 日志配置

日志配置在`modules/log_config.py`文件中：

```python
# 日志级别
LOG_LEVEL = logging.INFO

# 日志文件路径
LOG_FILE = 'logs/app.log'
```

## 5. 基本操作

### 5.1 启动系统

```bash
python main.py
```

### 5.2 运行特定任务

```bash
# 运行北京5月签约和奖励播报任务
python main.py --job signing_and_sales_incentive_may_beijing

# 运行上海5月签约和奖励播报任务
python main.py --job signing_and_sales_incentive_may_shanghai
```

### 5.3 切换存储模式

1. 编辑`modules/config.py`文件
2. 修改`USE_DATABASE_FOR_PERFORMANCE_DATA`的值
3. 重启系统

## 6. 数据管理

### 6.1 数据查询

可以使用以下脚本查询数据：

```bash
# 查询所有数据
python scripts/query_performance_data.py --all

# 按活动ID查询
python scripts/query_performance_data.py --campaign BJ-2025-05

# 按管家查询
python scripts/query_performance_data.py --housekeeper 石王磊

# 按合同ID查询
python scripts/query_performance_data.py --contract test_001
```

### 6.2 数据导出

可以使用以下脚本导出数据：

```bash
# 导出所有数据
python scripts/export_performance_data.py --all --output all_data.csv

# 按活动ID导出
python scripts/export_performance_data.py --campaign BJ-2025-05 --output bj_may_data.csv
```

### 6.3 数据备份

可以使用以下脚本备份数据库：

```bash
# 备份数据库
python scripts/backup_database.py --output backup_20250507.db
```

### 6.4 数据恢复

可以使用以下脚本恢复数据库：

```bash
# 恢复数据库
python scripts/restore_database.py --input backup_20250507.db
```

## 7. 任务调度

### 7.1 定时任务

系统支持以下定时任务：

| 任务名称 | 描述 | 默认调度 |
|---------|------|----------|
| signing_and_sales_incentive_may_beijing | 北京5月签约和奖励播报 | 每天9:00 |
| signing_and_sales_incentive_may_shanghai | 上海5月签约和奖励播报 | 每天9:30 |
| signing_and_sales_incentive_apr_beijing | 北京4月签约和奖励播报 | 每天10:00 |
| signing_and_sales_incentive_apr_shanghai | 上海4月签约和奖励播报 | 每天10:30 |

### 7.2 手动触发任务

可以使用以下命令手动触发任务：

```bash
# 触发北京5月签约和奖励播报任务
python main.py --job signing_and_sales_incentive_may_beijing

# 触发上海5月签约和奖励播报任务
python main.py --job signing_and_sales_incentive_may_shanghai
```

## 8. 监控与维护

### 8.1 日志查看

系统日志保存在`logs/app.log`文件中，可以使用以下命令查看：

```bash
# 查看最新的100行日志
tail -n 100 logs/app.log

# 实时查看日志
tail -f logs/app.log
```

### 8.2 数据库维护

定期维护数据库可以提高系统性能：

```bash
# 优化数据库
python scripts/optimize_database.py
```

### 8.3 性能监控

可以使用以下脚本监控系统性能：

```bash
# 监控数据库性能
python scripts/monitor_database_performance.py
```

## 9. 故障排除

### 9.1 常见问题

1. **系统无法启动**
   - 检查Python版本是否正确
   - 检查依赖库是否安装完整
   - 检查配置文件是否正确

2. **数据库连接失败**
   - 检查数据库文件是否存在
   - 检查数据库文件权限
   - 检查数据库是否被锁定

3. **任务执行失败**
   - 检查日志文件查看错误信息
   - 检查网络连接是否正常
   - 检查API是否可用

### 9.2 错误代码

| 错误代码 | 描述 | 解决方法 |
|---------|------|----------|
| E001 | 数据库连接失败 | 检查数据库文件和权限 |
| E002 | API请求失败 | 检查网络连接和API状态 |
| E003 | 数据处理失败 | 检查日志文件查看详细错误信息 |
| E004 | 通知发送失败 | 检查网络连接和通知配置 |

## 10. 常见操作示例

### 10.1 查看数据库中的签约台账数据

```python
from modules.performance_data_manager import get_all_performance_data

# 获取所有数据
all_data = get_all_performance_data()

# 打印数据
for data in all_data:
    print(f"合同ID: {data.contract_id}, 管家: {data.housekeeper}, 合同金额: {data.contract_amount}")
```

### 10.2 添加新的签约台账数据

```python
from modules.performance_data_manager import PerformanceData

# 创建新数据
new_data = PerformanceData(
    campaign_id="BJ-2025-05",
    contract_id="manual_001",
    province_code="110000",
    housekeeper="手动添加",
    contract_doc_num="YHWX-BJ-JDHS-2025050999",
    contract_amount=30000.0,
    paid_amount=15000.0,
    difference=15000.0,
    create_time="2025-05-07T11:36:22.444+08:00",
    org_name="北京久盾宏盛建筑工程有限公司",
    signed_date="2025-05-07T11:42:07.904+08:00"
)

# 保存数据
new_data.save()
```

### 10.3 更新签约台账数据

```python
from modules.performance_data_manager import get_performance_data_by_contract_id

# 获取数据
data = get_performance_data_by_contract_id("manual_001")

# 更新数据
if data:
    data.contract_amount = 35000.0
    data.paid_amount = 17500.0
    data.difference = 17500.0
    data.save()
```

### 10.4 删除签约台账数据

```python
from modules.performance_data_manager import get_performance_data_by_contract_id, delete_performance_data

# 获取数据
data = get_performance_data_by_contract_id("manual_001")

# 删除数据
if data:
    delete_performance_data(data.id)
```

## 11. 联系与支持

如有问题或需要支持，请联系：

- **项目负责人**: Frank
- **技术支持**: AI助手
