# task_manager.py

from datetime import datetime
import sqlite3

class Task:
    def __init__(self, task_type, recipient, message):
        self.task_type = task_type
        self.recipient = recipient
        self.message = message
        self.status = 'pending'
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.updated_at = self.created_at

    def save(self):
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        sql = '''
        INSERT INTO tasks (task_type, recipient, message, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(sql, (self.task_type, self.recipient, self.message, self.status, self.created_at, self.updated_at))
        conn.commit()
        conn.close()

    def update_status(self, status):
        self.status = status
        self.updated_at = datetime.now()
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        sql = '''
        UPDATE tasks
        SET status = ?, updated_at = ?
        WHERE id = ?
        '''
        cursor.execute(sql, (self.status, self.updated_at, self.id))  # Assuming `self.id` is set when saved
        conn.commit()
        conn.close()

def create_task(task_type, recipient, message):
    task = Task(task_type, recipient, message)
    task.save()
    return task

def update_task(task_id, status):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    if row:
        task = Task(row[1], row[2], row[3])  # Assuming the order of columns
        task.id = task_id  # Set the task ID
        task.update_status(status)
    conn.close()

def get_pending_tasks():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row  # Set row factory to Row to return dictionaries
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE status='pending'")
    tasks = cursor.fetchall()
    conn.close()
    return tasks