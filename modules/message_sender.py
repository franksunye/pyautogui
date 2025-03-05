import logging
import pyautogui
import pyperclip
import time
import pygetwindow as gw
import re

def send_wechat_message(user, message):
    logging.info(f"Preparing to open WeChat PC application to send message to {user}...")
    active_window = gw.getActiveWindow()
    is_active = re.match(r'^微信', active_window.title) is not None

    if not is_active:
        logging.info(f"Opening WeChat PC application to send message to {user}...")
        pyautogui.hotkey('ctrl', 'alt', 'w')
        time.sleep(1)
        
    pyautogui.hotkey('ctrl', 'f')
    pyperclip.copy(user)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(1)

    logging.info("Messages have been 'sent'.")

def send_wecom_message(user, message):
    logging.info(f"Preparing to open WeCom PC application to send message to {user}...")
    wechat_window = gw.getWindowsWithTitle('企业微信')[0] if gw.getWindowsWithTitle('企业微信') else None

    if not wechat_window or not wechat_window.isActive:
        logging.info(f"Opening WeCom PC application to send message to {user}...")
        pyautogui.hotkey('shift', 'alt', 's')
        time.sleep(1)

    pyautogui.hotkey('alt')
    time.sleep(0.1)
    pyautogui.hotkey('alt')
    
    pyperclip.copy(user)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(1)

    logging.info("Messages have been 'sent'.") 