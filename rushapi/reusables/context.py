"""
This file provides a context needed for the rest of the app to function.
This includes, providing a database, and the desired app configuration.
"""

import os
import sqlite3

if not os.environ.get('RUSH_SQLITE_FILE'):
    print("This app uses an sqlite3 database. You need to EXPORT a location of the database file to RUSH_SQLITE_FILE")
    raise SystemExit

SQLITE_FILE = os.environ.get('RUSH_SQLITE_FILE')

db_connection = sqlite3.connect(SQLITE_FILE, check_same_thread=False)
db_cursor = db_connection.cursor()
db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS "users" (
            "id"    INTEGER NOT NULL,
            "email"    TEXT,
            "username"    TEXT NOT NULL UNIQUE,
            "permissions"    INTEGER NOT NULL,
            "premium"    INTEGER NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
        )
""")
db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS "session_tokens" (
            "user_id"    INTEGER NOT NULL,
            "token"    TEXT NOT NULL,
            "timestamp"    TEXT NOT NULL,
            "user_agent"    TEXT NOT NULL,
            "ip_address"    INTEGER NOT NULL,
            "ipv6"    INTEGER NOT NULL
        )
""")
db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS "totp_seeds" (
            "user_id"    INTEGER NOT NULL,
            "seed"    TEXT NOT NULL,
            "enabled"    INTEGER NOT NULL
        )
""")
db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS "user_passwords" (
            "user_id"    INTEGER NOT NULL,
            "password_hash"    TEXT NOT NULL,
            "password_salt"    TEXT NOT NULL
        )
""")
db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS "domain_blacklist" (
            "domain"    TEXT NOT NULL
        )
""")
db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS "urls" (
            "id"    TEXT NOT NULL,
            "author_id"    INTEGER,
            "url"    TEXT NOT NULL,
            "creation_timestamp"    INTEGER NOT NULL,
            "premium"    INTEGER NOT NULL,
            "visits"    INTEGER NOT NULL,
            "delete_after"    INTEGER,
            "last_visit"    INTEGER NOT NULL
        )
""")
db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS "app_configuration" (
            "setting"    TEXT NOT NULL,
            "value"    TEXT NOT NULL
        )
""")
db_connection.commit()

website_context = {}
