from flask import Blueprint, request
import json
import flask
import socket
from .gmail_api import GmailAPI

mod_gmail_api = Blueprint('gmail', __name__, url_prefix='/gmail')

@mod_gmail_api.route('/push_inbox_procesor/', methods=['POST'])
def subscribe_to_gmail_inbox():
    print("app.gmail_api_module.controllers.subscribe_to_gmail_inbox")
    if request.method == 'POST':
        body = json.loads(request.data)
        print(body)
        gmailAPI = GmailAPI();
        credentials = gmailAPI.getCredentials(body["code"])
        service = gmailAPI.getService(credentials)
        subscribe = gmailAPI.subscribe(service,credentials)
    return '', 200

def process_gmail_history_id():
    print("app.gmail_api_module.controllers.push_inbox_procesor")
    if request.method == 'POST':
        print(request.data)
        body = json.loads(request.data)
        print(body)
    return '', 200



 