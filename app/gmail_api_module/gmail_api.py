# clase para comunicarse con google api
from apiclient.discovery import build
import base64
import email
from apiclient import errors
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient.discovery import build

CLIENTSECRETS_LOCATION = 'credentials.json'
#REDIRECT_URI = CLIENTSECRETS_LOCATION.redirect_uris
REDIRECT_URI = 'http://localhost:4200/code'
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    # Add other requested scopes.
]

class GmailAPI:

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    """
    Get google credentials with token comming from front end with scopes
    PARAMS: code
    """
    def getCredentials(self, code):
        try:
            return self.exchange_code(code)
        except Exception as error:
            print(error)

    """
    Get google service with credentials generated with token comming from front end with scopes
    PARAMS: codcredse
    """
    def getService(self, creds):
        try:
            return build('gmail', 'v1', credentials=creds)
        except Exception as error:
            print(error)
        
    """
    Subscribe to gmail push notifications with credentials generated with token comming from front end with scopes
    PARAMS: code
    """
    def subscribe(self, service, creds):
        try:
            request = {
                'labelIds': ['INBOX'],
                'topicName': 'projects/toolia-269321/topics/gmail_api'
            }
            return service.users().watch(userId='me', body=request).execute()
        except Exception as error:
            print(error)
            
    
    def getProfile(self, service, creds):
        try:
            profile = service.users().getProfile(userId='me').execute()
            return profile
        except Exception as error:
            print(error)
    
    def process_gmail_history_id(self, service, start_history_id, user_id="me"):
        try:
            return service.users().history().list(userId=user_id, startHistoryId=start_history_id).execute()
            """
            changes = history['history'] if 'history' in history else []
            while 'nextPageToken' in history:
                page_token = history['nextPageToken']
                history = (service.users().history().list(userId=user_id, startHistoryId=start_history_id, pageToken=page_token).execute())
                changes.extend(history['history'])
            return changes
            """
        except Exception as error:
            print(error)
    
    def GetMessage(self, service, msg_id, user_id="me"):
        """Get a Message with given ID.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            msg_id: The ID of the Message required.

        Returns:
            A Message.
        """
        try:
            message = service.users().messages().get(userId=user_id, id=msg_id).execute()

            print('Message snippet: {}'.format(message['snippet']))

            return message
        except Exception as error:
            print(error)% error


    def GetMimeMessage(self, service, msg_id, user_id="me"):
        """Get a Message and use it to create a MIME Message.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            msg_id: The ID of the Message required.

        Returns:
            A MIME Message, consisting of data from Message.
        """
        try:
            message = service.users().messages().get(userId=user_id, id=msg_id,
                                                    format='raw').execute()

            print('Message snippet: {}'.format(message['snippet']))

            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

            mime_msg = email.message_from_string(msg_str)

            return mime_msg
        except Exception as error:
            print(error)
    
    def exchange_code(self, authorization_code):
        """Exchange an authorization code for OAuth 2.0 credentials.

    Args:
        authorization_code: Authorization code to exchange for OAuth 2.0
                            credentials.
    Returns:
        oauth2client.client.OAuth2Credentials instance.
    Raises:
        CodeExchangeException: an error occurred.
    """
        flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
        flow.redirect_uri = REDIRECT_URI
        try:
            credentials = flow.step2_exchange(authorization_code)
            return credentials
        except FlowExchangeError as error:
            logging.error('An error occurred: %s', error)
            raise CodeExchangeException(None)

    

    
    
    
