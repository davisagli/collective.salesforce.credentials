from pkg_resources import resource_filename
from zope.component import getUtility
from collective.salesforce.credentials.interfaces import ISalesforceWebservice
from collective.salesforce.credentials.interfaces import ISalesforceCredentialsSettings
from plone.registry.interfaces import IRegistry
from z3c.suds import get_suds_client


def get_webservice_settings(id):
    registry = getUtility(IRegistry)
    sandbox = registry.forInterface(ISalesforceCredentialsSettings, False).sandbox
    if sandbox:
        id += '_' + sandbox
    webservices = registry.collectionOfInterface(ISalesforceWebservice,
        prefix='collective.salesforce.credentials.webservices')
    if id not in webservices:
        raise KeyError('Webservice %s not found in registry.' % id)
    return webservices[id]


SOCKET_TIMEOUT = 60


def get_wsdl_uri(spec):
    """Takes a spec in package:path format and returns the corresponding file:/// URI"""
    package, path = spec.split(':')
    return 'file://' + resource_filename(package, path)


def get_salesforce_suds_client(id):
    """Returns an authenticated suds client for the named Salesforce webservice."""
    auth_settings = get_webservice_settings('auth')
    settings = get_webservice_settings(id)
    login = settings.login or auth_settings.login
    password = (settings.password or auth_settings.password or '') + (settings.token or auth_settings.token or '')

    # log in via the auth service
    auth_client = get_suds_client(get_wsdl_uri(auth_settings.wsdl))
    auth_client.set_options(
        timeout = SOCKET_TIMEOUT,
        location = auth_settings.endpoint,
        )
    res = auth_client.service.login(login, password)

    # connect to the service
    client = get_suds_client(get_wsdl_uri(settings.wsdl))
    token = client.factory.create('SessionHeader')
    token.sessionId = res.sessionId
    client.set_options(
        timeout = SOCKET_TIMEOUT,
        location = settings.endpoint,
        soapheaders = [token]
        )

    return client
