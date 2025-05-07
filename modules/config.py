# config.py
"""
配置模块，负责管理应用程序的所有配置项。

重要说明：
----------
1. 环境变量加载机制：
   - 环境变量在 main.py 中的 load_environment 函数中加载
   - 这发生在程序启动后，命令行参数解析完成后

2. 敏感信息处理机制：
   - 所有敏感信息（API URL、密码、密钥等）都通过函数获取
   - 这确保了这些值在环境变量加载后才被获取
   - 使用这些敏感信息时，应调用相应的函数，而不是直接使用变量

3. 非敏感配置：
   - 非敏感配置（如文件路径、功能标志等）可以直接使用变量
   - 这些变量通常有默认值，即使环境变量未加载也不会导致严重问题
"""

import os
from dotenv import load_dotenv

# 环境变量已在 main.py 中加载
# load_dotenv()

# 环境变量获取辅助函数
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

# 验证必需的环境变量
def validate_required_env_vars():
    """验证所有必需的高敏感度环境变量是否已设置"""
    required_vars = [
        'METABASE_USERNAME',
        'METABASE_PASSWORD',
        'WECOM_WEBHOOK_DEFAULT',
        'WECOM_WEBHOOK_CONTACT_TIMEOUT',
        'CONTACT_PHONE_NUMBER',
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# 上海的特殊配置选项（提前定义，以便在REWARD_CONFIGS中使用）
# 业绩金额上限配置
PERFORMANCE_AMOUNT_CAP = 40000  # 单个合同计入业绩金额上限
# 是否启用业绩金额上限
ENABLE_PERFORMANCE_AMOUNT_CAP = False

# 通用奖励配置
REWARD_CONFIGS = {
    # 北京2024年11月活动配置
    "BJ-2024-11": {
        "lucky_number": "6",
        "lucky_rewards": {
            "base": {"name": "接好运", "threshold": 0},
            "high": {"name": "接好运万元以上", "threshold": 10000}
        },
        "performance_limits": {
            "single_project_limit": 50000,
            "enable_cap": False
        },
        "tiered_rewards": {
            "min_contracts": 6,
            "tiers": [
                {"name": "达标奖", "threshold": 40000},
                {"name": "优秀奖", "threshold": 60000},
                {"name": "精英奖", "threshold": 100000}
            ]
        }
    },
    # 北京2025年2月活动配置
    "BJ-2025-02": {
        "lucky_number": "6",
        "lucky_rewards": {
            "base": {"name": "接好运", "threshold": 0},
            "high": {"name": "接好运万元以上", "threshold": 10000}
        },
        "performance_limits": {
            "single_project_limit": 100000,
            "enable_cap": True,
            "single_contract_cap": 100000
        },
        "tiered_rewards": {
            "min_contracts": 6,
            "tiers": [
                {"name": "达标奖", "threshold": 60000},
                {"name": "优秀奖", "threshold": 100000},
                {"name": "精英奖", "threshold": 160000}
            ]
        }
    },
    # 北京2025年4月活动配置
    "BJ-2025-04": {
        "lucky_number": "8",
        "lucky_rewards": {
            "base": {"name": "接好运", "threshold": 0},
            "high": {"name": "接好运万元以上", "threshold": 10000}
        },
        "performance_limits": {
            "single_project_limit": 100000,
            "enable_cap": True,
            "single_contract_cap": 100000
        },
        "tiered_rewards": {
            "min_contracts": 6,
            "tiers": [
                {"name": "达标奖", "threshold": 40000},
                {"name": "优秀奖", "threshold": 80000},
                {"name": "精英奖", "threshold": 120000}
            ]
        }
    },
    # 北京2025年5月活动配置
    "BJ-2025-05": {
        "lucky_number": "6",
        "lucky_rewards": {
            "base": {"name": "接好运", "threshold": 0},
            "high": {"name": "接好运万元以上", "threshold": 10000}
        },
        "performance_limits": {
            "single_project_limit": 100000,
            "enable_cap": True,
            "single_contract_cap": 100000
        },
        "tiered_rewards": {
            "min_contracts": 6,
            "tiers": [
                {"name": "达标奖", "threshold": 80000},
                {"name": "优秀奖", "threshold": 120000},
                {"name": "精英奖", "threshold": 160000}
            ]
        }
    },
    # 上海2025年4月活动配置
    "SH-2025-04": {
        "lucky_number": "6",
        "lucky_rewards": {
            "base": {"name": "接好运", "threshold": 0},
            "high": {"name": "接好运万元以上", "threshold": 10000}
        },
        "performance_limits": {
            "single_project_limit": None,  # 上海没有工单金额上限
            "enable_cap": ENABLE_PERFORMANCE_AMOUNT_CAP,
            "single_contract_cap": PERFORMANCE_AMOUNT_CAP
        },
        "tiered_rewards": {
            "min_contracts": 5,  # 上海需要5个合同
            "tiers": [
                {"name": "基础奖", "threshold": 40000},
                {"name": "达标奖", "threshold": 60000},
                {"name": "优秀奖", "threshold": 80000},
                {"name": "精英奖", "threshold": 120000}
            ]
        }
    },
    # 上海2025年5月活动配置
    "SH-2025-05": {
        "lucky_number": "6",
        "lucky_rewards": {
            "base": {"name": "接好运", "threshold": 0},
            "high": {"name": "接好运万元以上", "threshold": 10000}
        },
        "performance_limits": {
            "single_project_limit": None,  # 上海没有工单金额上限
            "enable_cap": ENABLE_PERFORMANCE_AMOUNT_CAP,
            "single_contract_cap": PERFORMANCE_AMOUNT_CAP
        },
        "tiered_rewards": {
            "min_contracts": 5,  # 上海需要5个合同
            "tiers": [
                {"name": "基础奖", "threshold": 40000},
                {"name": "达标奖", "threshold": 60000},
                {"name": "优秀奖", "threshold": 80000},
                {"name": "精英奖", "threshold": 120000}
            ]
        }
    }
}

# 归档文件夹
ARCHIVE_DIR = 'archive'

# 业务数据源服务器配置
# 中敏感度信息，直接作为常量
METABASE_URL = 'http://metabase.fsgo365.cn:3000'
METABASE_SESSION = METABASE_URL + '/api/session/'

# 获取数据 账号密码（高敏感度信息）
def get_metabase_username():
    """获取 Metabase 用户名"""
    return get_env('METABASE_USERNAME')

def get_metabase_password():
    """获取 Metabase 密码"""
    return get_env('METABASE_PASSWORD')

# 每3分钟执行一次
RUN_JOBS_SERIALLY_SCHEDULE = 3

# 任务调度器检查间隔（秒）
TASK_CHECK_INTERVAL = 10

# 北京地区
# 北京运营企微群机器人通讯地址
def get_webhook_url_default():
    """获取默认企业微信 Webhook URL"""
    return get_env('WECOM_WEBHOOK_DEFAULT')

def get_phone_number():
    """获取联系电话"""
    return get_env('CONTACT_PHONE_NUMBER')

# 为了向后兼容，保留原变量名
WEBHOOK_URL_DEFAULT = get_webhook_url_default()
PHONE_NUMBER = get_phone_number()

# 第二个任务，北京技师状态检查 JOB check_technician_status
# 中敏感度信息，直接作为常量
API_URL_TS = METABASE_URL + "/api/card/719/query"
STATUS_FILENAME_TS = './state/technician_status_record.json'

# 第六个任务，工单联络超时提醒
# 中敏感度信息，直接作为常量
API_URL_CONTACT_TIMEOUT = METABASE_URL + "/api/card/980/query"

# 高敏感度信息，通过函数获取
def get_webhook_url_contact_timeout():
    """获取工单联络超时提醒 Webhook URL"""
    return get_env('WECOM_WEBHOOK_CONTACT_TIMEOUT')

# 为了向后兼容，保留原变量名
WEBHOOK_URL_CONTACT_TIMEOUT = get_webhook_url_contact_timeout()

## 上海地区，2025年4月活动
# 中敏感度信息，直接作为常量
API_URL_SH_APR = METABASE_URL + "/api/card/1617/query"

# 销售激励活动 JOB signing_and_sales_incentive_apr_shanghai
TEMP_CONTRACT_DATA_FILE_SH_APR = 'state/ContractData-SH-Apr.csv'
PERFORMANCE_DATA_FILENAME_SH_APR = 'state/PerformanceData-SH-Apr.csv'
STATUS_FILENAME_SH_APR = 'state/send_status_sh_apr.json'

# 中敏感度信息，直接作为常量
WECOM_GROUP_NAME_SH_APR = '（上海）运营群'
CAMPAIGN_CONTACT_SH_APR = '满浩浩'

## 上海地区，2025年5月活动
# 中敏感度信息，直接作为常量
API_URL_SH_MAY = METABASE_URL + "/api/card/1694/query"

# 销售激励活动 JOB signing_and_sales_incentive_may_shanghai
TEMP_CONTRACT_DATA_FILE_SH_MAY = 'state/ContractData-SH-May.csv'
PERFORMANCE_DATA_FILENAME_SH_MAY = 'state/PerformanceData-SH-May.csv'
STATUS_FILENAME_SH_MAY = 'state/send_status_sh_may.json'

# 中敏感度信息，直接作为常量
WECOM_GROUP_NAME_SH_MAY = '（上海）运营群'
CAMPAIGN_CONTACT_SH_MAY = '满浩浩'

## 上海的特殊配置选项
# 销售激励活动 奖金池计算比例
BONUS_POOL_RATIO = 0.002  # 默认为0.2%,可根据需要调整

# 注意：业绩金额上限配置和是否启用业绩金额上限已移至文件顶部

## 北京地区，2025年4月活动
# 中敏感度信息，直接作为常量
API_URL_BJ_APR = METABASE_URL + "/api/card/1616/query"

# 北京销售激励活动 JOB signing_and_sales_incentive_apr_beijing
TEMP_CONTRACT_DATA_FILE_BJ_APR = 'state/ContractData-BJ-Apr.csv'
PERFORMANCE_DATA_FILENAME_BJ_APR = 'state/PerformanceData-BJ-Apr.csv'
STATUS_FILENAME_BJ_APR = 'state/send_status_bj_apr.json'

# 中敏感度信息，直接作为常量
WECOM_GROUP_NAME_BJ_APR = '（北京）修链服务运营'
CAMPAIGN_CONTACT_BJ_APR = '王爽'

## 北京地区，2025年5月活动
# 中敏感度信息，直接作为常量
API_URL_BJ_MAY = METABASE_URL + "/api/card/1693/query"

# 北京销售激励活动 JOB signing_and_sales_incentive_may_beijing
TEMP_CONTRACT_DATA_FILE_BJ_MAY = 'state/ContractData-BJ-May.csv'
PERFORMANCE_DATA_FILENAME_BJ_MAY = 'state/PerformanceData-BJ-May.csv'
STATUS_FILENAME_BJ_MAY = 'state/send_status_bj_may.json'

# 中敏感度信息，直接作为常量
WECOM_GROUP_NAME_BJ_MAY = '（北京）修链服务运营'
CAMPAIGN_CONTACT_BJ_MAY = '王爽'

## 北京的特殊配置选项
# 销售激励活动 奖金池计算比例
BONUS_POOL_RATIO_BJ_FEB = 0.002  # 默认为0.2%,可根据需要调整

# 单个项目合同金额上限
SINGLE_PROJECT_CONTRACT_AMOUNT_LIMIT_BJ_FEB = 1000000
# 业绩金额上限配置
PERFORMANCE_AMOUNT_CAP_BJ_FEB = 100000
# 是否启用业绩金额上限
ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_FEB = True

# 昨日指定服务时效规范执行情况日报 JOB generate_daily_service_report
# 中敏感度信息，直接作为常量
API_URL_DAILY_SERVICE_REPORT = METABASE_URL + "/api/card/1514/query"
TEMP_DAILY_SERVICE_REPORT_FILE = 'state/daily_service_report_record.csv'
DAILY_SERVICE_REPORT_RECORD_FILE = 'state/daily_service_report_record.json'
# SLA违规记录文件路径
SLA_VIOLATIONS_RECORDS_FILE = './state/sla_violations.json'
# SLA监控配置
SLA_CONFIG = {
    "FORCE_MONDAY": False,  # 测试时设为 True，正式环境设为 False
}
# 服务商名称到接收人名称的映射
SERVICE_PROVIDER_MAPPING = {
    "北京博远恒泰装饰装修有限公司": "博远恒泰（沟通群）",
    "北京德客声商贸有限公司": "德客声（沟通群）",
    "北京恒润万通防水工程有限公司": "恒润万通（沟通群）",
    "北京华庭装饰工程有限公司": "华庭装饰（沟通群）",
    "北京华夏精程防水工程有限公司": "华夏精程（沟通群）",
    "北京怀军防水工程有限公司": "怀军防水（沟通群）",
    "北京建君盛华技术服务有限公司": "建君盛华（沟通群）",
    "北京虹象防水工程有限公司": "久安有方（沟通群）",
    "北京久盾宏盛建筑工程有限公司": "久盾宏盛（沟通群）",
    "北京盛达洪雨防水技术有限公司": "盛达洪雨（沟通群）",
    "北京腾飞瑞欧建筑装饰有限公司": "潇译防水（沟通群）",
    "北京众德森建材有限责任公司": "众德森（沟通群）",
    "北京九鼎建工建筑工程有限公司": "九鼎建工（沟通群）",
    "北京顺建为安工程有限公司": "顺建为安（沟通群）",
    "三河市中豫防水工程有限公司": "中豫防水（沟通群）",
    "北京华锐龙盛建筑工程有限公司": "华锐龙盛（沟通群）",
    "云尚虹（北京）建筑工程有限公司": "云尚虹（沟通群）",
    "虹途控股（北京）有限责任公司": "虹途控股（沟通群）",

    # 可以继续添加其他服务商的映射
    # "服务商名称": "接收人名称",
}

##------ 徽章功能 ------##
# 是否启用徽章，2025年4月新增
ENABLE_BADGE_MANAGEMENT = True
BADGE_EMOJI = "\U0001F396"  # 奖章
BADGE_NAME = f"【{BADGE_EMOJI}精英管家】"

# 精英管家列表，2025年4月份增加的逻辑，精英管家是技术工程师的一个头衔
ELITE_HOUSEKEEPER = ["胡林波", "余金凤", "文刘飞", "李卓", "吕世军"]  # 可以根据需要添加更多管家

# 在程序启动时验证必需的环境变量
# 注意：环境变量验证已移至 main.py 中，在加载环境变量后进行
# try:
#     validate_required_env_vars()
# except EnvironmentError as e:
#     import logging
#     logging.error(f"环境变量验证失败: {str(e)}")
#     # 在生产环境中，可能需要在这里退出程序
#     # import sys
#     # sys.exit(1)