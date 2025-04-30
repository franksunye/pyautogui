# 环境变量结构设计

## 文档信息
**文档类型**: 技术文档
**文档编号**: sensitive_information-DOC-002
**版本**: 1.0.0
**创建日期**: 2025-04-29
**最后更新**: 2025-04-29
**状态**: 草稿
**负责人**: Frank
**团队成员**: Frank, 小智

**相关文档**:
- [敏感信息保护计划](./sensitive_information_01_PLAN_protection.md) (sensitive_information-PLAN-001)
- [敏感信息保护任务清单](./sensitive_information_03_TASK_protection.md) (sensitive_information-TASK-001)
- [敏感信息清单](./sensitive_information_inventory.md) (sensitive_information-DOC-001)

## 1. 概述

本文档定义了项目中环境变量的命名规范和组织结构，以确保敏感信息的安全管理和系统配置的一致性。良好的环境变量结构有助于提高代码的可维护性和安全性。

## 2. 环境变量命名规范

### 2.1 基本规则

1. 使用大写字母和下划线
2. 使用有意义的名称，避免缩写（除非是广泛接受的缩写）
3. 使用前缀区分不同类型的环境变量
4. 相关的环境变量应使用相同的前缀
5. 避免使用特殊字符（除了下划线）

### 2.2 前缀定义

| 前缀 | 描述 | 示例 |
|------|------|------|
| `METABASE_` | Metabase相关配置 | `METABASE_URL`, `METABASE_USERNAME` |
| `WECOM_` | 企业微信相关配置 | `WECOM_WEBHOOK_DEFAULT` |
| `API_` | API端点 | `API_URL_TS` |
| `SECURITY_` | 安全相关配置 | `SECURITY_SESSION_KEY` |
| `DB_` | 数据库相关配置 | `DB_PATH` |
| `FILE_` | 文件路径相关配置 | `FILE_TEMP_CONTRACT_DATA_BJ_APR` |
| `CONTACT_` | 联系人相关配置 | `CONTACT_PHONE_NUMBER` |
| `CONFIG_` | 一般配置项 | `CONFIG_TASK_CHECK_INTERVAL` |
| `FEATURE_` | 功能标志 | `FEATURE_ENABLE_BADGE_MANAGEMENT` |

### 2.3 命名模式

对于特定城市和时间的配置，使用以下模式：

```
[前缀]_[城市代码]_[年份]_[月份]_[描述]
```

例如：
- `API_URL_BJ_2025_04` 代表北京2025年4月的API URL
- `WECOM_GROUP_NAME_SH_2025_05` 代表上海2025年5月的企业微信群名称

## 3. 环境变量分组

### 3.1 认证凭据

| 环境变量 | 描述 | 原配置变量 |
|----------|------|------------|
| `METABASE_USERNAME` | Metabase用户名 | `METABASE_USERNAME` |
| `METABASE_PASSWORD` | Metabase密码 | `METABASE_PASSWORD` |
| `SECURITY_SESSION_KEY` | 会话加密密钥 | 新增 |

### 3.2 API端点

| 环境变量 | 描述 | 原配置变量 |
|----------|------|------------|
| `METABASE_URL` | Metabase基础URL | `METABASE_URL` |
| `API_URL_TS` | 技师状态检查API URL | `API_URL_TS` |
| `API_URL_CONTACT_TIMEOUT` | 工单联络超时提醒API URL | `API_URL_CONTACT_TIMEOUT` |
| `API_URL_SH_2025_04` | 上海2025年4月活动API URL | `API_URL_SH_APR` |
| `API_URL_SH_2025_05` | 上海2025年5月活动API URL | `API_URL_SH_MAY` |
| `API_URL_BJ_2025_04` | 北京2025年4月活动API URL | `API_URL_BJ_APR` |
| `API_URL_BJ_2025_05` | 北京2025年5月活动API URL | `API_URL_BJ_MAY` |
| `API_URL_DAILY_SERVICE_REPORT` | 每日服务报告API URL | `API_URL_DAILY_SERVICE_REPORT` |

### 3.3 Webhook URLs

| 环境变量 | 描述 | 原配置变量 |
|----------|------|------------|
| `WECOM_WEBHOOK_DEFAULT` | 默认企业微信Webhook URL | `WEBHOOK_URL_DEFAULT` |
| `WECOM_WEBHOOK_CONTACT_TIMEOUT` | 工单联络超时提醒Webhook URL | `WEBHOOK_URL_CONTACT_TIMEOUT` |

### 3.4 文件路径

