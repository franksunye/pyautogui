# 更新的敏感信息清单

## 文档信息
**文档类型**: 技术文档
**文档编号**: sensitive_information-DOC-003
**版本**: 1.0.0
**创建日期**: 2025-04-29
**最后更新**: 2025-04-29
**状态**: 草稿
**负责人**: Frank
**团队成员**: Frank, 小智

**相关文档**:
- [敏感信息保护计划](./sensitive_information_01_PLAN_protection.md) (sensitive_information-PLAN-001)
- [敏感信息保护计划 - 调整方案](./sensitive_information_06_PLAN_adjustment.md) (sensitive_information-PLAN-002)
- [敏感信息清单](./sensitive_information_00_DOC_inventory.md) (sensitive_information-DOC-001)
- [环境变量结构设计](./sensitive_information_02_DOC_env_var_structure.md) (sensitive_information-DOC-002)
- [敏感信息保护任务清单](./sensitive_information_03_TASK_protection.md) (sensitive_information-TASK-001)
- [敏感信息保护调整任务清单](./sensitive_information_07_TASK_adjustment.md) (sensitive_information-TASK-002)

## 1. 概述

本文档是对原有敏感信息清单的更新，明确区分了敏感和非敏感配置，并提供了相应的处理建议。敏感信息应该从代码中移除，存储在环境变量中，而非敏感配置可以保留在代码中作为常量。

## 2. 敏感信息分类

### 2.1 敏感信息（应移至环境变量）

| ID | 信息描述 | 文件位置 | 行号 | 敏感度 | 建议处理方式 |
|----|----------|----------|------|--------|--------------|
| CRED-001 | Metabase用户名 | modules/config.py | 115 | 高 | 移至环境变量 METABASE_USERNAME |
| CRED-002 | Metabase密码 | modules/config.py | 116 | 高 | 移至环境变量 METABASE_PASSWORD |
| API-001 | 默认企业微信Webhook URL | modules/config.py | 123 | 高 | 移至环境变量 WECOM_WEBHOOK_DEFAULT |
| API-002 | 工单联络超时提醒Webhook URL | modules/config.py | 131 | 高 | 移至环境变量 WECOM_WEBHOOK_CONTACT_TIMEOUT |
| PII-001 | 电话号码 | modules/config.py | 124 | 高 | 移至环境变量 CONTACT_PHONE_NUMBER |
| LOG-001 | 日志中记录Metabase密码 | modules/request_module.py | 25 | 高 | 修改日志记录方式，避免记录密码 |

### 2.2 非敏感配置（可保留在代码中）

