# request_module.py
import requests
import datetime
from requests.exceptions import Timeout
import logging
from config import API_URL, METABASE_PASSWORD, METABASE_SESSION, METABASE_USERNAME
from log_config import setup_logging

# 设置日志
setup_logging()


def get_metabase_session():
    headers = {
        'Content-Type': 'application/json',
    }

    data = {"username": METABASE_USERNAME, "password": METABASE_PASSWORD}
    logging.info(f"Sending POST request to {METABASE_SESSION}")
    response = requests.post(METABASE_SESSION, headers=headers, json=data, timeout=30)
    return response.json()['id']
    
def send_request(session_id, api_url=None):
    if api_url is None:
        api_url = API_URL

    logging.info(f"send_request called at {datetime.datetime.now()}")

    try:
        # logging.info(f"Sending POST request to {API_URL} with headers {HEADERS} and cookies {COOKIES}")
        header = {
            'X-Metabase-Session': session_id,
            'Content-Type': 'application/json'
        }
        response = requests.post(api_url, headers=header, timeout=30)
        # logging.info(f"Received response with status code {response.status_code} and content {response.content}")

        if response.status_code == 202:
            return response.json()
        else:
            logging.error(f"Request failed with status code {response.status_code}")
            return None
    except Timeout:
        logging.error("Request timed out")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e.__class__.__name__}: {str(e)}")
        return None
