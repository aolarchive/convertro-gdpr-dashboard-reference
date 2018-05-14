# Copyright 2018 Oath, Inc.
# Licensed under the terms of the MIT license. See LICENSE file in convertro-gdpr-dashboard-reference for terms.
FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./app /app