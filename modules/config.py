# config.py

# 归档文件夹
ARCHIVE_DIR = 'archive'

# 业务数据源服务器配置
METABASE_URL = 'http://metabase.fsgo365.cn:3000'
METABASE_SESSION = METABASE_URL + '/api/session/'

# 获取数据 账号密码
METABASE_USERNAME = 'wangshuang@xlink.bj.cn'
METABASE_PASSWORD = 'xlink123456'

RUN_JOBS_SERIALLY_SCHEDULE = 10 # 每2分钟执行一次

# 北京地区
# 北京运营企微群机器人通讯地址
WEBHOOK_URL_DEFAULT = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=59cf22c5-0623-4b34-b207-0f404f13eeeb'
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
WECHAT_GROUP_NAME_SHANGHAI = '雨虹防水管家红包激励群'
CAMPAIGN_CONTACT_WECHAT_NAME_SHANGHAI = '满浩浩'

# 北京地区，2024年5月活动
# 第四个任务，北京销售激励活动（5月）API配置
API_URL_BJ_MAY = METABASE_URL + "/api/card/792/query"

# 北京销售激励活动 JOB signing_and_sales_incentive_ctt1mc_beijing
TEMP_CONTRACT_DATA_FILE_BJ_MAY = 'state/ContractData-BJ-May.csv'
PERFORMANCE_DATA_FILENAME_BJ_MAY = 'state/PerformanceData-BJ-May.csv'
STATUS_FILENAME_BJ_MAY = 'state/send_status_bj_may.json'

# Pro
# WECHAT_GROUP_NAME = '修链(北京)运营沟通群'
WECOM_GROUP_NAME_BJ_MAY = '（北京）修链服务运营'
CAMPAIGN_CONTACT_BJ_MAY = '王爽'

# 上海地区，2024年5月活动
# 第五个任务，销售激励活动（5月）API配置
API_URL_SH_MAY = METABASE_URL + "/api/card/798/query"

# 销售激励活动 JOB signing_and_sales_incentive_ctt1mc_shanghai
TEMP_CONTRACT_DATA_FILE_SH_MAY = 'state/ContractData-SH-May.csv'
PERFORMANCE_DATA_FILENAME_SH_MAY = 'state/PerformanceData-SH-May.csv'
STATUS_FILENAME_SH_MAY = 'state/send_status_sh_may.json'

# Pro
# WECHAT_GROUP_NAME_SH_MAY = '满浩浩'
WECOM_GROUP_NAME_SH_MAY = '（上海）运营群'
CAMPAIGN_CONTACT_SH_MAY = '满浩浩'

# 第六个任务，工单联络超时提醒
API_URL_CONTACT_TIMEOUT = "http://metabase.fsgo365.cn:3000/api/card/980/query"
# STATUS_FILENAME_CONTACT_TIMEOUT = './state/contact_timeout_status.json'
WEBHOOK_URL_CONTACT_TIMEOUT = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=80ab1f45-2526-4b41-a639-c580ccde3e2f"

# 北京地区，2024年6月活动
# 第七个任务，北京销售激励活动（6月）API配置
API_URL_BJ_JUNE = METABASE_URL + "/api/card/1078/query"

# 北京销售激励活动 JOB signing_and_sales_incentive_june_beijing
TEMP_CONTRACT_DATA_FILE_BJ_JUNE = 'state/ContractData-BJ-June.csv'
PERFORMANCE_DATA_FILENAME_BJ_JUNE = 'state/PerformanceData-BJ-June.csv'
STATUS_FILENAME_BJ_JUNE = 'state/send_status_bj_june.json'

# Pro
# WECHAT_GROUP_NAME = '修链(北京)运营沟通群'
WECOM_GROUP_NAME_BJ_JUNE = '（北京）修链服务运营'
CAMPAIGN_CONTACT_BJ_JUNE = '王爽'


# 上海地区，2024年6月活动
# 第八个任务，销售激励活动（6月）API配置
API_URL_SH_JUNE = METABASE_URL + "/api/card/1079/query"

# 销售激励活动 JOB signing_and_sales_incentive_june_shanghai
TEMP_CONTRACT_DATA_FILE_SH_JUNE = 'state/ContractData-SH-June.csv'
PERFORMANCE_DATA_FILENAME_SH_JUNE = 'state/PerformanceData-SH-June.csv'
STATUS_FILENAME_SH_JUNE = 'state/send_status_sh_june.json'

# Pro
# WECHAT_GROUP_NAME_SH_JUNE = '满浩浩'
WECOM_GROUP_NAME_SH_JUNE = '（上海）运营群'
CAMPAIGN_CONTACT_SH_JUNE = '满浩浩'


# 北京地区，2024年7月活动
# 第九个任务，北京销售激励活动（7月）API配置
API_URL_BJ_JULY = METABASE_URL + "/api/card/1196/query"

