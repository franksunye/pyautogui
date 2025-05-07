# 配置指南

## 配置系统概述

系统使用混合配置方式，将高敏感度信息（如密码、API密钥）存储在环境变量中，而中低敏感度信息（如API端点、文件路径）直接作为常量存储在代码中。这种方式既保护了关键敏感信息，又保持了代码的简洁性和可维护性。

## 环境变量配置

系统使用环境变量来存储高敏感度信息，以提高安全性。以下是必须配置的环境变量：

### 必需的环境变量

| 环境变量名称 | 描述 | 示例值 |
|------------|------|--------|
| `METABASE_USERNAME` | Metabase用户名 | `user@example.com` |
| `METABASE_PASSWORD` | Metabase密码 | `your_password` |
| `WECOM_WEBHOOK_DEFAULT` | 默认企业微信机器人Webhook URL | `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx` |
| `WECOM_WEBHOOK_CONTACT_TIMEOUT` | 工单联络超时提醒Webhook URL | `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx` |
| `CONTACT_PHONE_NUMBER` | 联系电话 | `12345678901` |

### 环境变量设置方法

#### Windows

在命令提示符中使用以下命令设置环境变量：

```cmd
setx METABASE_USERNAME "user@example.com"
setx METABASE_PASSWORD "your_password"
```

或者通过系统属性 -> 高级 -> 环境变量进行设置。

#### Linux/macOS

在终端中使用以下命令设置环境变量：

```bash
export METABASE_USERNAME="user@example.com"
export METABASE_PASSWORD="your_password"
```

要永久设置，请将这些命令添加到 `~/.bashrc` 或 `~/.zshrc` 文件中。

#### 使用 .env 文件

也可以创建一个 `.env` 文件，并使用 `python-dotenv` 库加载环境变量：

```
METABASE_USERNAME=user@example.com
METABASE_PASSWORD=your_password
METABASE_URL=http://metabase.example.com:3000
WECOM_WEBHOOK_DEFAULT=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
```

然后在代码中加载：

```python
from dotenv import load_dotenv
load_dotenv()
```

## 环境设置指南

本章节提供了设置和配置系统环境的详细步骤，帮助开发人员快速搭建开发环境。

### 开发环境设置

#### 1. 安装必要的软件

确保您的系统已安装以下软件：

- Python 3.8+
- Git
- SQLite3

#### 2. 克隆代码仓库

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

#### 3. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 4. 安装依赖

```bash
pip install -r requirements.txt
```

#### 5. 配置环境变量

1. 复制环境变量模板文件：
   ```bash
   cp config/.env.example config/.env
   ```

2. 编辑 `config/.env` 文件，填写实际值：
   ```
   METABASE_USERNAME=your_username
   METABASE_PASSWORD=your_password
   WECOM_WEBHOOK_DEFAULT=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_key
   WECOM_WEBHOOK_CONTACT_TIMEOUT=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_key
   CONTACT_PHONE_NUMBER=your_phone_number
   ```

3. 确保 `config/.env` 文件不会被提交到代码仓库：
   ```bash
   echo "config/.env" >> .gitignore
   ```

#### 6. 验证环境设置

运行以下命令验证环境设置是否正确：

```bash
python -m unittest tests/test_env_config.py
```

### 生产环境设置

#### 1. 服务器要求

- 操作系统：Linux (推荐 Ubuntu 20.04 LTS)
- Python 3.8+
- 足够的磁盘空间用于日志和数据文件

#### 2. 部署步骤

1. 在服务器上克隆代码仓库：
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. 创建虚拟环境并安装依赖：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. 设置环境变量：

   创建一个包含所有必要环境变量的文件，例如 `/etc/yourapp/env.sh`：
   ```bash
   export METABASE_USERNAME=your_username
   export METABASE_PASSWORD=your_password
   export WECOM_WEBHOOK_DEFAULT=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_key
   export WECOM_WEBHOOK_CONTACT_TIMEOUT=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_key
   export CONTACT_PHONE_NUMBER=your_phone_number
   # 添加其他环境变量...
   ```

   在应用启动脚本中加载这些环境变量：
   ```bash
   source /etc/yourapp/env.sh
   ```

4. 创建系统服务：

   创建一个 systemd 服务文件 `/etc/systemd/system/yourapp.service`：
   ```
   [Unit]
   Description=Your Application Service
   After=network.target

   [Service]
   User=youruser
   WorkingDirectory=/path/to/yourrepository
   EnvironmentFile=/etc/yourapp/env.sh
   ExecStart=/path/to/yourrepository/venv/bin/python main.py
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

   启用并启动服务：
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable yourapp
   sudo systemctl start yourapp
   ```