| ID | 信息描述 | 文件位置 | 行号 | 敏感度 | 建议处理方式 |
|----|----------|----------|------|--------|--------------|
| ENDPOINT-001 | Metabase URL | modules/config.py | 113 | 中 | 保留为常量 METABASE_URL |
| ENDPOINT-002 | 技师状态检查API URL | modules/config.py | 127 | 中 | 保留为常量 API_URL_TS |
| ENDPOINT-003 | 工单联络超时提醒API URL | modules/config.py | 130 | 中 | 保留为常量 API_URL_CONTACT_TIMEOUT |
| ENDPOINT-004 | 上海4月活动API URL | modules/config.py | 134 | 中 | 保留为常量 API_URL_SH_APR |
| ENDPOINT-005 | 上海5月活动API URL | modules/config.py | 145 | 中 | 保留为常量 API_URL_SH_MAY |
| ENDPOINT-006 | 北京4月活动API URL | modules/config.py | 159 | 中 | 保留为常量 API_URL_BJ_APR |
| ENDPOINT-007 | 北京5月活动API URL | modules/config.py | 170 | 中 | 保留为常量 API_URL_BJ_MAY |
| ENDPOINT-008 | 每日服务报告API URL | modules/config.py | 186 | 中 | 保留为常量 API_URL_DAILY_SERVICE_REPORT |
| CONFIG-001 | 任务检查间隔 | modules/config.py | 121 | 低 | 保留为常量 TASK_CHECK_INTERVAL |
| CONFIG-002 | 归档文件夹 | modules/config.py | 112 | 低 | 保留为常量 ARCHIVE_DIR |
| CONFIG-003 | 徽章表情符号 | modules/config.py | 192 | 低 | 保留为常量 BADGE_EMOJI |
| CONFIG-004 | 徽章名称 | modules/config.py | 193 | 低 | 保留为常量 BADGE_NAME |
| CONFIG-005 | 精英管家列表 | modules/config.py | 196 | 低 | 保留为常量 ELITE_HOUSEKEEPER |
| CONFIG-006 | 服务商映射 | modules/config.py | 200-220 | 低 | 保留为常量 SERVICE_PROVIDER_MAPPING |
| CONFIG-007 | 奖励配置 | modules/config.py | 60-100 | 低 | 保留为常量 REWARD_CONFIGS |
| CONFIG-008 | 业绩金额上限 | modules/config.py | 55 | 低 | 保留为常量 PERFORMANCE_AMOUNT_CAP |
| CONFIG-009 | 是否启用业绩金额上限 | modules/config.py | 57 | 低 | 保留为常量 ENABLE_PERFORMANCE_AMOUNT_CAP |
| CONFIG-010 | 奖金池计算比例 | modules/config.py | 150 | 低 | 保留为常量 BONUS_POOL_RATIO |
| CONFIG-011 | 单个项目合同金额上限 | modules/config.py | 180 | 低 | 保留为常量 SINGLE_PROJECT_CONTRACT_AMOUNT_LIMIT_BJ_FEB |
| CONFIG-012 | 北京2月业绩金额上限 | modules/config.py | 182 | 低 | 保留为常量 PERFORMANCE_AMOUNT_CAP_BJ_FEB |
| CONFIG-013 | 是否启用北京2月业绩金额上限 | modules/config.py | 184 | 低 | 保留为常量 ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_FEB |
| FILE-001 | 临时合同数据文件 | modules/config.py | 135 | 低 | 保留为常量 TEMP_CONTRACT_DATA_FILE_SH_APR |
| FILE-002 | 业绩数据文件名 | modules/config.py | 136 | 低 | 保留为常量 PERFORMANCE_DATA_FILENAME_SH_APR |
| FILE-003 | 状态文件名 | modules/config.py | 137 | 低 | 保留为常量 STATUS_FILENAME_SH_APR |
| FILE-004 | SLA违规记录文件路径 | modules/config.py | 190 | 低 | 保留为常量 SLA_VIOLATIONS_RECORDS_FILE |

## 3. 敏感信息详情

### 3.1 账号凭据

#### CRED-001: Metabase用户名
```python
METABASE_USERNAME = 'wangshuang@xlink.bj.cn'
```
- **敏感度**: 高
- **风险**: 如果代码泄露，可能导致未授权访问Metabase系统
- **建议处理方式**: 将用户名移至环境变量，使用函数获取
  ```python
  def get_metabase_username():
      return get_env('METABASE_USERNAME')
  ```

#### CRED-002: Metabase密码
```python
METABASE_PASSWORD = 'xlink123456'
```
- **敏感度**: 高
- **风险**: 如果代码泄露，可能导致未授权访问Metabase系统
- **建议处理方式**: 将密码移至环境变量，使用函数获取
  ```python
  def get_metabase_password():
      return get_env('METABASE_PASSWORD')
  ```

### 3.2 API密钥和Webhook URLs

#### API-001: 默认企业微信Webhook URL
```python
WEBHOOK_URL_DEFAULT = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=689cebff-3328-4150-9741-fed8b8ce4713'
```
- **敏感度**: 高
- **风险**: 如果代码泄露，可能导致未授权发送消息到企业微信群
- **建议处理方式**: 将URL移至环境变量，使用函数获取
  ```python
  def get_webhook_url_default():
      return get_env('WECOM_WEBHOOK_DEFAULT')
  ```

