from flask import Flask, Request
from app.middleware.log_middleware import LogMiddleware

# Define the WSGI application object
app = Flask(__name__)
from flask_cors import CORS

cors = CORS(app, resources={r"*": {"origins": "*"}})

# Middleware
app.wsgi_app = LogMiddleware(app.wsgi_app)

# Configurations
app.config.from_object('config')


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    print("Route not found")
    return "", 400


# import modules
from app.gmail_api_module.controllers import mod_gmail_api as mod_gmail_api
from app.twitter_api_module.controllers import mod_twitter_api as mod_twitter_api

app.register_blueprint(mod_gmail_api)
app.register_blueprint(mod_twitter_api)
