import sqlite3
import json
from datetime import datetime
import os
import hashlib
import secrets

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

        # Users table with authentication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                credits INTEGER DEFAULT 45,
                created_at TEXT,
                total_plans_generated INTEGER DEFAULT 0,
                is_verified INTEGER DEFAULT 0,
                last_login TEXT
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
            # Create new user with 45 credits
            cursor.execute('''
                INSERT INTO users (email, credits, created_at, total_plans_generated)
                VALUES (?, ?, ?, ?)
            ''', (email, 45, datetime.now().isoformat(), 0))
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

    def get_total_users(self):
        """Get total number of users in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]

        conn.close()
        return count

    def hash_password(self, password, salt=None):
        """Hash password with salt using SHA-256"""
        if salt is None:
            salt = secrets.token_hex(32)

        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        )
        return pwd_hash.hex(), salt

    def create_user(self, email, password):
        """Create new user with email and password"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Hash password
            password_hash, salt = self.hash_password(password)

            # Create user
            cursor.execute('''
                INSERT INTO users (email, password_hash, salt, credits, created_at, total_plans_generated, is_verified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (email, password_hash, salt, 45, datetime.now().isoformat(), 0, 0))

            conn.commit()
            conn.close()
            return True, "Account created successfully!"

        except sqlite3.IntegrityError:
            conn.close()
            return False, "Email already exists!"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"

    def verify_password(self, email, password):
        """Verify user password"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT password_hash, salt FROM users WHERE email = ?', (email,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return False, "Email not found!"

        stored_hash, salt = result
        input_hash, _ = self.hash_password(password, salt)

        if input_hash == stored_hash:
            # Update last login
            cursor.execute('UPDATE users SET last_login = ? WHERE email = ?',
                          (datetime.now().isoformat(), email))
            conn.commit()
            conn.close()
            return True, "Login successful!"
        else:
            conn.close()
            return False, "Incorrect password!"

    def get_user_by_email(self, email):
        """Get user by email (for authenticated users only)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        conn.close()
        return user
