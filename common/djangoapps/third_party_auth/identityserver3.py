"""
    python-social-auth backend for use with IdentityServer3
    docs: https://identityserver.github.io/Documentation/docsv2/endpoints/authorization.html
    docs for adding a new backend to python-social-auth:
    https://python-social-auth.readthedocs.io/en/latest/backends/implementation.html#oauth
"""
from social_core.backends.oauth import BaseOAuth2
from django.utils.functional import cached_property


class IdentityServer3(BaseOAuth2):
    """
    An extension of the BaseOAuth2 for use with an IdentityServer3 service.
    """

    name = "identityServer3"
    REDIRECT_STATE = False
    ACCESS_TOKEN_METHOD = 'POST'
    DEFAULT_SCOPE = ['openid']
    ID_KEY = "sub"

    def authorization_url(self):
        return self._id3_config.get_setting('auth_url')

    def access_token_url(self):
        return self._id3_config.get_setting('token_url')

    def get_redirect_uri(self, state=None):
        return self._id3_config.get_setting('redirect_uri')

    def user_data(self, access_token, *args, **kwargs):
        """
        consumes the access_token to get data about the user logged
        into the service.
        """
        url = self._id3_config.get_setting('user_info_url')
        # The access token returned from the service's token route.
        header = {"Authorization": u"Bearer %s" % access_token}
        return self.get_json(url, headers=header)

    def get_user_details(self, response):
        """
        Return details about the user account from the service
        """
        details = {"fullname": response["name"], "email": response["email"]}
        return details

    def get_user_id(self, details, response):
        """
        Gets the unique identifier from the user. this is
        how edx knows who's logging in, and if they have an account
        already through edx. IdentityServer emits standard claim type of sub
        to identify the user according to these docs:
        https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims
        """
        try:
            user_id = response.get(self.ID_KEY)
        except KeyError:
            user_id = None
        return user_id

    @cached_property
    def _id3_config(self):
        from .models import OAuth2ProviderConfig
        return OAuth2ProviderConfig.current("identityServer3")
