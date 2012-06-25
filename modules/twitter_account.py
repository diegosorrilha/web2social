from gluon import *
from gluon.contrib.login_methods.oauth10a_account import OAuthAccount
import oauth2 as oauth
import gluon.contrib.simplejson as json
import twitter
from urlparse import parse_qsl


class TwitterAccount(OAuthAccount):
    def get_user(self):
        if self.accessToken() is None:
            return

        client = oauth.Client(self.consumer, self.accessToken())
        url = 'http://api.twitter.com/1/account/verify_credentials.json'
        resp, content = client.request(url)

        if resp['status'] != '200':
            return None
        u = json.loads(content)

        token = current.session.access_token

        return dict(first_name=u['screen_name'],
                    username=u['screen_name'])
