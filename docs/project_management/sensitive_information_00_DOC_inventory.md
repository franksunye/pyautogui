# 敏感信息清单

## 文档信息
**文档类型**: 技术文档
**文档编号**: sensitive_information-DOC-001
**版本**: 1.0.0
**创建日期**: 2025-04-29
**最后更新**: 2025-04-29
**状态**: 草稿
**负责人**: Frank
**团队成员**: Frank, 小智

**相关文档**:
- [敏感信息保护计划](./sensitive_information_01_PLAN_protection.md) (sensitive_information-PLAN-001)
- [敏感信息保护任务清单](./sensitive_information_03_TASK_protection.md) (sensitive_information-TASK-001)
- [环境变量结构设计](./sensitive_information_02_DOC_env_var_structure.md) (sensitive_information-DOC-002)

## 1. 概述

本文档记录了项目中发现的所有敏感信息，包括其位置、类型和建议的处理方式。敏感信息按照类型分类，并提供了详细的位置信息，以便于后续的处理和保护工作。

## 2. 敏感信息分类

### 2.1 账号凭据

| ID | 信息描述 | 文件位置 | 行号 | 建议处理方式 |
|----|----------|----------|------|--------------|
| CRED-001 | Metabase用户名 | modules/config.py | 115 | 移至环境变量 |
| CRED-002 | Metabase密码 | modules/config.py | 116 | 移至环境变量 |

### 2.2 API密钥和Webhook URLs

| ID | 信息描述 | 文件位置 | 行号 | 建议处理方式 |
|----|----------|----------|------|--------------|
| API-001 | 默认企业微信Webhook URL | modules/config.py | 123 | 移至环境变量 |
| API-002 | 工单联络超时提醒Webhook URL | modules/config.py | 131 | 移至环境变量 |

### 2.3 API端点

| ID | 信息描述 | 文件位置 | 行号 | 建议处理方式 |
|----|----------|----------|------|--------------|
| ENDPOINT-001 | Metabase URL | modules/config.py | 113 | 移至环境变量 |
| ENDPOINT-002 | 技师状态检查API URL | modules/config.py | 127 | 移至环境变量 |
| ENDPOINT-003 | 工单联络超时提醒API URL | modules/config.py | 130 | 移至环境变量 |
| ENDPOINT-004 | 上海4月活动API URL | modules/config.py | 134 | 移至环境变量 |
| ENDPOINT-005 | 上海5月活动API URL | modules/config.py | 145 | 移至环境变量 |
| ENDPOINT-006 | 北京4月活动API URL | modules/config.py | 159 | 移至环境变量 |
| ENDPOINT-007 | 北京5月活动API URL | modules/config.py | 170 | 移至环境变量 |
| ENDPOINT-008 | 每日服务报告API URL | modules/config.py | 186 | 移至环境变量 |

### 2.4 个人信息

| ID | 信息描述 | 文件位置 | 行号 | 建议处理方式 |
|----|----------|----------|------|--------------|
| PII-001 | 电话号码 | modules/config.py | 124 | 移至环境变量 |

### 2.5 敏感日志

| ID | 信息描述 | 文件位置 | 行号 | 建议处理方式 |
|----|----------|----------|------|--------------|
| LOG-001 | 日志中记录Metabase密码 | modules/request_module.py | 25 | 修改日志记录方式，避免记录密码 |

## 3. 敏感信息详情

### 3.1 账号凭据

#### CRED-001: Metabase用户名
```python
METABASE_USERNAME = 'wangshuang@xlink.bj.cn'
```
- **风险**: 如果代码泄露，可能导致未授权访问Metabase系统
- **建议处理方式**: 将用户名移至环境变量，使用`os.getenv('METABASE_USERNAME')`获取

#### CRED-002: Metabase密码
```python
METABASE_PASSWORD = 'xlink123456'
```
- **风险**: 如果代码泄露，可能导致未授权访问Metabase系统
- **建议处理方式**: 将密码移至环境变量，使用`os.getenv('METABASE_PASSWORD')`获取

### 3.2 API密钥和Webhook URLs

#### API-001: 默认企业微信Webhook URL
```python
WEBHOOK_URL_DEFAULT = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=689cebff-3328-4150-9741-fed8b8ce4713'
```
- **风险**: 如果代码泄露，可能导致未授权发送消息到企业微信群
- **建议处理方式**: 将URL移至环境变量，使用`os.getenv('WEBHOOK_URL_DEFAULT')`获取

#### API-002: 工单联络超时提醒Webhook URL
```python
WEBHOOK_URL_CONTACT_TIMEOUT = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=80ab1f45-2526-4b41-a639-c580ccde3e2f"
```
- **风险**: 如果代码泄露，可能导致未授权发送消息到企业微信群
- **建议处理方式**: 将URL移至环境变量，使用`os.getenv('WEBHOOK_URL_CONTACT_TIMEOUT')`获取

### 3.3 API端点

#### ENDPOINT-001: Metabase URL
```python
METABASE_URL = 'http://metabase.fsgo365.cn:3000'
```
- **风险**: 如果代码泄露，可能暴露内部系统地址
- **建议处理方式**: 将URL移至环境变量，使用`os.getenv('METABASE_URL')`获取

### 3.4 个人信息

#### PII-001: 电话号码
```python
PHONE_NUMBER = '15327103039'
```
- **风险**: 如果代码泄露，可能暴露个人联系信息
- **建议处理方式**: 将电话号码移至环境变量，使用`os.getenv('PHONE_NUMBER')`获取

### 3.5 敏感日志

#### LOG-001: 日志中记录Metabase密码
```python
logging.debug(f"Sending POST request to {METABASE_SESSION} with username: {METABASE_USERNAME} and password: {METABASE_PASSWORD}")
```
- **风险**: 密码可能出现在日志文件中，增加泄露风险
- **建议处理方式**: 修改日志记录方式，避免记录密码，例如：
  ```python
  logging.debug(f"Sending POST request to {METABASE_SESSION} with username: {METABASE_USERNAME}")
  ```

## 4. 敏感信息处理建议

### 4.1 环境变量命名建议

为了保持一致性和可维护性，建议使用以下命名规范：

1. 使用大写字母和下划线
2. 使用前缀区分不同类型的环境变量
   - `METABASE_` 前缀用于Metabase相关配置
   - `WECOM_` 前缀用于企业微信相关配置
   - `API_` 前缀用于API端点
   - `SECURITY_` 前缀用于安全相关配置

### 4.2 环境变量分组建议

建议将环境变量按照以下分组组织：

1. **认证凭据**
   - `METABASE_USERNAME`
   - `METABASE_PASSWORD`
   - `SECURITY_SESSION_KEY` (用于会话加密)

2. **API端点**
   - `METABASE_URL`
   - `API_URL_TS`
   - `API_URL_CONTACT_TIMEOUT`
   - 等等

3. **Webhook URLs**
   - `WECOM_WEBHOOK_DEFAULT`
   - `WECOM_WEBHOOK_CONTACT_TIMEOUT`

4. **个人信息**
   - `CONTACT_PHONE_NUMBER`

### 4.3 环境变量验证建议

建议在应用启动时验证所有必需的环境变量是否已设置，例如：

```python
def validate_required_env_vars():
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

## 5. 后续步骤

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
