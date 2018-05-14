# Copyright 2018 Oath, Inc.
# Licensed under the terms of the MIT license. See LICENSE file in convertro-gdpr-dashboard-reference for terms.
import os
import requests
from flask import Flask, render_template, request, redirect, url_for

CLIENT_NAME = os.environ.get('CLIENT_NAME')
API_KEY = os.environ.get('API_KEY')
COOKIE_API_URL = os.environ.get('COOKIE_API_URL')
GDPR_API_URL = os.environ.get('GDPR_API_URL')

app = Flask(__name__)

logger = app.logger


def make_request_with_cookies(sid_cvo_domain, view_cookie_cvo_domain):
    url = GDPR_API_URL
    headers = {'x-api-key': API_KEY}
    payload = {
        'client_id': CLIENT_NAME,
        'request_id': '74ed5d41-7933-4cfc-8a81-a01740edfad3',  # sample UUID representing the request
        'request_type': 'ACCESS',  # "ACCESS" for retrieving data, "ERASE" for deleting
        'sid_client_domain': sid_cvo_domain,
        'sid_cvo_domain': view_cookie_cvo_domain,
    }

    resp = requests.post(url, headers=headers, json=payload)
    return resp.status_code


@app.route('/cookie-handler')
def handler():
    args = request.args  # get parameters submitted in the URL
    status_code = args.get('status_code', '')

    if status_code != str(requests.codes.ok):
        # Cookie Reflection API encountered an error
        logger.info("Cookie Reflection API returned HTTP {}".format(status_code))
        return redirect(url_for('show_error', reason='cookie'))
    else:
        status_code = make_request_with_cookies(
            args.get('sid_cvo_domain', ''),
            args.get('view_cookie_cvo_domain', '')
        )

        logger.info("GDPR API returned HTTP {}".format(status_code))
        if status_code >= requests.codes.bad_request:
            return redirect(url_for('show_error', reason='gdpr'))
        else:
            return redirect(url_for('show_success'))


@app.route('/success')
def show_success():
    return render_template('success.html')


@app.route('/error/<reason>')
def show_error(reason):
    return render_template('error.html', reason=reason)


@app.route('/')
def index():
    handler_url = '{}?redirect_url={}{}'.format(
        COOKIE_API_URL,
        request.url_root,
        url_for('handler')[1:]  # omit leading slash
    )
    return render_template('index.html', handler_url=handler_url)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
