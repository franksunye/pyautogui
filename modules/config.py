# config.py

# 归档文件夹
ARCHIVE_DIR = 'archive'

# 业务数据源服务器配置
METABASE_URL = 'http://metabase.fsgo365.cn:3000'
METABASE_SESSION = METABASE_URL + '/api/session/'

# 获取数据 账号密码
METABASE_USERNAME = 'wangshuang@xlink.bj.cn'
METABASE_PASSWORD = 'xlink123456'

RUN_JOBS_SERIALLY_SCHEDULE = 2 # 每2分钟执行一次

# 北京地区
# 北京运营企微群机器人通讯地址
WEBHOOK_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=59cf22c5-0623-4b34-b207-0f404f13eeeb'
PHONE_NUMBER = '15327103039'

# 第一个任务，北京销售激励活动API配置
API_URL = METABASE_URL + "/api/card/336/query"

# 北京销售激励活动 JOB check_signing_and_award_sales_incentive
TEMP_CONTRACT_DATA_FILE = 'state/ContractData.csv'
PERFORMANCE_DATA_FILENAME = 'state/PerformanceData.csv'
STATUS_FILENAME = 'state/send_status.json'

# Pro
WECHAT_GROUP_NAME = '修链(北京)运营沟通群'
CAMPAIGN_CONTACT_WECHAT_NAME = '王爽'

# Dev
# WECHAT_GROUP_NAME = '文件传输助手'
# CAMPAIGN_CONTACT_WECHAT_NAME = '文件传输助手'

# 第二个任务，北京技师状态检查 JOB check_technician_status
API_URL_TS = "http://metabase.fsgo365.cn:3000/api/card/719/query"
STATUS_FILENAME_TS = './state/technician_status_record.json'

# 上海地区 2024年3月22日活动

# 第三个任务，上海销售激励活动（4月）API配置
API_URL_SHANGHAI = METABASE_URL + "/api/card/736/query"

# 上海销售激励活动 JOB check_signing_and_award_sales_incentive
TEMP_CONTRACT_DATA_FILE_SHANGHAI = 'state/ContractData-SHANGHAI.csv'
PERFORMANCE_DATA_FILENAME_SHANGHAI = 'state/PerformanceData-SHANGHAI.csv'
STATUS_FILENAME_SHANGHAI = 'state/send_status_shanghai.json'

# Pro
# WECHAT_GROUP_NAME_SHANGHAI = '满浩浩'
# CAMPAIGN_CONTACT_WECHAT_NAME_SHANGHAI = '满浩浩'

# Dev
WECHAT_GROUP_NAME_SHANGHAI = '文件传输助手'
CAMPAIGN_CONTACT_WECHAT_NAME_SHANGHAI = '文件传输助手'

# 北京地区，2024年5月活动

# 第四个任务，北京销售激励活动（5月）API配置
API_URL_BJ_MAY = METABASE_URL + "/api/card/780/query"

# 北京销售激励活动 JOB signing_and_sales_incentive_ctt1mc_beijing
TEMP_CONTRACT_DATA_FILE_BJ_MAY = 'state/ContractData-BJ-May.csv'
PERFORMANCE_DATA_FILENAME_BJ_MAY = 'state/PerformanceData-BJ-May.csv'
STATUS_FILENAME_BJ_MAY = 'state/send_status_bj_may.json'

# Pro
# WECHAT_GROUP_NAME = '修链(北京)运营沟通群'
# CAMPAIGN_CONTACT_WECHAT_NAME = '王爽'

# Dev
WECHAT_GROUP_NAME_BJ_MAY = '文件传输助手'
CAMPAIGN_CONTACT_BJ_MAY = '文件传输助手'

WECOM_GROUP_NAME_BJ_MAY = '王爽'