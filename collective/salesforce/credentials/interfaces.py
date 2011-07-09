from zope.interface import Interface
from zope import schema

from collective.salesforce.credentials import _


class ISalesforceCredentialsSettings(Interface):
    sandbox = schema.ASCIILine(
        title = _(u'Sandbox name'),
        required = False,
        default = '',
        )


class ISalesforceWebservice(Interface):
    
    endpoint = schema.ASCIILine(
        title = _(u'Endpoint'),
        required = False,
        )

    login = schema.ASCIILine(
        title = _(u'Login'),
        required = False,
        )
    
    password = schema.Password(
        title = _(u'Password'),
        required = False,
        )

    token = schema.Password(
        title = _(u'Token'),
        required = False,
        )
    
    wsdl = schema.ASCIILine(
        title = _(u'WSDL'),
        required = False,
        )
