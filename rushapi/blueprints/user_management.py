import pyotp
from flask import Blueprint, request, make_response, redirect, json

import hashlib
import ipaddress
import time

from rushapi.reusables.rng import get_random_string
from rushapi.reusables.context import db_cursor
from rushapi.reusables.context import db_connection
from rushapi.reusables.user_validation import get_user_context
from rushapi.reusables.user_validation import is_administrator
from rushapi.reusables.user_validation import validate_user_credentials

user_management = Blueprint("user_management", __name__)


@user_management.route('/generate_token', methods=['POST'])
def generate_token():
    """
    This endpoint takes in username and password through POST and generates a token a client can use.
    :return: A newly generated token.
    """

    if get_user_context():
        return json.dumps({
            "error": "If you are generating a new token, don't put your current token in the headers. "
                     "This makes no sense. ",
        }), 401

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        otp = request.form['otp']
        user_id = validate_user_credentials(username, password, otp)
        if not user_id:
            return json.dumps({"error": "Username/Password/TOTP validation failed."}), 401

        new_session_token = get_random_string(32)

        hashed_token = hashlib.sha256(new_session_token.encode()).hexdigest()
        client_ip_address_str = request.remote_addr

        if "." in client_ip_address_str:
            client_ip_address_ipv6 = 0
            client_ip_address_int = ipaddress.IPv4Address(client_ip_address_str)
        elif ":" in client_ip_address_str:
            client_ip_address_ipv6 = 1
            client_ip_address_int = ipaddress.IPv6Address(client_ip_address_str)
        else:
            raise ValueError("something is wrong")

        db_cursor.execute("INSERT INTO session_tokens VALUES (?, ?, ?, ?, ?, ?)",
                          [int(user_id), hashed_token,
                           int(time.time()), str(request.user_agent.string),
                           int(client_ip_address_int), int(client_ip_address_ipv6)])
        db_connection.commit()

        return json.dumps({
            "token": new_session_token,
        })


@user_management.route('/generate_account', methods=['POST'])
def generate_account():
    """
    This endpoint is used to register a user account.
    :return: A newly generated token of the newly generated account.
    """

    is_anyone_registered = tuple(db_cursor.execute("SELECT id FROM users"))
    is_registration_enabled = tuple(db_cursor.execute(
        "SELECT value FROM app_configuration WHERE setting = ?", ["allow_registration"])
    )

    if not is_registration_enabled:
        if is_anyone_registered and not is_administrator():
            return make_response(redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        password_salt = get_random_string(32)

        hashed_password = hashlib.sha256((password + password_salt).encode()).hexdigest()

        if not is_anyone_registered:
            perms_to_give = 9
        else:
            perms_to_give = 2

        username_already_taken = tuple(db_cursor.execute("SELECT id FROM users WHERE username = ? COLLATE NOCASE",
                                                         [username.lower()]))

        if username_already_taken:
            return json.dumps({"error": "The username is already taken!"}), 401

        db_cursor.execute("INSERT INTO users (email, username, permissions, premium) "
                          "VALUES (?, ?, ?, ?)",
                          [str(email), str(username), perms_to_give, 0])
        db_connection.commit()

        # RETURNING SQL statement does not work so I have to do this
        user_id = tuple(db_cursor.execute("SELECT id FROM users WHERE username = ?",
                                          [str(username)]))

        db_cursor.execute("INSERT INTO user_passwords (user_id, password_hash, password_salt) VALUES (?, ?, ?)",
                          [int(user_id[0][0]), str(hashed_password), password_salt])
        db_connection.commit()

        totp_seed = pyotp.random_base32()

        db_cursor.execute("INSERT INTO totp_seeds VALUES (?, ?, 1)", [int(user_id[0][0]), totp_seed])
        db_connection.commit()

        return json.dumps({
            "user_id": int(user_id[0][0]),
            "totp_seed": totp_seed,
        })


@user_management.route('/destroy_token')
def destroy_token():
    """
    This endpoint is used to destroy a token.
    :return: A Success or Error message.
    """

    if not get_user_context():
        return json.dumps({"error": "You need to put the token in the headers!"}), 401

    hashed_token = hashlib.sha256((request.headers['Authorization']).encode()).hexdigest()

    db_cursor.execute("DELETE FROM session_tokens WHERE token = ?", [hashed_token])
    db_connection.commit()

    return json.dumps({"success": "This token has been destroyed!"}), 200


@user_management.route('/update_account_premium', methods=['POST'])
def update_account_premium():
    """
    This endpoint is used by an administrator to update the premium status of an account.
    :return: A success message.
    """

    if not is_administrator():
        return json.dumps({
            "error": "This endpoint is meant for use by an administrator only.",
        }), 401

    if request.method == 'POST':
        user_id = request.form['user_id']
        premium = request.form['premium']

        db_cursor.execute("UPDATE users SET premium = ? WHERE id = ?", [int(premium), int(user_id)])
        db_connection.commit()

        return json.dumps({
            "success": "Account updated",
        })


@user_management.route('/token_listing')
def token_listing():
    """
    This endpoint is temporarily disabled.
    :return: Should be returning all the token hashes tied to a user account, when not disabled.
    """

    return json.dumps({"error": "For security reasons, this endpoint is temporarily unavailable"}), 401

    user_context = get_user_context()
    if not user_context:
        return json.dumps({"error": "Put at least one token in the headers"}), 401

    session_listing = tuple(db_cursor.execute("SELECT token, timestamp, user_agent, ip_address, ipv6 "
                                              "FROM session_tokens WHERE user_id = ?"
                                              "ORDER BY timestamp DESC", [user_context.id]))

    return json.dumps(session_listing)
