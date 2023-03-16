#!/usr/bin/env python3
import os

DB_FILE = os.path.expanduser("~") + "/Documents/rush.sqlite3"
os.environ["RUSH_SQLITE_FILE"] = DB_FILE
print("Database file is saved at: ", DB_FILE)

from rushapi import app as application

application.run(
    host='127.0.0.1',
    port=8080,
    debug=True
)
