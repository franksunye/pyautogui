# 测试策略简述

## 测试重点

### 奖励确定函数测试
- **幸运数字奖励**: 测试不同合同编号和金额下的幸运数字奖励判定
- **节节高奖励**: 测试不同累计金额和合同数量下的节节高奖励判定
- **多重奖励**: 测试同时获得幸运数字和节节高奖励的情况
- **自动发放低级奖励**: 测试高金额合同自动发放低级别奖励的逻辑
- **边界条件**: 测试合同数量和金额在边界值附近的情况

### 数据处理函数测试
- **数据转换**: 测试合同数据到性能数据的转换
- **重复合同处理**: 测试对重复合同ID的处理
- **性能上限应用**: 测试性能金额上限的正确应用
- **工单金额累计**: 测试工单编号累计金额的计算
- **奖励状态更新**: 测试奖励状态的正确更新

### 通用函数测试
- **配置一致性**: 测试通用函数与特定函数的结果一致性
- **城市差异处理**: 测试对北京和上海差异的正确处理
- **错误处理**: 测试对无效输入的处理

## 测试数据管理

### 测试数据准备
- **模拟合同数据**: 创建包含各种场景的模拟合同数据
- **预设管家数据**: 准备不同状态的管家数据，覆盖各种奖励场景
- **边界值数据**: 特别准备边界条件的测试数据

### 测试数据存储
- **测试CSV文件**: 在tests目录下保存测试用CSV文件
- **测试数据版本控制**: 确保测试数据与代码版本匹配
- **测试数据隔离**: 测试数据与生产数据严格分离

## 常见测试案例

### 案例1: 幸运数字和节节高奖励同时获得
```python
def test_may_beijing_lucky_and_progressive_rewards(self):
    """测试5月北京活动同时获得幸运数字和节节高奖励"""
    # 设置管家数据，满足节节高奖励条件
    housekeeper_data = {
        'count': 6,  # 满足最低合同数量要求
        'total_amount': 85000,  # 达到达标奖阈值
        'performance_amount': 85000,  # 使用相同的绩效金额
        'awarded': []  # 尚未获得任何奖励
    }

    # 使用带有幸运数字6的合同编号和高于1万的合同金额
    reward_types, reward_names, gap = determine_rewards_may_beijing_generic(
        contract_number=16,  # 合同编号末位为6，触发幸运数字奖励
        housekeeper_data=housekeeper_data,
        current_contract_amount=15000  # 高于1万，触发高额幸运奖励
    )

    # 验证结果
    self.assertIn("幸运数字", reward_types)
    self.assertIn("接好运万元以上", reward_names)
    self.assertIn("节节高", reward_types)
    self.assertIn("达标奖", reward_names)
```

### 案例2: 高金额合同自动发放低级别奖励
```python
def test_may_beijing_auto_award_lower_tiers(self):
    """测试高金额合同自动发放低级别奖励"""
    # 设置管家数据，初始金额已经达到优秀奖阈值
    housekeeper_data = {
        'count': 6,  # 满足最低合同数量要求
        'total_amount': 130000,  # 已经达到优秀奖阈值(120000)
        'performance_amount': 130000,  # 使用相同的绩效金额
        'awarded': []  # 尚未获得任何奖励
    }

    # 使用不触发幸运数字的合同编号和普通合同金额
    reward_types, reward_names, gap = determine_rewards_may_beijing_generic(
        contract_number=11,  # 合同编号不触发幸运数字奖励
        housekeeper_data=housekeeper_data,
        current_contract_amount=5000  # 普通合同金额
    )

    # 验证结果
    self.assertIn("节节高", reward_types)
    self.assertIn("达标奖", reward_names)
    self.assertIn("优秀奖", reward_names)
```

