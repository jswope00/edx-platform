"""
    Unit tests for the IdentityServer3 OAuth2 Backend
"""

from mock import patch
from third_party_auth.identityServer3 import IdentityServer3
from third_party_auth.tests import testutil
from third_party_auth.tests.factories import OAuth2ProviderConfigFactory


class IdentityServer3Test(testutil.TestCase):
    """
    Unit tests for the IdentityServer3 OAuth2 Backend
    """
    def test_proper_get_of_user_id(self):
        """
            make sure the "sub" claim works properly to grab user Id
        """
        id3_instance = IdentityServer3()
        details = {"sub": 1, "email": "example@example.com"}
        self.assertEqual(id3_instance.get_user_id(details), 1)

    def test_key_error_thrown_with_no_sub(self):
        """
            test that a KeyError is thrown if the "sub" claim does not exist
        """
        id3_instance = IdentityServer3()
        self.assertRaises(KeyError, id3_instance.get_user_id(details={"id": 1}))

    def test_proper_config_access(self):
        """
            test that the IdentityServer3 model properly grabs OAuth2Configs
        """
        id3_instance = IdentityServer3()
        provider_config = OAuth2ProviderConfigFactory.create(backend_name="identityServer3")
        self.assertEqual(id3_instance._id3_config, provider_config)

    def test_config_after_updating(self):
        """
            Make sure when the OAuth2Config for this backend is updated, the new config is properly grabbed
        """
        id3_instance = IdentityServer3()
        original_provider_config = OAuth2ProviderConfigFactory.create(slug="original", backend_name="identityServer3")
        updated_provider_config = OAuth2ProviderConfigFactory.create(slug="updated", backend_name="identityServer3")
        self.assertEqual(id3_instance._id3_config, updated_provider_config)
        self.assertNotEqual(id3_instance._id3_config, original_provider_config)
