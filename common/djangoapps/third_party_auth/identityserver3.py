"""
  python-social-auth backend for use with IdentityServer3
  docs: https://identityserver.github.io/Documentation/docsv2/endpoints/authorization.html
  docs for adding a new backend to python-social-auth:
  https://python-social-auth.readthedocs.io/en/latest/backends/implementation.html#oauth
"""
from social_core.backends.oauth import BaseOAuth2


class IdentityServer3(BaseOAuth2):
    name = "identityServer3"

    # these settings and possibly others will be required from the customer.
    # depending on how the server is set up.
    AUTHORIZATION_URL = ''
    ACCESS_TOKEN_URL = ''
    REDIRECT_STATE = False
    DEFAULT_SCOPE = None

    def auth_complete(self, *args, **kwargs):
        # if we need data from the identity server, we need to
        # get that data during the auth completion process here by
        # implimenting our own auth_complete() and get_user_data()
        # functions. in that case, this function should return the
        # authentication strategy, i.e:
        # return self.strategy.authenticate(self, *args, **kwargs)
        return

    def get_user_details(self, response):
        # An example of an override of the get_user_details() function
        # Provided by BaseOAuth2
        # the userdata endpoint needed from the customer.
        url = ""
        header = {"Authorization": "Bearer %s" % response['access_token']}
        user = self.get_json(url, headers=header)
        # some example data to be returned from the service
        return {
            'fullname': "",
            'first_name': "",
            'last_name': "",
            'username': "",
            'email': "",
        }