### 案例3: 上海四档奖励测试
```python
def test_shanghai_four_tier_rewards(self):
    """测试上海活动四档奖励（基础奖、达标奖、优秀奖、精英奖）"""
    # 设置管家数据，满足基础奖条件
    housekeeper_data = {
        'count': 5,  # 满足最低合同数量要求（上海需要5个合同）
        'total_amount': 45000,  # 达到基础奖阈值
        'performance_amount': 45000,  # 使用相同的绩效金额
        'awarded': []  # 尚未获得任何奖励
    }

    # 调用奖励函数
    reward_types, reward_names, gap = determine_rewards_apr_shanghai_generic(
        contract_number=11,  # 合同编号不触发幸运数字奖励
        housekeeper_data=housekeeper_data,
        current_contract_amount=5000  # 普通合同金额
    )

    # 验证获得了基础奖
    self.assertEqual(reward_types, "节节高")
    self.assertEqual(reward_names, "基础奖")
    self.assertTrue("距离 达标奖 还需" in gap)
```

## 当前测试重点

当前重构工作中，测试重点是:

1. 为通用数据处理函数 (process_data_generic) 编写全面测试
2. 测试包装函数与原始函数的结果一致性
3. 测试功能标志的正确工作
4. 测试边界条件和特殊情况处理

所有新实现的函数必须通过现有测试，并且需要添加新测试覆盖新增功能和边界情况。

## 手动测试命令

在开发环境中，我们经常需要手动测试单个任务以验证其功能。以下是各种任务的手动测试命令。

### 基本命令格式

```bash
python main.py [--env dev|test|prod] [--run-once] [--task task_name]
```

参数说明：
- `--env`: 指定运行环境，可选值为 `dev`（开发环境，默认）、`test`（测试环境）或 `prod`（生产环境）
- `--run-once`: 运行一次后退出，不进入循环
- `--task`: 指定要运行的任务，可选值见下文

### 城市任务测试命令

#### 北京任务

```bash
# 北京5月任务
python main.py --task beijing-may --env dev
```

#### 上海任务

```bash
# 上海5月任务
python main.py --task shanghai-may --env dev
```

### 其他任务测试命令

```bash
# 技师状态检查
python main.py --task technician --env dev

# 日报服务
python main.py --task daily-report --env dev

# 运行所有任务一次
python main.py --task all --env dev
# 或
python main.py --run-once --env dev
```

### 数据库模式测试

要在数据库模式下测试，需要先修改 `modules/config.py` 中的配置：

```python
# 将此值设为 True 以使用数据库存储
USE_DATABASE_FOR_PERFORMANCE_DATA = True
```

然后运行相应的任务命令。测试完成后，可以将此值改回 `False` 以恢复使用文件存储。

### 清理测试数据

在开发环境中测试前，通常需要清理之前的测试数据：

1. 清理文件存储数据：
   - 删除或备份 `state/PerformanceData-*.csv` 文件

2. 清理数据库存储数据：
   - 使用 SQLite 命令行工具或 DB Browser for SQLite 等工具
   - 连接到数据库文件 `tasks.db`（位于项目根目录）
   - 执行 SQL 命令：`DELETE FROM performance_data WHERE campaign_id = 'XX-YYYY-MM'`
   - 或者针对测试数据：`DELETE FROM performance_data WHERE contract_id LIKE 'test_%'`

### 验证等价性测试

对于验证文件存储和数据库存储的等价性，可以使用以下命令：

```bash
# 北京5月数据等价性验证
python scripts/verify_beijing_may_equivalence.py

# 上海5月数据等价性验证
python scripts/verify_shanghai_may_equivalence.py

# 运行所有验证测试
python scripts/run_shanghai_may_verification.py
```

### 通知逻辑测试

要单独测试通知逻辑，可以使用以下命令：

```bash
# 北京5月通知逻辑测试
python scripts/verify_notification_equivalence.py

# 上海5月通知逻辑测试
python scripts/verify_shanghai_notification_equivalence.py
```

### 测试结果查看

测试结果通常保存在以下位置：
- 日志文件：`logs/app.log`
- 测试数据：`tests/test_data/`
- 验证报告：`tests/test_data/shanghai_may_verification_report.txt`

### 数据库结构与组织

项目使用 SQLite 数据库存储数据。主要的数据库文件是：

- `tasks.db`：位于项目根目录，用于存储生产数据
- `tests/tasks.db`：位于测试目录，用于存储测试数据

数据库中的主要表包括：

1. `performance_data`：存储签约台账数据
   - 包含合同信息、管家信息、奖励信息等
   - 用于替代原有的 CSV 文件存储方式