5. 配置日志轮转：

   创建一个 logrotate 配置文件 `/etc/logrotate.d/yourapp`：
   ```
   /path/to/yourrepository/logs/*.log {
       daily
       missingok
       rotate 14
       compress
       delaycompress
       notifempty
       create 0640 youruser yourgroup
   }
   ```

### 环境变量参考

详细的环境变量列表和说明请参考[环境变量结构设计](./project_management/env_var_structure_design.md)文档。

### 故障排除

#### 常见问题

1. **环境变量未加载**

   **症状**: 应用启动时报错 `Missing required environment variables`

   **解决方案**:
   - 确认 `.env` 文件存在并包含所有必需的环境变量
   - 检查环境变量名称是否正确（注意大小写）
   - 在 Windows 上，尝试重启命令提示符或 IDE
   - 在 Linux/macOS 上，确保使用 `source venv/bin/activate` 激活虚拟环境

2. **Metabase 连接失败**

   **症状**: 应用报错 `Error connecting to Metabase`

   **解决方案**:
   - 确认 `METABASE_URL`, `METABASE_USERNAME` 和 `METABASE_PASSWORD` 环境变量设置正确
   - 检查网络连接，确保可以访问 Metabase 服务器
   - 验证 Metabase 凭据是否有效（尝试直接登录 Metabase）

3. **企业微信通知失败**

   **症状**: 应用报错 `Error sending message to Webhook`

   **解决方案**:
   - 确认 `WECOM_WEBHOOK_DEFAULT` 环境变量设置正确
   - 检查 Webhook URL 是否有效（可以使用 curl 或 Postman 测试）
   - 确保消息格式符合企业微信 API 要求

4. **日志文件权限问题**

   **症状**: 应用报错 `Permission denied` 或无法写入日志

   **解决方案**:
   - 确保应用有权限写入日志目录
   - 在 Linux/macOS 上，使用 `chmod` 命令设置适当的权限
   - 在 Windows 上，检查用户账户控制 (UAC) 设置

#### 日志分析

系统日志位于 `logs/` 目录下，包含以下文件：

- `app.log`: 主应用日志
- `error.log`: 错误日志
- `debug.log`: 调试日志（仅在开发环境中启用）

使用以下命令查看最近的错误日志：

```bash
# Linux/macOS
tail -n 50 logs/error.log

# Windows
type logs\error.log | Select-Object -Last 50
```

## 敏感信息保护措施

系统实施了以下敏感信息保护措施：

1. **分级保护策略**：根据敏感度分级保护信息，只将高敏感度信息（如密码、API密钥、Webhook URLs）移至环境变量，保留中低敏感度信息（如API端点、文件路径）在代码中作为常量。
2. **环境变量存储高敏感度信息**：高敏感度信息（如密码、API密钥）都存储在环境变量中，而不是硬编码在代码中。
3. **日志脱敏**：日志中的敏感信息（如合同ID、管家姓名、金额）会被脱敏处理，只显示部分信息。
4. **会话信息安全存储**：Metabase会话信息存储在本地文件中，并定期刷新。
5. **错误处理增强**：增强了错误处理，确保在环境变量缺失或API调用失败时提供清晰的错误信息，而不泄露敏感信息。

## 关键配置项说明

### 奖励配置 (REWARD_CONFIGS)

`REWARD_CONFIGS` 字典是系统的核心配置，定义了各城市各月份的奖励规则。每个配置项包含:

```python
"BJ-2025-04": {
    "lucky_number": "8",  # 幸运数字
    "lucky_rewards": {
        "base": {"name": "接好运", "threshold": 0},  # 基础幸运奖
        "high": {"name": "接好运万元以上", "threshold": 10000}  # 高额幸运奖
    },
    "performance_limits": {
        "single_project_limit": 100000,  # 单个项目合同金额上限
        "enable_cap": True  # 是否启用业绩金额上限
    },
    "tiered_rewards": {
        "min_contracts": 6,  # 最低合同数量要求
        "tiers": [  # 奖励等级
            {"name": "达标奖", "threshold": 40000},
            {"name": "优秀奖", "threshold": 60000},
            {"name": "精英奖", "threshold": 100000}
        ]
    }
}
```

### 性能上限配置

- `PERFORMANCE_AMOUNT_CAP`: 上海单个合同计入业绩金额上限
- `ENABLE_PERFORMANCE_AMOUNT_CAP`: 上海是否启用业绩金额上限
- `PERFORMANCE_AMOUNT_CAP_BJ_FEB`: 北京单个合同计入业绩金额上限
- `ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_FEB`: 北京是否启用业绩金额上限

### 文件路径配置

