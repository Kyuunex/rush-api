"""
This file provides endpoints for everything URL shortener related
"""
from flask import Blueprint, request, make_response, redirect, json

import time
import validators

from rushapi.reusables.context import db_cursor
from rushapi.reusables.context import db_connection
from rushapi.reusables.rng import get_random_string
from rushapi.reusables.user_validation import get_user_context


url_shortener = Blueprint("url_shortener", __name__)


@url_shortener.route('/create_redirect', methods=['POST'])
@url_shortener.route('/create_redirect/<desired_id>', methods=['POST', 'PUT'])
def create_redirect(desired_id=None):
    """
    This endpoint handles the POST data submitted by the client.
    It will process this information and create a shortened a URL.

    :return: A newly created shortened URL.
    """

    if desired_id:
        user_context = get_user_context()
        if not (user_context and user_context.premium):
            return json.dumps({
                        "error": "Creating a custom redirect requires a premium account. "
                                 "If you already have one, put your token in the headers.",
            }), 401
        premium = 1
        url_id = desired_id
        author_id = user_context.id
    else:
        premium = 0
        url_id = get_random_string(7)
        author_id = None

    if request.method == 'POST':
        url = request.form['url']
        delete_after = request.args.get('delete_after')

        if delete_after:
            if len(delete_after) > 0:
                try:
                    delete_after = int(delete_after)
                except ValueError:
                    delete_after = 0
        else:
            delete_after = int(time.time()) + 2.592e+6

        if not len(url) < 250:
            return json.dumps({
                "error": "URL length must be below 250 characters.",
            }), 403

        if not validators.url(url):
            return json.dumps({
                "error": "URL is not valid",
            }), 403

        domain_blacklist = tuple(db_cursor.execute("SELECT domain FROM domain_blacklist"))
        for blacklisted_domain in domain_blacklist:
            if blacklisted_domain[0] in url:
                return json.dumps({
                    "error": "This domain is blacklisted.",
                }), 403

        db_cursor.execute("INSERT INTO urls "
                          "(id, author_id, url, creation_timestamp, premium, visits, delete_after, last_visit) "
                          "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          [url_id, author_id, url, int(time.time()), premium, 0, delete_after, int(time.time())])
        db_connection.commit()

        return json.dumps({
            "shortened_url": f"https://{request.host}/u/{url_id}"
        }), 200


@url_shortener.route('/u/<url_id>')
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


@url_shortener.route('/my_urls')
def my_urls():
    """
    :return: This endpoint returns all the URLs the user has created.
    """

    user_context = get_user_context()
    if not user_context:
        return json.dumps({
            "error": "This endpoint requires an account. "
                     "If you already have one, put your token in the headers.",
        }), 401

    urls = db_cursor.execute("SELECT id, author_id, url, creation_timestamp, premium, visits, delete_after, last_visit "
                             "FROM urls WHERE author_id = ?", [user_context.id])

    buffer = []
    for url in urls:
        buffer.append({
            "id": url[0],
            "author_id": url[1],
            "url": url[2],
            "creation_timestamp": url[3],
            "premium": url[4],
            "visits": url[5],
            "delete_after": url[6],
            "last_visit": url[7],
        })
    return json.dumps(buffer)