#### API-002: 工单联络超时提醒Webhook URL
```python
WEBHOOK_URL_CONTACT_TIMEOUT = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=80ab1f45-2526-4b41-a639-c580ccde3e2f"
```
- **敏感度**: 高
- **风险**: 如果代码泄露，可能导致未授权发送消息到企业微信群
- **建议处理方式**: 将URL移至环境变量，使用函数获取
  ```python
  def get_webhook_url_contact_timeout():
      return get_env('WECOM_WEBHOOK_CONTACT_TIMEOUT')
  ```

### 3.3 API端点

#### ENDPOINT-001: Metabase URL
```python
METABASE_URL = 'http://metabase.fsgo365.cn:3000'
```
- **敏感度**: 中
- **风险**: 如果代码泄露，可能暴露内部系统地址
- **建议处理方式**: 将URL移至环境变量，使用函数获取
  ```python
  def get_metabase_url():
      return get_env('METABASE_URL', 'http://metabase.fsgo365.cn:3000')
  ```

### 3.4 个人信息

#### PII-001: 电话号码
```python
PHONE_NUMBER = '15327103039'
```
- **敏感度**: 高
- **风险**: 如果代码泄露，可能暴露个人联系信息
- **建议处理方式**: 将电话号码移至环境变量，使用函数获取
  ```python
  def get_phone_number():
      return get_env('CONTACT_PHONE_NUMBER')
  ```

### 3.5 敏感日志

#### LOG-001: 日志中记录Metabase密码
```python
logging.debug(f"Sending POST request to {METABASE_SESSION} with username: {METABASE_USERNAME} and password: {METABASE_PASSWORD}")
```
- **敏感度**: 高
- **风险**: 密码可能出现在日志文件中，增加泄露风险
- **建议处理方式**: 修改日志记录方式，避免记录密码，例如：
  ```python
  logging.debug(f"Sending POST request to {METABASE_SESSION} with username: {METABASE_USERNAME}")
  ```

## 4. 非敏感配置详情

### 4.1 配置常量

#### CONFIG-001: 任务检查间隔
```python
TASK_CHECK_INTERVAL = 10
```
- **敏感度**: 低
- **建议处理方式**: 保留为常量，不需要移至环境变量

#### CONFIG-007: 奖励配置
```python
REWARD_CONFIGS = {
    # 北京2024年11月活动配置
    "BJ-2024-11": {
        "lucky_number": "6",
        "lucky_rewards": {
            "base": {"name": "接好运", "threshold": 0},
            "high": {"name": "接好运万元以上", "threshold": 10000}
        },
        # ...
    },
    # ...
}
```
- **敏感度**: 低
- **建议处理方式**: 保留为常量，不需要移至环境变量

### 4.2 文件路径

#### FILE-001: 临时合同数据文件
```python
TEMP_CONTRACT_DATA_FILE_SH_APR = 'state/ContractData-SH-Apr.csv'
```
- **敏感度**: 低
- **建议处理方式**: 保留为常量，不需要移至环境变量

## 5. 环境变量命名建议

为了保持一致性和可维护性，建议使用以下命名规范：

1. 使用大写字母和下划线
2. 使用前缀区分不同类型的环境变量
   - `METABASE_` 前缀用于Metabase相关配置
   - `WECOM_` 前缀用于企业微信相关配置
   - `API_URL_` 前缀用于API端点
   - `CONTACT_` 前缀用于联系信息
   - `SECURITY_` 前缀用于安全相关配置

## 更新记录

| 版本 | 日期 | 更新者 | 更新内容 |
|------|------|--------|----------|
| 1.0.0 | 2025-04-29 | 小智 | 初始版本 |
