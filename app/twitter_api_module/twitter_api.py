from app.setting.settings import APP_CONSUMER_KEY, APP_CONSUMER_SECRET
from flask import jsonify
import tweepy
import json

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'
show_user_url = 'https://api.twitter.com/1.1/users/show.json'
APP_CONSUMER_KEY = 'wsSu7MvVjT4bigdZRv67xiw7V'
APP_CONSUMER_SECRET = 'iV1HcVecqe2JyQirBoyR5JIcs3qAZ8JwNfxENJwr5eKx6LvNu6'

app_callback_url = "http://127.0.0.1:5000/start"
oauth_store = {}


class TwitterAPI:

    def __init__(self, *args, **kwargs):
        self.auth = tweepy.OAuthHandler(APP_CONSUMER_KEY, APP_CONSUMER_SECRET,
                                        app_callback_url)
        return super().__init__(*args, **kwargs)

    def generateOAuthUrl(self):
        """
        Generate the OAuth request tokens, then display them
        Genera un token via OAuth, el cual se envia como respuesta  al cliente
        se debe usar para el siguiente paso, el valor del token (oauth_token)
        """
        try:
            redirect_url = {"redirect_url": self.auth.get_authorization_url()}
            return redirect_url
        except tweepy.TweepError:
            print('Error! Failed to get request token.')

    def authorizeToken(self, request):
        """ 
        Accept the callback params, get the token and call the API to
        display the logged-in user's name and handle
        """
        oauth_token = request.args.get('oauth_token')
        oauth_verifier = request.args.get('oauth_verifier')
        oauth_denied = request.args.get('denied')

        # if the OAuth request was denied, delete our local token
        # and show an error message
        if oauth_denied:
            if oauth_denied in oauth_store:
                del oauth_store[oauth_denied]
            return jsonify(error_message="the OAuth request was denied by this user")

        if not oauth_token or not oauth_verifier:
            return jsonify(error_message="callback param(s) missing")
        self.auth.request_token = {'oauth_token': oauth_token, 'oauth_token_secret': oauth_verifier}
        try:
            oauth = self.auth.get_access_token(oauth_verifier)
            print(oauth[0], oauth[1])
            resp = {'oauth_token': oauth[0], 'oauth_token_secret': oauth[1]}

            return jsonify(resp)
        except tweepy.TweepError:
            return jsonify({"Error": "Failed to get access token."})

    def profile(self, oauth_token, oauth_verifier):
        """
        :param oauth_token:
        :param oauth_verifier:
        :return: profile user in twitter
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            me = api.me()._json
            return me

        except tweepy.TweepError:
            return jsonify({"Error": "Failed to get access token."})

    def send_direct_message(self, oauth_token, oauth_verifier, recipient_id, text):
        print(recipient_id)
        """

        :param oauth_token:
        :param oauth_verifier:
        :param recipient_id:
        :param text:
        :return:
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            api.send_direct_message(recipient_id=recipient_id, text=text)
            return jsonify({"OK": "New message sender"})

        except tweepy.TweepError as err:
            print(err)
            return jsonify({"Error": "Failed to get access token."})

    def update_status(self, oauth_token, oauth_verifier, tweet, image_path=None):
        """

        :param oauth_token:
        :param oauth_verifier:
        :param tweet:
        :param image_path:
        :return:  New status and id
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            update = None
            if tweet and image_path:
                update = api.update_with_media(filename=image_path, status=tweet)
            else:
                update = api.update_status(tweet)
            result = {'id_str': update.id_str, 'text': update.text, 'created_at': update.created_at}
            return jsonify(result)

        except tweepy.TweepError:
            print('Error! Failed to get access token.')
            return jsonify({"Error": "Failed to get access token."})

    def destroy_status(self, oauth_token, oauth_verifier, tweet_id):
        """
        Delete a Tweet
        :param oauth_token:
        :param oauth_verifier:
        :param tweet_id:
        :return:
        """
        # self.auth.request_token = {'oauth_token': oauth_token, 'oauth_token_secret': oauth_verifier}
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            api.destroy_status(tweet_id)
            return jsonify({"OK": "Deleted"})

        except tweepy.TweepError:
            return jsonify({"Error": "Failed to get access token."})

    def create_friendship(self, oauth_token, oauth_verifier, friend):
        """
        Follow people
        :param oauth_token:
        :param oauth_verifier:
        :param friend: '@YouTube'
        :return:
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            api.create_friendship(friend)
            return jsonify({"OK": "New follow"})

        except tweepy.TweepError:
            return jsonify({"Error": "Failed to get access token."})

    def destroy_friendship(self, oauth_token, oauth_verifier, friend):
        """
        Unfollow people
        :param oauth_token:
        :param oauth_verifier:
        :param friend: '@YouTube'
        :return:
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            api.destroy_friendship(friend)
            return jsonify({"OK": "Unfollow"})
        except tweepy.TweepError:
            return jsonify({"Error": "Failed to get access token."})

    def my_followers(self, oauth_token, oauth_verifier):
        """
        My followers
        :param oauth_token:
        :param oauth_verifier:
        :return: a list of followers
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            followers = api.followers(count=100)
            # noinspection PyProtectedMember
            results = [usr._json for usr in followers]

            return jsonify({"followers": results})
        except tweepy.TweepError as err:
            return jsonify({"Error": "Failed to get access,"+err})

    def direct_messages(self,oauth_token, oauth_verifier):
        """
        Direct messages
        :param oauth_token:
        :param oauth_verifier:
        :return: list of all messages created
        """

        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            messages = api.list_direct_messages()
            # noinspection PyProtectedMember
            results = [message.message_create for message in messages]

            return jsonify({"direct_messages": results})
        except tweepy.TweepError as err:
            return jsonify({"Error": "Failed to get access,"+err})

    def retweets_of_me(self, oauth_token, oauth_verifier):
        """
        List all retweets
        :param oauth_token:
        :param oauth_verifier:
        :return: All retweets by me
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            retweets = api.retweets_of_me()
            # noinspection PyProtectedMember
            results = [retweet._json for retweet in retweets]

            return jsonify({"retweets": results})
        except tweepy.TweepError as err:
            return jsonify({"Error": "Failed to get access,"+err})

    def retweet(self, oauth_token, oauth_verifier, id_tweet):
        """
        Do retweet,
        :param id_tweet:
        :param oauth_token:
        :param oauth_verifier:
        :return:
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            retweet = api.retweet(id_tweet)
            return jsonify(retweet._json)
        except tweepy.TweepError as err:
            return jsonify({"Error": "Failed to get access," + err.__str__()})

    def create_block(self, oauth_token, oauth_verifier, user_id):
        """
        Blocks the user specified in the ID parameter as the authenticating user.
        Destroys a friendship to the blocked user if it exists.
        :param oauth_token:
        :param oauth_verifier:
        :param user_id:
        :return: OK
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            api.create_block(user_id)
            return jsonify({"OK": "User Blocked"})
        except tweepy.TweepError as err:
            return jsonify({"Error": "Failed to get access," + err.__str__()})

    def destroy_create_block(self, oauth_token, oauth_verifier, user_id):
        """
        Un-blocks the user specified in the ID parameter for the authenticating user.
        :param oauth_token:
        :param oauth_verifier:
        :param user_id:
        :return:
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            api.destroy_create_block(user_id)
            return jsonify({"OK": "User Unlocked"})
        except tweepy.TweepError as err:
            return jsonify({"Error": "Failed to get access," + err.__str__()})

    def blocks(self, oauth_token, oauth_verifier, user_id):
        """
        :param oauth_token:
        :param oauth_verifier:
        :param user_id:
        :return:an array of user objects that the authenticating user is blocking.
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            blocks=api.blocks()

            return jsonify({"OK": "User Unlocked"})
        except tweepy.TweepError as err:
            return jsonify({"Error": "Failed to get access," + err.__str__()})



    def unretweet(self, oauth_token, oauth_verifier, id_tweet):

        """
        Do retweet
        :param id_tweet:
        :param oauth_token:
        :param oauth_verifier:
        :return:
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            unretweet = api.unretweet(id_tweet)
            # noinspection PyProtectedMember
            return jsonify(unretweet._json)

        except tweepy.TweepError as err:
            return jsonify({"Error": "Failed to get access," + err.__str__()})

    def user_timeline(self, oauth_token, oauth_verifier):
        """
        User time line
        :param oauth_token:
        :param oauth_verifier:
        :return: Returns the 20 most recent statuses posted from the authenticating user or the user specified.
        It’s also possible to request another user’s timeline via the id parameter.
        """
        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            timeline = api.user_timeline()
            # noinspection PyProtectedMember
            timeline = [status._json for status in timeline]
            return jsonify(timeline)

        except tweepy.TweepError as err:
            return jsonify({"Error": "Failed to get access," + err})

    def home_timeline(self, oauth_token, oauth_verifier):
        """
        This is the equivalent of /timeline/home on the Web.
        :param oauth_token:
        :param oauth_verifier:
        :return:Returns the 20 most recent statuses, including retweets, posted by the authenticating user and that user’s friends.
        """

        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            home_timeline = api.home_timeline()
            # noinspection PyProtectedMember
            timeline = [status._json for status in home_timeline]
            return jsonify(timeline)

        except tweepy.TweepError as err:
            return jsonify({"Error": "Failed to get access," + err})


    def get_user_info(self, oauth_token, oauth_verifier,screen_name):
        """
        This is the equivalent of /timeline/home on the Web.
        :param screen_name:
        :param oauth_token:
        :param oauth_verifier:
        :return:Returns the 20 most recent statuses, including retweets, posted by the authenticating user and that user’s friends.
        """

        try:
            self.auth.set_access_token(oauth_token, oauth_verifier)
            api = tweepy.API(self.auth)
            user_info = api.get_user(screen_name)
            # noinspection PyProtectedMember
            print(user_info._json['id'])
            return jsonify(user_info._json)

        except tweepy.TweepError as err:
            return jsonify({"Error": "Failed to get access," + err})


