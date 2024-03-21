# config.py

# API配置
METABASE_URL = 'http://metabase.fsgo365.cn:3000'
METABASE_SESSION = METABASE_URL + '/api/session/'

API_URL = METABASE_URL + "/api/card/336/query"

# 获取数据 账号密码
METABASE_USERNAME = 'wangshuang@xlink.bj.cn'
METABASE_PASSWORD = 'xlink123456'

WEBHOOK_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=59cf22c5-0623-4b34-b207-0f404f13eeeb'
PHONE_NUMBER = '15327103039'

ARCHIVE_DIR = 'archive'

# JOB check_signing_and_award_sales_incentive
TEMP_CONTRACT_DATA_FILE = 'state/ContractData.csv'
PERFORMANCE_DATA_FILENAME = 'state/PerformanceData.csv'
STATUS_FILENAME = 'state/send_status.json'

# JOB check_technician_status
API_URL_TS = "http://metabase.fsgo365.cn:3000/api/card/719/query"
STATUS_FILENAME_TS = './state/technician_status_record.json'

JOBS = {
    'check_signing_and_award_sales_incentive': {
        'schedule': 15, # 每15分钟运行一次
        'function': 'check_signing_and_award_sales_incentive',
        'args': [],
        'kwargs': {}
    },
    'check_technician_status': {
        'schedule': 30, # 每30分钟运行一次
        'function': 'check_technician_status',
        'args': [],
        'kwargs': {}
    }
}
