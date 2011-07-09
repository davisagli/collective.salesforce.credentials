from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class Layer(PloneSandboxLayer):
    
    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        import collective.salesforce.credentials
        self.loadZCML(package=collective.salesforce.credentials)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.salesforce.credentials:default')


FIXTURE = Layer()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name='collective.salesforce.credentials:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name='collective.salesforce.credentials:Functional')
