#!/usr/bin/env python3
"""Quick test of database connection"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trainer_lms.settings')
django.setup()

from django.db import connection

try:
    print("Testing database connection...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result:
            print("✓ Database connection successful!")
            cursor.execute("SELECT version()")
            version = cursor.fetchone()
            print(f"PostgreSQL version: {version[0]}")
            sys.exit(0)
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    print("\nThe Pinggy tunnel may not be responding.")
    print("Please ensure:")
    print("1. Pinggy tunnel is running on your local machine")
    print("2. The tunnel URL is correct")
    print("3. Your local PostgreSQL is running")
    sys.exit(1)
