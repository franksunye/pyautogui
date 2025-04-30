# request_module.py
import os
import json
import requests
import datetime
import logging
from modules.config import METABASE_PASSWORD, METABASE_SESSION, METABASE_USERNAME, get_env
from modules.log_config import setup_logging

# 设置日志
setup_logging()

SESSION_FILE = get_env('FILE_SESSION', 'metabase_session.json')
SESSION_DURATION = get_env('CONFIG_SESSION_DURATION', 14 * 24 * 60 * 60, int)  # 14 days in seconds

def get_metabase_session():
    logging.info("Attempting to get Metabase session.")

    # 验证必要的环境变量是否存在
    if not METABASE_USERNAME or not METABASE_PASSWORD or not METABASE_SESSION:
        error_msg = "Missing required environment variables for Metabase session"
        logging.error(error_msg)
        raise EnvironmentError(error_msg)

    headers = {
        'Content-Type': 'application/json',
    }

    data = {"username": METABASE_USERNAME, "password": METABASE_PASSWORD}
    logging.debug(f"Sending POST request to {METABASE_SESSION} with username: {METABASE_USERNAME}")

    try:
        response = requests.post(METABASE_SESSION, headers=headers, json=data, timeout=30)
        response.raise_for_status()  # 如果响应状态码不是200，抛出异常

        session_data = response.json()
        if 'id' not in session_data:
            error_msg = "Invalid response from Metabase: missing session ID"
            logging.error(error_msg)
            raise ValueError(error_msg)

        session_id = session_data['id']

        # Save session info to file
        session_info = {
            'id': session_id,
            'timestamp': datetime.datetime.now().timestamp()
        }
        logging.info(f"Saving session info to file: {SESSION_FILE}")
        with open(SESSION_FILE, 'w') as f:
            json.dump(session_info, f)

        logging.info(f"Metabase session obtained with ID: {session_id}")
        return session_id
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to Metabase: {str(e)}"
        logging.error(error_msg)
        raise ConnectionError(error_msg)
    except (ValueError, KeyError) as e:
        error_msg = f"Error parsing Metabase response: {str(e)}"
        logging.error(error_msg)
        raise ValueError(error_msg)

def load_session():
    logging.info("Attempting to load session from file.")
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            session_info = json.load(f)
        logging.info("Session loaded successfully.")
        return session_info
    logging.warning("No session found in file.")
    return None

def is_session_valid(session_info):
    logging.info("Checking session validity.")
    if session_info is None:
        logging.warning("Session info is None.")
        return False
    session_timestamp = session_info['timestamp']
    current_timestamp = datetime.datetime.now().timestamp()
    logging.info(f"Current timestamp: {current_timestamp}, Session timestamp: {session_timestamp}")
    return (current_timestamp - session_timestamp) < SESSION_DURATION

def get_valid_session():
    logging.info("Getting valid session.")
    session_info = load_session()
    if is_session_valid(session_info):
        logging.info("Valid session found, returning session ID.")
        return session_info['id']
    else:
        logging.info("Invalid session, getting a new one.")
        return get_metabase_session()

def _send_request_with_session(session_id, api_url):
    """
    使用会话ID发送请求到指定的API URL

    Args:
        session_id (str): Metabase会话ID
        api_url (str): API URL

    Returns:
        dict: 响应数据，如果请求失败则返回None

    Raises:
        ValueError: 如果session_id或api_url为空
        ConnectionError: 如果连接失败
        TimeoutError: 如果请求超时
        ValueError: 如果响应解析失败
    """
    if not session_id:
        error_msg = "Session ID is required"
        logging.error(error_msg)
        raise ValueError(error_msg)

    if not api_url:
        error_msg = "API URL is required"
        logging.error(error_msg)
        raise ValueError(error_msg)

    try:
        header = {
            'X-Metabase-Session': session_id,
            'Content-Type': 'application/json'
        }
        logging.debug(f"Sending request to {api_url} with session ID: {session_id}")
        response = requests.post(api_url, headers=header, timeout=30)

        if response.status_code == 202:
            try:
                return response.json()
            except ValueError as e:
                error_msg = f"Error parsing response JSON: {str(e)}"
                logging.error(error_msg)
                raise ValueError(error_msg)
        else:
            error_msg = f"Request failed with status code {response.status_code}"
            logging.error(error_msg)
            response.raise_for_status()  # 抛出适当的HTTPError异常
            return None  # 这行代码不会执行，因为raise_for_status会抛出异常
    except requests.exceptions.Timeout:
        error_msg = "Request timed out"
        logging.error(error_msg)
        raise TimeoutError(error_msg)
    except requests.exceptions.RequestException as e:
        error_msg = f"Request error: {str(e)}"
        logging.error(error_msg)
        raise ConnectionError(error_msg)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e.__class__.__name__}: {str(e)}"
        logging.error(error_msg)
        raise

def send_request(session_id, api_url=None):
    """
    使用指定的会话ID发送请求到API URL

    Args:
        session_id (str): Metabase会话ID
        api_url (str, optional): API URL

    Returns:
        dict: 响应数据，如果请求失败则返回None

    Raises:
        ValueError: 如果session_id或api_url为空
        ConnectionError: 如果连接失败
        TimeoutError: 如果请求超时
        ValueError: 如果响应解析失败
    """
    if api_url is None:
        error_msg = "API URL not provided"
        logging.error(error_msg)
        raise ValueError(error_msg)

    return _send_request_with_session(session_id, api_url)

def send_request_with_managed_session(api_url=None):
    """
    使用自动管理的会话发送请求到API URL

    Args:
        api_url (str, optional): API URL

    Returns:
        dict: 响应数据，如果请求失败则返回None

    Raises:
        ValueError: 如果api_url为空
        ConnectionError: 如果连接失败
        TimeoutError: 如果请求超时
        ValueError: 如果响应解析失败
        EnvironmentError: 如果环境变量缺失
    """
    if api_url is None:
        error_msg = "API URL not provided"
        logging.error(error_msg)
        raise ValueError(error_msg)

    logging.debug(f"send_request_with_managed_session called at {datetime.datetime.now()}")

    try:
        session_id = get_valid_session()
        return _send_request_with_session(session_id, api_url)
    except Exception as e:
        error_msg = f"Error in managed session request: {e.__class__.__name__}: {str(e)}"
        logging.error(error_msg)
        raise