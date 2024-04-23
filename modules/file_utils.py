# file_utils.py
import csv
import logging
import pandas as pd
import os
import shutil
import json
from datetime import datetime
import pandas as pd
import pytz
from modules.log_config import setup_logging

# 设置日志
setup_logging()

def save_to_csv_with_headers(data, filename='ContractData.csv', columns=None):
    if columns is None:
        columns = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)"]
    
    df = pd.DataFrame(data, columns=columns)   
    df.to_csv(filename, index=False)

def archive_file(filename, archive_dir='archive', days_to_keep=3):
    # Get current timestamp in China timezone
    china_tz = pytz.timezone('Asia/Shanghai')
    timestamp = datetime.now(china_tz).strftime('%Y%m%d%H%M')

    # Define archive file name
    base_name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    archive_file = f'{base_name}_{timestamp}{ext}'

    # Create archive directory if it doesn't exist
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    # If the filename includes a path, ensure the directory structure exists in the archive
    dir_path = os.path.dirname(filename)
    if dir_path:
        archive_subdir = os.path.join(archive_dir, dir_path)
        if not os.path.exists(archive_subdir):
            os.makedirs(archive_subdir)

    # Move file to archive directory
    shutil.move(filename, os.path.join(archive_dir, archive_file))
    
    # Check and delete files in the archive directory that are older than the specified number of days
    for file in os.listdir(archive_dir):
        file_path = os.path.join(archive_dir, file)
        if os.path.isfile(file_path):
            file_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if (datetime.now() - file_modified_time).days > days_to_keep:
                os.remove(file_path)
                logging.debug(f"Deleted old file: {file_path}")
                
def count_reward_types(file_path):
    try:
        data = pd.read_csv(file_path)
        reward_type_counts = {"签约奖励-50": 0, "签约奖励-100": 0}
        for index, row in data.iterrows():
            reward_type = row['奖励类型']
            if reward_type in reward_type_counts:
                reward_type_counts[reward_type] += 1
        return reward_type_counts # 确保函数返回了统计结果
    except FileNotFoundError:
        logging.error(f"文件 {file_path} 不存在。")
        return {}
        
def read_contract_data(filename):
    logging.debug(f"Read contract data: {filename}")
    logging.debug(f"Full path: {os.path.abspath(filename)}")    
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)

def read_performance_data(filename):
        
    logging.debug(f"Full path: {os.path.abspath(filename)}")
    
    try:
        existing_contract_ids = set()
        with open(filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_contract_ids.add(row['合同ID(_id)'].strip())
        return existing_contract_ids
    except FileNotFoundError:
        return set()

def write_performance_data(filename, data, headers):
    with open(filename, 'a', newline='', encoding='utf-8-sig') as file:  # 注意这里改为追加模式 'a'
        writer = csv.DictWriter(file, fieldnames=headers)
        if file.tell() == 0:  # 如果文件是空的，写入头部
            writer.writeheader()
        writer.writerows(data)
        
def read_performance_data_from_csv(filename):
    """读取性能数据文件并返回记录列表"""
    with open(filename, mode='r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_performance_data_to_csv(filename, data, fieldnames):
    """写入性能数据到文件"""
    with open(filename, mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
def get_housekeeper_award_list(file_path):

    try:
        # Load the CSV file
        data = pd.read_csv(file_path)
        
        # Group by '管家(serviceHousekeeper)' and aggregate '奖励名称' into a list
        grouped_rewards = data.groupby('管家(serviceHousekeeper)')['奖励名称'].apply(list).to_dict()
        
        # Clean: Remove NaN values, duplicates, and split combined rewards
        cleaned_grouped_rewards = {}
        for housekeeper, rewards in grouped_rewards.items():
            cleaned_rewards = []
            for reward in filter(pd.notna, rewards):
                # Split combined rewards and extend the list
                cleaned_rewards.extend(reward.split(", "))
            # Remove duplicates
            cleaned_grouped_rewards[housekeeper] = list(dict.fromkeys(cleaned_rewards))
        
        return cleaned_grouped_rewards
    except FileNotFoundError:
        return []
    
def load_send_status(filename):
    """加载发送状态文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_send_status(filename, status):
    """保存发送状态到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=4)

def update_send_status(filename, _id, status):
    """更新指定合同ID的发送状态"""
    logging.info(f"Starting update_send_status for _id: {_id}, status: {status}")

    send_status = load_send_status(filename)
    send_status[_id] = status

    logging.info(f"Updating send_status for _id: {_id} to status: {status}")

    save_send_status(filename, send_status)
    logging.info(f"Successfully updated send_status for _id: {_id} to status: {status}")