| 环境变量 | 描述 | 原配置变量 |
|----------|------|------------|
| `FILE_TEMP_CONTRACT_DATA_SH_2025_04` | 上海2025年4月合同数据临时文件 | `TEMP_CONTRACT_DATA_FILE_SH_APR` |
| `FILE_PERFORMANCE_DATA_SH_2025_04` | 上海2025年4月业绩数据文件 | `PERFORMANCE_DATA_FILENAME_SH_APR` |
| `FILE_STATUS_SH_2025_04` | 上海2025年4月发送状态文件 | `STATUS_FILENAME_SH_APR` |
| `FILE_TEMP_CONTRACT_DATA_SH_2025_05` | 上海2025年5月合同数据临时文件 | `TEMP_CONTRACT_DATA_FILE_SH_MAY` |
| `FILE_PERFORMANCE_DATA_SH_2025_05` | 上海2025年5月业绩数据文件 | `PERFORMANCE_DATA_FILENAME_SH_MAY` |
| `FILE_STATUS_SH_2025_05` | 上海2025年5月发送状态文件 | `STATUS_FILENAME_SH_MAY` |
| `FILE_TEMP_CONTRACT_DATA_BJ_2025_04` | 北京2025年4月合同数据临时文件 | `TEMP_CONTRACT_DATA_FILE_BJ_APR` |
| `FILE_PERFORMANCE_DATA_BJ_2025_04` | 北京2025年4月业绩数据文件 | `PERFORMANCE_DATA_FILENAME_BJ_APR` |
| `FILE_STATUS_BJ_2025_04` | 北京2025年4月发送状态文件 | `STATUS_FILENAME_BJ_APR` |
| `FILE_TEMP_CONTRACT_DATA_BJ_2025_05` | 北京2025年5月合同数据临时文件 | `TEMP_CONTRACT_DATA_FILE_BJ_MAY` |
| `FILE_PERFORMANCE_DATA_BJ_2025_05` | 北京2025年5月业绩数据文件 | `PERFORMANCE_DATA_FILENAME_BJ_MAY` |
| `FILE_STATUS_BJ_2025_05` | 北京2025年5月发送状态文件 | `STATUS_FILENAME_BJ_MAY` |
| `FILE_TEMP_DAILY_SERVICE_REPORT` | 每日服务报告临时文件 | `TEMP_DAILY_SERVICE_REPORT_FILE` |
| `FILE_DAILY_SERVICE_REPORT_RECORD` | 每日服务报告记录文件 | `DAILY_SERVICE_REPORT_RECORD_FILE` |
| `FILE_SLA_VIOLATIONS_RECORDS` | SLA违规记录文件 | `SLA_VIOLATIONS_RECORDS_FILE` |
| `FILE_SESSION` | 会话信息文件 | `SESSION_FILE` (在request_module.py中) |

### 3.5 联系人信息

| 环境变量 | 描述 | 原配置变量 |
|----------|------|------------|
| `CONTACT_PHONE_NUMBER` | 联系电话 | `PHONE_NUMBER` |
| `CONTACT_WECOM_GROUP_NAME_SH_2025_04` | 上海2025年4月企业微信群名称 | `WECOM_GROUP_NAME_SH_APR` |
| `CONTACT_CAMPAIGN_CONTACT_SH_2025_04` | 上海2025年4月活动联系人 | `CAMPAIGN_CONTACT_SH_APR` |
| `CONTACT_WECOM_GROUP_NAME_SH_2025_05` | 上海2025年5月企业微信群名称 | `WECOM_GROUP_NAME_SH_MAY` |
| `CONTACT_CAMPAIGN_CONTACT_SH_2025_05` | 上海2025年5月活动联系人 | `CAMPAIGN_CONTACT_SH_MAY` |
| `CONTACT_WECOM_GROUP_NAME_BJ_2025_04` | 北京2025年4月企业微信群名称 | `WECOM_GROUP_NAME_BJ_APR` |
| `CONTACT_CAMPAIGN_CONTACT_BJ_2025_04` | 北京2025年4月活动联系人 | `CAMPAIGN_CONTACT_BJ_APR` |
| `CONTACT_WECOM_GROUP_NAME_BJ_2025_05` | 北京2025年5月企业微信群名称 | `WECOM_GROUP_NAME_BJ_MAY` |
| `CONTACT_CAMPAIGN_CONTACT_BJ_2025_05` | 北京2025年5月活动联系人 | `CAMPAIGN_CONTACT_BJ_MAY` |

### 3.6 配置项

