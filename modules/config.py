# config.py
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

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
    """验证所有必需的环境变量是否已设置"""
    required_vars = [
        'METABASE_USERNAME',
        'METABASE_PASSWORD',
        'METABASE_URL',
        'WECOM_WEBHOOK_DEFAULT',
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# 上海的特殊配置选项（提前定义，以便在REWARD_CONFIGS中使用）
# 业绩金额上限配置
PERFORMANCE_AMOUNT_CAP = get_env('CONFIG_PERFORMANCE_AMOUNT_CAP', 40000, int)  # 单个合同计入业绩金额上限
# 是否启用业绩金额上限
ENABLE_PERFORMANCE_AMOUNT_CAP = get_env('CONFIG_ENABLE_PERFORMANCE_AMOUNT_CAP', 'false', bool)

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
ARCHIVE_DIR = get_env('ARCHIVE_DIR', 'archive')

# 业务数据源服务器配置
METABASE_URL = get_env('METABASE_URL', 'http://localhost:3000')
METABASE_SESSION = METABASE_URL + '/api/session/'

# 获取数据 账号密码
METABASE_USERNAME = get_env('METABASE_USERNAME')
METABASE_PASSWORD = get_env('METABASE_PASSWORD')

RUN_JOBS_SERIALLY_SCHEDULE = get_env('CONFIG_RUN_JOBS_SERIALLY_SCHEDULE', 3, int)  # 每3分钟执行一次

# 任务调度器检查间隔（秒）
TASK_CHECK_INTERVAL = get_env('CONFIG_TASK_CHECK_INTERVAL', 10, int)

# 北京地区
# 北京运营企微群机器人通讯地址
WEBHOOK_URL_DEFAULT = get_env('WECOM_WEBHOOK_DEFAULT')
PHONE_NUMBER = get_env('CONTACT_PHONE_NUMBER')

# 第二个任务，北京技师状态检查 JOB check_technician_status
API_URL_TS = get_env('API_URL_TS')
STATUS_FILENAME_TS = get_env('FILE_TECHNICIAN_STATUS_RECORD', './state/technician_status_record.json')

# 第六个任务，工单联络超时提醒
API_URL_CONTACT_TIMEOUT = get_env('API_URL_CONTACT_TIMEOUT')
WEBHOOK_URL_CONTACT_TIMEOUT = get_env('WECOM_WEBHOOK_CONTACT_TIMEOUT')

## 上海地区，2025年4月活动
API_URL_SH_APR = get_env('API_URL_SH_2025_04', METABASE_URL + "/api/card/1617/query")

# 销售激励活动 JOB signing_and_sales_incentive_apr_shanghai
TEMP_CONTRACT_DATA_FILE_SH_APR = get_env('FILE_TEMP_CONTRACT_DATA_SH_2025_04', 'state/ContractData-SH-Apr.csv')
PERFORMANCE_DATA_FILENAME_SH_APR = get_env('FILE_PERFORMANCE_DATA_SH_2025_04', 'state/PerformanceData-SH-Apr.csv')
STATUS_FILENAME_SH_APR = get_env('FILE_STATUS_SH_2025_04', 'state/send_status_sh_apr.json')

# Pro
WECOM_GROUP_NAME_SH_APR = get_env('CONTACT_WECOM_GROUP_NAME_SH_2025_04', '（上海）运营群')
CAMPAIGN_CONTACT_SH_APR = get_env('CONTACT_CAMPAIGN_CONTACT_SH_2025_04', '满浩浩')

## 上海地区，2025年5月活动
API_URL_SH_MAY = get_env('API_URL_SH_2025_05', METABASE_URL + "/api/card/1694/query")

# 销售激励活动 JOB signing_and_sales_incentive_may_shanghai
TEMP_CONTRACT_DATA_FILE_SH_MAY = get_env('FILE_TEMP_CONTRACT_DATA_SH_2025_05', 'state/ContractData-SH-May.csv')
PERFORMANCE_DATA_FILENAME_SH_MAY = get_env('FILE_PERFORMANCE_DATA_SH_2025_05', 'state/PerformanceData-SH-May.csv')
STATUS_FILENAME_SH_MAY = get_env('FILE_STATUS_SH_2025_05', 'state/send_status_sh_may.json')

# Pro
WECOM_GROUP_NAME_SH_MAY = get_env('CONTACT_WECOM_GROUP_NAME_SH_2025_05', '（上海）运营群')
CAMPAIGN_CONTACT_SH_MAY = get_env('CONTACT_CAMPAIGN_CONTACT_SH_2025_05', '满浩浩')

## 上海的特殊配置选项
# 销售激励活动 奖金池计算比例
BONUS_POOL_RATIO = get_env('CONFIG_BONUS_POOL_RATIO', 0.002, float)  # 默认为0.2%,可根据需要调整

# 注意：业绩金额上限配置和是否启用业绩金额上限已移至文件顶部

## 北京地区，2025年4月活动
API_URL_BJ_APR = get_env('API_URL_BJ_2025_04', METABASE_URL + "/api/card/1616/query")

# 北京销售激励活动 JOB signing_and_sales_incentive_apr_beijing
TEMP_CONTRACT_DATA_FILE_BJ_APR = get_env('FILE_TEMP_CONTRACT_DATA_BJ_2025_04', 'state/ContractData-BJ-Apr.csv')
PERFORMANCE_DATA_FILENAME_BJ_APR = get_env('FILE_PERFORMANCE_DATA_BJ_2025_04', 'state/PerformanceData-BJ-Apr.csv')
STATUS_FILENAME_BJ_APR = get_env('FILE_STATUS_BJ_2025_04', 'state/send_status_bj_apr.json')

# Pro
WECOM_GROUP_NAME_BJ_APR = get_env('CONTACT_WECOM_GROUP_NAME_BJ_2025_04', '（北京）修链服务运营')
CAMPAIGN_CONTACT_BJ_APR = get_env('CONTACT_CAMPAIGN_CONTACT_BJ_2025_04', '王爽')

## 北京地区，2025年5月活动
API_URL_BJ_MAY = get_env('API_URL_BJ_2025_05', METABASE_URL + "/api/card/1693/query")

# 北京销售激励活动 JOB signing_and_sales_incentive_may_beijing
TEMP_CONTRACT_DATA_FILE_BJ_MAY = get_env('FILE_TEMP_CONTRACT_DATA_BJ_2025_05', 'state/ContractData-BJ-May.csv')
PERFORMANCE_DATA_FILENAME_BJ_MAY = get_env('FILE_PERFORMANCE_DATA_BJ_2025_05', 'state/PerformanceData-BJ-May.csv')
STATUS_FILENAME_BJ_MAY = get_env('FILE_STATUS_BJ_2025_05', 'state/send_status_bj_may.json')

# Pro
WECOM_GROUP_NAME_BJ_MAY = get_env('CONTACT_WECOM_GROUP_NAME_BJ_2025_05', '（北京）修链服务运营')
CAMPAIGN_CONTACT_BJ_MAY = get_env('CONTACT_CAMPAIGN_CONTACT_BJ_2025_05', '王爽')

## 北京的特殊配置选项
# 销售激励活动 奖金池计算比例
BONUS_POOL_RATIO_BJ_FEB = get_env('CONFIG_BONUS_POOL_RATIO_BJ_2025_02', 0.002, float)  # 默认为0.2%,可根据需要调整

# 单个项目合同金额上限
SINGLE_PROJECT_CONTRACT_AMOUNT_LIMIT_BJ_FEB = get_env('CONFIG_SINGLE_PROJECT_CONTRACT_AMOUNT_LIMIT_BJ_2025_02', 1000000, int)
# 业绩金额上限配置
PERFORMANCE_AMOUNT_CAP_BJ_FEB = get_env('CONFIG_PERFORMANCE_AMOUNT_CAP_BJ_2025_02', 100000, int)
# 是否启用业绩金额上限
ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_FEB = get_env('CONFIG_ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_2025_02', 'true', bool)

# 昨日指定服务时效规范执行情况日报 JOB generate_daily_service_report
API_URL_DAILY_SERVICE_REPORT = get_env('API_URL_DAILY_SERVICE_REPORT', METABASE_URL + "/api/card/1514/query")
TEMP_DAILY_SERVICE_REPORT_FILE = get_env('FILE_TEMP_DAILY_SERVICE_REPORT', 'state/daily_service_report_record.csv')
DAILY_SERVICE_REPORT_RECORD_FILE = get_env('FILE_DAILY_SERVICE_REPORT_RECORD', 'state/daily_service_report_record.json')
# SLA违规记录文件路径
SLA_VIOLATIONS_RECORDS_FILE = get_env('FILE_SLA_VIOLATIONS_RECORDS', './state/sla_violations.json')
# SLA监控配置
SLA_CONFIG = {
    "FORCE_MONDAY": get_env('FEATURE_SLA_FORCE_MONDAY', 'false', bool),  # 测试时设为 True，正式环境设为 False
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
ENABLE_BADGE_MANAGEMENT = get_env('FEATURE_ENABLE_BADGE_MANAGEMENT', 'true', bool)
BADGE_EMOJI = "\U0001F396"  # 奖章
BADGE_NAME = f"【{BADGE_EMOJI}精英管家】"

# 精英管家列表，2025年4月份增加的逻辑，精英管家是技术工程师的一个头衔
ELITE_HOUSEKEEPER = ["胡林波", "余金凤", "文刘飞", "李卓", "吕世军"]  # 可以根据需要添加更多管家

# 在程序启动时验证必需的环境变量
try:
    validate_required_env_vars()
except EnvironmentError as e:
    import logging
    logging.error(f"环境变量验证失败: {str(e)}")
    # 在生产环境中，可能需要在这里退出程序
    # import sys
    # sys.exit(1)