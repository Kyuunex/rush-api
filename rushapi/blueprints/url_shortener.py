"""
This file provides endpoints for everything URL shortener related
"""
from flask import Blueprint, request, make_response, redirect, json

import time

from rushapi.reusables.context import db_cursor
from rushapi.reusables.context import db_connection
from rushapi.reusables.rng import get_random_string
from rushapi.reusables.user_validation import get_user_context


url_shortener = Blueprint("url_shortener", __name__)


@url_shortener.route('/make_redirect', methods=['POST'])
@url_shortener.route('/make_redirect/<desired_id>', methods=['POST', 'PUT'])
def make_post(desired_id=None):
    """
    This endpoint handles the POST data submitted by the client.
    It will process this information and create a shortened a URL.

    :return: A newly created shortened URL.
    """

    # TODO: add a blacklist

    if desired_id:
        user_context = get_user_context()
        if not (user_context & user_context.premium):
            return json.dumps({
                        "code": 401,
                        "description": "Creating a custom redirect requires a premium account. "
                                       "If you already have one, put your token in the headers.",
            })
        premium = 1
        url_id = desired_id
        author_id = user_context.id
        delete_after = None
    else:
        premium = 0
        url_id = get_random_string(8)
        author_id = None
        delete_after = int(time.time()) + 2.592e+6

    if request.method == 'POST':
        url = request.form['url']

        db_cursor.execute("INSERT INTO urls "
                          "(id, author_id, url, creation_timestamp, premium, visits, delete_after, last_visit) "
                          "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          [url_id, author_id, url, int(time.time()), premium, 0, delete_after, int(time.time())])
        db_connection.commit()

        return json.dumps({
            "shortened_url": f"https://{request.host}/url/{url_id}"
        }), 200


@url_shortener.route('/url/<url_id>')
def redirect_url(url_id):
    """
    This endpoint looks up the unique identifier of the URL and redirects the user there.
    Along the way it takes note of the time visited and increase the visit count.

    :param url_id: URL's unique identifier
    :return: A redirect to that URL
    """

    post_url_lookup = tuple(db_cursor.execute("SELECT url, visits, delete_after FROM urls WHERE id = ?", [url_id]))
    if not post_url_lookup:
        return make_response(redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

    visits = int(post_url_lookup[0][1])

    db_cursor.execute("UPDATE urls SET visits = ? AND last_visit = ? WHERE id = ?",
                      [(visits+1), int(time.time()), url_id])
    db_connection.commit()

    return make_response(redirect(post_url_lookup[0][0]))
