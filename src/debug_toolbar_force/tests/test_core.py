# -*- coding: utf-8 -*-

import unittest

from bs4 import BeautifulSoup

from django.test import TestCase, Client

from nine.versions import DJANGO_GTE_1_10

from ..settings import GET_PARAM_NAME_FORCE
from .base import log_info
from .helpers import setup_app

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'debug_toolbar_force.tests.test_core'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = ('DebugToolbarForceCoreTest',)


class DebugToolbarForceCoreTest(TestCase):
    """Testing `django-debug-toolbar-force` core functionality."""

    def setUp(self):
        """Set up."""
        setup_app(collectstatic=True, migrate=True)
        self.client = Client()
        self.ddt_element_id = 'djDebug'

    def __get_url(self, reverse_url, force=True):
        """Get URL."""
        url = reverse(reverse_url)
        if force:
            url += '?' + GET_PARAM_NAME_FORCE
        return url

    @log_info
    def __test_view(self, reverse_url, force=True):
        url = self.__get_url(reverse_url, force=force)
        response = self.client.get(url)
        response_content = getattr(response, 'content', "")
        soup = BeautifulSoup(response_content, "html.parser")
        ddt_div = soup.find('div', attrs={'id': self.ddt_element_id})
        self.assertIsNotNone(ddt_div)
        return ddt_div

    @log_info
    def test_01_json_view(self):
        """Test JSON view."""
        return self.__test_view('foo.json_view')

    @log_info
    def test_02_ajax_view(self):
        """Test AJAX view."""
        return self.__test_view('foo.ajax_view')

    @log_info
    def test_03_html_view(self):
        """Test HTML view."""
        return self.__test_view('foo.html_view')

    @log_info
    def test_04_partial_html_view(self):
        """Test partial HTML view."""
        return self.__test_view('foo.partial_html_view')


if __name__ == '__main__':
    unittest.main()
