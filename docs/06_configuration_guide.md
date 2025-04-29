# 配置指南

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

## 当前配置重点

当前重构工作中，需要重点关注:

1. 添加 `USE_GENERIC_PROCESS_FUNCTION` 功能标志，控制是否使用通用数据处理函数
2. 确保上海配置 (`SH-2025-04`, `SH-2025-05`) 正确设置，与现有上海奖励规则一致
3. 确保配置项能够处理北京和上海的所有差异，包括:
   - 不同的幸运数字
   - 不同的最低合同数量要求
   - 不同的奖励等级结构
   - 不同的性能上限规则
