# config.py

# 归档文件夹
ARCHIVE_DIR = 'archive'

# 业务数据源服务器配置
METABASE_URL = 'http://metabase.fsgo365.cn:3000'
METABASE_SESSION = METABASE_URL + '/api/session/'

# 获取数据 账号密码
METABASE_USERNAME = 'wangshuang@xlink.bj.cn'
METABASE_PASSWORD = 'xlink123456'

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

# 第二个任务，北京技师状态检查 JOB check_technician_status
API_URL_TS = "http://metabase.fsgo365.cn:3000/api/card/719/query"
STATUS_FILENAME_TS = './state/technician_status_record.json'

# 上海地区

# 第三个任务，上海销售激励活动（4月）API配置
API_URL_SHANGHAI = METABASE_URL + "/api/card/736/query"

# 上海销售激励活动 JOB check_signing_and_award_sales_incentive
TEMP_CONTRACT_DATA_FILE_SHANGHAI = 'state/ContractData-SHANGHAI.csv'
PERFORMANCE_DATA_FILENAME_SHANGHAI = 'state/PerformanceData-SHANGHAI.csv'
STATUS_FILENAME_SHANGHAI = 'state/send_status_shanghai.json'


# 所有任务的参数定义，当前只有周期和名称
JOBS = {
    'check_signing_and_award_sales_incentive': {
        'schedule': 3, # 每15分钟运行一次
        'function': 'check_signing_and_award_sales_incentive',
        'args': [],
        'kwargs': {}
    },
    'check_technician_status': {
        'schedule': 30, # 每30分钟运行一次
        'function': 'check_technician_status',
        'args': [],
        'kwargs': {}
    },
    'check_signing_and_award_sales_incentive_shanghai': {
        'schedule': 7, # 每15分钟运行一次
        'function': 'check_signing_and_award_sales_incentive_shanghai',
        'args': [],
        'kwargs': {}
    }
}
