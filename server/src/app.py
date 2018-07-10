# app.py
#!/usr/bin/env python3
# encoding: utf-8
# Author: lyndon

import os
import time
import csv
import asyncio
from sanic import Sanic
from sanic_cors import CORS
from sanic.response import json
from aoiklivereload import LiveReloader
from config import huey
from task import addjob
import csv


# How is Support hot reload in Sanic?
# Just do it !
reloader = LiveReloader()
reloader.start_watcher_thread()

app = Sanic(__name__)

# but due to not support http `options` method in sanic core (https://github.com/channelcat/sanic/issues/251).
# So have to use third package extension for Sanic-Cors. Thank you @ashleysommer!

CORS(app,
     automatic_options=True)  # resolve pre-flight request problem (https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request)

filename = './user.csv'
data = []
with open(filename) as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)


# @app.middleware('response')
# async def custom_banner(request, response):
#     response.headers["content-type"] = "application/json"

@app.route("/users")
async def users(request):
    return json(data)

@app.route("/join", methods=['POST'])
async def join(request):
    url=request.json['url']
    users=request.json['users']
    try:
        addjob(url, users)
    except Exception as err:
        print(err)
    return json({ "received": True, "message": request.json })


app.run(host='0.0.0.0', port=8888, debug=True)