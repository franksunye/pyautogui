import csv
from faker import Faker
import datetime

# Initialize the Faker generator
fake = Faker()

# Define the header for the CSV file
header = [
    "合同ID(_id)", "活动城市(province)", "工单编号(serviceAppointmentNum)", "Status",
    "管家(serviceHousekeeper)", "合同编号(contractdocNum)", "合同金额(adjustRefundMoney)",
    "支付金额(paidAmount)", "差额(difference)", "State", "创建时间(createTime)",
    "服务商(orgName)", "签约时间(signedDate)", "Doorsill", "款项来源类型(tradeIn)"
]
# List of possible housekeeper names
housekeepers = ["张三", "李四", "王五"]

# Open the CSV file in write mode
with open('TestData.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header
    writer.writerow(header)
    # 生成并写入100条测试记录
    for _ in range(100):
        date_str = fake.date()  # 获取字符串类型的日期
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')  # 将字符串转换为日期对象
        
        row = [
            fake.random_int(min=1000000000000000000, max=9999999999999999999), # 合同ID(_id)
            fake.random_int(min=10000, max=99999), # 活动城市(province)
            f"GD{date_obj.year}{date_obj.month:02d}{date_obj.day:02d}{fake.random_int(min=1000, max=9999)}", # 工单编号(serviceAppointmentNum)
            fake.random_element(['1', '2', '3']), # Status
            fake.random_element(housekeepers), # 管家(serviceHousekeeper)
            f"YHWX-BJ-SDHY-{fake.random_int(min=2000000000, max=9999999999)}", # 合同编号(contractdocNum)
            fake.random_number(digits=4, fix_len=False), # 合同金额(adjustRefundMoney)
            fake.random_number(digits=4, fix_len=False), # 支付金额(paidAmount)
            "0.0", # 差额(difference)
            fake.random_element(['1', '2']), # State
            fake.iso8601(), # 创建时间(createTime)
            fake.company(), # 服务商(orgName)
            fake.iso8601(), # 签约时间(signedDate)
            fake.random_number(digits=5, fix_len=True), # Doorsill
            fake.random_element(['1', '2', '3']) # 款项来源类型(tradeIn)
        ]
        writer.writerow(row)
