import sqlite3
import json
from datetime import datetime
import os

class Database:
    def __init__(self, db_path="data/users.db"):
        self.db_path = db_path
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()

    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                credits INTEGER DEFAULT 100,
                created_at TEXT,
                total_plans_generated INTEGER DEFAULT 0
            )
        ''')

        # Plans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT,
                subject TEXT,
                field TEXT,
                level TEXT,
                plan_content TEXT,
                created_at TEXT,
                FOREIGN KEY (user_email) REFERENCES users (email)
            )
        ''')

        conn.commit()
        conn.close()

    def get_user(self, email):
        """Get user by email, create if doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if not user:
            # Create new user with 100 credits
            cursor.execute('''
                INSERT INTO users (email, credits, created_at, total_plans_generated)
                VALUES (?, ?, ?, ?)
            ''', (email, 100, datetime.now().isoformat(), 0))
            conn.commit()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()

        conn.close()
        return user

    def get_credits(self, email):
        """Get user's credit balance"""
        user = self.get_user(email)
        return user[2]  # credits column

    def deduct_credits(self, email, amount):
        """Deduct credits from user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE users
            SET credits = credits - ?,
                total_plans_generated = total_plans_generated + 1
            WHERE email = ?
        ''', (amount, email))

        conn.commit()
        conn.close()

    def add_credits(self, email, amount):
        """Add credits to user (for purchases)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE users
            SET credits = credits + ?
            WHERE email = ?
        ''', (amount, email))

        conn.commit()
        conn.close()

    def save_plan(self, email, subject, field, level, plan_content):
        """Save generated study plan"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO plans (user_email, subject, field, level, plan_content, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, subject, field, level, plan_content, datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def get_user_plans(self, email):
        """Get all plans for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM plans
            WHERE user_email = ?
            ORDER BY created_at DESC
        ''', (email,))

        plans = cursor.fetchall()
        conn.close()
        return plans