2. `tasks`：存储通知任务
   - 包含任务类型、接收人、消息内容、状态等
   - 用于跟踪消息发送状态

在开发和测试过程中，应确保使用正确的数据库文件。

### 数据库检查工具

在开发过程中，我们经常需要检查数据库中的数据。以下是一些有用的工具和命令：

#### SQLite 命令行工具

```bash
# 打开数据库
sqlite3 tasks.db

# 常用命令
.tables                                  # 显示所有表
.schema performance_data                 # 显示表结构
SELECT * FROM performance_data LIMIT 5;  # 查看前5条记录
SELECT COUNT(*) FROM performance_data;   # 统计记录数
SELECT campaign_id, COUNT(*) FROM performance_data GROUP BY campaign_id;  # 按活动统计

# 导出查询结果到CSV
.mode csv
.output query_results.csv
SELECT * FROM performance_data WHERE campaign_id = 'SH-2025-05';
.output stdout
```

#### Python 脚本查询

也可以创建简单的Python脚本来查询数据库：

```python
# 示例: query_db.py
import sqlite3
import sys

def query_db(query):
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # 打印列名
    if rows:
        print(','.join([k for k in rows[0].keys()]))

    # 打印数据
    for row in rows:
        print(','.join([str(row[k]) for k in row.keys()]))

    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query_db(sys.argv[1])
    else:
        print("Usage: python query_db.py \"SELECT * FROM performance_data LIMIT 5\"")
```

使用方法：
```bash
python query_db.py "SELECT * FROM performance_data WHERE campaign_id = 'SH-2025-05'"
```

#### 数据库备份与恢复

在进行重要测试前，建议备份数据库：

```bash
# 简单备份方法
copy tasks.db tasks.db.backup

# 恢复备份
copy tasks.db.backup tasks.db
```

也可以使用 SQLite 命令行工具进行备份：

```bash
# 备份数据库
sqlite3 tasks.db ".backup 'tasks.db.backup'"

# 恢复数据库
sqlite3 tasks.db.backup ".restore 'tasks.db'"
```

#### 数据库维护

定期维护数据库可以提高性能：

```bash
# 进入 SQLite 命令行
sqlite3 tasks.db

# 分析数据库
.analyze

# 优化数据库
VACUUM;
ANALYZE;

# 检查数据库完整性
PRAGMA integrity_check;
```

### 调试技巧

在开发和测试过程中，以下调试技巧可能会有所帮助：

#### 增加日志输出

临时增加日志输出是最简单的调试方法：

```python
import logging
logging.info(f"变量值: {variable}")
logging.debug(f"详细信息: {detailed_info}")
```

#### 使用 print 语句

在关键位置添加 print 语句可以快速查看变量值：

```python
print(f"处理合同: {contract_id}, 金额: {contract_amount}")
```

#### 使用断言

添加断言可以在开发阶段捕获意外情况：

```python
assert contract_amount > 0, f"合同金额不应为负: {contract_amount}"
```

#### 数据比较

比较文件存储和数据库存储的数据差异：

```python
# 文件数据
file_data = get_all_records_from_csv(performance_data_filename)

# 数据库数据
db_data = get_performance_data_by_campaign(campaign_id)

# 比较数据
for file_record in file_data:
    file_contract_id = file_record['合同ID(_id)']
    db_record = next((d for d in db_data if d.contract_id == file_contract_id), None)

    if db_record:
        # 比较关键字段
        if float(file_record['合同金额(adjustRefundMoney)']) != float(db_record.contract_amount):
            print(f"合同金额不一致: {file_contract_id}")
```

#### 模拟数据

创建模拟数据进行测试：

```python
test_data = [
    {
        '合同ID(_id)': 'test_001',
        '活动城市(province)': '110000',
        '工单编号(serviceAppointmentNum)': 'GD2025045001',
        '管家(serviceHousekeeper)': '张三',
        '合同编号(contractdocNum)': 'YHWX-BJ-JDHS-2025050001',
        '合同金额(adjustRefundMoney)': '25000.0',
        # 其他必要字段...
    }
]
```
