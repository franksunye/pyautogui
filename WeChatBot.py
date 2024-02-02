import pyautogui
import pyperclip
import time
import logging
import requests
import json

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    # Open WeChat PC application
    logging.info("Opening WeChat PC application...")
    pyautogui.hotkey('ctrl', 'alt', 'w')
    time.sleep(1)

    # # Find user
    logging.info("Finding user...")
    pyautogui.hotkey('ctrl', 'f')
    pyperclip.copy('文件传输助手')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.hotkey('Enter')
    time.sleep(1)

    # # Send content
    logging.info("Sending content...")
    messages = ['Hello wechat', 'Goodbye wechat', 'See you later wechat']
    for message in messages:
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('Enter')
        time.sleep(1) # Wait for a second before sending the next message