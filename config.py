# config.py

# API配置
API_URL = "http://metabase.fsgo365.cn:3000/api/card/336/query"
SESSION_ID = "38f4939c-ad7f-4cbe-ae54-30946daf8593"

# 请求头
HEADERS = {
    'X-Metabase-Session': SESSION_ID,
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

# Cookie
COOKIES = {
    'metabase.DEVICE': '468f67f0-ea48-4c50-8fc2-bd0568899daf',
    'metabase.TIMEOUT': 'alive',
    'metabase.SESSION': '99fc8a39-f824-474e-a87f-c738ec3250b7'
}
