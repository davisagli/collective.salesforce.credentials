import unittest2 as unittest
from zope.component import provideUtility
from plone.testing import zca


class TestUtils(unittest.TestCase):
    
    layer = zca.UNIT_TESTING
    
    def setUp(self):
        from plone.registry.tests import setUp
        setUp()

        from plone.registry import Registry
        from plone.registry.interfaces import IRegistry
        self.registry = Registry()
        provideUtility(self.registry, provides=IRegistry)
    
    def test_get_webservice_settings(self):
        
        class DummyWebservice:
            endpoint = 'https://login.salesforce.com/services/Soap/u/21.0'
            login = 'test@example.com'
            password = u'foo'
            token = u'bar'
            wsdl = ''
        
        from collective.salesforce.credentials.interfaces import ISalesforceWebservice
        webservices = self.registry.collectionOfInterface(ISalesforceWebservice,
            prefix='collective.salesforce.credentials.webservices')
        webservices['dummy'] = DummyWebservice()
        self.assertEqual(['collective.salesforce.credentials.webservices/dummy.endpoint',
                          'collective.salesforce.credentials.webservices/dummy.login',
                          'collective.salesforce.credentials.webservices/dummy.password',
                          'collective.salesforce.credentials.webservices/dummy.token',
                          'collective.salesforce.credentials.webservices/dummy.wsdl'], list(self.registry.records.keys()))
        
        from collective.salesforce.credentials.utils import get_webservice_settings
        settings = get_webservice_settings('dummy')
        self.assertEqual(DummyWebservice.endpoint, settings.endpoint)
        self.assertEqual(DummyWebservice.login, settings.login)
        self.assertEqual(DummyWebservice.password, settings.password)
        self.assertEqual(DummyWebservice.token, settings.token)
        self.assertEqual(DummyWebservice.wsdl, settings.wsdl)
    
    def test_get_webservice_settings_missing_id(self):
        from collective.salesforce.credentials.utils import get_webservice_settings
        try:
            get_webservice_settings('foobar')
        except Exception, e:
            self.assertEqual("'Webservice foobar not found in registry.'", str(e))
    
    def test_get_webservice_settings_sandbox(self):

        from collective.salesforce.credentials.interfaces import ISalesforceCredentialsSettings
        self.registry.registerInterface(ISalesforceCredentialsSettings)
        self.registry.forInterface(ISalesforceCredentialsSettings).sandbox = 'sb01'

        class DummyWebservice:
            endpoint = 'https://login.salesforce.com/services/Soap/u/21.0'
            login = 'test@example.com'
            password = u'foo'
            token = u'bar'
            wsdl = ''
        
        # add a non-sandbox and a sandbox webservice
        from collective.salesforce.credentials.interfaces import ISalesforceWebservice
        webservices = self.registry.collectionOfInterface(ISalesforceWebservice,
            prefix='collective.salesforce.credentials.webservices')
        webservices['dummy'] = DummyWebservice()
        DummyWebservice.wsdl = "Look I'm a sandbox"
        webservices['dummy_sb01'] = DummyWebservice()
        
        from collective.salesforce.credentials.utils import get_webservice_settings
        settings = get_webservice_settings('dummy')
        self.assertEqual("Look I'm a sandbox", settings.wsdl)