# 北京销售激励活动 JOB signing_and_sales_incentive_july_beijing
TEMP_CONTRACT_DATA_FILE_BJ_JULY = 'state/ContractData-BJ-July.csv'
PERFORMANCE_DATA_FILENAME_BJ_JULY = 'state/PerformanceData-BJ-July.csv'
STATUS_FILENAME_BJ_JULY = 'state/send_status_bj_july.json'

# Pro
# WECHAT_GROUP_NAME = '修链(北京)运营沟通群'
WECOM_GROUP_NAME_BJ_JULY = '（北京）修链服务运营'
CAMPAIGN_CONTACT_BJ_JULY = '王爽'

# Dev
# WECHAT_GROUP_NAME_BJ_JULY = '文件传输助手'
# WECOM_GROUP_NAME_BJ_JULY = '孙埜'
# CAMPAIGN_CONTACT_BJ_JULY = '文件传输助手'

# 上海地区，2024年7月活动
# 第十个任务，销售激励活动（7月）API配置
API_URL_SH_JULY = METABASE_URL + "/api/card/1197/query"

# 销售激励活动 JOB signing_and_sales_incentive_june_shanghai
TEMP_CONTRACT_DATA_FILE_SH_JULY = 'state/ContractData-SH-July.csv'
PERFORMANCE_DATA_FILENAME_SH_JULY = 'state/PerformanceData-SH-July.csv'
STATUS_FILENAME_SH_JULY = 'state/send_status_sh_july.json'

# Pro
# WECHAT_GROUP_NAME_SH_JULY = '满浩浩'
WECOM_GROUP_NAME_SH_JULY = '（上海）运营群'
CAMPAIGN_CONTACT_SH_JULY = '满浩浩'

# Dev
# WECHAT_GROUP_NAME_SH_JULY = '文件传输助手'
# WECOM_GROUP_NAME_SH_JULY = '孙埜'
# CAMPAIGN_CONTACT_SH_JULY = '文件传输助手'

## 北京地区，2024年8月活动
# 第十一个任务，北京销售激励活动（8月）API配置
API_URL_BJ_AUG = METABASE_URL + "/api/card/1340/query"
# API_URL_BJ_AUG = METABASE_URL + "/api/card/1456/query"

# 北京销售激励活动 JOB signing_and_sales_incentive_aug_beijing
TEMP_CONTRACT_DATA_FILE_BJ_AUG = 'state/ContractData-BJ-Aug.csv'
PERFORMANCE_DATA_FILENAME_BJ_AUG = 'state/PerformanceData-BJ-Aug.csv'
STATUS_FILENAME_BJ_AUG = 'state/send_status_bj_aug.json'

# Pro
# WECHAT_GROUP_NAME = '修链(北京)运营沟通群'
WECOM_GROUP_NAME_BJ_AUG = '（北京）修链服务运营'
CAMPAIGN_CONTACT_BJ_AUG = '王爽'


## 上海地区，2024年8月活动
# 第十个任务，销售激励活动（8月）API配置
API_URL_SH_AUG = METABASE_URL + "/api/card/1197/query"

# 销售激励活动 JOB signing_and_sales_incentive_aug_shanghai
TEMP_CONTRACT_DATA_FILE_SH_AUG = 'state/ContractData-SH-Aug.csv'
PERFORMANCE_DATA_FILENAME_SH_AUG = 'state/PerformanceData-SH-Aug.csv'
STATUS_FILENAME_SH_AUG = 'state/send_status_sh_aug.json'

# Pro
# WECHAT_GROUP_NAME_SH_AUG = '满浩浩'
WECOM_GROUP_NAME_SH_AUG = '（上海）运营群'
CAMPAIGN_CONTACT_SH_AUG = '满浩浩'

## 北京地区，2024年9月活动
# 第十一个任务，北京销售激励活动（8月）API配置
API_URL_BJ_SEP = METABASE_URL + "/api/card/1465/query"

# 北京销售激励活动 JOB signing_and_sales_incentive_sep_beijing
TEMP_CONTRACT_DATA_FILE_BJ_SEP = 'state/ContractData-BJ-Sep.csv'
PERFORMANCE_DATA_FILENAME_BJ_SEP = 'state/PerformanceData-BJ-Sep.csv'
STATUS_FILENAME_BJ_SEP = 'state/send_status_bj_sep.json'

# Pro
WECOM_GROUP_NAME_BJ_SEP = '（北京）修链服务运营'
CAMPAIGN_CONTACT_BJ_SEP = '王爽'


## 上海地区，2024年9月活动
# 第十个任务，销售激励活动（9月）API配置
API_URL_SH_SEP = METABASE_URL + "/api/card/1469/query"

# 销售激励活动 JOB signing_and_sales_incentive_sep_shanghai
TEMP_CONTRACT_DATA_FILE_SH_SEP = 'state/ContractData-SH-Sep.csv'
PERFORMANCE_DATA_FILENAME_SH_SEP = 'state/PerformanceData-SH-Sep.csv'
STATUS_FILENAME_SH_SEP = 'state/send_status_sh_sep.json'

# Pro
WECOM_GROUP_NAME_SH_SEP = '（上海）运营群'
CAMPAIGN_CONTACT_SH_SEP = '满浩浩'