| 环境变量 | 描述 | 原配置变量 |
|----------|------|------------|
| `CONFIG_TASK_CHECK_INTERVAL` | 任务调度器检查间隔（秒） | `TASK_CHECK_INTERVAL` |
| `CONFIG_RUN_JOBS_SERIALLY_SCHEDULE` | 串行执行作业的间隔（分钟） | `RUN_JOBS_SERIALLY_SCHEDULE` |
| `CONFIG_SESSION_DURATION` | 会话持续时间（秒） | `SESSION_DURATION` (在request_module.py中) |
| `CONFIG_BONUS_POOL_RATIO` | 奖金池计算比例 | `BONUS_POOL_RATIO` |
| `CONFIG_BONUS_POOL_RATIO_BJ_2025_02` | 北京2025年2月奖金池计算比例 | `BONUS_POOL_RATIO_BJ_FEB` |
| `CONFIG_PERFORMANCE_AMOUNT_CAP` | 上海单个合同计入业绩金额上限 | `PERFORMANCE_AMOUNT_CAP` |
| `CONFIG_ENABLE_PERFORMANCE_AMOUNT_CAP` | 上海是否启用业绩金额上限 | `ENABLE_PERFORMANCE_AMOUNT_CAP` |
| `CONFIG_PERFORMANCE_AMOUNT_CAP_BJ_2025_02` | 北京2025年2月单个合同计入业绩金额上限 | `PERFORMANCE_AMOUNT_CAP_BJ_FEB` |
| `CONFIG_ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_2025_02` | 北京2025年2月是否启用业绩金额上限 | `ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_FEB` |
| `CONFIG_SINGLE_PROJECT_CONTRACT_AMOUNT_LIMIT_BJ_2025_02` | 北京2025年2月单个项目合同金额上限 | `SINGLE_PROJECT_CONTRACT_AMOUNT_LIMIT_BJ_FEB` |

### 3.7 功能标志

| 环境变量 | 描述 | 原配置变量 |
|----------|------|------------|
| `FEATURE_ENABLE_BADGE_MANAGEMENT` | 是否启用徽章功能 | `ENABLE_BADGE_MANAGEMENT` |
| `FEATURE_SLA_FORCE_MONDAY` | SLA监控是否强制在周一执行 | `SLA_CONFIG["FORCE_MONDAY"]` |

## 4. 环境变量加载和验证

### 4.1 环境变量加载

在应用启动时，使用python-dotenv库加载环境变量：

```python
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
```

### 4.2 环境变量验证

实现环境变量验证函数，确保所有必需的环境变量都已设置：

```python
def validate_required_env_vars():
    """验证所有必需的环境变量是否已设置"""
    required_vars = [
        'METABASE_USERNAME',
        'METABASE_PASSWORD',
        'METABASE_URL',
        'WECOM_WEBHOOK_DEFAULT',
        # 其他必需的环境变量
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
```

### 4.3 环境变量获取

创建辅助函数，用于获取环境变量，并提供默认值和类型转换：

```python
def get_env(name, default=None, cast=None):
    """获取环境变量，支持默认值和类型转换"""
    value = os.getenv(name, default)
    if value is None:
        return None
    
    if cast is not None:
        if cast is bool:
            return value.lower() in ('true', 'yes', '1', 'y')
        return cast(value)
    
    return value
```

## 5. 环境变量使用示例

### 5.1 配置文件中使用环境变量

```python
# config.py
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取环境变量，提供默认值
METABASE_URL = os.getenv('METABASE_URL', 'http://localhost:3000')
METABASE_USERNAME = os.getenv('METABASE_USERNAME')
METABASE_PASSWORD = os.getenv('METABASE_PASSWORD')

# 使用辅助函数获取环境变量
TASK_CHECK_INTERVAL = get_env('CONFIG_TASK_CHECK_INTERVAL', 10, int)
ENABLE_BADGE_MANAGEMENT = get_env('FEATURE_ENABLE_BADGE_MANAGEMENT', 'True', bool)
```

### 5.2 日志配置中使用环境变量

```python
# log_config.py
import logging
import os
from dotenv import load_dotenv

def get_log_level():
    """根据环境变量设置日志级别"""
    load_dotenv()
    env = os.getenv('ENVIRONMENT', 'production').lower()
    if env == 'development':
        return logging.DEBUG
    else:
        return logging.INFO
```

## 6. 后续步骤

1. 创建`.env.example`文件模板
2. 修改`modules/config.py`使用环境变量
3. 更新`.gitignore`文件
4. 修改日志记录代码
5. 实现会话信息加密存储
6. 编写测试验证修改

## 更新记录

| 版本 | 日期 | 更新者 | 更新内容 |
|------|------|--------|----------|
| 1.0.0 | 2025-04-29 | Frank | 初始版本 |
