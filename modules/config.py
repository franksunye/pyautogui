# config.py

# 归档文件夹
ARCHIVE_DIR = 'archive'

# 业务数据源服务器配置
METABASE_URL = 'http://metabase.fsgo365.cn:3000'
METABASE_SESSION = METABASE_URL + '/api/session/'

# 获取数据 账号密码
METABASE_USERNAME = 'wangshuang@xlink.bj.cn'
METABASE_PASSWORD = 'xlink123456'

RUN_JOBS_SERIALLY_SCHEDULE = 3 # 每3分钟执行一次

# 任务调度器检查间隔（秒）
TASK_CHECK_INTERVAL = 10

# 北京地区
# 北京运营企微群机器人通讯地址
# WEBHOOK_URL_DEFAULT = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=59cf22c5-0623-4b34-b207-0f404f13eeeb'
WEBHOOK_URL_DEFAULT = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=689cebff-3328-4150-9741-fed8b8ce4713'
PHONE_NUMBER = '15327103039'

# 第二个任务，北京技师状态检查 JOB check_technician_status
API_URL_TS = "http://metabase.fsgo365.cn:3000/api/card/719/query"
STATUS_FILENAME_TS = './state/technician_status_record.json'

# 第六个任务，工单联络超时提醒
API_URL_CONTACT_TIMEOUT = "http://metabase.fsgo365.cn:3000/api/card/980/query"
# STATUS_FILENAME_CONTACT_TIMEOUT = './state/contact_timeout_status.json'
WEBHOOK_URL_CONTACT_TIMEOUT = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=80ab1f45-2526-4b41-a639-c580ccde3e2f"


## 北京地区，2024年11月活动
API_URL_BJ_NOV = METABASE_URL + "/api/card/1522/query"

# 北京销售激励活动 JOB signing_and_sales_incentive_oct_beijing
TEMP_CONTRACT_DATA_FILE_BJ_NOV = 'state/ContractData-BJ-Nov.csv'
PERFORMANCE_DATA_FILENAME_BJ_NOV = 'state/PerformanceData-BJ-Nov.csv'
STATUS_FILENAME_BJ_NOV = 'state/send_status_bj_nov.json'

# Pro
WECOM_GROUP_NAME_BJ_NOV = '（北京）修链服务运营'
CAMPAIGN_CONTACT_BJ_NOV = '王爽'

## 上海地区，2024年12月活动
API_URL_SH_DEC = METABASE_URL + "/api/card/1558/query"

# 销售激励活动 JOB signing_and_sales_incentive_nov_shanghai
TEMP_CONTRACT_DATA_FILE_SH_DEC = 'state/ContractData-SH-Dec.csv'
PERFORMANCE_DATA_FILENAME_SH_DEC = 'state/PerformanceData-SH-Dec.csv'
STATUS_FILENAME_SH_DEC = 'state/send_status_sh_dec.json'

# # Pro
WECOM_GROUP_NAME_SH_DEC = '（上海）运营群'
CAMPAIGN_CONTACT_SH_DEC = '满浩浩'

## 上海地区，2025年1月活动
API_URL_SH_JAN = METABASE_URL + "/api/card/1567/query"

# 销售激励活动 JOB signing_and_sales_incentive_nov_shanghai
TEMP_CONTRACT_DATA_FILE_SH_JAN = 'state/ContractData-SH-Jan.csv'
PERFORMANCE_DATA_FILENAME_SH_JAN = 'state/PerformanceData-SH-Jan.csv'
STATUS_FILENAME_SH_JAN = 'state/send_status_sh_jan.json'

# Pro
WECOM_GROUP_NAME_SH_JAN = '（上海）运营群'
CAMPAIGN_CONTACT_SH_JAN = '满浩浩'

## 上海地区，2025年2月活动
API_URL_SH_FEB = METABASE_URL + "/api/card/1575/query"

# 销售激励活动 JOB signing_and_sales_incentive_nov_shanghai
TEMP_CONTRACT_DATA_FILE_SH_FEB = 'state/ContractData-SH-Feb.csv'
PERFORMANCE_DATA_FILENAME_SH_FEB = 'state/PerformanceData-SH-Feb.csv'
STATUS_FILENAME_SH_FEB = 'state/send_status_sh_feb.json'

# Pro
WECOM_GROUP_NAME_SH_FEB = '（上海）运营群'
CAMPAIGN_CONTACT_SH_FEB = '满浩浩'

## 上海地区，2025年3月活动
API_URL_SH_MAR = METABASE_URL + "/api/card/1601/query"

# 销售激励活动 JOB signing_and_sales_incentive_mar_shanghai
TEMP_CONTRACT_DATA_FILE_SH_MAR = 'state/ContractData-SH-Mar.csv'
PERFORMANCE_DATA_FILENAME_SH_MAR = 'state/PerformanceData-SH-Mar.csv'
STATUS_FILENAME_SH_MAR = 'state/send_status_sh_mar.json'

# Pro
WECOM_GROUP_NAME_SH_MAR = '（上海）运营群'
CAMPAIGN_CONTACT_SH_MAR = '满浩浩'

## 上海地区，2025年4月活动
API_URL_SH_APR = METABASE_URL + "/api/card/1601/query"

