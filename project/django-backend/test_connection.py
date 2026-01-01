#!/usr/bin/env python3
"""Test PostgreSQL connection"""
import psycopg2
import sys

try:
    print("Attempting to connect to PostgreSQL via Pinggy tunnel...")
    conn = psycopg2.connect(
        host='zhyyz-106-213-84-233.a.free.pinggy.link',
        port='5432',
        database='lms',
        user='postgres',
        password='Admin@123',
        connect_timeout=10
    )
    print("✓ Connection successful!")

    # Test query
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"PostgreSQL version: {version[0]}")

    cur.close()
    conn.close()

except psycopg2.OperationalError as e:
    print(f"✗ Connection failed: {e}")
    print("\nPossible issues:")
    print("1. Pinggy tunnel is not running")
    print("2. Database credentials are incorrect")
    print("3. Database 'lms' does not exist")
    print("4. Network connectivity issues")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    sys.exit(1)
