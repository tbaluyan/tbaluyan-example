from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from .views import view_report


class ReportViewPageTest(TestCase):

    def test_report_url_resolves_to_report_view(self):
        found = resolve('/projects/testproject/reports/')
        self.assertEqual(found.func, view_report)

    def test_report_view_page_returns_correct_html(self):
        request = HttpRequest()
        response = view_report(request, project='testproject')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Отчет -')
        self.assertTrue(html.endswith('</html'))
