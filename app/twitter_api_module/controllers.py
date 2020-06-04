from flask import Blueprint, request
import json
from .twitter_api import TwitterAPI

mod_twitter_api = Blueprint('twitter', __name__, url_prefix='/twitter')


@mod_twitter_api.route('/generateOAuthToken/', methods=['GET'])
def get_token_twitter():
    print("app.twitter_api_module.controllers.get_token_twitter")
    if request.method == 'GET':
        twitterAPI = TwitterAPI()
    return twitterAPI.generateOAuthUrl()


@mod_twitter_api.route('/autorize', methods=['POST'])
def authorize_token_twitter():
    print("app.twitter_api_module.controllers.authorize_token_twitter")
    if request.method == 'POST':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.authorizeToken(request)


@mod_twitter_api.route('/profile', methods=['GET'])
def get_profile_twitter():
    print("app.twitter_api_module.controllers.get_profile_twitter")
    if request.method == 'GET':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.profile(body['oauth_token'], body['oauth_token_secret'])


@mod_twitter_api.route('/update_status', methods=['POST'])
def update_status():
    print("app.twitter_api_module.controllers.update_status")
    if request.method == 'POST':
        body = json.loads(request.data)
        if 'oauth_token' and 'oauth_token_secret' in body.keys():
            twitterAPI = TwitterAPI()
            if 'tweet' and 'image_path' in body:
                return twitterAPI.update_status(body['oauth_token'], body['oauth_token_secret'], body['tweet'],
                                                body['image_path'])
            else:
                return twitterAPI.update_status(body['oauth_token'], body['oauth_token_secret'], body['tweet'])
        else:
            print("NO data in request")


@mod_twitter_api.route('/destroy_status', methods=['POST'])
def destroy_status_twitter():
    print("app.twitter_api_module.controllers.destroy_status_twitter")
    if request.method == 'POST':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.destroy_status(body['oauth_token'], body['oauth_token_secret'], body['tweet_id'])


@mod_twitter_api.route('/follow', methods=['POST'])
def follow_people_twitter():
    print("app.twitter_api_module.controllers.follow_people_twitter")
    if request.method == 'POST':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.create_friendship(body['oauth_token'], body['oauth_token_secret'], body['friend'])


@mod_twitter_api.route('/unfollow', methods=['POST'])
def unfollow_people_twitter():
    print("app.twitter_api_module.controllers.unfollow_people_twitter")
    if request.method == 'POST':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.destroy_friendship(body['oauth_token'], body['oauth_token_secret'], body['friend'])


@mod_twitter_api.route('/send_direct', methods=['POST'])
def send_direct_sms_twitter():
    print("app.twitter_api_module.controllers.send_direct")
    if request.method == 'POST':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.send_direct_message(body['oauth_token'], body['oauth_token_secret'], body['friend'],body['text'])


@mod_twitter_api.route('/my_followers', methods=['POST'])
def list_my_followers_twitter():
    print("app.twitter_api_module.controllers.list_my_followers_twitter")
    if request.method == 'POST':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.my_followers(body['oauth_token'], body['oauth_token_secret'])\



@mod_twitter_api.route('/direct_messages', methods=['GET'])
def list_direct_messages_twitter():
    print("app.twitter_api_module.controllers.list_direct_messages_twitter")
    if request.method == 'GET':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.direct_messages(body['oauth_token'], body['oauth_token_secret'])


@mod_twitter_api.route('/retweets_of_me', methods=['GET'])
def list_retweets_twitter():
    print("app.twitter_api_module.controllers.list_retweets_twitter")
    if request.method == 'GET':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.retweets_of_me(body['oauth_token'], body['oauth_token_secret'])


@mod_twitter_api.route('/retweet', methods=['POST'])
def retweet_twitter():
    print("app.twitter_api_module.controllers.retweet_twitter")
    if request.method == 'POST':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.retweet(body['oauth_token'], body['oauth_token_secret'], body['id_tweet'])

@mod_twitter_api.route('/unretweet', methods=['POST'])
def unretweet_twitter():
    print("app.twitter_api_module.controllers.unretweet_twitter")
    if request.method == 'POST':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.unretweet(body['oauth_token'], body['oauth_token_secret'], body['id_tweet'])


@mod_twitter_api.route('/timeline', methods=['POST'])
def time_line_user_twitter():
    print("app.twitter_api_module.controllers.time_line_user_twitter")
    if request.method == 'POST':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.user_timeline(body['oauth_token'], body['oauth_token_secret'])


@mod_twitter_api.route('/home_timeline', methods=['POST'])
def home_time_line_user_twitter():
    print("app.twitter_api_module.controllers.home_timeline")
    if request.method == 'POST':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.home_timeline(body['oauth_token'], body['oauth_token_secret'])


@mod_twitter_api.route('/about_user', methods=['POST'])
def info_user_twitter():
    print("app.twitter_api_module.controllers.about_user")
    if request.method == 'POST':
        body = json.loads(request.data)
        print(body)
        twitterAPI = TwitterAPI()
    return twitterAPI.get_user_info(body['oauth_token'], body['oauth_token_secret'], body['screen_name'])
