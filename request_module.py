# request_module.py
import requests
import datetime
from requests.exceptions import Timeout
import logging
from config import API_URL, HEADERS, COOKIES
from log_config import setup_logging

# 设置日志
setup_logging()

def send_request():

    logging.info(f"send_request called at {datetime.datetime.now()}")

    try:
        logging.info(f"Sending POST request to {API_URL} with headers {HEADERS} and cookies {COOKIES}")
        response = requests.post(API_URL, headers=HEADERS, cookies=COOKIES, timeout=30)
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
