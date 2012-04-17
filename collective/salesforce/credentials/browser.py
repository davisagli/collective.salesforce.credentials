from z3c.form import field, form
from z3c.form.interfaces import DISPLAY_MODE
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.component import getUtility
from zope.interface import implements
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from plone.z3cform.crud.crud import CrudForm
from plone.z3cform.layout import wrap_form
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.registry.interfaces import IRegistry

from . import _
from .interfaces import ISalesforceCredentialsSettings
from .interfaces import ISalesforceWebservice
from .interfaces import ISalesforceWebserviceIdentity


class IIdentifiedSalesforceWebservice(ISalesforceWebserviceIdentity,
                                      ISalesforceWebservice):
    pass


class ServiceMetadataAdapter(object):
    implements(IIdentifiedSalesforceWebservice)

    def __init__(self, name, context):
        attrs = {}
        if '_' in name:
            attrs['name'], attrs['sandbox'] = name.rsplit('_', 1)
        else:
            attrs['name'] = name
            attrs['sandbox'] = None
        attrs['context'] = context
        self.__dict__.update(attrs)

    def __getattr__(self, name):
        return getattr(self.context, name)

    def __setattr__(self, name, value):
        setattr(self.context, name, value)


class CredentialsForm(CrudForm, form.EditForm):

    label = _(u'Salesforce Credentials')
    template = ViewPageTemplateFile('controlpanel.pt')

    fields = field.Fields(ISalesforceCredentialsSettings)
    add_schema = IIdentifiedSalesforceWebservice

    @property
    def update_schema(self):
        fields = field.Fields(IIdentifiedSalesforceWebservice)
        fields['name'].mode = DISPLAY_MODE
        fields['sandbox'].mode = DISPLAY_MODE
        return fields

    def getContent(self):
        registry = getUtility(IRegistry)
        return registry.forInterface(ISalesforceCredentialsSettings)

    @lazy_property
    def services(self):
        registry = getUtility(IRegistry)
        return registry.collectionOfInterface(ISalesforceWebservice,
            prefix='collective.salesforce.credentials.webservices')

    def get_items(self):
        return [(name, ServiceMetadataAdapter(name, svc))
                for name, svc in self.services.items()]

    def add(self, data):
        name = data['name']
        if data['sandbox']:
            name += '_' + data['sandbox']
        record = self.services.setdefault(name)
        for fname in ISalesforceWebservice.names():
            setattr(record, fname, data[fname])

    def remove(self, (id, data)):
        del self.services[id]


CredentialsControlPanel = wrap_form(CredentialsForm, ControlPanelFormWrapper)
