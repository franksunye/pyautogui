# config.py

# API配置
METABASE_URL = 'http://metabase.fsgo365.cn:3000'
METABASE_SESSION = METABASE_URL + '/api/session/'
API_URL = METABASE_URL + "/api/card/336/query"
SESSION_ID = "38f4939c-ad7f-4cbe-ae54-30946daf8593"

# 获取数据 账号密码
METABASE_USERNAME = 'wangshuang@xlink.bj.cn'
METABASE_PASSWORD = 'xlink123456'

# 请求头
# HEADERS = {
#     'X-Metabase-Session': SESSION_ID,
#     'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
# }

# Cookie
# COOKIES = {
#     'metabase.DEVICE': '468f67f0-ea48-4c50-8fc2-bd0568899daf',
#     'metabase.TIMEOUT': 'alive',
#     'metabase.SESSION': '99fc8a39-f824-474e-a87f-c738ec3250b7'
# }

WEBHOOK_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=59cf22c5-0623-4b34-b207-0f404f13eeeb'
PHONE_NUMBER = '15327103039'
