# encoding:utf-8

# Autenticação com Facebook

CLIENT_ID ='185048221624484'
CLIENT_SECRET ='be1dbf193675dc6f0bb58d7866bd633d'


from facebook import GraphAPI, GraphAPIError
from gluon.contrib.login_methods.oauth20_account import OAuthAccount

class FaceBookAccount(OAuthAccount):
    """OAuth impl for FaceBook"""
    AUTH_URL="https://graph.facebook.com/oauth/authorize"
    TOKEN_URL="https://graph.facebook.com/oauth/access_token"

    def __init__(self, g, db):

        OAuthAccount.__init__(self, g, CLIENT_ID, CLIENT_SECRET,
                              self.AUTH_URL, self.TOKEN_URL,
                              scope='publish_actions, publish_stream, user_likes')
        self.graph = None
        self.db = db

    def get_user(self):
        '''Returns the user using the Graph API.
        '''

        db = self.db

        if not self.accessToken():
            return None

        if not self.graph:
            self.graph = GraphAPI((self.accessToken()))

        user = None
        try:
            user = self.graph.get_object("me")

        except GraphAPIError, e:
            self.session.token = None
            self.graph = None


        if user:
            return dict(first_name = user['first_name'],
                        last_name = user['last_name'],
                        username = user['id'])