- `TEMP_CONTRACT_DATA_FILE_BJ_APR`: 北京4月合同数据临时文件
- `PERFORMANCE_DATA_FILENAME_BJ_APR`: 北京4月业绩数据文件
- `STATUS_FILENAME_BJ_APR`: 北京4月发送状态文件

### API配置

- `API_URL_BJ_APR`: 北京4月数据API地址
- `API_URL_SH_MAY`: 上海5月数据API地址

### 通知配置

- `WEBHOOK_URL_DEFAULT`: 默认企业微信机器人地址
- `WECOM_GROUP_NAME_BJ_APR`: 北京4月企业微信群名称
- `CAMPAIGN_CONTACT_BJ_APR`: 北京4月活动联系人

## 配置示例

### 添加新城市配置

```python
# 添加新城市(广州)的配置
"GZ-2025-06": {
    "lucky_number": "9",
    "lucky_rewards": {
        "base": {"name": "接好运", "threshold": 0},
        "high": {"name": "接好运万元以上", "threshold": 10000}
    },
    "performance_limits": {
        "single_project_limit": 80000,
        "enable_cap": True
    },
    "tiered_rewards": {
        "min_contracts": 5,
        "tiers": [
            {"name": "达标奖", "threshold": 50000},
            {"name": "优秀奖", "threshold": 80000},
            {"name": "精英奖", "threshold": 120000}
        ]
    }
}
```

### 修改奖励阈值

```python
# 修改北京5月优秀奖阈值
REWARD_CONFIGS["BJ-2025-05"]["tiered_rewards"]["tiers"][1]["threshold"] = 70000
```

## 配置最佳实践

1. **集中管理**: 所有配置应集中在 `config.py` 文件中
2. **避免硬编码**: 不要在代码中硬编码配置值，始终使用 `config.x` 引用
3. **配置注释**: 为复杂配置添加注释说明用途
4. **配置验证**: 添加新配置后，运行测试验证其正确性
5. **配置分组**: 相关配置项应放在一起，便于管理
6. **变量顺序**: 确保变量在使用前已定义，特别是在 `REWARD_CONFIGS` 中引用的变量
7. **敏感信息使用环境变量**: 所有敏感信息（密码、API密钥等）应使用环境变量存储，而不是硬编码在配置文件中
8. **环境变量命名规范**: 使用统一的命名规范，如 `API_URL_BJ_2025_05` 表示北京2025年5月的API URL
9. **环境变量验证**: 在应用启动时验证所有必需的环境变量是否存在

## 环境变量最佳实践

1. **只将高敏感度信息存储在环境变量中**: 只将真正敏感的信息（密码、API密钥、Webhook URLs等）存储在环境变量中，保留中低敏感度信息在代码中作为常量
2. **不要在代码仓库中存储敏感信息**: 不要将包含敏感信息的 `config/.env` 文件提交到代码仓库
3. **使用环境变量模板**: 提供一个 `config/.env.example` 文件，列出所有需要的环境变量，但不包含实际值
4. **限制环境变量访问**: 限制对包含敏感环境变量的生产服务器的访问
5. **定期轮换密钥**: 定期更改密码和API密钥，并更新相应的环境变量
6. **使用不同环境的不同值**: 为开发、测试和生产环境使用不同的环境变量值
7. **记录环境变量**: 在文档中记录所有环境变量的用途和格式，但不记录实际值

## 日志安全最佳实践

1. **避免记录敏感信息**: 不要在日志中记录密码、完整的合同ID、个人身份信息等敏感数据
2. **使用掩码**: 对敏感信息使用掩码，如只显示合同ID的最后4位
3. **使用适当的日志级别**: 使用适当的日志级别（DEBUG、INFO、WARNING、ERROR），避免在生产环境中使用过于详细的日志级别
4. **限制日志访问**: 限制对日志文件的访问，确保只有授权人员可以查看日志
5. **定期清理日志**: 定期清理旧的日志文件，避免敏感信息长期存储

## 当前配置重点

当前敏感信息保护调整工作中，需要重点关注:

1. 确保只将高敏感度信息移至环境变量，包括:
   - Metabase凭据（用户名、密码）
   - 企业微信Webhook URL
   - 联系电话等个人信息
2. 保留中低敏感度信息在代码中作为常量，包括:
   - API端点和服务器URL
   - 文件路径和文件名
   - 功能标志和开关
   - 时间间隔和超时设置
   - 业务规则和参数（如奖励配置）
3. 确保日志中不包含敏感信息，特别是:
   - 完整的合同ID
   - 管家姓名
   - 合同金额
   - 密码和API密钥
4. 确保配置项能够处理北京和上海的所有差异，包括:
   - 不同的幸运数字
   - 不同的最低合同数量要求
   - 不同的奖励等级结构
   - 不同的性能上限规则
