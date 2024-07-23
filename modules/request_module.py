# request_module.py
import os
import json
import requests
import datetime
from requests.exceptions import Timeout, RequestException
import logging
from time import sleep
from modules.config import API_URL, METABASE_PASSWORD, METABASE_SESSION, METABASE_USERNAME
from modules.log_config import setup_logging

# 设置日志
setup_logging()

SESSION_FILE = 'metabase_session.json'
SESSION_DURATION = 14 * 24 * 60 * 60  # 14 days in seconds
MAX_RETRIES = 5  # 最大重试次数
RETRY_DELAY = 15  # 每次重试的延迟时间（秒）

def get_metabase_session() -> str:
    logging.info("Attempting to get Metabase session.")
    
    headers = {'Content-Type': 'application/json'}
    data = {"username": METABASE_USERNAME, "password": METABASE_PASSWORD}
    logging.debug(f"Sending POST request to {METABASE_SESSION} with username: {METABASE_USERNAME}")
    
    response = requests.post(METABASE_SESSION, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    session_id = response.json()['id']
    
    session_info = {'id': session_id, 'timestamp': datetime.datetime.now().timestamp()}
    logging.info(f"Saving session info to file: {SESSION_FILE}")
    
    with open(SESSION_FILE, 'w') as f:
        json.dump(session_info, f)
    
    logging.info(f"Metabase session obtained with ID: {session_id}")
    return session_id

def load_session() -> dict:
    logging.info("Attempting to load session from file.")
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            session_info = json.load(f)
        logging.info("Session loaded successfully.")
        return session_info
    logging.warning("No session found in file.")
    return None

def is_session_valid(session_info: dict) -> bool:
    logging.info("Checking session validity.")
    if not session_info:
        logging.warning("Session info is None.")
        return False
    session_timestamp = session_info['timestamp']
    current_timestamp = datetime.datetime.now().timestamp()
    logging.info(f"Current timestamp: {current_timestamp}, Session timestamp: {session_timestamp}")
    return (current_timestamp - session_timestamp) < SESSION_DURATION

def get_valid_session() -> str:
    logging.info("Getting valid session.")
    session_info = load_session()
    if is_session_valid(session_info):
        logging.info("Valid session found, returning session ID.")
        return session_info['id']
    else:
        logging.info("Invalid session, getting a new one.")
        return get_metabase_session()

def send_request_with_retries(func, max_retries: int = MAX_RETRIES, delay: int = RETRY_DELAY):
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except RequestException as e:
            if attempt < max_retries and isinstance(e.response, requests.Response) and e.response.status_code == 503:
                logging.warning(f"Request failed with status code 503. Attempt {attempt} of {max_retries}")
                sleep(delay)
            else:
                logging.error(f"Request failed: {e}")
                raise
    logging.error("Max retries reached. Request failed.")
    return None

def _send_request_with_session(session_id: str, api_url: str) -> dict:
    def make_request():
        headers = {
            'X-Metabase-Session': session_id,
            'Content-Type': 'application/json'
        }
        response = requests.post(api_url, headers=headers, timeout=180)
        response.raise_for_status()
        return response.json()

    return send_request_with_retries(make_request)

def send_request(session_id: str, api_url: str = None) -> dict:
    if api_url is None:
        api_url = API_URL
    return _send_request_with_session(session_id, api_url)

def send_request_with_managed_session(api_url: str = None) -> dict:
    if api_url is None:
        api_url = API_URL

    logging.debug(f"send_request_with_managed_session called at {datetime.datetime.now()}")

    session_id = get_valid_session()
    return _send_request_with_session(session_id, api_url)
