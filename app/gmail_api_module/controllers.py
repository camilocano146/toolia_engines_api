from flask import Blueprint, request
import json
import flask
import socket

mod_gmail_api = Blueprint('gmail', __name__, url_prefix='/gmail')

@mod_gmail_api.route('/push_inbox_procesor/', methods=['POST'])
def push_inbox_procesor():
    print("app.gmail_api_module.controllers.push_inbox_procesor")
    if request.method == 'POST':
        print(request.data)
        body = json.loads(request.data)
        print(body)
    return '', 200