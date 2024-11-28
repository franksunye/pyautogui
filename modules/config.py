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

# 北京地区
# 北京运营企微群机器人通讯地址
WEBHOOK_URL_DEFAULT = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=59cf22c5-0623-4b34-b207-0f404f13eeeb'
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

## 上海地区，2024年11月活动
API_URL_SH_NOV = METABASE_URL + "/api/card/1523/query"

# 销售激励活动 JOB signing_and_sales_incentive_nov_shanghai
TEMP_CONTRACT_DATA_FILE_SH_NOV = 'state/ContractData-SH-Nov.csv'
PERFORMANCE_DATA_FILENAME_SH_NOV = 'state/PerformanceData-SH-Nov.csv'
STATUS_FILENAME_SH_NOV = 'state/send_status_sh_nov.json'

# Pro
WECOM_GROUP_NAME_SH_NOV = '（上海）运营群'
CAMPAIGN_CONTACT_SH_NOV = '满浩浩'

# 昨日指定服务时效规范执行情况日报 JOB generate_daily_service_report
API_URL_DAILY_SERVICE_REPORT = METABASE_URL + "/api/card/1514/query"
TEMP_DAILY_SERVICE_REPORT_FILE = 'state/daily_service_report_record.csv'
# SLA违规记录文件路径
SLA_VIOLATIONS_RECORDS_FILE = './state/sla_violations.json'
# SLA监控配置
SLA_CONFIG = {
    "FORCE_MONDAY": False,  # 测试时设为True，正式环境设为False
}
# 服务商名称到接收人名称的映射
SERVICE_PROVIDER_MAPPING = {

    "北京恒润万通防水工程有限公司": "孙埜",
    "北京博远恒泰装饰装修有限公司": "孙埜",
    "北京腾飞瑞欧建筑装饰有限公司": "孙埜",
    "北京德客声商贸有限公司": "孙埜",

    # "北京博远恒泰装饰装修有限公司": "博远恒泰（沟通群）",
    # "北京德客声商贸有限公司": "德客声（沟通群）",
    # "北京恒润万通防水工程有限公司": "恒润万通（沟通群）",
    # "北京华庭装饰工程有限公司": "华庭装饰（沟通群）",
    # "北京怀军防水工程有限公司": "怀军防水（沟通群）",
    # "北京建君盛华技术服务有限公司": "建君盛华（沟通群）",
    # "北京久安有方建筑工程有限公司": "久安有方（沟通群）",
    # "北京久盾宏盛建筑工程有限公司": "久盾宏盛（沟通群）",
    # "北京盛达洪雨防水技术有限公司": "盛达洪雨（沟通群）",
    # "北京腾飞瑞欧建筑装饰有限公司": "潇译防水（沟通群）",
    # "北京众德森建材有限责任公司": "众德森（沟通群）",
    # "云尚虹（北京）建筑工程有限公司": "云尚虹（沟通群）",

    # 可以继续添加其他服务商的映射
    # "服务商名称": "接收人名称",
}