# 销售激励活动 JOB signing_and_sales_incentive_apr_shanghai
TEMP_CONTRACT_DATA_FILE_SH_APR = 'state/ContractData-SH-Apr.csv'
PERFORMANCE_DATA_FILENAME_SH_APR = 'state/PerformanceData-SH-Apr.csv'
STATUS_FILENAME_SH_APR = 'state/send_status_sh_apr.json'

# Pro
WECOM_GROUP_NAME_SH_APR = '（上海）运营群'
CAMPAIGN_CONTACT_SH_APR = '满浩浩'

## 上海的特殊配置选项
# 销售激励活动 奖金池计算比例
BONUS_POOL_RATIO = 0.002  # 默认为0.2%,可根据需要调整

# 业绩金额上限配置
PERFORMANCE_AMOUNT_CAP = 40000  # 单个合同计入业绩金额上限
# 是否启用业绩金额上限
ENABLE_PERFORMANCE_AMOUNT_CAP = False

## 北京地区，2025年2月活动
API_URL_BJ_FEB = METABASE_URL + "/api/card/1576/query"

# 北京销售激励活动 JOB signing_and_sales_incentive_feb_beijing
TEMP_CONTRACT_DATA_FILE_BJ_FEB = 'state/ContractData-BJ-Feb.csv'
PERFORMANCE_DATA_FILENAME_BJ_FEB = 'state/PerformanceData-BJ-Feb.csv'
STATUS_FILENAME_BJ_FEB = 'state/send_status_bj_feb.json'

# Pro
WECOM_GROUP_NAME_BJ_FEB = '（北京）修链服务运营'
CAMPAIGN_CONTACT_BJ_FEB = '王爽'

# # Test
# WECOM_GROUP_NAME_BJ_FEB = '孙埜'
# CAMPAIGN_CONTACT_BJ_FEB = '文件传输助手'

## 北京地区，2025年4月活动
API_URL_BJ_APR = METABASE_URL + "/api/card/1576/query"

# 北京销售激励活动 JOB signing_and_sales_incentive_apr_beijing
TEMP_CONTRACT_DATA_FILE_BJ_APR = 'state/ContractData-BJ-Apr.csv'
PERFORMANCE_DATA_FILENAME_BJ_APR = 'state/PerformanceData-BJ-Apr.csv'
STATUS_FILENAME_BJ_APR = 'state/send_status_bj_apr.json'

# # Pro
WECOM_GROUP_NAME_BJ_APR = '（北京）修链服务运营'
CAMPAIGN_CONTACT_BJ_APR = '王爽'

## 北京的特殊配置选项
# 销售激励活动 奖金池计算比例
BONUS_POOL_RATIO_BJ_FEB = 0.002  # 默认为0.2%,可根据需要调整

# 单个项目合同金额上限
SINGLE_PROJECT_CONTRACT_AMOUNT_LIMIT_BJ_FEB = 1000000  # 单个项目合同金额上限
# 业绩金额上限配置
PERFORMANCE_AMOUNT_CAP_BJ_FEB = 100000  # 单个合同计入业绩金额上限
# 是否启用业绩金额上限
ENABLE_PERFORMANCE_AMOUNT_CAP_BJ_FEB = True

# 昨日指定服务时效规范执行情况日报 JOB generate_daily_service_report
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

    # "北京恒润万通防水工程有限公司": "孙埜",
    # "北京博远恒泰装饰装修有限公司": "孙埜",
    # "北京腾飞瑞欧建筑装饰有限公司": "孙埜",
    # "北京久安有方建筑工程有限公司": "孙埜",

    "北京博远恒泰装饰装修有限公司": "博远恒泰（沟通群）",
    "北京德客声商贸有限公司": "德客声（沟通群）",
    "北京恒润万通防水工程有限公司": "恒润万通（沟通群）",
    "北京华庭装饰工程有限公司": "华庭装饰（沟通群）",
    "北京怀军防水工程有限公司": "怀军防水（沟通群）",
    "北京建君盛华技术服务有限公司": "建君盛华（沟通群）",
    "北京久安有方建筑工程有限公司": "久安有方（沟通群）",
    "北京久盾宏盛建筑工程有限公司": "久盾宏盛（沟通群）",
    "北京盛达洪雨防水技术有限公司": "盛达洪雨（沟通群）",
    "北京腾飞瑞欧建筑装饰有限公司": "潇译防水（沟通群）",
    "北京众德森建材有限责任公司": "众德森（沟通群）",
    "北京九鼎建工建筑工程有限公司": "九鼎建工（沟通群）",
    "北京顺建为安工程有限公司": "顺建为安（沟通群）",
    "三河市中豫防水工程有限公司": "中豫防水（沟通群）",
    "北京华锐龙盛建筑工程有限公司": "华锐龙盛（沟通群）",
    "云尚虹（北京）建筑工程有限公司": "云尚虹（沟通群）",

    # 可以继续添加其他服务商的映射
    # "服务商名称": "接收人名称",
}

##------ 徽章功能 ------##
# 是否启用徽章，2025年4月新增
ENABLE_BADGE_MANAGEMENT = True
BADGE_EMOJI = "\U0001F396"  # 奖章
BADGE_NAME = f"【{BADGE_EMOJI}精英管家】"

# 精英管家列表，2025年4月份增加的逻辑，精英管家是技术工程师的一个头衔
ELITE_HOUSEKEEPER = ["孔祥达1", "吕世军"]  # 可以根据需要添加更多管家