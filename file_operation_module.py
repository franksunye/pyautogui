# file_operation_module.py
import csv
import logging
import pandas as pd
import os
import shutil
import time
from datetime import datetime
import pandas as pd
import pytz
from log_config import setup_logging

# 设置日志
setup_logging()

def save_to_csv(data, filename="ContractData.csv"):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

# Define column names
column_names = ["合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status", "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)", "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)", "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)"]

def save_to_csv_with_headers(data, filename='ContractData.csv'):
    # Convert data to DataFrame with specified column names
    df = pd.DataFrame(data, columns=column_names)

    # Write DataFrame to CSV file
    df.to_csv(filename, index=False)

def archive_file(filename, archive_dir='archive'):
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

    # Move file to archive directory
    shutil.move(filename, os.path.join(archive_dir, archive_file))

def read_contract_data(filename):
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)

def read_performance_data(filename):
    try:
        existing_contract_ids = set()
        with open(filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_contract_ids.add(row['合同ID(_id)'].strip())
        return existing_contract_ids
    except FileNotFoundError:
        return set()

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
    
def write_performance_data(filename, data, headers):
    with open(filename, 'a', newline='', encoding='utf-8-sig') as file:  # 注意这里改为追加模式 'a'
        writer = csv.DictWriter(file, fieldnames=headers)
        if file.tell() == 0:  # 如果文件是空的，写入头部
            writer.writeheader()
        writer.writerows(data)