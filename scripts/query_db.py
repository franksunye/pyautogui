#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
查询数据库中的数据
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.db_module import get_db_connection

def query_performance_data(campaign_id, limit=10):
    """
    查询指定活动的性能数据

    Args:
        campaign_id: 活动ID
        limit: 限制返回的记录数

    Returns:
        rows: 查询结果
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = f"SELECT * FROM performance_data WHERE campaign_id = ? LIMIT ?"
    cursor.execute(query, (campaign_id, limit))

    rows = cursor.fetchall()

    # 获取列名
    column_names = [description[0] for description in cursor.description]

    conn.close()

    return column_names, rows

def main():
    """
    主函数
    """
    campaign_id = "BJ-2025-05"
    limit = 10

    print(f"查询活动 {campaign_id} 的数据，限制 {limit} 条记录")

    column_names, rows = query_performance_data(campaign_id, limit)

    # 打印列名
    print("列名:")
    print(column_names)

    # 打印数据
    print("\n数据:")
    for row in rows:
        print(row)

    # 打印总记录数
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM performance_data WHERE campaign_id = ?", (campaign_id,))
    count = cursor.fetchone()[0]
    conn.close()

    print(f"\n总记录数: {count}")

if __name__ == "__main__":
    main()
