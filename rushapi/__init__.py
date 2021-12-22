#!/usr/bin/env python3
"""
This file stitches the whole flask app together
"""

from flask import Flask, json

from rushapi.reusables.context import db_connection
from rushapi.reusables.context import website_context
from rushapi.reusables.user_validation import is_administrator

from rushapi.blueprints.url_shortener import url_shortener
from rushapi.blueprints.user_management import user_management

app = Flask(__name__)
app.register_blueprint(url_shortener)
app.register_blueprint(user_management)


@app.route('/server_shutdown')
def server_shutdown():
    """
    This endpoint provides the website administrator a way to
    safely commit database changes before shutting the app down.

    :return: Success or Error message depending on the circumstances.
    """

    user_context = is_administrator()
    if not user_context:
        return json.dumps({"error": "Unauthorized"}), 401

    db_connection.commit()
    db_connection.close()
    return json.dumps({"success": "The server is ready for shutdown"}), 200
