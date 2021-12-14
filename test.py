#!/usr/bin/env python3
from rushapi import app as application

application.run(
    host='127.0.0.1',
    port=8080,
    debug=True
)
