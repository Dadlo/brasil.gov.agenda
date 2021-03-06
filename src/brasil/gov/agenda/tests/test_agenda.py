# -*- coding: utf-8 -*-

from brasil.gov.agenda.interfaces import IAgenda
from brasil.gov.agenda.testing import INTEGRATION_TESTING
from plone.app.dexterity.behaviors.nextprevious import INextPreviousToggle
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from zope.component import createObject
from zope.component import queryUtility

import unittest2 as unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('Agenda', 'agenda')
        self.agenda = self.folder['agenda']

    def test_adding(self):
        self.assertTrue(IAgenda.providedBy(self.agenda))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Agenda')
        self.assertIsNotNone(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Agenda')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IAgenda.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.agenda))
        self.assertTrue(IAttributeUUID.providedBy(self.agenda))

    def test_next_previous(self):
        self.assertTrue(INextPreviousToggle.providedBy(self.agenda))

    def test_agendadiaria_ordering(self):
        # Create two AgendaDiaria objects
        self.agenda.invokeFactory('AgendaDiaria', '2013-10-17')
        self.agenda.invokeFactory('AgendaDiaria', '2013-02-05')
        oIds = list(self.agenda.objectIds())
        # Sorting should be ascending
        self.assertEqual(['2013-02-05', '2013-10-17'], oIds)
        # Add an older one, should be on top of the list
        self.agenda.invokeFactory('AgendaDiaria', '2012-02-05')
        oIds = list(self.agenda.objectIds())
        self.assertEqual(['2012-02-05', '2013-02-05', '2013-10-17'], oIds)

    def test_agenda_icon(self):
        from plone.testing.z2 import Browser
        portal = self.portal
        app = self.layer['app']

        browser = Browser(app)
        portal_url = portal.absolute_url()

        browser.open('%s/++resource++brasil.gov.agenda/agenda_icon.png' % portal_url)
        self.assertEqual(browser.headers['status'], '200 Ok')
